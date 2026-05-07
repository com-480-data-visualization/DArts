<script>
  import { flip } from 'svelte/animate';
  import { filters } from '../stores/filters.js';
  import './mediumExplorer.css';

  let { data = [] } = $props();

  const genders = [
    ['female', 'var(--gender-female)'],
    ['male', 'var(--gender-male)'],
    ['non-binary', 'var(--gender-nonbinary)'],
    ['unknown', 'var(--gender-unknown)'],
  ];
  const regions = [
    ['North America', 'var(--region-namerica)'],
    ['Latin America & Caribbean', 'var(--region-latam)'],
    ['Europe', 'var(--region-europe)'],
    ['Africa', 'var(--region-africa)'],
    ['Western & Central Asia', 'var(--region-wcasia)'],
    ['East Asia', 'var(--region-easia)'],
    ['South & Southeast Asia', 'var(--region-ssasia)'],
    ['Oceania', 'var(--region-oceania)'],
    ['Unknown', 'var(--gender-unknown)'],
  ];

  let expanded = $state('');
  let artistIndex = $state([]);
  let loadingArtists = $state(false);

  let filtered = $derived(filterRows(data, $filters));
  let panels = $derived(buildPanels(filtered));

  function filterRows(rows, state) {
    return rows.filter((row) => {
      if (row.decade !== null && (row.decade < state.decadeRange[0] || row.decade > state.decadeRange[1])) return false;
      if (state.selectedCountry && row.iso3 !== state.selectedCountry) return false;
      if (state.selectedDepartments.size && !state.selectedDepartments.has(row.department)) return false;
      if (state.selectedRegions.size && !state.selectedRegions.has(row.region)) return false;
      return true;
    });
  }

  function buildPanels(rows) {
    const byMedium = new Map();
    for (const row of rows) {
      if (!byMedium.has(row.medium)) byMedium.set(row.medium, []);
      byMedium.get(row.medium).push(row);
    }
    return [...byMedium.entries()]
      .map(([medium, values]) => {
        const total = values.reduce((sum, row) => sum + row.n, 0);
        return {
          medium,
          total,
          gender: aggregate(values, 'gender', total),
          region: aggregate(values, 'region', total),
        };
      })
      .filter((panel) => panel.total > 0)
      .sort((a, b) => b.total - a.total)
      .slice(0, 9);
  }

  function aggregate(rows, key, total) {
    const counts = new Map();
    for (const row of rows) counts.set(row[key], (counts.get(row[key]) || 0) + row.n);
    return [...counts.entries()].map(([label, n]) => ({ label, n, pct: total ? n / total : 0 }));
  }

  function colorFor(label, palette) {
    return palette.find(([name]) => name === label)?.[1] ?? 'var(--gender-unknown)';
  }

  function showTooltip(event, segment, total) {
    window.dispatchEvent(new CustomEvent('darts:tooltip', {
      detail: {
        x: event.clientX,
        y: event.clientY,
        content: `<strong>${segment.label}</strong><br><span class="num">${segment.n.toLocaleString()}</span> works<br><span class="num">${(segment.n / total * 100).toFixed(1)}%</span> of medium`
      }
    }));
  }

  function hideTooltip() {
    window.dispatchEvent(new CustomEvent('darts:tooltip-hide'));
  }

  async function expand(medium) {
    expanded = expanded === medium ? '' : medium;
    if (!artistIndex.length && !loadingArtists) {
      loadingArtists = true;
      artistIndex = await fetch('./data/artist_index.json').then((r) => r.json());
      loadingArtists = false;
    }
  }

  function topArtists(medium) {
    const state = $filters;
    return artistIndex
      .filter((artist) => artist.medium_primary === medium)
      .filter((artist) => !state.selectedCountry || artist.iso3 === state.selectedCountry)
      .filter((artist) => !state.selectedRegions.size || state.selectedRegions.has(artist.region))
      .filter((artist) => {
        const first = artist.decade_active_first ?? 1860;
        const last = artist.decade_active_last ?? 2020;
        return last >= state.decadeRange[0] && first <= state.decadeRange[1];
      })
      .sort((a, b) => b.n_works - a.n_works || a.name.localeCompare(b.name))
      .slice(0, 5);
  }
</script>

{#if panels.length === 0}
  <div class="empty">
    <p>No works match these filters.</p>
  </div>
{:else}
  <div class="medium-grid" class:has-expanded={expanded}>
    {#each panels as panel (panel.medium)}
      <article class:expanded={expanded === panel.medium} class:dimmed={expanded && expanded !== panel.medium} animate:flip={{ duration: 450 }}>
        <button type="button" class="panel-button" onclick={() => expand(panel.medium)} aria-expanded={expanded === panel.medium}>
          <header>
            <h3>{panel.medium}</h3>
            <p class="type-mono">n={panel.total.toLocaleString()}</p>
          </header>
          <div class="bar-group" aria-label={`${panel.medium} gender and region split`}>
            <div class="bar-row">
              <span>gender</span>
              <div class="stack">
                {#each panel.gender as segment}
                  <i
                    style:width={`${segment.pct * 100}%`}
                    style:background={colorFor(segment.label, genders)}
                    onpointermove={(event) => showTooltip(event, segment, panel.total)}
                    onpointerleave={hideTooltip}
                    role="img"
                    aria-label={`${segment.label}: ${segment.n} works`}
                  ></i>
                {/each}
              </div>
            </div>
            <div class="bar-row">
              <span>region</span>
              <div class="stack">
                {#each panel.region as segment}
                  <i
                    style:width={`${segment.pct * 100}%`}
                    style:background={colorFor(segment.label, regions)}
                    onpointermove={(event) => showTooltip(event, segment, panel.total)}
                    onpointerleave={hideTooltip}
                    role="img"
                    aria-label={`${segment.label}: ${segment.n} works`}
                  ></i>
                {/each}
              </div>
            </div>
          </div>
        </button>
        {#if expanded === panel.medium}
          <div class="expanded-body">
            {#if loadingArtists}
              <p>Loading artists...</p>
            {:else}
              {#each topArtists(panel.medium) as artist}
                <div class="artist-row">
                  <span>{artist.name}</span>
                  <b style:width={`${Math.min(100, artist.n_works / Math.max(1, topArtists(panel.medium)[0]?.n_works) * 100)}%`}></b>
                  <em class="type-mono">{artist.n_works}</em>
                </div>
              {/each}
            {/if}
          </div>
        {/if}
      </article>
    {/each}
  </div>
{/if}
