<script>
  import { filters } from '../stores/filters.js';
  import FilterChip from '../components/FilterChip.svelte';
  import SceneTitle from '../components/SceneTitle.svelte';
  import ScrollStep from '../components/ScrollStep.svelte';
  import Treemap from '../charts/Treemap.svelte';

  let { data = [] } = $props();

  let lockedMedium = $state('');

  let step = $derived($filters.activeScene === 1 ? $filters.activeStep : 0);
  let highlighted = $derived(lockedMedium ? [lockedMedium] : stepHighlight(step));
  let annotation = $derived(stepAnnotation(step));

  function stepHighlight(activeStep) {
    if (activeStep === 1) return ['Drawings & Prints'];
    if (activeStep === 2) return ['Photography', 'Architecture & Design'];
    if (activeStep === 3) return ['Painting & Sculpture'];
    return [];
  }

  function stepAnnotation(activeStep) {
    if (activeStep === 0) {
      return {
        x: 150,
        y: 120,
        dx: 110,
        dy: 64,
        value: '144,149',
        label: 'cleaned works anchor the analysis.',
        width: 205,
      };
    }
    if (activeStep === 1) {
      return { x: 360, y: 214, dx: 86, dy: -86, value: '1 in 2', label: 'works is on paper.', width: 170 };
    }
    if (activeStep === 2) {
      return {
        x: 260,
        y: 508,
        dx: 170,
        dy: -70,
        value: '44.2%',
        label: 'sit in Photography or Architecture & Design.',
        width: 245,
      };
    }
    return {
      x: 608,
      y: 504,
      dx: -244,
      dy: -94,
      value: '1 in 30',
      label: 'works belongs to Painting & Sculpture.',
      width: 210,
    };
  }
</script>

<section class="scene scene-mediums" aria-labelledby="scene-1-title">
  <div class="scene-grid">
    <div class="sticky-chart">
      <SceneTitle
        kicker="Scene 1"
        title="What MoMA actually collects isn't what you think."
        subline="Area encodes works in each collection area; one color pop-out carries the active claim."
      />
      {#if lockedMedium}
        <div class="lock-row">
          <FilterChip label="Locked" value={lockedMedium} onRemove={() => (lockedMedium = '')} />
        </div>
      {/if}
      <Treemap {data} {highlighted} {annotation} {lockedMedium} onLock={(medium) => (lockedMedium = medium)} />
      <p class="source">
        Source: MoMA Collection. n = {data.reduce((sum, d) => sum + d.n, 0).toLocaleString()} cleaned works.
      </p>
    </div>
    <div class="text-rail">
      <ScrollStep scene={1} step={0}>
        <p>
          Start with the whole collection. The first surprise is not geography or gender; it is the shape of the archive
          itself.
        </p>
      </ScrollStep>
      <ScrollStep scene={1} step={1}>
        <p>
          Drawings & Prints dominates the count. The familiar museum visit is only one view into a much larger paper
          collection.
        </p>
      </ScrollStep>
      <ScrollStep scene={1} step={2}>
        <p>
          Photography and Architecture & Design account for most of the remaining volume, reinforcing how much of MoMA
          is reproducible, archival, or design-oriented.
        </p>
      </ScrollStep>
      <ScrollStep scene={1} step={3}>
        <p>
          Painting & Sculpture is culturally central, but numerically small. That imbalance matters before we ask who is
          represented.
        </p>
      </ScrollStep>
    </div>
  </div>
</section>

<style>
  .scene-mediums {
    background: var(--bg-light);
    color: var(--fg-on-light-strong);
  }

  .scene-grid {
    display: grid;
    grid-template-columns: minmax(0, 3fr) minmax(18rem, 2fr);
    gap: var(--space-6);
    width: min(var(--max-content), calc(100% - var(--space-4)));
    margin: 0 auto;
    padding: var(--space-10) 0;
  }

  .sticky-chart {
    position: sticky;
    top: var(--space-2);
    align-self: start;
    min-height: calc(100vh - var(--space-4));
    display: grid;
    align-content: center;
    gap: var(--space-3);
  }

  .text-rail {
    font-family: var(--font-body);
    font-size: clamp(var(--type-body-size), 2vw, 1.25rem);
    line-height: var(--type-body-line);
    color: var(--fg-on-light-mute);
  }

  .text-rail p {
    max-width: 28rem;
    margin: 0;
  }

  .lock-row {
    display: flex;
  }

  .source {
    margin: 0;
    color: var(--fg-on-light-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  @media (max-width: 900px) {
    .scene-grid {
      grid-template-columns: 1fr;
      padding: var(--space-6) 0;
    }

    .sticky-chart {
      position: relative;
      top: auto;
      min-height: auto;
    }
  }
</style>
