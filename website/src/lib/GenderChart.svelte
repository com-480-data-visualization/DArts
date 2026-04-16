<script>
  import * as d3 from 'd3';

  let { data, byDecade, selectedDecade } = $props();

  let donutEl;
  let areaEl;

  const genderColorHex = { male: '#4a7fb5', female: '#c1440e', other: '#6a9e5f', '': '#6a9e5f' };
  const genderOrder = ['male', 'female', 'other'];

  function getGenderLabel(gender) {
    const normalized = String(gender || '').trim().toLowerCase();
    if (normalized === 'male' || normalized === 'female') return normalized;
    return 'other';
  }

  function getGenderColor(gender) {
    return genderColorHex[getGenderLabel(gender)] || genderColorHex.other;
  }

  let filteredGender = $derived.by(() => {
    const range = selectedDecade;
    if (!range) return data;

    const filtered = byDecade.filter(d => d.decade >= range.min && d.decade <= range.max);
    if (!filtered.length) return data;

    const map = {};
    filtered.forEach(d => {
      const key = getGenderLabel(d.gender);
      map[key] = (map[key] || 0) + d.count;
    });

    return Object.entries(map)
      .map(([gender, count]) => ({ gender, count }))
      .sort((a, b) => {
        const orderDiff = genderOrder.indexOf(a.gender) - genderOrder.indexOf(b.gender);
        return orderDiff !== 0 ? orderDiff : b.count - a.count;
      });
  });

  let rangeKey = $derived(selectedDecade ? `${selectedDecade.min}-${selectedDecade.max}` : 'all');

  $effect(() => {
    const _ = rangeKey;
    if (!donutEl) return;
    if (!filteredGender.length) {
      d3.select(donutEl).selectAll('*').remove();
      return;
    }
    drawDonut(filteredGender);
  });

  $effect(() => {
    const _ = rangeKey;
    if (!areaEl) return;
    if (!byDecade.length) {
      d3.select(areaEl).selectAll('*').remove();
      return;
    }
    drawArea(byDecade);
  });

  function drawDonut(gdata) {
    const el = d3.select(donutEl);
    el.selectAll('*').remove();

    const size = 280, radius = size / 2 - 10;
    const svg = el.append('svg')
      .attr('viewBox', `0 0 ${size} ${size}`)
      .append('g').attr('transform', `translate(${size / 2},${size / 2})`);

    const total = d3.sum(gdata, d => d.count);
    const pie = d3.pie().value(d => d.count).sort(null).padAngle(0.03);
    const arc = d3.arc().innerRadius(radius * 0.58).outerRadius(radius).cornerRadius(4);

    svg.selectAll('path')
      .data(pie(gdata))
      .join('path')
      .attr('d', arc)
      .attr('fill', d => getGenderColor(d.data.gender))
      .style('filter', 'drop-shadow(0 2px 4px rgba(0,0,0,0.1))')
      .append('title')
      .text(d => `${getGenderLabel(d.data.gender)}: ${d.data.count.toLocaleString()} (${(d.data.count / total * 100).toFixed(1)}%)`);

    svg.append('text')
      .attr('text-anchor', 'middle').attr('dy', '-0.1em')
      .attr('fill', 'var(--color-text)').attr('font-size', '1.6rem')
      .attr('font-weight', '700').attr('font-family', 'var(--font-heading)')
      .text(total.toLocaleString());

    svg.append('text')
      .attr('text-anchor', 'middle').attr('dy', '1.4em')
      .attr('fill', 'var(--color-text-muted)').attr('font-size', '0.7rem')
      .text(selectedDecade ? `${selectedDecade.min}s-${selectedDecade.max}s` : 'all periods');

    const legendDiv = el.append('div').style('display', 'flex').style('gap', '1.2rem')
      .style('justify-content', 'center').style('margin-top', '1rem');

    gdata.forEach(d => {
      const item = legendDiv.append('div').style('display', 'flex').style('align-items', 'center').style('gap', '0.35rem');
      item.append('div').style('width', '10px').style('height', '10px').style('border-radius', '50%')
        .style('background', getGenderColor(d.gender));
      item.append('span').style('font-size', '0.8rem').style('color', 'var(--color-text-muted)')
        .text(`${getGenderLabel(d.gender)} ${(d.count / total * 100).toFixed(1)}%`);
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

    const genders = [...new Set(bdata.map(d => getGenderLabel(d.gender)))]
      .sort((a, b) => genderOrder.indexOf(a) - genderOrder.indexOf(b));
    const decades = [...new Set(bdata.map(d => d.decade))].sort((a, b) => a - b);
    const pivoted = decades.map(dec => {
      const row = { decade: dec };
      genders.forEach(g => {
        const m = bdata.find(d => d.decade === dec && getGenderLabel(d.gender) === g);
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

    const defs = svg.append('defs');
    genders.forEach((g, i) => {
      const grad = defs.append('linearGradient').attr('id', `grad-${i}`).attr('x1', 0).attr('y1', 0).attr('x2', 0).attr('y2', 1);
      grad.append('stop').attr('offset', '0%').attr('stop-color', getGenderColor(g)).attr('stop-opacity', 0.8);
      grad.append('stop').attr('offset', '100%').attr('stop-color', getGenderColor(g)).attr('stop-opacity', 0.4);
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
