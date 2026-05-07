<footer class="scene-footer" aria-label="Credits and data source">
  <div class="footer-inner">
    <div>
      <h2>DArts</h2>
      <p>Made for COM-480, EPFL · 2026</p>
    </div>
    <div>
      <h3>Team</h3>
      <p>Oussama Ghali · 341478</p>
      <p>Nour Guermazi · 314474</p>
      <p>Isabella Linde · 423106</p>
    </div>
    <div>
      <h3>Links</h3>
      <p><a href="https://github.com/com-480-data-visualization/DArts">GitHub repository</a></p>
      <p><a href="./process_book.pdf">Process book</a></p>
      <p><a href="./screencast.mp4">Screencast</a></p>
    </div>
    <div class="wide">
      <p>Data: Museum of Modern Art Collection (CC0). github.com/MuseumofModernArt/collection.</p>
      <p>
        This project analyzes the <em>recorded</em> MoMA collection. Demographic fields are limited to what MoMA records.
        Absence in the data is not a judgment of curatorial intent or of an artist's significance.
      </p>
    </div>
  </div>
</footer>

<style>
  .scene-footer {
    color: var(--fg-on-dark-mute);
    background: var(--bg-dark);
    border-top: 1px solid color-mix(in srgb, var(--fg-on-dark-mute) 35%, transparent);
  }

  .footer-inner {
    width: min(var(--max-content), calc(100% - var(--space-4)));
    margin: 0 auto;
    padding: var(--space-6) 0;
    display: grid;
    grid-template-columns: 1.2fr 1fr 1fr;
    gap: var(--space-4);
  }

  h2,
  h3,
  p {
    margin: 0;
  }

  h2,
  h3 {
    color: var(--fg-on-dark-strong);
  }

  h2 {
    font-family: var(--font-display);
    font-size: var(--type-h2-size);
  }

  h3 {
    margin-bottom: var(--space-1);
    font-family: var(--font-ui);
    font-size: var(--type-h3-size);
  }

  p,
  a {
    color: var(--fg-on-dark-mute);
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  a:hover {
    color: var(--accent-primary);
  }

  .wide {
    grid-column: 1 / -1;
    max-width: 52rem;
    display: grid;
    gap: var(--space-1);
  }

  @media (max-width: 760px) {
    .footer-inner {
      grid-template-columns: 1fr;
    }
  }
</style>
