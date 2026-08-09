# Quick Script Template

Use this template when adding scripts to a Skill.

## Skeleton: One-Job Script

```bash
#!/bin/bash
# script-name.sh - Brief description

set -e

# 1. Parse arguments
PARAM1="${1:?Error: Missing parameter}"
PARAM2="$2"

# 2. Validate inputs
if [ ! -d "$PARAM1" ]; then
  echo "Error: Directory not found: $PARAM1" >&2
  exit 1
fi

# 3. Main logic
while IFS= read -r item; do
  # Process each item
  echo "Processing: $item" >&2
done < <(find "$PARAM1" -type f)

# 4. Output results to stdout (structured)
echo "result_line_1"
echo "result_line_2"
```

## Documentation Template

```markdown
### script-name.sh

One-sentence description.

**Usage**:
\`\`\`bash
./scripts/script-name.sh <param1> [param2]
\`\`\`

**Parameters**:
- `$1` — Description and constraints
- `$2` — Optional, description

**Output**: Format of results
\`\`\`
output_line_1
output_line_2
\`\`\`

**Prerequisites**:
- Required tool: X must be installed (`brew install X`)

**Example**:
\`\`\`bash
./scripts/script-name.sh ./path/to/file
\`\`\`
```

## Checklist Before Deploying

- [ ] Script has `set -e` (fail on error)
- [ ] Arguments are validated (check files exist, directories accessible)
- [ ] Logs go to stderr (`>&2`), data to stdout
- [ ] Output is structured (tab-separated or one-per-line)
- [ ] No hardcoded paths or values
- [ ] Scripts are executable (`chmod +x`)
- [ ] Tested on macOS AND Linux
- [ ] Documented in `references/scripts.md`
- [ ] Platform differences handled (sed -i, stat, etc.)
- [ ] Script referenced from SKILL.md routing or workflow

## One-Liner Tests

```bash
# Make scripts executable
chmod +x ./scripts/*.sh

# Test argument validation
./scripts/script-name.sh

# Test with valid input
./scripts/script-name.sh ./valid/path

# Test error handling
./scripts/script-name.sh ./invalid/path 2>&1
```
