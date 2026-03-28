<script>
  import * as d3 from 'd3';

  let { data, byDecade, selectedDecade } = $props();

  let donutEl;
  let areaEl;

  const genderColor = { male: 'var(--color-male)', female: 'var(--color-female)', '': 'var(--color-other)' };
  const genderColorHex = { male: '#4a7fb5', female: '#c1440e', '': '#6a9e5f' };

  function inRange(decade) {
    if (!selectedDecade) return true;
    return decade >= selectedDecade.min && decade <= selectedDecade.max;
  }

  let filteredGender = $derived.by(() => {
    if (!selectedDecade) return data;
    const filtered = byDecade.filter(d => inRange(d.decade));
    if (!filtered.length) return data;
    // Aggregate by gender
    const map = {};
    filtered.forEach(d => { map[d.gender] = (map[d.gender] || 0) + d.count; });
    return Object.entries(map).map(([gender, count]) => ({ gender, count }));
  });

  $effect(() => { if (donutEl && filteredGender.length) drawDonut(filteredGender); });
  $effect(() => { if (areaEl && byDecade.length) drawArea(byDecade); });

  function drawDonut(gdata) {
    const el = d3.select(donutEl);
    el.selectAll('*').remove();

    const size = 280, radius = size / 2 - 10;
    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${size} ${size}`)
      .append('g').attr('transform', `translate(${size/2},${size/2})`);

    const total = d3.sum(gdata, d => d.count);
    const pie = d3.pie().value(d => d.count).sort(null).padAngle(0.03);
    const arc = d3.arc().innerRadius(radius * 0.58).outerRadius(radius).cornerRadius(4);

    svg.selectAll('path')
      .data(pie(gdata))
      .join('path')
      .attr('d', arc)
      .attr('fill', d => genderColorHex[d.data.gender] || '#999')
      .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))')
      .append('title')
      .text(d => `${d.data.gender || 'other'}: ${d.data.count.toLocaleString()} (${(d.data.count/total*100).toFixed(1)}%)`);

    svg.append('text')
      .attr('text-anchor', 'middle').attr('dy', '-0.1em')
      .attr('fill', 'var(--color-text)').attr('font-size', '1.6rem')
      .attr('font-weight', '700').attr('font-family', 'var(--font-heading)')
      .text(total.toLocaleString());

    svg.append('text')
      .attr('text-anchor', 'middle').attr('dy', '1.4em')
      .attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem')
      .text(selectedDecade ? `${selectedDecade.min}s–${selectedDecade.max}s` : 'all periods');

    // Legend below
    const legendDiv = el.append('div').style('display', 'flex').style('gap', '1.2rem')
      .style('justify-content', 'center').style('margin-top', '1rem');

    gdata.forEach(d => {
      const item = legendDiv.append('div').style('display', 'flex').style('align-items', 'center').style('gap', '0.35rem');
      item.append('div').style('width', '10px').style('height', '10px').style('border-radius', '50%')
        .style('background', genderColorHex[d.gender] || '#999');
      item.append('span').style('font-size', '0.8rem').style('color', 'var(--color-text-muted)')
        .text(`${d.gender || 'other'} ${(d.count/total*100).toFixed(1)}%`);
    });
  }

  function drawArea(bdata) {
    const el = d3.select(areaEl);
    el.selectAll('*').remove();

    const margin = { top: 20, right: 20, bottom: 35, left: 45 };
    const width = 600, height = 260;

    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${width + margin.left + margin.right} ${height + margin.top + margin.bottom}`)
      .append('g').attr('transform', `translate(${margin.left},${margin.top})`);

    const genders = [...new Set(bdata.map(d => d.gender))];
    const decades = [...new Set(bdata.map(d => d.decade))].sort((a,b) => a-b);
    const pivoted = decades.map(dec => {
      const row = { decade: dec };
      genders.forEach(g => {
        const m = bdata.find(d => d.decade === dec && d.gender === g);
        row[g] = m ? m.count : 0;
      });
      return row;
    });

    const stack = d3.stack().keys(genders);
    const series = stack(pivoted);
    const x = d3.scaleLinear().domain(d3.extent(decades)).range([0, width]);
    const y = d3.scaleLinear().domain([0, d3.max(series, s => d3.max(s, d => d[1]))]).range([height, 0]);

    const area = d3.area()
      .x(d => x(d.data.decade))
      .y0(d => y(d[0])).y1(d => y(d[1]))
      .curve(d3.curveMonotoneX);

    // Gradient fills
    const defs = svg.append('defs');
    genders.forEach((g, i) => {
      const grad = defs.append('linearGradient').attr('id', `grad-${i}`).attr('x1', 0).attr('y1', 0).attr('x2', 0).attr('y2', 1);
      grad.append('stop').attr('offset', '0%').attr('stop-color', genderColorHex[g] || '#999').attr('stop-opacity', 0.8);
      grad.append('stop').attr('offset', '100%').attr('stop-color', genderColorHex[g] || '#999').attr('stop-opacity', 0.4);
    });

    svg.selectAll('.area')
      .data(series)
      .join('path')
      .attr('d', area)
      .attr('fill', (d, i) => `url(#grad-${i})`);

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

    svg.append('g')
      .call(d3.axisLeft(y).ticks(5).tickFormat(d3.format('.2s')))
      .call(g => g.select('.domain').remove())
      .call(g => g.selectAll('.tick line').attr('stroke', 'var(--color-border)').attr('stroke-dasharray', '2,2').attr('x2', width))
      .selectAll('text').attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem');
  }
</script>

<div class="chart-card gender-layout">
  <div class="donut-side" bind:this={donutEl}></div>
  <div class="area-side" bind:this={areaEl}></div>
</div>

<style>
  .gender-layout {
    display: flex;
    gap: 2.5rem;
    align-items: center;
    flex-wrap: wrap;
  }
  .donut-side { flex: 0 0 280px; }
  .area-side { flex: 1; min-width: 300px; }
</style>
