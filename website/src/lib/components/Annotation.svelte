<script>
  export let x = 0;
  export let y = 0;
  export let dx = 0;
  export let dy = 0;
  export let label;
  export let value = '';
  export let emphasis = '';
  export let width = 180;
</script>

<g class="annotation" class:strong={emphasis === 'strong'}>
  <line x1={x} y1={y} x2={x + dx} y2={y + dy} />
  <circle cx={x} cy={y} r="3" />
  <foreignObject x={x + dx} y={y + dy - 20} {width} height="120">
    <div class="note">
      {#if value}
        <span class="value">{value}</span>
      {/if}
      <span>{label}</span>
    </div>
  </foreignObject>
</g>

<style>
  .annotation {
    color: var(--fg-on-light-strong);
    pointer-events: none;
  }

  line {
    stroke: currentColor;
    stroke-width: 1;
  }

  circle {
    fill: currentColor;
  }

  .note {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    color: currentColor;
    font-family: var(--font-body);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  .value {
    color: var(--fg-on-light-strong);
    font-family: var(--font-mono);
    font-weight: 500;
    font-variant-numeric: tabular-nums;
  }

  .strong .value {
    color: var(--accent-primary);
    font-weight: 700;
  }
</style>
