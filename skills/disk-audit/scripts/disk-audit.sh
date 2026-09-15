#!/usr/bin/env bash
# disk-audit.sh — read-only disk usage audit for macOS. Deletes nothing.
# Usage: disk-audit.sh [project-dir ...]
#   Defaults to whichever of ~/Workspace ~/Projects ~/code ~/dev ~/src exist.

if [ $# -gt 0 ]; then
  PROJECT_DIRS=("$@")
else
  PROJECT_DIRS=()
  for d in "$HOME/Workspace" "$HOME/Projects" "$HOME/code" "$HOME/dev" "$HOME/src"; do
    [ -d "$d" ] && PROJECT_DIRS+=("$d")
  done
fi

top() { du -sh "$@" 2>/dev/null | sort -rh | head -"${N:-10}"; }
hr()  { printf '\n== %s ==\n' "$1"; }

hr "Disk"
df -h /System/Volumes/Data 2>/dev/null || df -h /

hr "Home directory (top 30)"
N=30 top "$HOME"/* "$HOME"/.[!.]*

hr "~/Library";                  top "$HOME/Library"/*
hr "~/Library/Application Support"; N=15 top "$HOME/Library/Application Support"/*
hr "~/Library/Containers";       top "$HOME/Library/Containers"/*
hr "~/Library/Group Containers"; N=5 top "$HOME/Library/Group Containers"/*
hr "~/Library/Caches";           top "$HOME/Library/Caches"/*
hr "~/.cache";                   top "$HOME/.cache"/*

hr "Known caches and tool stores"
cd "$HOME" || exit 1
for p in .npm .yarn/cache Library/Caches/Yarn .pnpm-store Library/pnpm .bun/install/cache \
  .gradle .m2 .cocoapods .pub-cache .rustup .cargo .pyenv .nvm .conda miniconda3 anaconda3 \
  .android/avd Library/Android/sdk/system-images Library/Android/sdk/ndk .ollama \
  Library/Containers/com.docker.docker .docker \
  Library/Developer/Xcode/DerivedData Library/Developer/Xcode/Archives \
  "Library/Developer/Xcode/iOS DeviceSupport" Library/Developer/CoreSimulator \
  "Library/Application Support/MobileSync/Backup" \
  "Library/Application Support/Code/Cache" "Library/Application Support/Code/CachedData" \
  Library/Logs .Trash Downloads Movies; do
  [ -e "$p" ] && du -sh "$p" 2>/dev/null
done | sort -rh

if [ ${#PROJECT_DIRS[@]} -gt 0 ]; then
  hr "Project dirs: ${PROJECT_DIRS[*]}"
  for d in "${PROJECT_DIRS[@]}"; do du -sh "$d"/* 2>/dev/null; done | sort -rh | head -15

  hr "node_modules (top 20)"
  find "${PROJECT_DIRS[@]}" -maxdepth 6 -type d -name node_modules -prune -print0 2>/dev/null \
    | xargs -0 du -sh 2>/dev/null | sort -rh | head -20

  hr "Build artifacts and virtualenvs (top 25)"
  find "${PROJECT_DIRS[@]}" -maxdepth 6 -type d \( -name .next -o -name build -o -name dist \
    -o -name target -o -name .dart_tool -o -name Pods -o -name .venv -o -name venv \
    -o -name .gradle -o -name .turbo -o -name .parcel-cache \) -prune -print0 2>/dev/null \
    | xargs -0 du -sh 2>/dev/null | sort -rh | head -25
fi

hr "Files over 1 GB"
find "$HOME" -xdev -type f -size +1G -print0 2>/dev/null \
  | xargs -0 du -sh 2>/dev/null | sort -rh | head -30

hr "Android SDK system images"
ls -d "$HOME"/Library/Android/sdk/system-images/*/* 2>/dev/null

hr "Tools"
command -v docker >/dev/null && { echo "# docker"; docker system df 2>/dev/null || echo "(docker not running)"; }
command -v ollama >/dev/null && { echo "# ollama"; ollama list 2>/dev/null; }
command -v brew   >/dev/null && { echo "# brew cleanup -n"; brew cleanup -n 2>/dev/null | tail -1; }
command -v xcrun  >/dev/null && { echo "# unavailable simulators"; xcrun simctl list devices unavailable 2>/dev/null | grep -c "unavailable"; }
echo "# Time Machine local snapshots"; tmutil listlocalsnapshots / 2>/dev/null

hr "Access check"
ls "$HOME/.Trash" >/dev/null 2>&1 || echo "Cannot read ~/.Trash — grant the terminal Full Disk Access for complete results."
