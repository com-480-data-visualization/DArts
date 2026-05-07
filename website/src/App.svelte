<script>
  import { onMount } from 'svelte';
  import ComponentDemo from './lib/components/ComponentDemo.svelte';
  import FilterStoreDebug from './lib/components/FilterStoreDebug.svelte';
  import Tooltip from './lib/components/Tooltip.svelte';
  import Scene0Hero from './lib/scenes/Scene0Hero.svelte';
  import { initFilterHashSync } from './lib/stores/filters.js';

  let summary = $state(null);
  let genderByDecade = $state([]);
  let genderByDepartment = $state([]);
  let timelineData = $state([]);
  let mediumTotals = $state([]);
  let countryByDecade = $state([]);
  let countrySummary = $state([]);
  let genderByCountry = $state([]);
  let mediumBreakdown = $state([]);
  let sceneModules = $state(null);
  let showFilterDebug = $state(false);
  let showComponentDemo = $state(false);

  function deferStoryLoad(callback) {
    let done = false;
    const events = ['wheel', 'touchstart', 'keydown', 'pointerdown'];
    const cleanup = () => events.forEach((event) => window.removeEventListener(event, run));
    const run = () => {
      if (done) return;
      done = true;
      window.clearTimeout(timeoutId);
      cleanup();
      window.setTimeout(callback, 0);
    };
    const timeoutId = window.setTimeout(run, 5500);
    events.forEach((event) => window.addEventListener(event, run, { once: true, passive: true }));
    return () => {
      done = true;
      window.clearTimeout(timeoutId);
      cleanup();
    };
  }

  onMount(() => {
    const stopHashSync = initFilterHashSync();
    showFilterDebug = import.meta.env.DEV && window.location.pathname.endsWith('/filters');
    showComponentDemo = import.meta.env.DEV && window.location.pathname.endsWith('/components');
    let cancelled = false;
    const files = [
      'gender_by_decade',
      'timeline',
      'medium_totals',
      'country_by_decade',
      'country_summary',
      'gender_by_decade_country',
      'gender_by_decade_department',
      'medium_breakdown',
    ];

    fetch('./data/summary.json')
      .then((response) => response.json())
      .then((result) => {
        if (!cancelled) summary = result;
      });

    const cancelSceneLoad = deferStoryLoad(async () => {
      const [modules, results] = await Promise.all([
        Promise.all([
          import('./lib/scenes/Scene1Mediums.svelte'),
          import('./lib/scenes/Scene2Globe.svelte'),
          import('./lib/scenes/Scene3Gender.svelte'),
          import('./lib/scenes/Scene4Explorer.svelte'),
          import('./lib/scenes/Scene5Quiz.svelte'),
          import('./lib/scenes/Scene6Footer.svelte'),
        ]),
        Promise.all(files.map((file) => fetch(`./data/${file}.json`).then((response) => response.json()))),
      ]);
      if (cancelled) return;
      sceneModules = {
        Scene1Mediums: modules[0].default,
        Scene2Globe: modules[1].default,
        Scene3Gender: modules[2].default,
        Scene4Explorer: modules[3].default,
        Scene5Quiz: modules[4].default,
        Scene6Footer: modules[5].default,
      };
      [
        genderByDecade,
        timelineData,
        mediumTotals,
        countryByDecade,
        countrySummary,
        genderByCountry,
        genderByDepartment,
        mediumBreakdown,
      ] = results;
    });

    return () => {
      cancelSceneLoad();
      cancelled = true;
      stopHashSync();
    };
  });
</script>

<Tooltip />

{#if showFilterDebug}
  <FilterStoreDebug />
{/if}

{#if showComponentDemo}
  <ComponentDemo />
{:else if summary}
  <main>
    <Scene0Hero {summary} />
    {#if sceneModules}
      {@const Scene1 = sceneModules.Scene1Mediums}
      {@const Scene2 = sceneModules.Scene2Globe}
      {@const Scene3 = sceneModules.Scene3Gender}
      {@const Scene4 = sceneModules.Scene4Explorer}
      {@const Scene5 = sceneModules.Scene5Quiz}
      <Scene1 data={mediumTotals} />
      <Scene2 {countryByDecade} {countrySummary} timeline={timelineData} />
      <Scene3 {genderByDecade} {genderByDepartment} {genderByCountry} {countrySummary} timeline={timelineData} />
      <Scene4 data={mediumBreakdown} {countrySummary} timeline={timelineData} />
      <Scene5 />
    {:else}
      <section class="story-loading" aria-live="polite">
        <p>Preparing the story...</p>
      </section>
    {/if}
  </main>
  {#if sceneModules}
    {@const Scene6 = sceneModules.Scene6Footer}
    <Scene6 />
  {/if}
{:else}
  <div class="loading">
    <div class="loading-spinner"></div>
    <p>Loading collection data...</p>
  </div>
{/if}

<style>
  .loading {
    min-height: 100vh;
    display: grid;
    place-items: center;
    gap: var(--space-2);
    color: var(--fg-on-light-mute);
    background: var(--bg-light);
    font-family: var(--font-ui);
  }

  .loading-spinner {
    width: 2rem;
    height: 2rem;
    border: 2px solid var(--rule-on-light);
    border-top-color: var(--accent-primary);
    animation: spin 800ms linear infinite;
  }

  .story-loading {
    min-height: 40vh;
    display: grid;
    place-items: center;
    color: var(--fg-on-light-mute);
    background: var(--bg-light);
    font-family: var(--font-ui);
  }

  @keyframes spin {
    to {
      rotate: 360deg;
    }
  }

  @media (prefers-reduced-motion: reduce) {
    .loading-spinner {
      animation: none;
    }
  }
</style>
