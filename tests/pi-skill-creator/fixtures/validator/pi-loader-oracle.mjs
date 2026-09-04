import { join } from "node:path";
import { pathToFileURL } from "node:url";

const [piCheckout, ...fixtureDirectories] = process.argv.slice(2);
if (!piCheckout || fixtureDirectories.length === 0) {
  throw new Error("usage: pi-loader-oracle.mjs <pi-checkout> <fixture-dir> [...]");
}

const loaderUrl = pathToFileURL(
  join(piCheckout, "packages/coding-agent/src/core/skills.ts"),
).href;
const { loadSkillsFromDir } = await import(loaderUrl);
const results = {};
for (const directory of fixtureDirectories) {
  const result = loadSkillsFromDir({ dir: directory, source: "contract-test" });
  const name = directory.split(/[\\/]/).at(-1);
  results[name] = {
    loadable: result.skills.length === 1,
    diagnostics: result.diagnostics.map(({ type, message }) => ({ type, message })),
  };
}
process.stdout.write(`${JSON.stringify(results)}\n`);
