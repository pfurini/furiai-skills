#!/usr/bin/env node
/**
 * Compact A4 PDF from one markdown file.
 *
 *   node md-to-pdf.mjs [--engine chrome|typst] <input.md> [output.pdf]
 *
 * Writes <same-dir>/<same-name>.pdf when the output path is omitted.
 * stdout is the output path only. Requires pandoc, plus Chromium/Chrome
 * (preferred) or typst.
 */

import { execFileSync } from 'node:child_process';
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { fileURLToPath, pathToFileURL } from 'node:url';

export class MdPdfError extends Error {}

const SKILL_DIR = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '..');
const PRINT_CSS_PATH = path.join(SKILL_DIR, 'assets', 'print.css');
const TYPST_PRELUDE_PATH = path.join(SKILL_DIR, 'assets', 'compact-prelude.typ');
const MARKDOWN_EXT = new Set(['.md', '.markdown']);
const ENGINES = new Set(['chrome', 'typst']);

const CHROME_CANDIDATES = [
  process.env.CHROME_PATH,
  '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
  '/Applications/Chromium.app/Contents/MacOS/Chromium',
  '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge',
  'chromium',
  'chromium-browser',
  'google-chrome',
  'google-chrome-stable',
  'msedge',
].filter(Boolean);

export const USAGE = `Usage: node md-to-pdf.mjs [--engine chrome|typst] <input.md> [output.pdf]

Converts one markdown file to a compact A4 PDF next to the source.
Requires pandoc, and either Chromium/Chrome or typst.
`;

export function fail(message) {
  throw new MdPdfError(message);
}

export function parseArgs(argv) {
  const args = [...argv];
  const opts = { engine: null, help: false, input: null, output: null };
  while (args.length > 0) {
    const arg = args.shift();
    if (arg === '--help' || arg === '-h') {
      opts.help = true;
    } else if (arg === '--engine') {
      const value = args.shift();
      if (!value || !ENGINES.has(value)) {
        fail('--engine must be chrome or typst');
      }
      opts.engine = value;
    } else if (arg === '--') {
      if (args[0]) opts.input = args.shift();
      if (args[0]) opts.output = args.shift();
      break;
    } else if (arg.startsWith('-')) {
      fail(`unknown option ${arg}`);
    } else if (!opts.input) {
      opts.input = arg;
    } else if (!opts.output) {
      opts.output = arg;
    } else {
      fail('too many arguments');
    }
  }
  return opts;
}

export function resolvePaths(input, output) {
  if (!input) fail('missing markdown file');
  const inputPath = path.resolve(input);
  if (!fs.existsSync(inputPath) || !fs.statSync(inputPath).isFile()) {
    fail(`markdown file not found: ${input}`);
  }
  const ext = path.extname(inputPath).toLowerCase();
  if (!MARKDOWN_EXT.has(ext)) fail('input must be a .md or .markdown file');
  const outputPath = output
    ? path.resolve(output)
    : path.join(path.dirname(inputPath), `${path.basename(inputPath, ext)}.pdf`);
  return { inputPath, outputPath, inputDir: path.dirname(inputPath) };
}

export function extractTitle(markdown, fallback) {
  const match = markdown.match(/^#\s+(.+?)\s*$/m);
  return match ? match[1].trim() : fallback;
}

export function cssString(value) {
  return value.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

export function escapeHtml(value) {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;');
}

export function wrapHtml(body, { title, css }) {
  const styled = css.replaceAll('__DOC_TITLE__', cssString(title));
  return [
    '<!doctype html>',
    '<html lang="en">',
    '<head>',
    '<meta charset="utf-8">',
    `<title>${escapeHtml(title)}</title>`,
    '<style>',
    styled,
    '</style>',
    '</head>',
    '<body>',
    body,
    '</body>',
    '</html>',
    '',
  ].join('\n');
}

export function which(command) {
  if (command.includes(path.sep) || command.includes('/')) {
    return fs.existsSync(command) ? command : null;
  }
  try {
    return execFileSync('which', [command], { encoding: 'utf8' }).trim();
  } catch {
    return null;
  }
}

export function findPandoc() {
  return which(process.env.PANDOC_PATH || 'pandoc');
}

export function findChrome() {
  for (const candidate of CHROME_CANDIDATES) {
    const resolved = which(candidate);
    if (resolved) return resolved;
  }
  return null;
}

export function findTypst() {
  return which(process.env.TYPST_PATH || 'typst');
}

export function selectEngine(requested) {
  if (requested === 'chrome') {
    const chrome = findChrome();
    if (!chrome) fail('chrome engine requested, but Chromium/Chrome was not found');
    return { engine: 'chrome', chrome };
  }
  if (requested === 'typst') {
    const typst = findTypst();
    if (!typst) fail('typst engine requested, but typst was not found');
    return { engine: 'typst', typst };
  }
  const chrome = findChrome();
  if (chrome) return { engine: 'chrome', chrome };
  const typst = findTypst();
  if (typst) return { engine: 'typst', typst };
  fail('no PDF engine found: install Chromium/Chrome, or typst');
}

function runPandoc(pandoc, args, cwd) {
  try {
    return execFileSync(pandoc, args, {
      encoding: 'utf8',
      cwd,
      maxBuffer: 32 * 1024 * 1024,
    });
  } catch (error) {
    const detail = error.stderr?.toString().trim() || error.message;
    fail(`pandoc failed: ${detail}`);
  }
}

function printWithChrome(chrome, htmlPath, outputPath) {
  const args = [
    '--headless=new',
    '--disable-gpu',
    '--no-first-run',
    '--no-default-browser-check',
    '--disable-extensions',
    '--no-pdf-header-footer',
    `--print-to-pdf=${outputPath}`,
    pathToFileURL(htmlPath).href,
  ];
  try {
    execFileSync(chrome, args, {
      encoding: 'utf8',
      stdio: ['ignore', 'pipe', 'pipe'],
      timeout: 60_000,
    });
  } catch (error) {
    if (fs.existsSync(outputPath) && fs.statSync(outputPath).size > 0) return;
    const detail = error.stderr?.toString().trim() || error.message;
    fail(`chrome print failed: ${detail}`);
  }
}

function compileTypst(typst, typPath, outputPath, root) {
  try {
    execFileSync(typst, ['compile', '--root', root, typPath, outputPath], {
      encoding: 'utf8',
      timeout: 60_000,
    });
  } catch (error) {
    const detail = error.stderr?.toString().trim() || error.message;
    fail(`typst failed: ${detail}`);
  }
}

function assertPdf(outputPath) {
  if (!fs.existsSync(outputPath)) fail(`PDF was not written: ${outputPath}`);
  const fd = fs.openSync(outputPath, 'r');
  const magic = Buffer.alloc(4);
  fs.readSync(fd, magic, 0, 4, 0);
  fs.closeSync(fd);
  if (magic.toString('utf8') !== '%PDF') fail(`output is not a PDF: ${outputPath}`);
}

export function convert(input, output, { engine: requestedEngine } = {}) {
  const pandoc = findPandoc();
  if (!pandoc) fail('pandoc is required (https://pandoc.org)');
  const { inputPath, outputPath, inputDir } = resolvePaths(input, output);
  const selected = selectEngine(requestedEngine);
  const markdown = fs.readFileSync(inputPath, 'utf8');
  const title = extractTitle(markdown, path.basename(inputPath, path.extname(inputPath)));
  const tmpDir = fs.mkdtempSync(path.join(os.tmpdir(), 'md-to-pdf-'));
  try {
    if (selected.engine === 'chrome') {
      const body = runPandoc(pandoc, [
        '-f', 'gfm+smart',
        '-t', 'html5',
        '--wrap=none',
        '--embed-resources',
        inputPath,
      ], inputDir);
      const css = fs.readFileSync(PRINT_CSS_PATH, 'utf8');
      const htmlPath = path.join(tmpDir, 'document.html');
      fs.writeFileSync(htmlPath, wrapHtml(body, { title, css }));
      printWithChrome(selected.chrome, htmlPath, outputPath);
    } else {
      const body = runPandoc(pandoc, [
        '-f', 'gfm+smart',
        '-t', 'typst',
        '--wrap=none',
        '--extract-media', tmpDir,
        inputPath,
      ], inputDir);
      const prelude = fs.readFileSync(TYPST_PRELUDE_PATH, 'utf8');
      const typPath = path.join(tmpDir, 'document.typ');
      fs.writeFileSync(typPath, `${prelude}\n${body}\n`);
      compileTypst(selected.typst, typPath, outputPath, tmpDir);
    }
    assertPdf(outputPath);
    return outputPath;
  } finally {
    fs.rmSync(tmpDir, { recursive: true, force: true });
  }
}

export function main(argv) {
  const opts = parseArgs(argv);
  if (opts.help) {
    process.stdout.write(USAGE);
    return 0;
  }
  const outputPath = convert(opts.input, opts.output, { engine: opts.engine });
  process.stdout.write(`${outputPath}\n`);
  return 0;
}

function isInvokedAsMain() {
  if (!process.argv[1]) return false;
  try {
    return import.meta.url === pathToFileURL(fs.realpathSync(process.argv[1])).href;
  } catch {
    return import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href;
  }
}

if (isInvokedAsMain()) {
  try {
    process.exitCode = main(process.argv.slice(2));
  } catch (error) {
    if (error instanceof MdPdfError) {
      process.stderr.write(`md-to-pdf: ${error.message}\n`);
      process.exitCode = 1;
    } else {
      throw error;
    }
  }
}
