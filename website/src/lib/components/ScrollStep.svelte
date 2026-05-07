<script>
  import { onMount } from 'svelte';
  import { filters, setActiveSceneStep } from '../stores/filters.js';
  import { observeScrollStep } from '../utils/scrollytelling.js';

  export let scene = 0;
  export let step = 0;

  let node;
  $: isActive = $filters.activeScene === scene && $filters.activeStep === step;

  onMount(() => {
    if (!node) return undefined;
    return observeScrollStep(node, {
      scene,
      step,
      onActive: () => setActiveSceneStep(scene, step),
    });
  });
</script>

<div bind:this={node} class="scroll-step" class:is-active={isActive} data-scene={scene} data-step={step}>
  <slot />
</div>

<style>
  .scroll-step {
    min-height: 70vh;
    display: flex;
    align-items: center;
    border-left: 2px solid transparent;
    padding-left: var(--space-2);
    transition: border-color var(--duration-state) var(--ease-out);
  }

  .scroll-step.is-active {
    border-color: var(--accent-primary);
  }

  @media (prefers-reduced-motion: reduce) {
    .scroll-step {
      transition: none;
    }
  }
</style>
