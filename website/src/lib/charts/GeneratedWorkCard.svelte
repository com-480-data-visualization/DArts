<script>
  let { artist } = $props();

  const palette = ['var(--accent-primary)', 'var(--accent-secondary)', 'var(--seq-2)', 'var(--gender-nonbinary)'];

  function hashString(value = '') {
    let hash = 2166136261;
    for (const char of value) {
      hash ^= char.charCodeAt(0);
      hash = Math.imul(hash, 16777619);
    }
    return hash >>> 0;
  }

  function createRandom(seed) {
    let value = seed || 1;
    return () => {
      value = Math.imul(value, 1664525) + 1013904223;
      return (value >>> 0) / 4294967296;
    };
  }

  function buildArtwork(source) {
    const seed = hashString(`${source?.artist_id}-${source?.sample_work_title}-${source?.medium_primary}`);
    const random = createRandom(seed);
    const medium = source?.medium_primary ?? 'Other';
    const lineCount = medium === 'Drawing' ? 8 : medium === 'Photography' ? 3 : medium === 'Film/Video' ? 5 : 6;
    const circles = Array.from({ length: 2 + (seed % 3) }, () => ({
      cx: 64 + random() * 292,
      cy: 58 + random() * 126,
      r: 12 + random() * 24,
      color: palette[Math.floor(random() * palette.length)],
    }));
    const lines = Array.from({ length: lineCount }, (_, index) => {
      const y = 54 + random() * 142;
      const wobble = 18 + random() * 42;
      return {
        d: `M ${44 + random() * 34} ${y.toFixed(1)} C ${(118 + random() * 74).toFixed(1)} ${(y - wobble).toFixed(
          1,
        )}, ${(214 + random() * 70).toFixed(1)} ${(y + wobble).toFixed(1)}, ${(338 + random() * 36).toFixed(1)} ${(
          50 +
          random() * 152
        ).toFixed(1)}`,
        width: index % 3 === 0 ? 3 : 2,
      };
    });
    const panels = Array.from({ length: medium === 'Film/Video' ? 5 : medium === 'Design' ? 6 : 0 }, (_, index) => ({
      x: 48 + index * 58,
      y: 44 + random() * 20,
      height: 92 + random() * 52,
    }));
    return { circles, lines, panels, accent: palette[seed % palette.length], medium };
  }

  let artwork = $derived(buildArtwork(artist));
</script>

<figure class="work-card generated-work-card" aria-label={`Generated visual proxy for ${artist.sample_work_title}`}>
  <svg viewBox="0 0 420 250" aria-hidden="true">
    <rect class="outer" x="18" y="18" width="384" height="214"></rect>
    {#if artwork.panels.length}
      {#each artwork.panels as panel}
        <rect class="panel" x={panel.x} y={panel.y} width="42" height={panel.height}></rect>
      {/each}
    {/if}
    {#if artwork.medium === 'Photography'}
      <rect class="photo-field" x="72" y="56" width="276" height="138"></rect>
      <line class="horizon" x1="72" x2="348" y1="152" y2="152"></line>
    {/if}
    {#each artwork.lines as line}
      <path d={line.d} style:stroke-width={line.width}></path>
    {/each}
    {#each artwork.circles as circle}
      <circle cx={circle.cx} cy={circle.cy} r={circle.r} style:fill={circle.color}></circle>
    {/each}
    <line class="baseline" x1="48" y1="206" x2="372" y2="206"></line>
    <path class="accent" d="M58 34 L362 34" style:stroke={artwork.accent}></path>
  </svg>
  <figcaption>
    <span>Representative artwork</span>
    <em>{artist.sample_work_title}</em>
    {#if artist.sample_work_year}
      <b>{artist.sample_work_year}</b>
    {/if}
    <b>{artist.medium_primary}</b>
  </figcaption>
</figure>

<style>
  .generated-work-card svg {
    background: var(--bg-paper);
  }

  .generated-work-card .outer,
  .generated-work-card path,
  .generated-work-card line,
  .generated-work-card .panel {
    fill: none;
    stroke: var(--fg-on-light-strong);
    stroke-linecap: round;
    stroke-linejoin: round;
  }

  .generated-work-card .outer {
    stroke-width: 2;
  }

  .generated-work-card path,
  .generated-work-card line {
    stroke-width: 2;
  }

  .generated-work-card circle {
    opacity: 0.18;
    stroke: var(--fg-on-light-strong);
    stroke-width: 1.5;
  }

  .generated-work-card .panel,
  .generated-work-card .photo-field {
    fill: color-mix(in srgb, var(--fg-on-light-strong) 6%, transparent);
    stroke-width: 1.5;
  }

  .generated-work-card .horizon,
  .generated-work-card .baseline {
    stroke-width: 2.5;
  }

  .generated-work-card .accent {
    stroke-width: 3;
  }
</style>
