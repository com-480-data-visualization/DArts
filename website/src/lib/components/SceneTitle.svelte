<script>
  export let kicker = '';
  export let title;
  export let subline = '';
  export let dark = false;
</script>

<header class="scene-title" class:dark>
  {#if kicker}
    <p class="kicker">{kicker}</p>
  {/if}
  <h2>{title}</h2>
  {#if subline}
    <p class="subline">{subline}</p>
  {/if}
</header>

<style>
  .scene-title {
    max-width: 44rem;
    color: var(--fg-on-light-strong);
  }

  .scene-title.dark {
    color: var(--fg-on-dark-strong);
  }

  .kicker {
    margin: 0 0 var(--space-1);
    color: var(--fg-on-light-strong);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    font-weight: 600;
    letter-spacing: 0.08em;
    line-height: var(--type-small-line);
    text-transform: uppercase;
  }

  h2 {
    margin: 0;
    color: inherit;
    font-family: var(--font-display);
    font-size: var(--type-h1-size);
    line-height: var(--type-h1-line);
  }

  .subline {
    margin: var(--space-2) 0 0;
    color: var(--fg-on-light-mute);
    font-family: var(--font-body);
    font-size: var(--type-body-size);
    line-height: var(--type-body-line);
  }

  .dark .subline {
    color: var(--fg-on-dark-mute);
  }

  .dark .kicker {
    color: var(--fg-on-dark-strong);
  }
</style>
