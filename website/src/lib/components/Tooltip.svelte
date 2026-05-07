<script>
  import { onDestroy, onMount } from 'svelte';

  const EDGE_GUARD = 200;

  let visible = $state(false);
  let x = $state(0);
  let y = $state(0);
  let content = $state('');
  let placement = $state('right');

  function positionTooltip(detail) {
    x = detail.x ?? 0;
    y = detail.y ?? 0;
    content = detail.content ?? '';
    placement = x > window.innerWidth - EDGE_GUARD ? 'left' : 'right';
    visible = Boolean(content);
  }

  function show(event) {
    positionTooltip(event.detail ?? {});
  }

  function hide() {
    visible = false;
  }

  onMount(() => {
    window.addEventListener('darts:tooltip', show);
    window.addEventListener('darts:tooltip-hide', hide);
  });

  onDestroy(() => {
    window.removeEventListener('darts:tooltip', show);
    window.removeEventListener('darts:tooltip-hide', hide);
  });
</script>

<div
  class="tooltip"
  class:is-visible={visible}
  class:left={placement === 'left'}
  style:transform={`translate(${x}px, ${y}px)`}
  role="status"
  aria-live="polite"
>
  {@html content}
</div>

<style>
  .tooltip {
    position: fixed;
    top: 0;
    left: 0;
    z-index: 2000;
    max-width: 18rem;
    padding: var(--space-1) var(--space-2);
    color: var(--fg-on-dark-strong);
    background: var(--rule);
    border: 1px solid var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
    opacity: 0;
    pointer-events: none;
    translate: var(--space-2) calc(-1 * var(--space-2));
    transition: opacity var(--duration-tooltip-out) var(--ease-out);
  }

  .tooltip.left {
    translate: calc(-100% - var(--space-2)) calc(-1 * var(--space-2));
  }

  .tooltip.is-visible {
    opacity: 1;
    transition-duration: var(--duration-tooltip-in);
  }

  .tooltip :global(.num) {
    font-family: var(--font-mono);
    font-variant-numeric: tabular-nums;
  }
</style>
