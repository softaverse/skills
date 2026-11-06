#!/usr/bin/env bash
# disk-audit.sh — read-only disk usage audit for macOS. Deletes nothing.
# Usage: disk-audit.sh [project-dir ...]
#   Defaults to whichever of ~/Workspace ~/Projects ~/code ~/dev ~/src exist.
#
# Speed: the home directory is walked exactly once (`du -akx`), keeping every
# file or directory >= MIN_KB in a temp file; every section below is a filter
# over that file. Slow tool commands (docker, brew, …) run in parallel.

MIN_KB=${MIN_KB:-51200}   # 50 MB: smaller entries are never reported

if [ $# -gt 0 ]; then
  PROJECT_DIRS=()
  for d in "$@"; do PROJECT_DIRS+=("$(cd "$d" 2>/dev/null && pwd -P || echo "$d")"); done
else
  PROJECT_DIRS=()
  for d in "$HOME/Workspace" "$HOME/Projects" "$HOME/code" "$HOME/dev" "$HOME/src"; do
    [ -d "$d" ] && PROJECT_DIRS+=("$d")
  done
fi

TMP=$(mktemp -d -t disk-audit)
trap 'rm -rf "$TMP"' EXIT
DB="$TMP/du.tsv"

# --- background jobs -------------------------------------------------------
{ du -akx "$HOME" 2>/dev/null | awk -F'\t' -v min="$MIN_KB" '$1 >= min' > "$DB"; } &

# Project dirs outside $HOME are not covered by the home walk.
for d in "${PROJECT_DIRS[@]}"; do
  case "$d/" in "$HOME"/*) ;; *)
    { du -akx "$d" 2>/dev/null | awk -F'\t' -v min="$MIN_KB" '$1 >= min' > "$TMP/extra.$RANDOM.tsv"; } & ;;
  esac
done

{
  command -v docker >/dev/null && { echo "# docker"; docker system df 2>/dev/null || echo "(docker not running)"; }
  command -v ollama >/dev/null && { echo "# ollama"; ollama list 2>/dev/null; }
  command -v brew   >/dev/null && { echo "# brew cleanup -n"; brew cleanup -n 2>/dev/null | tail -1; }
  command -v xcrun  >/dev/null && { echo "# unavailable simulators"; xcrun simctl list devices unavailable 2>/dev/null | grep -c "unavailable"; }
  echo "# Time Machine local snapshots"; tmutil listlocalsnapshots / 2>/dev/null
} > "$TMP/tools.txt" 2>&1 &

hr() { printf '\n== %s ==\n' "$1"; }

hr "Disk"
df -h /System/Volumes/Data 2>/dev/null || df -h /

wait   # du walk(s) and tools
cat "$TMP"/extra.*.tsv >> "$DB" 2>/dev/null

# Format "kb<TAB>path" lines, already sorted, as human-readable sizes.
human() {
  awk -F'\t' '{ k=$1; split("K M G T", u, " "); i=1
    while (k >= 1024 && i < 4) { k /= 1024; i++ }
    fmt = (k < 10 && i > 1) ? "%4.1f%s\t%s\n" : "%4d%s\t%s\n"; printf fmt, k, u[i], $2 }'
}

# Direct children of a directory, raw "kb<TAB>path": kids DIR
kids() { awk -F'\t' -v p="$1/" 'index($2, p) == 1 && index(substr($2, length(p) + 1), "/") == 0' "$DB"; }
# Top N children, human-readable: children DIR [N]
children() { kids "$1" | sort -t$'\t' -k1,1rn | head -"${2:-10}" | human; }

hr "Home directory (top 30)";       children "$HOME" 30
hr "~/Library";                     children "$HOME/Library"
hr "~/Library/Application Support"; children "$HOME/Library/Application Support" 15
hr "~/Library/Containers";          children "$HOME/Library/Containers"
hr "~/Library/Group Containers";    children "$HOME/Library/Group Containers" 5
hr "~/Library/Caches";              children "$HOME/Library/Caches"
hr "~/.cache";                      children "$HOME/.cache"

hr "Known caches and tool stores (>= 50 MB)"
for p in .npm .yarn/cache Library/Caches/Yarn .pnpm-store Library/pnpm .bun/install/cache \
  .gradle .m2 .cocoapods .pub-cache .rustup .cargo .pyenv .nvm .conda miniconda3 anaconda3 \
  .android/avd Library/Android/sdk/system-images Library/Android/sdk/ndk .ollama \
  Library/Containers/com.docker.docker .docker \
  Library/Developer/Xcode/DerivedData Library/Developer/Xcode/Archives \
  "Library/Developer/Xcode/iOS DeviceSupport" Library/Developer/CoreSimulator \
  "Library/Application Support/MobileSync/Backup" \
  "Library/Application Support/Code/Cache" "Library/Application Support/Code/CachedData" \
  Library/Logs .Trash Downloads Movies; do
  echo "$HOME/$p"
done | awk -F'\t' 'NR == FNR { want[$0] = 1; next } ($2 in want)' - "$DB" \
  | sort -t$'\t' -k1,1rn | human | sed "s|$HOME/||"

if [ ${#PROJECT_DIRS[@]} -gt 0 ]; then
  hr "Project dirs: ${PROJECT_DIRS[*]}"
  for d in "${PROJECT_DIRS[@]}"; do kids "$d"; done | sort -t$'\t' -k1,1rn | head -15 | human

  # Entries under the project dirs only.
  printf '%s\n' "${PROJECT_DIRS[@]}" \
    | awk -F'\t' 'NR == FNR { roots[$0 "/"] = 1; next }
                  { for (r in roots) if (index($2, r) == 1) { print; next } }' - "$DB" > "$TMP/proj.tsv"

  hr "node_modules (top 20, outermost only)"
  awk -F'\t' '$2 ~ /\/node_modules$/ && $2 !~ /\/node_modules\/.*\/node_modules$/ && $2 !~ /\/(\.cxx|build)\//' "$TMP/proj.tsv" \
    | sort -t$'\t' -k1,1rn | head -20 | human

  hr "Build artifacts and virtualenvs (top 25)"
  awk -F'\t' '
    BEGIN { split(".next build dist target .dart_tool Pods .venv venv .gradle .turbo .parcel-cache .cxx", a, " ")
            for (i in a) art[a[i]] = 1 }
    { n = split($2, c, "/"); if (!(c[n] in art)) next
      if (c[n] == "dist" && $2 ~ /\/node_modules\//) next   # published package contents, not build output
      for (i = 1; i < n; i++) if (c[i] in art) next   # outermost match only, like find -prune
      print }' "$TMP/proj.tsv" \
    | sort -t$'\t' -k1,1rn | head -25 | human
fi

hr "Files over 1 GB"
awk -F'\t' '$1 >= 1048576' "$DB" | sort -t$'\t' -k1,1rn \
  | while IFS=$'\t' read -r kb path; do [ -f "$path" ] && printf '%s\t%s\n' "$kb" "$path"; done \
  | head -30 | human

hr "Android SDK system images"
ls -d "$HOME"/Library/Android/sdk/system-images/*/* 2>/dev/null

hr "Tools"
cat "$TMP/tools.txt"

hr "Access check"
ls "$HOME/.Trash" >/dev/null 2>&1 || echo "Cannot read ~/.Trash — grant the terminal Full Disk Access for complete results."
