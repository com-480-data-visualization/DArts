<script>
  let { summary } = $props();
</script>

<header class="hero">
  <div class="hero-bg">
    <div class="hero-brushstroke s1"></div>
    <div class="hero-brushstroke s2"></div>
    <div class="hero-brushstroke s3"></div>
  </div>
  <div class="hero-content">
    <p class="hero-eyebrow">COM-480 Data Visualization</p>
    <h1 class="hero-title">DArts</h1>
    <p class="hero-tagline">Exploring Diversity in the<br/>Museum of Modern Art Collection</p>

    <div class="stat-grid">
      <div class="stat-card">
        <div class="value">{summary.total_artworks.toLocaleString()}</div>
        <div class="label">Artworks</div>
      </div>
      <div class="stat-card">
        <div class="value">{summary.total_artists.toLocaleString()}</div>
        <div class="label">Artists</div>
      </div>
      <div class="stat-card">
        <div class="value">{summary.unique_nationalities}</div>
        <div class="label">Nationalities</div>
      </div>
      <div class="stat-card">
        <div class="value">{summary.date_max - summary.date_min}</div>
        <div class="label">Years of Art</div>
      </div>
    </div>

    <nav class="hero-nav">
      <a href="#globe">Globe</a>
      <a href="#gender">Gender</a>
      <a href="#geography">Geography</a>
      <a href="#departments">Departments</a>
      <a href="#timeline">Timeline</a>
    </nav>

    <div class="scroll-hint">
      <span>Scroll to explore</span>
      <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
        <path d="M10 4v12m0 0l-4-4m4 4l4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
      </svg>
    </div>
  </div>
</header>

<style>
  .hero {
    min-height: 100vh;
    display: flex;
    align-items: center;
    justify-content: center;
    text-align: center;
    padding: 2rem;
    position: relative;
    overflow: hidden;
    background: linear-gradient(160deg, #faf8f5 0%, #f3efe9 40%, #ede4d8 100%);
  }

  .hero-bg {
    position: absolute;
    inset: 0;
    pointer-events: none;
    overflow: hidden;
  }

  .hero-brushstroke {
    position: absolute;
    border-radius: 50%;
    filter: blur(80px);
    opacity: 0.35;
  }
  .s1 {
    width: 500px; height: 500px;
    background: #c1440e;
    top: -10%; right: -5%;
    animation: float1 20s ease-in-out infinite;
  }
  .s2 {
    width: 400px; height: 400px;
    background: #2c5f7c;
    bottom: -10%; left: -5%;
    animation: float2 25s ease-in-out infinite;
  }
  .s3 {
    width: 300px; height: 300px;
    background: #8b6914;
    top: 40%; left: 50%;
    animation: float3 18s ease-in-out infinite;
  }

  @keyframes float1 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-30px, 20px); } }
  @keyframes float2 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(20px, -30px); } }
  @keyframes float3 { 0%,100% { transform: translate(0,0); } 50% { transform: translate(-20px, -15px); } }

  .hero-content {
    position: relative;
    z-index: 1;
    max-width: 800px;
  }

  .hero-eyebrow {
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.2em;
    color: var(--color-text-muted);
    font-weight: 500;
    margin-bottom: 0.75rem;
  }

  .hero-title {
    font-family: var(--font-heading);
    font-size: clamp(4rem, 10vw, 7rem);
    font-weight: 700;
    letter-spacing: -0.03em;
    color: var(--color-primary);
    margin-bottom: 0.3rem;
    line-height: 1;
  }

  .hero-tagline {
    font-family: var(--font-heading);
    font-size: clamp(1.1rem, 2.5vw, 1.5rem);
    font-weight: 400;
    font-style: italic;
    color: var(--color-text-muted);
    margin-bottom: 3rem;
    line-height: 1.4;
  }

  .hero-nav {
    display: flex;
    gap: 0.75rem;
    justify-content: center;
    flex-wrap: wrap;
    margin-top: 2.5rem;
  }

  .hero-nav a {
    color: var(--color-text-muted);
    text-decoration: none;
    font-size: 0.85rem;
    font-weight: 500;
    padding: 0.5rem 1.2rem;
    border: 1px solid var(--color-border);
    border-radius: 100px;
    transition: all 0.25s;
    background: rgba(255,255,255,0.6);
    backdrop-filter: blur(4px);
  }

  .hero-nav a:hover {
    color: var(--color-primary);
    border-color: var(--color-primary);
    background: white;
    transform: translateY(-1px);
    box-shadow: var(--shadow-sm);
  }

  .scroll-hint {
    margin-top: 3rem;
    color: var(--color-text-light);
    font-size: 0.75rem;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    animation: pulse 2s ease-in-out infinite;
  }

  @keyframes pulse { 0%,100% { opacity: 0.5; } 50% { opacity: 1; } }
</style>
