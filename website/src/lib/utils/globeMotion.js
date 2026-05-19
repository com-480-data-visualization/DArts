/**
 * @typedef {[number, number]} GlobeRotation
 * @typedef {{decade: number | null, iso3: string, n: number}} CountryDecadeRow
 */

export const TOP_THREE_ROTATION = [38, -32];
export const TOP_THREE_ISO3 = new Set(['USA', 'FRA', 'DEU']);
export const IDLE_DEGREES_PER_MS = 0.0022;
export const IDLE_RESUME_DELAY = 1400;
export const TOP_THREE_HOLD_DELAY = 1700;

/**
 * @param {CountryDecadeRow[]} rows
 * @param {[number, number]} decadeRange
 * @returns {Record<string, number>}
 */
export function buildIsoCounts(rows, decadeRange) {
  const counts = {};
  for (const row of rows) {
    if (row.decade === null || row.decade < decadeRange[0] || row.decade > decadeRange[1]) continue;
    counts[row.iso3] = (counts[row.iso3] || 0) + row.n;
  }
  return counts;
}

/**
 * @param {string | undefined} iso3
 * @param {number} count
 * @param {number} maxCount
 * @param {number} step
 * @returns {string}
 */
export function globeFillFor(iso3, count, maxCount, step) {
  if (!iso3 || count === 0) return 'var(--seq-0)';
  if (step >= 2 && TOP_THREE_ISO3.has(iso3)) return 'var(--accent-primary)';
  if (step === 0) return 'var(--seq-0)';
  const bucket = Math.min(4, Math.max(0, Math.floor((Math.log10(count) / Math.log10(maxCount)) * 4)));
  return `var(--seq-${bucket})`;
}

/**
 * @param {number} t
 * @returns {number}
 */
export function easeInOutCubic(t) {
  return t < 0.5 ? 4 * t * t * t : 1 - Math.pow(-2 * t + 2, 3) / 2;
}

/**
 * @param {GlobeRotation} start
 * @param {GlobeRotation} target
 * @returns {GlobeRotation}
 */
export function closestRotationStart(start, target) {
  let lon = start[0];
  while (lon - target[0] > 180) lon -= 360;
  while (target[0] - lon > 180) lon += 360;
  return [lon, start[1]];
}
