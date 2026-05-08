<script>
  import AnchorBar from '../charts/AnchorBar.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import { matchArtist } from '../utils/match.js';
  import './scene5Quiz.css';

  const decadeChoices = [
    ['Pre-1900s', [1860, 1900]],
    ['1910s-30s', [1910, 1930]],
    ['1940s-60s', [1940, 1960]],
    ['1970s-80s', [1970, 1980]],
    ['1990s-2000s', [1990, 2000]],
    ['2010s-now', [2010, 2020]],
  ];
  const regions = [
    'North America',
    'Latin America & Caribbean',
    'Europe',
    'Africa',
    'Western & Central Asia',
    'East Asia',
    'South & Southeast Asia',
    'Oceania',
  ];
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

  function decadeLabel(range) {
    return decadeChoices.find(([, value]) => value[0] === range?.[0] && value[1] === range?.[1])?.[0] ?? '';
  }

  function initials(name = '') {
    return name
      .split(' ')
      .filter(Boolean)
      .slice(0, 2)
      .map((part) => part[0])
      .join('');
  }
</script>

<section class="scene-quiz" aria-labelledby="scene-5-title">
  <div class="quiz-shell">
    <SceneTitle
      kicker="Scene 5"
      title="Who are you in the collection?"
      subline="Meet someone you'd never have heard of."
      dark
    />
    <div class="quiz-layout">
      <div class="question-panel">
        <ol class="answer-trail" aria-label="Quiz progress">
          <li class:active={stage === 0} class:done={answers.decadeRange}>
            <span>1</span>
            <p>Decade</p>
            <strong>{answers.decadeRange ? decadeLabel(answers.decadeRange) : 'Choose'}</strong>
          </li>
          <li class:active={stage === 1} class:done={answers.region}>
            <span>2</span>
            <p>Region</p>
            <strong>{answers.region || 'Choose'}</strong>
          </li>
          <li class:active={stage === 2} class:done={answers.medium}>
            <span>3</span>
            <p>Medium</p>
            <strong>{answers.medium || 'Choose'}</strong>
          </li>
        </ol>

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
        {:else}
          <div class="complete-copy">
            <p>Your choices are set. The match favors artists with fewer MoMA records inside that slice.</p>
            <button type="button" onclick={reset}>Start over</button>
          </div>
        {/if}
      </div>

      <aside class="result-panel" class:ready={result?.artist} aria-live="polite">
        {#if loading}
          <div class="loader">
            <span></span>
            <p>Finding someone for you...</p>
          </div>
        {:else if result?.artist}
          <article class="result">
            {#if result.relaxed}
              <p class="note">No exact match. Showing closest fit.</p>
            {/if}
            <div class="result-heading">
              <div class="portrait" aria-hidden="true">{initials(result.artist.name)}</div>
              <div>
                <h3>{result.artist.name}</h3>
                <p>
                  {result.artist.nationality ?? 'nationality unknown'} &middot; {result.artist.gender} &middot; {lifespan(
                    result.artist,
                  )}
                </p>
              </div>
            </div>
            <figure class="work-card">
              <svg viewBox="0 0 420 250" aria-hidden="true">
                <rect x="18" y="18" width="384" height="214"></rect>
                <path d="M52 184 C102 126 130 156 174 98 S274 78 350 150"></path>
                <path d="M58 72 L148 118 L232 62 L356 116"></path>
                <circle cx="108" cy="166" r="18"></circle>
                <circle cx="302" cy="92" r="26"></circle>
                <line x1="42" y1="204" x2="372" y2="204"></line>
              </svg>
              <figcaption>
                <span>Representative artwork</span>
                <em>{result.artist.sample_work_title}</em>
                {#if result.artist.sample_work_year}
                  <b>{result.artist.sample_work_year}</b>
                {/if}
                <b>{result.artist.medium_primary}</b>
              </figcaption>
            </figure>
            <AnchorBar artistName={result.artist.name} artistCount={result.artist.n_works} />
            <div class="actions">
              <button type="button" onclick={reset}>Try again</button>
              <a href={`https://www.moma.org/artists/${result.artist.artist_id}`} target="_blank" rel="noopener"
                >Open on MoMA</a
              >
            </div>
          </article>
        {:else}
          <div class="empty-result">
            <div class="portrait preview" aria-hidden="true">?</div>
            <p>Your artist match will appear here.</p>
          </div>
        {/if}
      </aside>
    </div>
  </div>
</section>
