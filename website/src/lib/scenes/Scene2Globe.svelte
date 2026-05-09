<script>
  import { filters, clearSelectedCountry } from '../stores/filters.js';
  import DecadeSlider from '../components/DecadeSlider.svelte';
  import FilterChip from '../components/FilterChip.svelte';
  import Legend from '../components/Legend.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import ScrollStep from '../components/ScrollStep.svelte';
  import Globe from '../charts/Globe.svelte';
  import './scene2Globe.css';

  let { countryByDecade = [], countrySummary = [], timeline = [] } = $props();

  const topThree = new Set(['USA', 'FRA', 'DEU']);

  let active = $derived($filters.activeScene === 2);
  let step = $derived(active ? $filters.activeStep : 0);
  let range = $derived($filters.decadeRange);
  let selectedCountry = $derived($filters.selectedCountry);
  let summaryByIso = $derived(new Map(countrySummary.map((d) => [d.iso3, d])));
  let selectedSummary = $derived(selectedCountry ? summaryByIso.get(selectedCountry) : null);
  let topThreeShare = $derived(computeTopThreeShare(countryByDecade, range));
  let selectedArtistUrl = $derived(
    selectedSummary?.featured_artist_id ? `https://www.moma.org/artists/${selectedSummary.featured_artist_id}` : '',
  );
  let selectedArtistName = $derived(selectedSummary?.featured_artist ?? selectedSummary?.sample_artist ?? '');
  let selectedWorkTitle = $derived(selectedSummary?.featured_work_title ?? selectedSummary?.sample_work_title ?? '');
  let selectedWorkYear = $derived(selectedSummary?.featured_work_year ?? selectedSummary?.sample_work_year ?? '');
  let selectedStory = $derived(
    selectedSummary?.featured_story ??
      `${selectedSummary?.sample_artist} appears in the selected country's records with the representative work ${selectedSummary?.sample_work_title}.`,
  );
  let selectedScore = $derived(selectedSummary?.featured_artist_score ?? null);

  function computeTopThreeShare(rows, decadeRange) {
    const counts = {};
    for (const row of rows) {
      if (row.decade === null || row.decade < decadeRange[0] || row.decade > decadeRange[1]) continue;
      counts[row.iso3] = (counts[row.iso3] || 0) + row.n;
    }
    const total = Object.values(counts).reduce((sum, n) => sum + n, 0);
    const top = [...topThree].reduce((sum, iso3) => sum + (counts[iso3] || 0), 0);
    return total ? top / total : 0;
  }

  function artistInitials(name) {
    return name
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0])
      .join('');
  }
</script>

<section class="scene-globe" aria-labelledby="scene-2-title">
  <div class="globe-stage">
    <div class="globe-copy">
      <SceneTitle
        kicker="Scene 2"
        title="Three countries hold two-thirds of MoMA."
        subline="Country color uses a sequential luminance ramp on credited works. The red-orange exception marks the top three."
        dark
      />
      <div class="steps">
        <ScrollStep scene={2} step={0}
          ><p>Artists from <strong>129</strong> recorded nationalities enter the collection.</p></ScrollStep
        >
        <ScrollStep scene={2} step={1}
          ><p>But once counts appear, the map stops looking global and starts looking concentrated.</p></ScrollStep
        >
        <ScrollStep scene={2} step={2}
          ><p>
            <strong>{(topThreeShare * 100).toFixed(0)}%</strong> of mapped credited works come from the United States, France,
            and Germany.
          </p></ScrollStep
        >
        <ScrollStep scene={2} step={3}
          ><p>Scrub time: the concentration bends, but it does not disappear.</p></ScrollStep
        >
      </div>
      <Legend
        mode="sequential"
        minLabel="< 10"
        midLabel="100"
        maxLabel=">= 1,000"
        caption="Color encodes credited works in the active decade range."
        dark
      />
      <p class="exclusion">Excluded: 2.3% of artist credits have no mapped nationality in the cleaned corpus.</p>
      {#if step >= 3}
        <div class="slider-panel">
          <DecadeSlider {timeline} ariaLabel="Filter globe by decade range" dark />
          <p class="share type-mono">Top-three share: {(topThreeShare * 100).toFixed(1)}%</p>
        </div>
      {/if}
    </div>
    <div class="globe-wrap">
      <Globe {countryByDecade} {step} {active} />
    </div>
    {#if selectedSummary}
      <aside class="country-panel" aria-label={`Selected country ${selectedSummary.country_name}`}>
        <button type="button" class="close" aria-label="Clear selected country" onclick={clearSelectedCountry}>x</button
        >
        <FilterChip label="Filtered" value={selectedSummary.country_name} dark onRemove={clearSelectedCountry} />
        <h3>{selectedSummary.country_name}</h3>
        <dl>
          <div>
            <dt>Works</dt>
            <dd>{selectedSummary.n.toLocaleString()}</dd>
          </div>
          <div>
            <dt>Artists</dt>
            <dd>{selectedSummary.n_artists.toLocaleString()}</dd>
          </div>
          <div>
            <dt>Top medium</dt>
            <dd>{selectedSummary.top_medium}</dd>
          </div>
        </dl>
        <article class="artist-label">
          <p class="eyebrow">Collection prominence pick</p>
          <div class="artist-heading">
            <span class="monogram" aria-hidden="true">{artistInitials(selectedArtistName)}</span>
            <div>
              <h4>{selectedArtistName}</h4>
              <p>
                {selectedSummary.featured_artist_lifespan ?? selectedSummary.sample_lifespan}
                {#if selectedSummary.featured_artist_gender}
                  &middot; {selectedSummary.featured_artist_gender}
                {/if}
                {#if selectedSummary.featured_artist_medium}
                  &middot; {selectedSummary.featured_artist_medium}
                {/if}
              </p>
            </div>
          </div>
          <p class="story">{selectedStory}</p>
          {#if selectedScore !== null}
            <dl class="score-card" aria-label="Collection prominence score components">
              <div>
                <dt>Score</dt>
                <dd>{selectedScore.toFixed(1)}/100</dd>
              </div>
              <div>
                <dt>Works</dt>
                <dd>{selectedSummary.featured_artist_n_works.toLocaleString()}</dd>
              </div>
              <div>
                <dt>Breadth</dt>
                <dd>
                  {selectedSummary.featured_artist_n_departments} departments / {selectedSummary.featured_artist_n_mediums}
                  media
                </dd>
              </div>
            </dl>
          {/if}
          <p class="representative">
            <span>Representative record</span>
            <em>{selectedWorkTitle}</em>
            {#if selectedWorkYear}
              <span>{selectedWorkYear}</span>
            {/if}
          </p>
          <p class="caveat">Collection-based proxy, not a true fame ranking.</p>
          {#if selectedSummary.featured_artist_score_method}
            <details class="score-method">
              <summary>How score is computed</summary>
              <p>{selectedSummary.featured_artist_score_method}</p>
            </details>
          {/if}
          {#if selectedArtistUrl}
            <a class="moma-link" href={selectedArtistUrl} target="_blank" rel="noopener">Open artist on MoMA</a>
          {/if}
        </article>
      </aside>
    {/if}
  </div>
</section>
