<script>
  import { onMount } from 'svelte';
  import DecadeSlider from './lib/DecadeSlider.svelte';
  import GlobeChart from './lib/GlobeChart.svelte';
  import GenderChart from './lib/GenderChart.svelte';
  import NationalityChart from './lib/NationalityChart.svelte';
  import TimelineChart from './lib/TimelineChart.svelte';
  import DepartmentChart from './lib/DepartmentChart.svelte';
  import ComponentDemo from './lib/components/ComponentDemo.svelte';
  import FilterStoreDebug from './lib/components/FilterStoreDebug.svelte';
  import Tooltip from './lib/components/Tooltip.svelte';
  import Scene0Hero from './lib/scenes/Scene0Hero.svelte';
  import Scene1Mediums from './lib/scenes/Scene1Mediums.svelte';
  import { initFilterHashSync } from './lib/stores/filters.js';

  let summary = $state(null);
  let genderData = $state([]);
  let genderByDecade = $state([]);
  let nationalityData = $state([]);
  let nationalityByDecade = $state([]);
  let departmentData = $state([]);
  let departmentByDecade = $state([]);
  let timelineData = $state([]);
  let globeCountries = $state([]);
  let globeArtists = $state([]);
  let mediumTotals = $state([]);
  let selectedDecade = $state(null);
  let showFilterDebug = $state(false);
  let showComponentDemo = $state(false);

  onMount(() => {
    const stopHashSync = initFilterHashSync();
    showFilterDebug = import.meta.env.DEV && window.location.pathname.endsWith('/filters');
    showComponentDemo = import.meta.env.DEV && window.location.pathname.endsWith('/components');
    let cancelled = false;
    const files = [
      'summary', 'gender', 'gender_by_decade',
      'nationality', 'nationality_by_decade',
      'department', 'department_by_decade', 'timeline',
      'globe_countries', 'globe_artists', 'medium_totals'
    ];

    Promise.all(files.map(f => fetch(`./data/${f}.json`).then(r => r.json())))
      .then((results) => {
        if (cancelled) return;
        [summary, genderData, genderByDecade, nationalityData,
         nationalityByDecade, departmentData, departmentByDecade,
         timelineData, globeCountries, globeArtists, mediumTotals] = results;
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
  <Scene0Hero {summary} />
  <Scene1Mediums data={mediumTotals} />

  <div class="section">
    <DecadeSlider {timelineData} bind:selectedDecade />
  </div>

  <div class="section" id="globe">
    <div class="section-header">
      <h2 class="section-title">The World at MoMA</h2>
      <p class="section-subtitle">
        Explore the geographic origins of artists in the collection.
        Click any highlighted country to discover a random artist.
      </p>
      <hr class="section-divider" />
    </div>
    <GlobeChart countriesData={globeCountries} artistsData={globeArtists} {selectedDecade} />
  </div>

  <div class="section" id="gender">
    <div class="section-header">
      <h2 class="section-title">Gender Representation</h2>
      <p class="section-subtitle">
        How the balance between male and female artists has evolved across the collection
      </p>
      <hr class="section-divider" />
    </div>
    <GenderChart data={genderData} byDecade={genderByDecade} {selectedDecade} />
  </div>

  <div class="section" id="geography">
    <div class="section-header">
      <h2 class="section-title">Geographic Origins</h2>
      <p class="section-subtitle">
        Where MoMA's artists come from — and how geographic concentration has shifted over time
      </p>
      <hr class="section-divider" />
    </div>
    <NationalityChart data={nationalityData} byDecade={nationalityByDecade} {selectedDecade} />
  </div>

  <div class="section" id="departments">
    <div class="section-header">
      <h2 class="section-title">Curatorial Departments</h2>
      <p class="section-subtitle">
        The composition of the collection across MoMA's curatorial divisions
      </p>
      <hr class="section-divider" />
    </div>
    <DepartmentChart data={departmentData} byDecade={departmentByDecade} {selectedDecade} />
  </div>

  <div class="section" id="timeline">
    <div class="section-header">
      <h2 class="section-title">Temporal Arc</h2>
      <p class="section-subtitle">
        The distribution of artworks across time — the pulse of modern art at MoMA
      </p>
      <hr class="section-divider" />
    </div>
    <TimelineChart data={timelineData} {selectedDecade} />
  </div>

  <footer class="footer">
    <div class="footer-inner">
      <div class="footer-brand">
        <h3 class="footer-title">DArts</h3>
        <p class="footer-description">
          An interactive exploration of diversity in the Museum of Modern Art collection.
          Built for COM-480 Data Visualization at EPFL.
        </p>
      </div>
      <div class="footer-team">
        <p class="team-label">Team</p>
        <div class="team-members">
          <div class="team-member">
            <span class="member-name">Oussama Ghali</span>
            <span class="member-sciper">341478</span>
          </div>
          <div class="team-member">
            <span class="member-name">Nour Guermazi</span>
            <span class="member-sciper">314474</span>
          </div>
          <div class="team-member">
            <span class="member-name">Isabella Linde</span>
            <span class="member-sciper">423106</span>
          </div>
        </div>
      </div>
      <div class="footer-meta">
        <p>Data: <a href="https://github.com/MuseumofModernArt/collection" target="_blank" rel="noopener">MoMA Collection</a></p>
        <p>Built with Svelte & D3.js</p>
        <p class="footer-year">EPFL, 2025</p>
      </div>
    </div>
  </footer>
{:else}
  <div class="loading">
    <div class="loading-spinner"></div>
    <p>Loading collection data...</p>
  </div>
{/if}

<style>
  .loading {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100vh;
    gap: 1rem;
    color: var(--color-text-muted);
  }
  .loading-spinner {
    width: 32px;
    height: 32px;
    border: 3px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
  }
  @keyframes spin { to { transform: rotate(360deg); } }

  .footer {
    background: var(--color-surface-alt);
    border-top: 1px solid var(--color-border);
    margin-top: 2rem;
  }
  .footer-inner {
    max-width: 1100px;
    margin: 0 auto;
    padding: 4rem 2rem 3rem;
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr;
    gap: 3rem;
  }
  .footer-title {
    font-family: var(--font-heading);
    font-size: 1.8rem;
    color: var(--color-primary);
    margin-bottom: 0.75rem;
  }
  .footer-description {
    color: var(--color-text-muted);
    font-size: 0.9rem;
    line-height: 1.7;
    max-width: 320px;
  }
  .team-label {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    color: var(--color-text-light);
    font-weight: 600;
    margin-bottom: 1rem;
  }
  .team-members {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
  }
  .team-member {
    display: flex;
    flex-direction: column;
  }
  .member-name {
    font-weight: 500;
    font-size: 0.95rem;
    color: var(--color-text);
  }
  .member-sciper {
    font-size: 0.78rem;
    color: var(--color-text-light);
    font-family: monospace;
  }
  .footer-meta {
    font-size: 0.85rem;
    color: var(--color-text-muted);
    line-height: 2;
  }
  .footer-meta a {
    color: var(--color-secondary);
    text-decoration: none;
    border-bottom: 1px solid transparent;
    transition: border-color 0.2s;
  }
  .footer-meta a:hover {
    border-color: var(--color-secondary);
  }
  .footer-year {
    margin-top: 0.5rem;
    color: var(--color-text-light);
    font-size: 0.8rem;
  }

  @media (max-width: 768px) {
    .footer-inner {
      grid-template-columns: 1fr;
      gap: 2rem;
    }
  }
</style>
