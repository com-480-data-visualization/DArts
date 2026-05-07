<script>
  import { line, scaleLinear } from 'd3';

  export let data = [];

  const width = 210;
  const height = 120;
  const margin = { top: 18, right: 10, bottom: 18, left: 28 };
  const x = scaleLinear()
    .domain([1860, 2020])
    .range([margin.left, width - margin.right]);
  const y = scaleLinear()
    .domain([0, 0.6])
    .range([height - margin.bottom, margin.top]);
  const pathFor = line()
    .x((d) => x(d.decade))
    .y((d) => y(d.femaleShare));

  $: panels = buildPanels(data);

  function buildPanels(rows) {
    const grouped = new Map();
    for (const row of rows) {
      if (row.decade === null) continue;
      const key = row.department;
      if (!grouped.has(key)) grouped.set(key, new Map());
      const bucket = grouped.get(key);
      const item = bucket.get(row.decade) ?? { decade: row.decade, female: 0, total: 0 };
      item.total += row.n;
      if (row.gender === 'female') item.female += row.n;
      bucket.set(row.decade, item);
    }
    return [...grouped.entries()]
      .map(([department, values]) => {
        const series = [...values.values()]
          .sort((a, b) => a.decade - b.decade)
          .map((d) => ({
            decade: d.decade,
            femaleShare: d.total ? d.female / d.total : 0,
            n: d.total,
          }));
        const final = [...series].reverse().find((d) => d.n > 0) ?? { femaleShare: 0, n: 0 };
        return { department, series, finalShare: final.femaleShare, finalN: final.n };
      })
      .sort((a, b) => b.finalShare - a.finalShare)
      .slice(0, 8);
  }
</script>

<div class="multiples" aria-label="Department small multiples of female-credited share">
  {#each panels as panel}
    <article>
      <h3>{panel.department}</h3>
      <p class="type-mono">{(panel.finalShare * 100).toFixed(0)}%</p>
      <svg viewBox={`0 0 ${width} ${height}`} role="img" aria-label={`${panel.department} female share trend`}>
        <line class="parity" x1={margin.left} x2={width - margin.right} y1={y(0.5)} y2={y(0.5)} />
        <path d={pathFor(panel.series)} />
      </svg>
    </article>
  {/each}
</div>

<style>
  .multiples {
    display: grid;
    grid-template-columns: repeat(4, minmax(0, 1fr));
    gap: var(--space-2);
  }

  article {
    padding: var(--space-2);
    background: var(--bg-paper);
    border: 1px solid var(--rule-on-light);
  }

  h3 {
    margin: 0;
    min-height: 2.8rem;
    font-family: var(--font-ui);
    font-size: var(--type-small-size);
    line-height: var(--type-small-line);
  }

  p {
    margin: var(--space-1) 0;
    color: var(--gender-female);
  }

  svg {
    width: 100%;
    height: auto;
  }

  path {
    fill: none;
    stroke: var(--gender-female);
    stroke-width: 2;
  }

  .parity {
    stroke: var(--fg-on-light-mute);
    stroke-dasharray: 3 3;
    opacity: 0.55;
  }

  @media (max-width: 900px) {
    .multiples {
      grid-template-columns: repeat(2, minmax(0, 1fr));
    }
  }

  @media (max-width: 560px) {
    .multiples {
      grid-template-columns: 1fr;
    }

    h3 {
      min-height: auto;
    }
  }
</style>
