// Behavioural tests for md-to-pdf.mjs.
// Run: node --test skills/md-to-pdf/scripts/md-to-pdf.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

import {
  USAGE,
  convert,
  cssString,
  escapeHtml,
  extractTitle,
  findPandoc,
  findTypst,
  parseArgs,
  resolvePaths,
  wrapHtml,
} from './md-to-pdf.mjs';

const SCRIPT = fileURLToPath(new URL('./md-to-pdf.mjs', import.meta.url));

function cli(args, options = {}) {
  return spawnSync(process.execPath, [SCRIPT, ...args], {
    encoding: 'utf8',
    ...options,
  });
}

test('parseArgs reads the input, optional output, and --engine', () => {
  assert.deepEqual(parseArgs(['notes.md']).input, 'notes.md');
  assert.equal(parseArgs(['notes.md', 'out.pdf']).output, 'out.pdf');
  assert.equal(parseArgs(['--engine', 'typst', 'notes.md']).engine, 'typst');
  assert.equal(parseArgs(['--help']).help, true);
});

test('parseArgs refuses a bad engine and extra positionals', () => {
  assert.throws(() => parseArgs(['--engine', 'prince', 'a.md']), /chrome or typst/);
  assert.throws(() => parseArgs(['a.md', 'b.pdf', 'c.pdf']), /too many arguments/);
});

test('resolvePaths writes a same-named PDF beside the markdown file', () => {
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'md-to-pdf-test-'));
  const input = path.join(dir, 'brief.md');
  fs.writeFileSync(input, '# Brief\n');
  const resolved = resolvePaths(input);
  assert.equal(resolved.outputPath, path.join(dir, 'brief.pdf'));
  fs.rmSync(dir, { recursive: true, force: true });
});

test('resolvePaths refuses a missing file and a non-markdown path', () => {
  assert.throws(() => resolvePaths('/tmp/does-not-exist-md-to-pdf.md'), /not found/);
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'md-to-pdf-test-'));
  const input = path.join(dir, 'notes.txt');
  fs.writeFileSync(input, 'nope');
  assert.throws(() => resolvePaths(input), /must be a \.md/);
  fs.rmSync(dir, { recursive: true, force: true });
});

test('extractTitle uses the first ATX h1 and otherwise the fallback', () => {
  assert.equal(extractTitle('# Architecture direction\n\nBody\n', 'x'), 'Architecture direction');
  assert.equal(extractTitle('No heading\n', 'file-name'), 'file-name');
});

test('wrapHtml inlines the title into the stylesheet and the document title', () => {
  const html = wrapHtml('<p>Hi</p>', {
    title: 'Architecture "direction"',
    css: '@top-center { content: "__DOC_TITLE__"; }',
  });
  assert.match(html, /content: "Architecture \\"direction\\""/);
  assert.match(html, /<title>Architecture &quot;direction&quot;<\/title>/);
  assert.match(html, /<p>Hi<\/p>/);
});

test('cssString and escapeHtml keep quotes and brackets literal', () => {
  assert.equal(cssString('Say "hi"'), 'Say \\"hi\\"');
  assert.equal(escapeHtml('<a>"&'), '&lt;a&gt;&quot;&amp;');
});

test('CLI --help prints usage and does not write a PDF', () => {
  const result = cli(['--help']);
  assert.equal(result.status, 0);
  assert.equal(result.stdout, USAGE);
});

test('CLI reports a missing file on stderr and writes nothing to stdout', () => {
  const result = cli([path.join(os.tmpdir(), 'missing-md-to-pdf.md')]);
  assert.equal(result.status, 1);
  assert.equal(result.stdout, '');
  assert.match(result.stderr, /^md-to-pdf: markdown file not found/);
});

test('typst engine writes a PDF next to a small markdown fixture', (t) => {
  if (!findPandoc() || !findTypst()) {
    t.skip('pandoc and typst are required for this conversion');
    return;
  }
  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'md-to-pdf-test-'));
  const input = path.join(dir, 'sample.md');
  fs.writeFileSync(input, [
    '# Sample',
    '',
    'A **compact** table:',
    '',
    '| a | b |',
    '| --- | --- |',
    '| 1 | 2 |',
    '',
    'And `code`.',
    '',
  ].join('\n'));
  const output = convert(input, undefined, { engine: 'typst' });
  assert.equal(output, path.join(dir, 'sample.pdf'));
  assert.equal(fs.readFileSync(output).subarray(0, 4).toString(), '%PDF');
  assert.ok(fs.statSync(output).size > 100);
  fs.rmSync(dir, { recursive: true, force: true });
});
