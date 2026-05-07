/**
 * @typedef {Object} ScrollStepMeta
 * @property {number} scene
 * @property {number} step
 * @property {() => void} [onActive]
 */

/** @type {IntersectionObserver | null} */
let observer = null;
/** @type {WeakMap<Element, ScrollStepMeta>} */
const stepMeta = new WeakMap();
/** @type {Set<(meta: ScrollStepMeta) => void>} */
const listeners = new Set();

function ensureObserver() {
  if (observer || typeof IntersectionObserver === 'undefined') return observer;

  observer = new IntersectionObserver(handleEntries, {
    root: null,
    rootMargin: '-50% 0px -50% 0px',
    threshold: 0,
  });

  return observer;
}

/** @param {IntersectionObserverEntry[]} entries */
function handleEntries(entries) {
  const visible = entries
    .filter((entry) => entry.isIntersecting)
    .map((entry) => ({ entry, meta: stepMeta.get(entry.target) }))
    .filter((item) => item.meta);

  if (visible.length === 0) return;

  visible.sort((a, b) => {
    const center = window.innerHeight / 2;
    const aDistance = Math.abs(a.entry.boundingClientRect.top + a.entry.boundingClientRect.height / 2 - center);
    const bDistance = Math.abs(b.entry.boundingClientRect.top + b.entry.boundingClientRect.height / 2 - center);
    return aDistance - bDistance;
  });

  const active = visible[0].meta;
  if (!active) return;
  active.onActive?.();
  listeners.forEach((listener) => listener(active));
}

/**
 * Register a DOM node as a scrollytelling step.
 *
 * @param {Element} node
 * @param {ScrollStepMeta} meta
 * @returns {() => void}
 */
export function observeScrollStep(node, meta) {
  const io = ensureObserver();
  stepMeta.set(node, meta);

  if (!io) {
    meta.onActive?.();
    return () => stepMeta.delete(node);
  }

  io.observe(node);
  return () => {
    io.unobserve(node);
    stepMeta.delete(node);
  };
}

/**
 * Subscribe to active scrollytelling step changes.
 *
 * @param {(meta: ScrollStepMeta) => void} listener
 * @returns {() => void}
 */
export function onScrollStep(listener) {
  listeners.add(listener);
  return () => listeners.delete(listener);
}

export function destroyScrollDriver() {
  observer?.disconnect();
  observer = null;
  listeners.clear();
}
