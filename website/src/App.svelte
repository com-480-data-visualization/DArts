<script>
  import { onMount } from 'svelte';
  import ComponentDemo from './lib/components/ComponentDemo.svelte';
  import FilterStoreDebug from './lib/components/FilterStoreDebug.svelte';
  import Tooltip from './lib/components/Tooltip.svelte';
  import Scene0Hero from './lib/scenes/Scene0Hero.svelte';
  import Scene1Mediums from './lib/scenes/Scene1Mediums.svelte';
  import Scene2Globe from './lib/scenes/Scene2Globe.svelte';
  import Scene3Gender from './lib/scenes/Scene3Gender.svelte';
  import Scene4Explorer from './lib/scenes/Scene4Explorer.svelte';
  import Scene5Quiz from './lib/scenes/Scene5Quiz.svelte';
  import Scene6Footer from './lib/scenes/Scene6Footer.svelte';
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
  let showFilterDebug = $state(false);
  let showComponentDemo = $state(false);

  onMount(() => {
    const stopHashSync = initFilterHashSync();
    showFilterDebug = import.meta.env.DEV && window.location.pathname.endsWith('/filters');
    showComponentDemo = import.meta.env.DEV && window.location.pathname.endsWith('/components');
    let cancelled = false;
    const files = [
      'summary',
      'gender_by_decade',
      'timeline',
      'medium_totals',
      'country_by_decade',
      'country_summary',
      'gender_by_decade_country',
      'gender_by_decade_department',
      'medium_breakdown',
    ];

    Promise.all(files.map((file) => fetch(`./data/${file}.json`).then((response) => response.json())))
      .then((results) => {
        if (cancelled) return;
        [
          summary,
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
    <Scene1Mediums data={mediumTotals} />
    <Scene2Globe {countryByDecade} {countrySummary} timeline={timelineData} />
    <Scene3Gender
      genderByDecade={genderByDecade}
      genderByDepartment={genderByDepartment}
      genderByCountry={genderByCountry}
      {countrySummary}
      timeline={timelineData}
    />
    <Scene4Explorer data={mediumBreakdown} {countrySummary} timeline={timelineData} />
    <Scene5Quiz />
  </main>
  <Scene6Footer />
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
