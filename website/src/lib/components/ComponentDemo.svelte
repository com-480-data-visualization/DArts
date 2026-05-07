<script>
  import Annotation from './Annotation.svelte';
  import DecadeSlider from './DecadeSlider.svelte';
  import FilterChip from './FilterChip.svelte';
  import Legend from './Legend.svelte';
  import SceneTitle from './SceneTitle.svelte';

  const timeline = [
    { decade: 1860, n: 5 },
    { decade: 1900, n: 80 },
    { decade: 1940, n: 220 },
    { decade: 1980, n: 900 },
    { decade: 2020, n: 340 },
  ];

  const genderItems = [
    { label: 'female', color: 'var(--gender-female)' },
    { label: 'male', color: 'var(--gender-male)' },
    { label: 'non-binary', color: 'var(--gender-nonbinary)' },
    { label: 'unknown', color: 'var(--gender-unknown)' },
  ];
</script>

<main class="component-demo">
  <SceneTitle
    kicker="Component demo"
    title="Shared chart primitives are wired to the final design system."
    subline="This route is available in development at /components."
  />
  <section>
    <h3>Decade Slider</h3>
    <DecadeSlider {timeline} />
  </section>
  <section>
    <h3>Legend and Chips</h3>
    <Legend mode="categorical" items={genderItems} caption="Gender encoding is fixed across the site." />
    <div class="chips">
      <FilterChip label="Country" value="France" />
      <FilterChip label="Region" value="Europe" />
    </div>
  </section>
  <section>
    <h3>Annotation</h3>
    <svg viewBox="0 0 420 180" role="img" aria-label="Annotation component demo">
      <rect x="40" y="60" width="180" height="64" fill="var(--seq-1)" />
      <Annotation x={180} y={92} dx={64} dy={-32} value="52%" label="of works sit in one collection area." emphasis="strong" />
    </svg>
  </section>
</main>

<style>
  .component-demo {
    min-height: 100vh;
    padding: var(--space-8) var(--space-4);
    background: var(--bg-light);
  }

  section {
    max-width: var(--max-content);
    margin-top: var(--space-6);
  }

  h3 {
    margin-bottom: var(--space-2);
    font-family: var(--font-ui);
    font-size: var(--type-h3-size);
  }

  .chips {
    display: flex;
    flex-wrap: wrap;
    gap: var(--space-1);
    margin-top: var(--space-2);
  }

  svg {
    width: min(40rem, 100%);
    height: auto;
    background: var(--bg-paper);
    border: 1px solid var(--rule-on-light);
  }
</style>
