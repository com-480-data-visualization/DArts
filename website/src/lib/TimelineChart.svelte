<script>
  import * as d3 from 'd3';

  let { data, selectedDecade } = $props();

  let chartEl;

  $effect(() => { if (chartEl && data.length) drawChart(data); });

  function drawChart(tdata) {
    const el = d3.select(chartEl);
    el.selectAll('*').remove();

    const sorted = [...tdata].sort((a, b) => a.decade - b.decade);
    const margin = { top: 20, right: 20, bottom: 40, left: 55 };
    const width = 850, height = 280;

    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    const x = d3.scaleBand().domain(sorted.map(d => d.decade)).range([0, width]).padding(0.2);
    const y = d3.scaleLinear().domain([0, d3.max(sorted, d => d.count) * 1.08]).range([height, 0]);

    // Gridlines
    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickSize(-width).tickFormat(''))
      .call(g => g.select('.domain').remove())
      .selectAll('line').attr('stroke', 'var(--color-border)').attr('stroke-dasharray', '3,3');

    // Gradient
    const defs = svg.append('defs');
    const grad = defs.append('linearGradient').attr('id', 'tl-grad').attr('x1',0).attr('y1',0).attr('x2',0).attr('y2',1);
    grad.append('stop').attr('offset', '0%').attr('stop-color', '#8b6914').attr('stop-opacity', 0.9);
    grad.append('stop').attr('offset', '100%').attr('stop-color', '#8b6914').attr('stop-opacity', 0.4);

    const gradActive = defs.append('linearGradient').attr('id', 'tl-active').attr('x1',0).attr('y1',0).attr('x2',0).attr('y2',1);
    gradActive.append('stop').attr('offset', '0%').attr('stop-color', '#c1440e').attr('stop-opacity', 1);
    gradActive.append('stop').attr('offset', '100%').attr('stop-color', '#c1440e').attr('stop-opacity', 0.6);

    svg.selectAll('rect')
      .data(sorted)
      .join('rect')
      .attr('x', d => x(d.decade))
      .attr('y', d => y(d.count))
      .attr('width', x.bandwidth())
      .attr('height', d => height - y(d.count))
      .attr('fill', d => selectedDecade && d.decade >= selectedDecade.min && d.decade <= selectedDecade.max ? 'url(#tl-active)' : 'url(#tl-grad)')
      .attr('opacity', d => selectedDecade && (d.decade < selectedDecade.min || d.decade > selectedDecade.max) ? 0.25 : 1)
      .attr('rx', 4)
      .append('title').text(d => `${d.decade}s: ${d.count.toLocaleString()} artworks`);

    // Labels on active range
    if (selectedDecade) {
      const inRange = sorted.filter(d => d.decade >= selectedDecade.min && d.decade <= selectedDecade.max);
      const total = d3.sum(inRange, d => d.count);
      if (inRange.length) {
        const midBar = inRange[Math.floor(inRange.length / 2)];
        svg.append('text')
          .attr('x', x(midBar.decade) + x.bandwidth() / 2)
          .attr('y', y(d3.max(inRange, d => d.count)) - 10)
          .attr('text-anchor', 'middle')
          .attr('fill', 'var(--color-primary)').attr('font-size', '0.8rem').attr('font-weight', '700')
          .text(`${total.toLocaleString()} artworks`);
      }
    }

    svg.append('g').attr('transform', `translate(0,${height})`)
      .call(d3.axisBottom(x).tickFormat(d => `${d}s`))
      .call(g => g.select('.domain').attr('stroke', 'var(--color-border)'))
      .selectAll('text').attr('fill', 'var(--color-text-muted)').attr('font-size', '0.68rem')
      .attr('transform', 'rotate(-45)').attr('text-anchor', 'end');

    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.2s')))
      .call(g => g.select('.domain').remove())
      .selectAll('text').attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem');
  }
</script>

<div class="chart-card" bind:this={chartEl}></div>
