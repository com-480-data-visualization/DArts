<script>
  import * as d3 from 'd3';

  let { data, byDecade, selectedDecade } = $props();

  let chartEl;

  const palette = ['#c1440e', '#2c5f7c', '#8b6914', '#6a9e5f', '#9b59b6', '#e67e22', '#1abc9c', '#34495e'];

  function inRange(decade) {
    if (!selectedDecade) return true;
    return decade >= selectedDecade.min && decade <= selectedDecade.max;
  }

  let filteredData = $derived.by(() => {
    if (!selectedDecade) return data;
    const filtered = byDecade.filter(d => inRange(d.decade));
    if (!filtered.length) return data;
    const map = {};
    filtered.forEach(d => { map[d.department] = (map[d.department] || 0) + d.count; });
    return Object.entries(map).map(([department, count]) => ({ department, count }))
      .sort((a, b) => b.count - a.count);
  });

  $effect(() => { if (chartEl && filteredData.length) drawChart(filteredData); });

  function drawChart(cdata) {
    const el = d3.select(chartEl);
    el.selectAll('*').remove();

    const margin = { top: 10, right: 20, bottom: 70, left: 55 };
    const width = 700, height = 320;

    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand().domain(cdata.map(d => d.department)).range([0, width]).padding(0.3);
    const y = d3.scaleLinear().domain([0, d3.max(cdata, d => d.count) * 1.08]).range([height, 0]);

    // Gridlines
    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickSize(-width).tickFormat(''))
      .call(g => g.select('.domain').remove())
      .selectAll('line').attr('stroke', 'var(--color-border)').attr('stroke-dasharray', '3,3');

    // Bars with gradient
    const defs = svg.append('defs');
    cdata.forEach((d, i) => {
      const grad = defs.append('linearGradient').attr('id', `dept-${i}`).attr('x1',0).attr('y1',0).attr('x2',0).attr('y2',1);
      grad.append('stop').attr('offset', '0%').attr('stop-color', palette[i % palette.length]).attr('stop-opacity', 0.9);
      grad.append('stop').attr('offset', '100%').attr('stop-color', palette[i % palette.length]).attr('stop-opacity', 0.6);
    });

    svg.selectAll('rect')
      .data(cdata)
      .join('rect')
      .attr('x', d => x(d.department))
      .attr('y', d => y(d.count))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.count))
      .attr('fill', (d, i) => `url(#dept-${i})`)
      .attr('rx', 6)
      .append('title').text(d => `${d.department}: ${d.count.toLocaleString()}`);

    // Value labels
    svg.selectAll('.val')
      .data(cdata)
      .join('text')
      .attr('x', d => x(d.department) + x.bandwidth() / 2)
      .attr('y', d => y(d.count) - 8)
      .attr('text-anchor', 'middle')
      .attr('fill', 'var(--color-text-muted)')
      .attr('font-size', '0.72rem')
      .attr('font-weight', '600')
      .text(d => d.count >= 1000 ? `${(d.count/1000).toFixed(1)}k` : d.count);

    svg.append('g').attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x))
      .call(g => g.select('.domain').attr('stroke', 'var(--color-border)'))
      .selectAll('text')
      .attr('fill', 'var(--color-text-muted)').attr('font-size', '0.72rem')
      .attr('transform', 'rotate(-30)').attr('text-anchor', 'end');

    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.2s')))
      .call(g => g.select('.domain').remove())
      .selectAll('text').attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem');
  }
</script>

<div class="chart-card" bind:this={chartEl}></div>
