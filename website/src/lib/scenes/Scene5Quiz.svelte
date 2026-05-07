<script>
  import AnchorBar from '../charts/AnchorBar.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import { matchArtist } from '../utils/match.js';

  const decadeChoices = [
    ['Pre-1900s', [1860, 1900]],
    ['1910s-30s', [1910, 1930]],
    ['1940s-60s', [1940, 1960]],
    ['1970s-80s', [1970, 1980]],
    ['1990s-2000s', [1990, 2000]],
    ['2010s-now', [2010, 2020]],
  ];
  const regions = ['North America', 'Latin America & Caribbean', 'Europe', 'Africa', 'Western & Central Asia', 'East Asia', 'South & Southeast Asia', 'Oceania'];
  const mediums = ['Photography', 'Drawing', 'Sculpture', 'Painting', 'Film/Video', 'Design'];

  let stage = $state(0);
  let answers = $state({ decadeRange: null, region: '', medium: '' });
  let artists = $state([]);
  let loading = $state(false);
  let result = $state(null);
  let loadPromise = null;

  async function loadArtists() {
    if (artists.length) return artists;
    if (!loadPromise) loadPromise = fetch('./data/artist_index.json').then((r) => r.json());
    artists = await loadPromise;
    return artists;
  }

  function chooseDecade(range) {
    answers = { ...answers, decadeRange: range };
    window.setTimeout(() => (stage = 1), 200);
  }

  function chooseRegion(region) {
    answers = { ...answers, region };
    window.setTimeout(() => (stage = 2), 200);
  }

  async function chooseMedium(medium) {
    answers = { ...answers, medium };
    stage = 3;
    loading = true;
    const started = performance.now();
    const loaded = await loadArtists();
    const elapsed = performance.now() - started;
    if (elapsed < 600) await new Promise((resolve) => window.setTimeout(resolve, 600 - elapsed));
    result = matchArtist(loaded, { ...answers, medium });
    loading = false;
    stage = 3;
  }

  function reset() {
    stage = 0;
    answers = { decadeRange: null, region: '', medium: '' };
    result = null;
    loading = false;
  }

  function lifespan(artist) {
    if (artist.year_birth && artist.year_death) return `${artist.year_birth}-${artist.year_death}`;
    if (artist.year_birth) return `born ${artist.year_birth}`;
    return 'lifespan unknown';
  }
</script>

<section class="scene-quiz" aria-labelledby="scene-5-title">
  <div class="quiz-card">
    <SceneTitle kicker="Scene 5" title="Meet someone you'd never have heard of." dark />
    {#if stage === 0}
      <fieldset>
        <legend>Which decade are you drawn to?</legend>
        {#each decadeChoices as [label, range]}
          <button type="button" onclick={() => chooseDecade(range)}>{label}</button>
        {/each}
      </fieldset>
    {:else if stage === 1}
      <fieldset>
        <legend>Which part of the world?</legend>
        {#each regions as region}
          <button type="button" onclick={() => chooseRegion(region)}>{region}</button>
        {/each}
      </fieldset>
    {:else if stage === 2}
      <fieldset>
        <legend>Which medium speaks to you?</legend>
        {#each mediums as medium}
          <button type="button" onclick={() => chooseMedium(medium)}>{medium}</button>
        {/each}
      </fieldset>
    {:else if loading}
      <p class="loader">Finding someone for you...</p>
    {:else if result?.artist}
      <article class="result">
        {#if result.relaxed}
          <p class="note">No exact match. Showing closest fit.</p>
        {/if}
        <h3>{result.artist.name}</h3>
        <p>{result.artist.nationality} · {result.artist.gender} · {lifespan(result.artist)}</p>
        <p><em>{result.artist.sample_work_title}</em>{#if result.artist.sample_work_year}, {result.artist.sample_work_year}{/if} · {result.artist.sample_work_medium}</p>
        <AnchorBar artistName={result.artist.name} artistCount={result.artist.n_works} />
        <div class="actions">
          <button type="button" onclick={reset}>Try again</button>
          <a href={`https://www.moma.org/artists/${result.artist.artist_id}`} target="_blank" rel="noopener">Open on MoMA</a>
        </div>
      </article>
    {/if}
  </div>
</section>

<style>
  .scene-quiz {
    min-height: 100vh;
    display: grid;
    place-items: center;
    padding: var(--space-4);
    color: var(--fg-on-dark-strong);
    background: var(--bg-dark);
  }

  .quiz-card {
    width: min(44rem, 100%);
  }

  fieldset {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
    margin: var(--space-4) 0 0;
    padding: 0;
    border: 0;
  }

  legend {
    width: 100%;
    margin-bottom: var(--space-2);
    color: var(--fg-on-dark-mute);
    font-family: var(--font-body);
    font-size: var(--type-h2-size);
    line-height: var(--type-h2-line);
  }

  button,
  a {
    border: 1px solid var(--fg-on-dark-mute);
    padding: var(--space-1) var(--space-2);
    color: var(--fg-on-dark-strong);
    background: transparent;
    cursor: pointer;
    font-family: var(--font-ui);
    font-size: var(--type-body-size);
    text-decoration: none;
  }

  button:hover,
  a:hover {
    border-color: var(--accent-primary);
    color: var(--accent-primary);
  }

  .loader,
  .note,
  .result p {
    color: var(--fg-on-dark-mute);
    font-family: var(--font-body);
  }

  .result {
    margin-top: var(--space-4);
  }

  h3 {
    margin: var(--space-2) 0;
    color: var(--fg-on-dark-strong);
    font-family: var(--font-display);
    font-size: var(--type-h1-size);
    line-height: var(--type-h1-line);
  }

  .actions {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
    margin-top: var(--space-3);
  }
</style>
