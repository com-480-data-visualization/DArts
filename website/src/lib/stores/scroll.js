import { derived } from 'svelte/store';
import { filters, setActiveSceneStep } from './filters.js';

export const scrollState = derived(filters, ($filters) => ({
  activeScene: $filters.activeScene,
  activeStep: $filters.activeStep,
}));

export { setActiveSceneStep };
