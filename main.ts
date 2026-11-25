// Entry for "Post the Meme, Win the Feed" (program/v1, Node 22, standard library only).
// The scored entry is the X post named by POST.json; this program only copies that
// file into /output so the gate can read the post's address. Deterministic: no
// network, no clock, no randomness, no files outside the repository. The copy is
// byte-for-byte, so the two grader runs write identical bytes.
//
// Improvement over the first draft: validate that POST.json is a JSON object with
// a non-empty string "url" before copying (the gate's binding is a post address),
// and report one clear line of confirmation with the byte count.
//
// Local run:
//   mkdir -p out && MAKEFUN_BOT_DIR=. MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const BOT_DIR = process.env.MAKEFUN_BOT_DIR ?? '/bot';
const OUTPUT_DIR = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const SOURCE = join(BOT_DIR, 'POST.json');
const DEST = join(OUTPUT_DIR, 'POST.json');

function fail(message: string): never {
  console.error(`main.ts: ${message}`);
  process.exit(1);
}

let bytes: Buffer;
try {
  bytes = readFileSync(SOURCE);
} catch (err) {
  fail(`cannot read ${SOURCE}: ${(err as Error).message}`);
}

let parsed: unknown;
try {
  parsed = JSON.parse(bytes.toString('utf8'));
} catch (err) {
  fail(`POST.json is not valid JSON: ${(err as Error).message}`);
}
if (
  typeof parsed !== 'object' ||
  parsed === null ||
  Array.isArray(parsed) ||
  typeof (parsed as { url?: unknown }).url !== 'string' ||
  (parsed as { url: string }).url.trim() === ''
) {
  fail('POST.json must be a JSON object with a non-empty string "url"');
}

mkdirSync(OUTPUT_DIR, { recursive: true });
try {
  writeFileSync(DEST, bytes);
} catch (err) {
  fail(`cannot write ${DEST}: ${(err as Error).message}`);
}
console.log(`Copied POST.json to ${DEST} (${bytes.length} bytes).`);
