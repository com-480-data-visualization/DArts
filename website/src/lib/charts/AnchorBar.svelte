<script>
  export let artistName;
  export let artistCount = 0;

  const picassoCount = 1242;
  $: pct = Math.max(0.5, Math.min(100, (artistCount / picassoCount) * 100));
</script>

<figure class="anchor-bar" aria-label={`Comparison between Picasso and ${artistName}`}>
  <div class="row">
    <span>Picasso</span>
    <b style:width="100%"></b>
    <em class="type-mono">{picassoCount.toLocaleString()}</em>
  </div>
  <div class="row">
    <span>{artistName}</span>
    <b class="artist" style:width={`${pct}%`}></b>
    <em class="type-mono">{artistCount.toLocaleString()}</em>
  </div>
  <figcaption><strong>Picasso has 1,242 works in the collection.</strong> This artist has {artistCount}.</figcaption>
</figure>

<style>
  .anchor-bar {
    margin: var(--space-3) 0 0;
    display: grid;
    gap: var(--space-1);
  }

  .row {
    display: grid;
    grid-template-columns: 7rem 1fr 4rem;
    gap: var(--space-1);
    align-items: center;
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
  }

  b {
    display: block;
    height: 0.75rem;
    background: var(--fg-on-dark-mute);
  }

  b.artist {
    background: var(--accent-primary);
  }

  em {
    font-style: normal;
    text-align: right;
  }

  figcaption {
    margin-top: var(--space-1);
    color: var(--fg-on-dark-mute);
    font-family: var(--font-body);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  figcaption strong {
    color: var(--fg-on-dark-strong);
  }

  @media (max-width: 480px) {
    .row {
      grid-template-columns: minmax(4rem, 6rem) 1fr 3rem;
    }
  }
</style>
