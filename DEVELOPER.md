# 🛠️ Developer Guide

> Complete guide for building, testing, and contributing to Runtipi for ASUSTOR.

---

## 📋 Table of Contents

- [📁 Package Structure](#-package-structure)
- [🔨 Build System](#-build-system)
- [🏷️ Version Management](#️-version-management)
- [📝 Changelog Generation](#-changelog-generation)
- [🐳 Docker Images Management](#-docker-images-management)
- [📜 Key Scripts](#-key-scripts)
- [🔄 GitHub Workflows](#-github-workflows)
- [🧪 Testing](#-testing)
- [💻 VS Code Integration](#-vs-code-integration)

---

## 📁 Package Structure

```
├── apk/CONTROL/          # Package scripts (POSIX/sh)
│   ├── config.json       # Package metadata
│   ├── common.sh         # Shared logging & utilities
│   ├── start-stop.sh     # Service lifecycle
│   ├── pre-install.sh    # Validation & image pulls
│   ├── post-install.sh   # Setup & configuration
│   ├── pre-uninstall.sh  # Cleanup
│   └── ...
├── build/                # Build tools (Python 3.7+)
│   ├── build.py          # APK builder (v1.5.0)
│   ├── package-notes.md  # ASUSTOR-specific changelog notes
│   └── ...
├── scripts/              # Utility scripts (Bash)
├── releases/             # Built packages (git-ignored)
│   └── dev/              # Dev builds (auto-cleaned)
├── CHANGELOG.md          # Auto-generated changelog
└── LICENSE               # MIT license (auto-synced to APK)
```

### 📂 Runtime Paths

| Path | Description |
|------|-------------|
| `/share/Docker/RunTipi` | Persistent data directory |
| `/share/Docker/RunTipi/logs/package.log` | Package script logs |
| `/share/Docker/RunTipi/logs/cli.log` | CLI output logs |
| `$APKG_PKG_DIR` | ADM package installation directory |
| `$AS_NAS_ARCH` | NAS architecture (x86_64/aarch64) |

---

## 🔨 Build System

### Building Packages

```bash
# 📦 Production build (output to releases/)
python build/build.py

# 🧪 Dev build (auto-increment counter, output to releases/dev/)
python build/build.py --dev

# 📁 Custom output directory
python build/build.py --destination ./output

# 📋 List APK contents
python build/build.py --list releases/io.runtipi_4.6.5_x86-64.apk

# 📂 Extract APK
python build/build.py --extract package.apk -d ./extracted
```

### 🧪 Dev Builds

Dev builds are for local testing and don't modify `config.json` or changelog:

```bash
python build/build.py --dev
# → releases/dev/io.runtipi_4.6.5.dev1_x86-64.apk

python build/build.py --dev
# → releases/dev/io.runtipi_4.6.5.dev2_x86-64.apk (counter increments)
```

| Feature | Behavior |
|---------|----------|
| 🔢 Counter | Resets when package version changes |
| 🧹 Cleanup | Old dev builds auto-cleaned (keeps last 5) |
| 💾 Storage | Counter stored in `build/.dev-build-counter` |

---

## 🏷️ Version Management

> ⚠️ ASUSTOR App Central doesn't allow updating with the same version number. Use revisions for package-only fixes.

### Version Format

| Type | Format | Example | Usage |
|------|--------|---------|-------|
| 🆕 Base | `X.Y.Z` | `4.6.5` | New Runtipi version |
| 🔧 Revision | `X.Y.Z.rN` | `4.6.5.r1` | Package fix, same Runtipi |
| 🧪 Dev | `X.Y.Z.devN` | `4.6.5.dev1` | Local testing |
| 🧪 Dev+Rev | `X.Y.Z.rN.devN` | `4.6.5.r1.dev1` | Local testing on revision |

### Commands

```bash
# 🔍 Check if revision is needed
python build/version-manager.py --check

# ➡️ Get next version (auto-detects if revision needed)
python build/version-manager.py --get-next

# ⬆️ Update config.json with next version
python build/version-manager.py --update

# 🎯 Set specific base version (auto-adds revision if tag exists)
python build/version-manager.py --set 4.6.5

# 📋 List existing version tags
python build/version-manager.py --tags
```

---

## 📝 Changelog Generation

The changelog is **auto-generated** during build from:

| Source | Description |
|--------|-------------|
| 🌐 GitHub Releases | Runtipi upstream release notes |
| 📦 Package Notes | ASUSTOR-specific changes (`build/package-notes.md`) |

### Package Notes Format

```markdown
# build/package-notes.md

## Current
- Added: New feature for this release
- Fixed: Bug fix description

## [4.6.5]
- Previous version notes (for history)
```

### Output Files

| File | Location | Purpose |
|------|----------|---------|
| `CHANGELOG.md` | Root | Visible on GitHub |
| `changelog.txt` | `apk/CONTROL/` | APK copy |

### License Sync

The `LICENSE` file is automatically:
- ✅ Copied to `apk/CONTROL/license.txt` during build
- ✅ Updated with current year (e.g., 2023 → 2025)

---

## 🐳 Docker Images Management

The package pre-pulls Docker images used by Runtipi:

```bash
# 📋 Show current images in pre-install.sh
python build/docker-images.py --show

# 🔍 Fetch correct versions for a Runtipi version
python build/docker-images.py --fetch --version 4.6.5

# ⬆️ Update pre-install.sh with correct versions
python build/docker-images.py --update --version 4.7.0
```

### Managed Images

| Image | Description |
|-------|-------------|
| `traefik` | Reverse proxy (version from Runtipi release) |
| `postgres:14` | Database (stable at v14) |
| `rabbitmq:4-alpine` | Message queue |
| `ghcr.io/runtipi/runtipi:vX.Y.Z` | Main application |

---

## 📜 Key Scripts

### Logging System

All scripts use unified emoji logging via `common.sh`:

```bash
source "${CONTROL_DIR}/common.sh"

log_info "Information message"      # ℹ️
log_success "Success message"       # ✅
log_warn "Warning message"          # ⚠️
log_error "Error message"           # ❌
log_debug "Debug message"           # 🐛
log_section "Section Header"        # ══════════
```

### Log Files

| File | Content |
|------|---------|
| `package.log` | Package script output |
| `cli.log` | Runtipi CLI output (via `run_cli` wrapper) |

### Script Reference

| Script | Purpose |
|--------|---------|
| `common.sh` | Shared functions, logging, environment |
| `pre-install.sh` | Validation, Docker image pulls |
| `post-install.sh` | Setup, .env creation, permissions |
| `start-stop.sh` | Service lifecycle, port checks |
| `pre-uninstall.sh` | Cleanup (binaries, logs, temp) |
| `helper.sh` | Log rotation (called by ADM) |
| `pre-snapshot-restore.sh` | Pre-restore checks |
| `post-snapshot-restore.sh` | Post-restore setup |

---

## 🔄 GitHub Workflows

| Workflow | Trigger | Description |
|----------|---------|-------------|
| `ci.yml` | Push/PR to main | Lint + build validation |
| `release.yml` | Tag `v*` or manual | Build + create GitHub release |
| `sync-upstream.yml` | Daily or manual | Check for new Runtipi versions |
| `publish-devcenter.yml` | After release | Upload to ASUSTOR Dev Center |
| `codeql.yml` | Push/PR/Weekly | Security scanning for Python |

### Creating a Release

#### Option 1: Via Tag

```bash
git tag v4.6.5
git push origin v4.6.5
```

#### Option 2: Via Workflow Dispatch

1. Go to **Actions** → **Release** → **Run workflow**
2. Enter base version (e.g., `4.6.5`)
3. Revision is auto-added if tag already exists

---

## 🧪 Testing

### Local Testing

```bash
# 🔨 Build dev package
python build/build.py --dev

# 📤 Copy to NAS and install
scp releases/dev/*.apk admin@nas:/tmp/
ssh admin@nas "apkg install /tmp/io.runtipi_*.apk"
```

### Test Checklist

| Test | Description |
|------|-------------|
| ✅ Fresh install | Install on clean ADM 5.x |
| ✅ Upgrade | Upgrade from previous version |
| ✅ Start/Stop | Service lifecycle |
| ✅ Logs | Check `/share/Docker/RunTipi/logs/` |
| ✅ .env sync | Verify configuration sync |
| ✅ Snapshot | Test backup/restore |
| ✅ Uninstall | Data should be preserved |

---

## 💻 VS Code Integration

Install recommended extensions for the best development experience.

### Available Debug Configurations

| Config | Description |
|--------|-------------|
| 🔨 Build | Build packages |
| 🏷️ Version | Version management |
| 🧪 Test | Test scripts |
| 🎬 Act | Local GitHub Actions testing |

---

## 📚 Related Documentation

| Document | Description |
|----------|-------------|
| [CONTRIBUTING.md](CONTRIBUTING.md) | Contribution guidelines |
| [SECURITY.md](SECURITY.md) | Security policy |
| [CHANGELOG.md](CHANGELOG.md) | Version history |
| [README.md](README.md) | User documentation |

---

## 📄 License

MIT - See [LICENSE](LICENSE)

---

*Last updated: November 2025*
