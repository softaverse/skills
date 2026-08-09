# Adding Reusable Scripts to Skills

When a Skill performs deterministic, repetitive tasks, package those tasks as modular shell scripts in a `scripts/` directory. This follows Claude's [Agent Skills architecture](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview): scripts run without consuming context tokens, can be reused across conversations, and produce structured output for Claude to process.

## When to Add Scripts

Add scripts when your Skill involves:

- **File scanning or enumeration** (e.g., find all images, list files matching a pattern)
- **Deterministic transformations** (e.g., convert format, resize, compress)
- **Searching and replacing** (e.g., update references, batch edits)
- **Data aggregation** (e.g., calculate statistics, format results)
- **Cross-platform operations** that need consistent behavior (macOS + Linux)

**Do NOT script:**
- Tasks requiring user decisions or real-time interaction
- Multi-step reasoning or branching logic
- Anything that should be visible to the user as Claude's thought process

## Script Design Principles

### 1. One Responsibility Per Script

Each script should do one thing well:

```bash
# ✓ Good: scan-images.sh finds images
# ✓ Good: convert-images.sh converts them
# ✗ Bad:  process-images.sh does both
```

### 2. Parameterize, Don't Hardcode

Use command-line arguments instead of editing the script:

```bash
# ✓ Good: script accepts arguments
./scripts/convert-images.sh 80 file1.png file2.png

# ✗ Bad: script has hardcoded quality
QUALITY=80; cwebp -q $QUALITY ...
```

### 3. Structured Output for Downstream Processing

Output data Claude can easily parse (tab-separated, one result per line):

```bash
# ✓ Good: structured data
echo "image.png	1024000	512000	50%"

# ✗ Bad: prose that Claude must interpret
echo "Image image.png was compressed from 1MB to 512KB, saving 50%"
```

### 4. Error Handling and Logging

- Use `set -e` to exit on first error
- Validate required inputs and file existence
- Send logs to stderr (`>&2`), data to stdout
- Return non-zero exit codes on failure

```bash
set -e

if [ ! -d "$SRC_DIR" ]; then
  echo "Error: Directory not found: $SRC_DIR" >&2
  exit 1
fi

# Process...
echo "message" >&2  # Log to stderr
echo "result_data"  # Output to stdout
```

### 5. Cross-Platform Compatibility

Test on macOS and Linux. Use platform detection for differences:

```bash
# Detect platform
if [[ "$OSTYPE" == "darwin"* ]]; then
  # macOS (BSD sed)
  sed -i '' 's/old/new/g' file
else
  # Linux (GNU sed)
  sed -i 's/old/new/g' file
fi
```

Common differences:
- `sed -i ''` (macOS) vs `sed -i` (Linux)
- `stat -f%z` (macOS) vs `stat -c%s` (Linux)
- `brew install` (macOS) vs `apt-get` (Linux)

### 6. Make Scripts Executable

```bash
chmod +x ./scripts/*.sh
```

## File Organization

```
my-skill/
├── SKILL.md
├── references/
│   ├── README.md
│   ├── scripts.md          # ← Documents the scripts directory
│   └── other-topics.md
└── scripts/                # ← Level 3 resources (no context cost)
    ├── scan-items.sh
    ├── process-items.sh
    ├── find-references.sh
    └── update-references.sh
```

## How Claude Uses Scripts

1. **Invokes script via bash**: `bash ./scripts/scan-images.sh ./public/images`
2. **Script runs deterministically**: Produces output without asking for help
3. **Claude reads only the output**: Script code never enters context window
4. **Claude processes output**: Formats results for user or passes to next script

**Example flow**:

```
User: "Optimize my images"
  ↓
Claude: "I'll scan for images first"
  ↓
bash ./scripts/scan-images.sh ./public
  ↓ (only output enters context)
image.png    1024000
photo.jpg    2048000
  ↓
Claude: "Found 2 images. Should I convert to WebP?"
  ↓
bash ./scripts/convert-images.sh 80 image.png photo.jpg
  ↓ (only output enters context)
image.png    1024000    512000    50%
photo.jpg    2048000    900000    56%
  ↓
Claude: "Saved 50% and 56% respectively. Done!"
```

## Documenting Scripts

Create a `references/scripts.md` file that documents:

1. **Purpose** — What each script does
2. **Usage** — Command examples with parameters
3. **Output format** — What Claude will receive
4. **Environment variables** — Optional settings like `FORCE=true`
5. **Prerequisites** — Required tools (e.g., `cwebp` must be installed)
6. **Testing** — How to verify scripts work locally

Example template:

````markdown
# Reusable Scripts

## script-name.sh

Convert images to WebP format.

**Usage**:
```bash
./scripts/convert-images.sh <quality> <image1> [image2 ...]
```

**Parameters**:
- `$1` — Quality (1-100, default: 80)
- `$2...$n` — Image paths

**Output**: Tab-separated results
```
image.png	1024000	512000	50%
```

**Environment**:
- `FORCE=true` — Overwrite existing files

**Prerequisites**:
- `cwebp` must be installed
````

## Benefits for Reusability

- **No context penalty** — Script code costs 0 tokens when executed
- **Write once, use forever** — Same script across all conversations
- **Deterministic behavior** — Identical results every time
- **Modular composition** — Chain scripts together in workflows
- **Easy to test** — Run locally before deploying to Skill

## Anti-Patterns to Avoid

| Anti-Pattern | Problem | Solution |
|---|---|---|
| Inline all logic in SKILL.md | Bloats instructions, hard to update | Move to scripts/ |
| Hardcoded paths | Breaks across projects | Use parameters/variables |
| No error handling | Silent failures | Use `set -e`, validate inputs |
| Single mega-script | Hard to reuse parts | One responsibility per script |
| Platform-specific code | Only works on one OS | Test macOS + Linux |
| Prose-style output | Claude must interpret | Use structured data |
