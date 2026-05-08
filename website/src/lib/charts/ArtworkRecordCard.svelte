<script>
  let { artist } = $props();
</script>

<figure class="artwork-record-card" aria-label={`Representative artwork record for ${artist.sample_work_title}`}>
  <figcaption>
    <span>Representative artwork record</span>
    <em>{artist.sample_work_title}</em>
    <p class="rights-note">Image not embedded for copyright safety.</p>
    <dl>
      {#if artist.sample_work_year}
        <div>
          <dt>Year</dt>
          <dd>{artist.sample_work_year}</dd>
        </div>
      {/if}
      <div>
        <dt>Medium</dt>
        <dd>{artist.medium_primary}</dd>
      </div>
    </dl>
    {#if artist.sample_work_url}
      <a class="artwork-link" href={artist.sample_work_url} target="_blank" rel="noopener">View real artwork on MoMA</a>
    {:else}
      <p class="missing-link">MoMA artwork record unavailable in this dataset row.</p>
    {/if}
  </figcaption>
</figure>

<style>
  .artwork-record-card {
    margin: var(--space-4) 0 var(--space-2);
    border: 1px solid color-mix(in srgb, var(--fg-on-dark-mute) 40%, transparent);
    border-top: 2px solid var(--accent-primary);
    background: color-mix(in srgb, var(--fg-on-dark-strong) 5%, transparent);
  }

  figcaption {
    display: grid;
    gap: var(--space-1);
    padding: var(--space-3);
    font-family: var(--font-body);
  }

  span,
  dt,
  .rights-note,
  .missing-link {
    margin: 0;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  span,
  dt {
    text-transform: uppercase;
  }

  em {
    color: var(--fg-on-dark-strong);
    font-size: clamp(1.4rem, 3vw, var(--type-h2-size));
    line-height: var(--type-h2-line);
  }

  .rights-note {
    max-width: 34rem;
    line-height: var(--type-small-line);
  }

  dl {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: var(--space-2);
    margin: var(--space-1) 0 0;
    padding: var(--space-1) 0 0;
    border-top: 1px solid color-mix(in srgb, var(--fg-on-dark-mute) 28%, transparent);
  }

  dd {
    margin: 0.125rem 0 0;
    color: var(--fg-on-dark-strong);
    font-family: var(--font-ui);
    font-size: var(--type-body-size);
  }

  .artwork-link {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: fit-content;
    margin-top: var(--space-2);
    border: 1px solid var(--accent-primary);
    padding: var(--space-1) var(--space-2);
    color: var(--fg-on-dark-strong);
    background: color-mix(in srgb, var(--accent-primary) 18%, transparent);
    font-family: var(--font-ui);
    font-size: var(--type-body-size);
    font-weight: 600;
    text-decoration: none;
    transition:
      color var(--duration-tooltip-in) var(--ease-out),
      background-color var(--duration-tooltip-in) var(--ease-out),
      transform var(--duration-tooltip-in) var(--ease-out);
  }

  .artwork-link:hover,
  .artwork-link:focus-visible {
    color: var(--bg-dark);
    background: var(--accent-primary);
    transform: translateY(-1px);
  }

  @media (max-width: 520px) {
    dl {
      grid-template-columns: 1fr;
    }
  }
</style>
