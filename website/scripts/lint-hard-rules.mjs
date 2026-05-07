import { readdirSync, readFileSync, statSync } from 'node:fs';
import { extname, join, relative } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = fileURLToPath(new URL('..', import.meta.url));
const src = join(root, 'src');
const forbidden = [
  [/Mercator/gi, 'Mercator projection'],
  [/\bpie\b/gi, 'pie chart'],
  [/\bdonut\b/gi, 'donut chart'],
  [/interpolateRainbow|schemeRainbow|\brainbow\b|\bjet\b/gi, 'rainbow or jet palette'],
  [/https:\/\/fonts\.googleapis\.com/gi, 'runtime Google Fonts fetch'],
  [/console\./g, 'console call'],
];

function files(dir) {
  return readdirSync(dir).flatMap((name) => {
    const path = join(dir, name);
    const stat = statSync(path);
    if (stat.isDirectory()) return files(path);
    return path;
  });
}

const sourceFiles = files(src).filter((path) => ['.js', '.svelte', '.css'].includes(extname(path)));
const failures = [];

for (const path of sourceFiles) {
  const text = readFileSync(path, 'utf8');
  const rel = relative(root, path);
  for (const [pattern, label] of forbidden) {
    pattern.lastIndex = 0;
    if (pattern.test(text)) failures.push(`${rel}: forbidden ${label}`);
  }
  if (extname(path) === '.svelte') {
    const lines = text.split(/\r?\n/).length;
    if (lines > 250) failures.push(`${rel}: ${lines} lines, exceeds 250-line component budget`);
  }
}

if (failures.length) {
  console.error(failures.join('\n'));
  process.exit(1);
}

console.log('Hard-rule lint passed.');
