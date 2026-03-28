<script>
  import { onMount, tick } from 'svelte';
  import * as d3 from 'd3';
  import * as topojson from 'topojson-client';

  let { countriesData, artistsData, selectedDecade } = $props();

  let globeEl = $state(null);
  let spotlightArtist = $state(null);
  let worldGeo = $state(null);
  let rotating = true;
  let currentTimer = null;

  // Shared lookup table
  const NUM_TO_ALPHA = {
    '840': 'USA', '250': 'FRA', '276': 'DEU', '826': 'GBR', '380': 'ITA',
    '392': 'JPN', '756': 'CHE', '528': 'NLD', '124': 'CAN', '040': 'AUT',
    '724': 'ESP', '076': 'BRA', '484': 'MEX', '643': 'RUS', '032': 'ARG',
    '752': 'SWE', '208': 'DNK', '056': 'BEL', '376': 'ISR', '036': 'AUS',
    '616': 'POL', '203': 'CZE', '356': 'IND', '156': 'CHN', '410': 'KOR',
    '170': 'COL', '192': 'CUB', '152': 'CHL', '578': 'NOR', '246': 'FIN',
    '710': 'ZAF', '372': 'IRL', '620': 'PRT', '862': 'VEN', '604': 'PER',
    '300': 'GRC', '792': 'TUR', '642': 'ROU', '348': 'HUN', '191': 'HRV',
    '352': 'ISL', '566': 'NGA', '818': 'EGY', '364': 'IRN', '586': 'PAK',
    '764': 'THA', '608': 'PHL', '858': 'URY', '218': 'ECU', '320': 'GTM',
    '158': 'TWN', '554': 'NZL', '440': 'LTU', '428': 'LVA', '233': 'EST',
    '688': 'SRB', '705': 'SVN', '703': 'SVK', '804': 'UKR', '070': 'BIH',
    '008': 'ALB', '442': 'LUX', '288': 'GHA', '404': 'KEN', '686': 'SEN',
    '504': 'MAR', '788': 'TUN', '422': 'LBN', '368': 'IRQ', '414': 'KWT',
    '784': 'ARE', '702': 'SGP', '458': 'MYS', '360': 'IDN', '704': 'VNM',
    '116': 'KHM', '332': 'HTI', '388': 'JAM', '630': 'PRI', '188': 'CRI',
    '600': 'PRY', '068': 'BOL', '591': 'PAN', '558': 'NIC', '222': 'SLV',
    '214': 'DOM', '780': 'TTO', '44': 'BHS',
  };

  onMount(async () => {
    const resp = await fetch('https://cdn.jsdelivr.net/npm/world-atlas@2/countries-110m.json');
    const world = await resp.json();
    worldGeo = topojson.feature(world, world.objects.countries);
  });

  // Redraw whenever worldGeo, globeEl, or selectedDecade changes
  $effect(() => {
    if (worldGeo && globeEl) {
      // Access selectedDecade to track it as a dependency
      const _ = selectedDecade;
      drawGlobe();
    }
  });

  function inRange(decade) {
    if (!selectedDecade) return true;
    return decade >= selectedDecade.min && decade <= selectedDecade.max;
  }

  function pickRandomArtist(iso) {
    let pool = artistsData.filter(a => a.iso === iso);
    if (selectedDecade) pool = pool.filter(a => inRange(a.decade));
    if (pool.length === 0) pool = artistsData.filter(a => a.iso === iso);
    if (pool.length === 0) return null;
    return pool[Math.floor(Math.random() * pool.length)];
  }

  function toAlpha(topoId) {
    return NUM_TO_ALPHA[String(topoId)] || null;
  }

  function getCount(topoId, countByIso) {
    const alpha = toAlpha(topoId);
    return alpha ? (countByIso[alpha] || 0) : 0;
  }

  function drawGlobe() {
    if (currentTimer) { currentTimer.stop(); currentTimer = null; }

    const container = d3.select(globeEl);
    container.selectAll('*').remove();

    const containerWidth = globeEl.clientWidth || 520;
    const size = Math.min(520, containerWidth);

    if (size < 10) return; // not mounted yet

    const projection = d3.geoOrthographic()
      .scale(size / 2.2)
      .translate([size / 2, size / 2])
      .clipAngle(90)
      .rotate([-10, -30]);

    const path = d3.geoPath().projection(projection);

    // Build country count lookup
    const countByIso = {};
    if (selectedDecade) {
      const rangeArtists = artistsData.filter(a => inRange(a.decade));
      rangeArtists.forEach(a => { countByIso[a.iso] = (countByIso[a.iso] || 0) + 1; });
    } else {
      countriesData.forEach(d => { countByIso[d.iso] = d.count; });
    }

    const maxCount = Math.max(...Object.values(countByIso), 1);
    const colorScale = d3.scaleSequential(d3.interpolateYlOrRd)
      .domain([0, Math.sqrt(maxCount)]);

    const svg = container.append('svg')
      .attr('width', size)
      .attr('height', size)
      .style('cursor', 'grab')
      .style('display', 'block')
      .style('margin', '0 auto');

    // Ocean gradient
    const defs = svg.append('defs');
    const oceanGrad = defs.append('radialGradient').attr('id', 'ocean');
    oceanGrad.append('stop').attr('offset', '0%').attr('stop-color', '#e8f4fc');
    oceanGrad.append('stop').attr('offset', '100%').attr('stop-color', '#d0e4f0');

    svg.append('circle')
      .attr('cx', size/2).attr('cy', size/2).attr('r', size/2.2)
      .attr('fill', 'url(#ocean)')
      .attr('stroke', '#b8ccd8')
      .attr('stroke-width', 0.5);

    // Graticule
    svg.append('path')
      .datum(d3.geoGraticule10())
      .attr('d', path)
      .attr('fill', 'none')
      .attr('stroke', '#ccdce8')
      .attr('stroke-width', 0.3)
      .attr('class', 'graticule');

    // Countries
    svg.selectAll('.country')
      .data(worldGeo.features)
      .join('path')
      .attr('class', 'country')
      .attr('d', path)
      .attr('fill', d => {
        const count = getCount(d.id, countByIso);
        return count > 0 ? colorScale(Math.sqrt(count)) : '#e8e2d9';
      })
      .attr('stroke', '#fff')
      .attr('stroke-width', 0.4)
      .style('cursor', d => getCount(d.id, countByIso) > 0 ? 'pointer' : 'default')
      .on('click', (event, d) => {
        const alpha = toAlpha(d.id);
        if (alpha && countByIso[alpha]) {
          const artist = pickRandomArtist(alpha);
          if (artist) spotlightArtist = artist;
        }
      })
      .on('mouseenter', function() {
        d3.select(this).attr('stroke', '#c1440e').attr('stroke-width', 1.5);
      })
      .on('mouseleave', function() {
        d3.select(this).attr('stroke', '#fff').attr('stroke-width', 0.4);
      });

    // Drag to rotate
    const drag = d3.drag()
      .on('start', () => {
        rotating = false;
        if (currentTimer) { currentTimer.stop(); currentTimer = null; }
        svg.style('cursor', 'grabbing');
      })
      .on('drag', (event) => {
        const r = projection.rotate();
        projection.rotate([r[0] + event.dx * 0.4, r[1] - event.dy * 0.4]);
        svg.selectAll('path').attr('d', path);
      })
      .on('end', () => { svg.style('cursor', 'grab'); });

    svg.call(drag);

    // Auto-rotate
    rotating = true;
    currentTimer = d3.timer(() => {
      if (!rotating) { currentTimer.stop(); currentTimer = null; return; }
      const r = projection.rotate();
      projection.rotate([r[0] + 0.15, r[1]]);
      svg.selectAll('path').attr('d', path);
    });
  }
</script>

<div class="globe-layout">
  <div class="globe-wrapper" bind:this={globeEl}></div>
  <div class="spotlight-panel">
    {#if spotlightArtist}
      <div class="spotlight-card">
        <p class="spotlight-label">Artist Spotlight</p>
        <h3 class="spotlight-name">{spotlightArtist.artist}</h3>
        <div class="spotlight-details">
          <p><strong>Nationality:</strong> {spotlightArtist.nationality}</p>
          <p><strong>Gender:</strong> {spotlightArtist.gender}</p>
          <p><strong>Artwork:</strong> <em>{spotlightArtist.title}</em></p>
          <p><strong>Date:</strong> {spotlightArtist.date}</p>
          <p><strong>Medium:</strong> {spotlightArtist.medium}</p>
        </div>
        <button class="spotlight-refresh" onclick={() => {
          const a = pickRandomArtist(spotlightArtist.iso);
          if (a) spotlightArtist = a;
        }}>
          Show another artist
        </button>
      </div>
    {:else}
      <div class="spotlight-empty">
        <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="var(--color-text-light)" stroke-width="1.5" stroke-linecap="round">
          <circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
        </svg>
        <p>Click on a <strong>highlighted country</strong> to discover a random artist from that region</p>
        <p class="hint">Drag to rotate the globe</p>
      </div>
    {/if}
  </div>
</div>

<style>
  .globe-layout {
    display: flex;
    gap: 2.5rem;
    align-items: center;
    flex-wrap: wrap;
    justify-content: center;
  }
  .globe-wrapper {
    flex: 0 0 520px;
    min-height: 520px;
  }
  .globe-wrapper :global(svg) {
    filter: drop-shadow(0 8px 24px rgba(44,95,124,0.12));
  }
  .spotlight-panel {
    flex: 1;
    min-width: 280px;
    max-width: 360px;
  }
  .spotlight-card {
    background: var(--color-surface);
    border-radius: var(--radius);
    padding: 2rem;
    box-shadow: var(--shadow-md);
    border: 1px solid var(--color-border);
    border-left: 4px solid var(--color-primary);
  }
  .spotlight-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-primary);
    font-weight: 600;
    margin-bottom: 0.5rem;
  }
  .spotlight-name {
    font-family: var(--font-heading);
    font-size: 1.6rem;
    margin-bottom: 1rem;
    color: var(--color-text);
  }
  .spotlight-details p {
    font-size: 0.88rem;
    margin-bottom: 0.4rem;
    color: var(--color-text-muted);
  }
  .spotlight-details strong {
    color: var(--color-text);
    font-weight: 500;
  }
  .spotlight-details em {
    font-style: italic;
    color: var(--color-secondary);
  }
  .spotlight-refresh {
    margin-top: 1.25rem;
    background: none;
    border: 1px solid var(--color-border);
    padding: 0.5rem 1rem;
    border-radius: 100px;
    font-family: var(--font-body);
    font-size: 0.8rem;
    color: var(--color-text-muted);
    cursor: pointer;
    transition: all 0.2s;
  }
  .spotlight-refresh:hover {
    border-color: var(--color-primary);
    color: var(--color-primary);
  }
  .spotlight-empty {
    text-align: center;
    color: var(--color-text-muted);
    padding: 2rem;
  }
  .spotlight-empty p {
    margin-top: 1rem;
    font-size: 0.95rem;
    line-height: 1.6;
  }
  .spotlight-empty .hint {
    font-size: 0.8rem;
    color: var(--color-text-light);
    font-style: italic;
    margin-top: 0.5rem;
  }

  @media (max-width: 900px) {
    .globe-wrapper {
      flex: 0 0 100%;
      min-height: 360px;
    }
  }
</style>
