/**
 * @typedef {Object} QuizAnswers
 * @property {[number, number]} decadeRange
 * @property {string} region
 * @property {string} medium
 */

function overlaps(artist, decadeRange) {
  const first = artist.decade_active_first ?? 1860;
  const last = artist.decade_active_last ?? 2020;
  return last >= decadeRange[0] && first <= decadeRange[1];
}

function ranked(candidates) {
  return [...candidates].sort((a, b) => a.n_works - b.n_works || a.name.localeCompare(b.name));
}

/**
 * Deterministically match a quiz result to an underrepresented artist.
 *
 * @param {Array<Object>} artists
 * @param {QuizAnswers} answers
 * @returns {{artist: Object | null, relaxed: string | null}}
 */
export function matchArtist(artists, answers) {
  const withWork = artists.filter((artist) => artist.n_works > 0 && artist.sample_work_title);
  const exact = ranked(withWork.filter((artist) => overlaps(artist, answers.decadeRange) && artist.region === answers.region && artist.medium_primary === answers.medium));
  if (exact.length) return { artist: exact[Math.min(2, exact.length - 1)], relaxed: null };

  const dropRegion = ranked(withWork.filter((artist) => overlaps(artist, answers.decadeRange) && artist.medium_primary === answers.medium));
  if (dropRegion.length) return { artist: dropRegion[Math.min(2, dropRegion.length - 1)], relaxed: 'region' };

  const dropMedium = ranked(withWork.filter((artist) => overlaps(artist, answers.decadeRange)));
  if (dropMedium.length) return { artist: dropMedium[Math.min(2, dropMedium.length - 1)], relaxed: 'medium' };

  const fallback = ranked(withWork);
  return { artist: fallback[Math.min(2, fallback.length - 1)] ?? null, relaxed: 'decade' };
}
