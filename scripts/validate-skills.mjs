#!/usr/bin/env node
// Validates every skill in ./skills so `npx skills add softaverse/skills`
// never silently drops one, and keeps the README catalog honest.
//
//   node scripts/validate-skills.mjs

import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const skillsDir = path.join(root, "skills");
const readmeFile = path.join(root, "README.md");

const errors = [];

/**
 * Reads a scalar field out of YAML frontmatter, supporting plain, quoted,
 * and block (`>` / `|`) values that continue onto indented lines.
 */
function readField(frontmatter, field) {
  const lines = frontmatter.split("\n");
  const startIndex = lines.findIndex((line) =>
    new RegExp(`^${field}:(\\s|$)`).test(line)
  );

  if (startIndex === -1) {
    return undefined;
  }

  const firstValue = lines[startIndex].slice(field.length + 1).trim();

  if (firstValue && !/^[>|][-+\d]*$/.test(firstValue)) {
    return firstValue.replace(/^["']|["']$/g, "");
  }

  const continuation = [];
  for (const line of lines.slice(startIndex + 1)) {
    if (line.trim() && !/^\s/.test(line)) {
      break;
    }
    continuation.push(line.trim());
  }

  return continuation.join(" ").trim() || undefined;
}

async function validateSkill(name) {
  const skillDir = path.join(skillsDir, name);
  let markdown;

  try {
    markdown = await fs.readFile(path.join(skillDir, "SKILL.md"), "utf8");
  } catch {
    errors.push(`${name}: missing SKILL.md`);
    return;
  }

  const frontmatter = markdown.match(/^---\n([\s\S]*?)\n---/)?.[1];

  if (!frontmatter) {
    errors.push(`${name}: SKILL.md has no frontmatter block`);
    return;
  }

  const declaredName = readField(frontmatter, "name");
  const description = readField(frontmatter, "description");

  if (!declaredName) {
    errors.push(`${name}: frontmatter is missing "name" — installers skip this skill`);
  } else if (declaredName !== name) {
    errors.push(`${name}: frontmatter name "${declaredName}" does not match its directory`);
  }

  if (!description) {
    errors.push(`${name}: frontmatter is missing "description"`);
  }

  // Every concrete references/ link in SKILL.md must resolve, or the routing is dead.
  // Glob-style mentions such as `references/*.md` describe the shape, not a file.
  for (const [, link] of markdown.matchAll(/`(references\/[^`*]+\.md)`/g)) {
    if (!(await fs.access(path.join(skillDir, link)).then(() => true, () => false))) {
      errors.push(`${name}: SKILL.md routes to "${link}", which does not exist`);
    }
  }
}

const entries = await fs.readdir(skillsDir, { withFileTypes: true });
const names = entries
  .filter((entry) => entry.isDirectory() && !entry.name.startsWith("."))
  .map((entry) => entry.name)
  .sort();

for (const name of names) {
  await validateSkill(name);
}

// The README table is the curated catalog — hand-written blurbs, but no gaps.
const readme = await fs.readFile(readmeFile, "utf8");
const listed = new Set(
  [...readme.matchAll(/\[`([^`]+)`\]\(skills\/[^)]+\/SKILL\.md\)/g)].map((m) => m[1])
);

for (const name of names) {
  if (!listed.has(name)) {
    errors.push(`${name}: not listed in the README skills table`);
  }
}

for (const name of listed) {
  if (!names.includes(name)) {
    errors.push(`${name}: listed in the README but has no skills/${name}/ directory`);
  }
}

if (errors.length) {
  console.error(`Found ${errors.length} problem(s):`);
  console.error(errors.map((e) => `  - ${e}`).join("\n"));
  process.exit(1);
}

console.log(`All ${names.length} skills are valid and listed in the README.`);
