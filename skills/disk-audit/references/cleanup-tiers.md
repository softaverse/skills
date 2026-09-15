# Cleanup Tiers

How to classify what `disk-audit.sh` finds, with the preferred cleanup command for each.

## 🟢 Safe — regenerates automatically

Deleting these costs only re-download or rebuild time.

| Location | Command | Notes |
|---|---|---|
| Flutter `build/`, `.dart_tool/` | `flutter clean` in each project | Often 1 GB+ per project |
| Next.js `.next/`, `.turbo/`, `.parcel-cache/` | `rm -rf .next` | |
| Generic `dist/`, `build/` in JS projects | `rm -rf dist` | Check it is not a committed output folder |
| Rust `target/` | `cargo clean` | |
| `~/.npm` | `npm cache clean --force` | |
| `~/Library/pnpm`, `~/.pnpm-store` | `pnpm store prune` | Keeps packages still linked by projects |
| Yarn cache | `yarn cache clean` | |
| `~/.bun/install/cache` | `bun pm cache rm` | |
| `~/Library/Caches/*` | `rm -rf ~/Library/Caches/<app>` | Quit the app first |
| Homebrew | `brew cleanup --prune=all` | |
| pip | `pip cache purge` | |
| `~/.cache/puppeteer`, `~/Library/Caches/ms-playwright` | `rm -rf` | Re-downloaded on next run |
| `~/.gradle/caches` | `rm -rf ~/.gradle/caches` | |
| Xcode `DerivedData` | `rm -rf ~/Library/Developer/Xcode/DerivedData/*` | |
| Unavailable iOS simulators | `xcrun simctl delete unavailable` | |
| Docker unused images / build cache | `docker system prune -a` (add `--volumes` for volumes) | Removes everything not used by a **running** container — warn first |
| `~/Library/Logs` | `rm -rf ~/Library/Logs/*` | Usually small |
| `~/.Trash` | Empty Trash in Finder | |

## 🟡 Confirm first — reclaimable, but the user may still need it

| Location | How to remove | What to ask |
|---|---|---|
| `node_modules` in projects | `rm -rf node_modules` | Is the project still active? `npm install` restores it |
| `.venv` / `venv` | `rm -rf .venv` | Is the project still used? Needs reinstall |
| `~/Library/Android/sdk/system-images/*` | Android Studio → SDK Manager | Which API levels are still tested? |
| `~/.android/avd/*` | Android Studio → Device Manager | Which emulators are used? |
| `~/Library/Android/sdk/ndk/*` | SDK Manager | Old NDK versions are usually unused |
| Xcode `Archives`, `iOS DeviceSupport` | Xcode → Organizer, or `rm -rf` old versions | Needed for crash symbolication of shipped builds |
| `~/.ollama` models | `ollama rm <name>` | Which models are still used? |
| `~/.cache/huggingface` | `huggingface-cli delete-cache` | Re-download can be several GB |
| `~/.pyenv/versions/*`, `~/.nvm/versions/*`, `~/.rustup/toolchains/*` | `pyenv uninstall`, `nvm uninstall`, `rustup toolchain uninstall` | Which versions do projects pin? |
| `Application Support/Claude/vm_bundles` | Delete in the Claude desktop app settings or `rm -rf` | Is the desktop VM feature used? Re-downloads if needed |
| `Application Support/Google/Chrome/OptGuideOnDeviceModel` | Disable on-device AI in `chrome://flags`, then delete | Chrome re-downloads it unless disabled |
| `Application Support/Postman/Partitions`, Slack, Discord, Teams caches | Clear cache in app settings | Mostly cache, may hold offline data |
| `Library/Containers/com.docker.docker` (the VM disk) | Docker Desktop → Settings → Resources → disk limit, or reset | Resetting wipes all images and volumes |
| iPhone backups (`MobileSync/Backup`) | Finder → device → Manage Backups | Is there a newer backup elsewhere? |
| Time Machine local snapshots | `tmutil thinlocalsnapshots / 999999999999 4` | macOS frees these automatically when space is needed |

## 🔴 Personal data — the user decides

List these with size and a suggestion only. Never delete them.

- Mail stores (`~/Library/Mail`, `~/Library/Thunderbird`): suggest limiting offline sync to recent mail, since the server keeps a copy
- Photos library, `~/Movies`, `~/Music`, `~/Pictures`
- `~/Downloads`, `~/Documents`, `~/Desktop`: point out the largest or oldest files
- Cloud-drive folders (Google Drive, iCloud, Dropbox): check for duplicate mount points and suggest "stream / online-only" mode
- Project source folders that are large beyond their `node_modules` and build output: point to the biggest subfolders and let the user decide
- Messaging app data (LINE, WhatsApp, Telegram media)
