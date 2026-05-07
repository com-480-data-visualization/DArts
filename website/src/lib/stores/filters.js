import { derived, get, writable } from 'svelte/store';

export const DECADE_MIN = 1860;
export const DECADE_MAX = 2020;
const HASH_DEBOUNCE_MS = 300;

/**
 * @typedef {Object} FilterState
 * @property {[number, number]} decadeRange
 * @property {string | null} selectedCountry
 * @property {Set<string>} selectedDepartments
 * @property {Set<string>} selectedRegions
 * @property {number} activeScene
 * @property {number} activeStep
 */

/** @type {FilterState} */
const DEFAULT_FILTERS = {
  decadeRange: [DECADE_MIN, DECADE_MAX],
  selectedCountry: null,
  selectedDepartments: new Set(),
  selectedRegions: new Set(),
  activeScene: 0,
  activeStep: 0,
};

/** @returns {FilterState} */
function createDefaultState() {
  return {
    decadeRange: [...DEFAULT_FILTERS.decadeRange],
    selectedCountry: DEFAULT_FILTERS.selectedCountry,
    selectedDepartments: new Set(DEFAULT_FILTERS.selectedDepartments),
    selectedRegions: new Set(DEFAULT_FILTERS.selectedRegions),
    activeScene: DEFAULT_FILTERS.activeScene,
    activeStep: DEFAULT_FILTERS.activeStep,
  };
}

/**
 * @param {FilterState} state
 * @returns {FilterState}
 */
function cloneState(state) {
  return {
    decadeRange: [...state.decadeRange],
    selectedCountry: state.selectedCountry,
    selectedDepartments: new Set(state.selectedDepartments),
    selectedRegions: new Set(state.selectedRegions),
    activeScene: state.activeScene,
    activeStep: state.activeStep,
  };
}

/**
 * @param {number} value
 * @param {number} min
 * @param {number} max
 */
function clamp(value, min, max) {
  return Math.min(max, Math.max(min, value));
}

/**
 * @param {string | null} value
 * @returns {Set<string>}
 */
function parseSetParam(value) {
  if (!value) return new Set();
  return new Set(
    value
      .split(',')
      .map((item) => decodeURIComponent(item.trim()))
      .filter(Boolean),
  );
}

/**
 * @param {Set<string>} values
 * @returns {string}
 */
function serializeSet(values) {
  return [...values].sort().map(encodeURIComponent).join(',');
}

/**
 * @param {string} hash
 * @returns {FilterState}
 */
export function parseHash(hash) {
  const state = createDefaultState();
  const params = new URLSearchParams(hash.replace(/^#/, ''));
  const decadeParam = params.get('d');

  if (decadeParam && /^\d{4}-\d{4}$/.test(decadeParam)) {
    const [rawMin, rawMax] = decadeParam.split('-').map(Number);
    const min = clamp(Math.round(rawMin / 10) * 10, DECADE_MIN, DECADE_MAX);
    const max = clamp(Math.round(rawMax / 10) * 10, DECADE_MIN, DECADE_MAX);
    state.decadeRange = min <= max ? [min, max] : [max, min];
  }

  const country = params.get('c');
  state.selectedCountry = country ? decodeURIComponent(country).toUpperCase() : null;
  state.selectedDepartments = parseSetParam(params.get('dep'));
  state.selectedRegions = parseSetParam(params.get('reg'));

  return state;
}

/**
 * @param {FilterState} state
 * @returns {string}
 */
export function serializeHash(state) {
  const params = new URLSearchParams();
  const [min, max] = state.decadeRange;

  if (min !== DECADE_MIN || max !== DECADE_MAX) {
    params.set('d', `${min}-${max}`);
  }
  if (state.selectedCountry) {
    params.set('c', state.selectedCountry);
  }
  if (state.selectedDepartments.size > 0) {
    params.set('dep', serializeSet(state.selectedDepartments));
  }
  if (state.selectedRegions.size > 0) {
    params.set('reg', serializeSet(state.selectedRegions));
  }

  const next = params.toString();
  return next ? `#${next}` : '';
}

export const filters = writable(createDefaultState());
export const decadeRange = derived(filters, ($filters) => $filters.decadeRange);
export const selection = derived(filters, ($filters) => ({
  selectedCountry: $filters.selectedCountry,
  selectedDepartments: new Set($filters.selectedDepartments),
  selectedRegions: new Set($filters.selectedRegions),
}));
export const activeScene = derived(filters, ($filters) => $filters.activeScene);
export const activeStep = derived(filters, ($filters) => $filters.activeStep);

let syncInitialized = false;
let applyingHash = false;
/** @type {number | null} */
let syncTimer = null;

/** @param {FilterState} state */
function writeHash(state) {
  if (typeof window === 'undefined') return;
  const nextHash = serializeHash(state);
  const currentHash = window.location.hash || '';
  if (nextHash === currentHash) return;
  history.replaceState(null, '', `${window.location.pathname}${window.location.search}${nextHash}`);
}

/** @param {FilterState} state */
function scheduleHashWrite(state) {
  if (typeof window === 'undefined' || applyingHash) return;
  if (syncTimer !== null) window.clearTimeout(syncTimer);
  syncTimer = window.setTimeout(() => {
    writeHash(state);
    syncTimer = null;
  }, HASH_DEBOUNCE_MS);
}

export function hydrateFromHash() {
  if (typeof window === 'undefined') return;
  applyingHash = true;
  filters.set(parseHash(window.location.hash));
  applyingHash = false;
}

export function syncToHash() {
  writeHash(get(filters));
}

/**
 * Starts bidirectional synchronization between the global filter store and
 * URL hash. Safe to call more than once during hot reload.
 *
 * @returns {() => void}
 */
export function initFilterHashSync() {
  if (typeof window === 'undefined' || syncInitialized) return () => {};
  syncInitialized = true;
  hydrateFromHash();
  const unsubscribe = filters.subscribe((state) => scheduleHashWrite(state));
  const onHashChange = () => hydrateFromHash();
  window.addEventListener('hashchange', onHashChange);

  return () => {
    unsubscribe();
    window.removeEventListener('hashchange', onHashChange);
    syncInitialized = false;
    if (syncTimer !== null) {
      window.clearTimeout(syncTimer);
      syncTimer = null;
    }
  };
}

/** @param {[number, number]} range */
export function setDecadeRange(range) {
  filters.update((state) => {
    const min = clamp(Math.round(range[0] / 10) * 10, DECADE_MIN, DECADE_MAX - 10);
    const max = clamp(Math.round(range[1] / 10) * 10, min + 10, DECADE_MAX);
    return { ...cloneState(state), decadeRange: [min, max] };
  });
}

/** @param {string | null} iso3 */
export function setSelectedCountry(iso3) {
  filters.update((state) => ({
    ...cloneState(state),
    selectedCountry: iso3 ? iso3.toUpperCase() : null,
  }));
}

export function clearSelectedCountry() {
  setSelectedCountry(null);
}

/** @param {string} department */
export function toggleDepartment(department) {
  filters.update((state) => {
    const next = cloneState(state);
    if (next.selectedDepartments.has(department)) {
      next.selectedDepartments.delete(department);
    } else {
      next.selectedDepartments.add(department);
    }
    return next;
  });
}

/** @param {string} region */
export function toggleRegion(region) {
  filters.update((state) => {
    const next = cloneState(state);
    if (next.selectedRegions.has(region)) {
      next.selectedRegions.delete(region);
    } else {
      next.selectedRegions.add(region);
    }
    return next;
  });
}

export function resetFilters() {
  filters.set(createDefaultState());
}

/**
 * @param {number} scene
 * @param {number} step
 */
export function setActiveSceneStep(scene, step) {
  filters.update((state) => ({
    ...cloneState(state),
    activeScene: scene,
    activeStep: step,
  }));
}
