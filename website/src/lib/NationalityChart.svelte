<script>
  import * as d3 from 'd3';

  let { data, byDecade, selectedDecade } = $props();

  let barEl;
  let bumpEl;

  const palette = ['#c1440e','#2c5f7c','#8b6914','#6a9e5f','#9b59b6','#e67e22','#1abc9c','#e74c3c','#3498db','#2ecc71','#f39c12','#8e44ad','#16a085','#d35400','#2980b9'];

  let filteredData = $derived.by(() => {
    const range = selectedDecade;
    if (!range) return data;

    const filtered = byDecade.filter(d => d.decade >= range.min && d.decade <= range.max);
    if (!filtered.length) return data;
    const map = {};
    filtered.forEach(d => { map[d.nationality] = (map[d.nationality] || 0) + d.count; });
    return Object.entries(map).map(([nationality, count]) => ({ nationality, count }))
      .sort((a, b) => b.count - a.count);
  });

  let rangeKey = $derived(selectedDecade ? `${selectedDecade.min}-${selectedDecade.max}` : 'all');

  $effect(() => {
    const _ = rangeKey;
    if (!barEl) return;
    const topData = filteredData.slice(0, 12);
    if (!topData.length) {
      d3.select(barEl).selectAll('*').remove();
      return;
    }
    drawBar(topData);
  });

  $effect(() => {
    const _ = rangeKey;
    if (!bumpEl) return;
    if (!byDecade.length) {
      d3.select(bumpEl).selectAll('*').remove();
      return;
    }
    drawBump(byDecade);
  });

  function drawBar(bdata) {
    const el = d3.select(barEl);
    el.selectAll('*').remove();

    const margin = { top: 5, right: 60, bottom: 5, left: 95 };
    const width = 400, height = bdata.length * 32;

    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleLinear().domain([0, d3.max(bdata, d => d.count)]).range([0, width]);
    const y = d3.scaleBand().domain(bdata.map(d => d.nationality)).range([0, height]).padding(0.3);

    svg.selectAll('rect')
      .data(bdata)
      .join('rect')
      .attr('x', 0).attr('y', d => y(d.nationality))
      .attr('width', d => x(d.count)).attr('height', y.bandwidth())
      .attr('fill', (d, i) => palette[i % palette.length])
      .attr('rx', 4)
      .attr('opacity', 0.85);

    svg.selectAll('.label')
      .data(bdata)
      .join('text')
      .attr('x', d => x(d.count) + 6)
      .attr('y', d => y(d.nationality) + y.bandwidth() / 2)
      .attr('dy', '0.35em')
      .attr('fill', 'var(--color-text-muted)')
      .attr('font-size', '0.7rem')
      .text(d => d.count.toLocaleString());

    svg.selectAll('.name')
      .data(bdata)
      .join('text')
      .attr('x', -6)
      .attr('y', d => y(d.nationality) + y.bandwidth() / 2)
      .attr('dy', '0.35em')
      .attr('text-anchor', 'end')
      .attr('fill', 'var(--color-text)')
      .attr('font-size', '0.78rem')
      .attr('font-weight', '500')
      .text(d => d.nationality);
  }

  function drawBump(sdata) {
    const el = d3.select(bumpEl);
    el.selectAll('*').remove();

    const margin = { top: 20, right: 110, bottom: 35, left: 45 };
    const width = 550, height = 300;

    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    const nationalities = [...new Set(sdata.map(d => d.nationality))];
    const decades = [...new Set(sdata.map(d => d.decade))].sort((a,b) => a-b);

    const pivoted = decades.map(dec => {
      const row = { decade: dec };
      nationalities.forEach(n => {
        const m = sdata.find(d => d.decade === dec && d.nationality === n);
        row[n] = m ? m.count : 0;
      });
      return row;
    });

    const stack = d3.stack().keys(nationalities).offset(d3.stackOffsetSilhouette);
    const series = stack(pivoted);

    const x = d3.scaleLinear().domain(d3.extent(decades)).range([0, width]);
    const y = d3.scaleLinear()
      .domain([d3.min(series, s => d3.min(s, d => d[0])), d3.max(series, s => d3.max(s, d => d[1]))])
      .range([height, 0]);

    const area = d3.area()
      .x(d => x(d.data.decade))
      .y0(d => y(d[0])).y1(d => y(d[1]))
      .curve(d3.curveBasis);

    svg.selectAll('.stream')
      .data(series)
      .join('path')
      .attr('d', area)
      .attr('fill', (d, i) => palette[i % palette.length])
      .attr('opacity', 0.7)
      .append('title').text(d => d.key);

    if (selectedDecade) {
      svg.append('rect')
        .attr('x', x(selectedDecade.min))
        .attr('width', x(selectedDecade.max) - x(selectedDecade.min))
        .attr('y', 0).attr('height', height)
        .attr('fill', 'var(--color-primary)').attr('opacity', 0.08);
      [selectedDecade.min, selectedDecade.max].forEach(dec => {
        svg.append('line')
          .attr('x1', x(dec)).attr('x2', x(dec))
          .attr('y1', 0).attr('y2', height)
          .attr('stroke', 'var(--color-primary)').attr('stroke-width', 1.5)
          .attr('stroke-dasharray', '6,3');
      });
    }

    svg.append('g').attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).tickFormat(d => `${d}`).ticks(8))
      .call(g => g.select('.domain').attr('stroke', 'var(--color-border)'))
      .selectAll('text').attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem');

    // Legend
    const legend = svg.append('g').attr('transform', `translate(${width + 12}, ${height/2 - nationalities.length * 9})`);
    nationalities.forEach((n, i) => {
      const g = legend.append('g').attr('transform', `translate(0, ${i * 18})`);
      g.append('circle').attr('cx', 5).attr('cy', 5).attr('r', 5).attr('fill', palette[i % palette.length]);
      g.append('text').attr('x', 14).attr('y', 9).attr('fill', 'var(--color-text-muted)')
        .attr('font-size', '0.65rem').text(n);
    });
  }
</script>

<div class="chart-card nat-layout">
  <div class="nat-bar" bind:this={barEl}></div>
  <div class="nat-stream" bind:this={bumpEl}></div>
</div>

<style>
  .nat-layout {
    display: flex;
    gap: 2rem;
    flex-wrap: wrap;
  }
  .nat-bar { flex: 0 0 380px; min-width: 300px; }
  .nat-stream { flex: 1; min-width: 350px; }
</style>
