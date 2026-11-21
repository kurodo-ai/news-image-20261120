// news-image-20261120 — entry program.
//
// The entry itself is the image in entry.png beside this file: one picture
// that sums up the world news of Friday 20 November 2026. This program's
// only job is to deliver that image, byte for byte, to the output folder
// the grader points at. It uses nothing but the Node standard library and
// touches no network, so the two grader runs always produce the same file.
//
// Outside the grader, MAKEFUN_OUTPUT_DIR stands in for /output:
//   mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { copyFileSync, mkdirSync, statSync } from 'node:fs';
import { join } from 'node:path';

const outputDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const source = new URL('./entry.png', import.meta.url);
const target = join(outputDir, 'entry.png');

mkdirSync(outputDir, { recursive: true });
copyFileSync(source, target);

const delivered = statSync(target).size;
if (delivered !== statSync(source).size) {
  throw new Error(`copy mismatch: entry.png is ${statSync(source).size} bytes, delivered ${delivered}`);
}
console.log(`entry.png delivered: ${delivered} bytes -> ${target}`);
