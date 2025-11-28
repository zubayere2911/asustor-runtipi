# 🤝 Contributing Guide

Thank you for your interest in contributing! 🎉

---

## 📋 Table of Contents

- [🚀 Getting Started](#-getting-started)
- [💻 Development Setup](#-development-setup)
- [✏️ Making Changes](#️-making-changes)
- [📤 Pull Request Process](#-pull-request-process)
- [📏 Coding Standards](#-coding-standards)
- [🧪 Testing](#-testing)
- [❓ Questions](#-questions)

---

## 🚀 Getting Started

### Prerequisites

| Requirement | Version | Notes |
|-------------|---------|-------|
| Python | 3.7+ | For build scripts |
| Git | Latest | Version control |
| ASUSTOR NAS | ADM 5.x | For testing (optional) |

### Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/asustor-runtipi.git
cd asustor-runtipi
```

---

## 💻 Development Setup

### 📁 Project Structure

```
asustor-runtipi/
├── apk/CONTROL/             # Package scripts (POSIX/sh)
│   ├── config.json          # Package metadata
│   ├── common.sh            # Shared logging & utilities
│   ├── start-stop.sh        # Service lifecycle
│   └── *.sh                 # Other lifecycle scripts
├── build/                   # Build tools (Python)
│   ├── build.py             # APK builder (v1.5.0)
│   ├── package-notes.md     # ASUSTOR-specific changelog
│   ├── version-manager.py   # Version management
│   └── docker-images.py     # Docker image sync
├── scripts/                 # Utility scripts
├── releases/                # Built packages (git-ignored)
│   └── dev/                 # Dev builds
├── CHANGELOG.md             # Auto-generated
├── LICENSE                  # MIT (auto-synced to APK)
└── .github/workflows/       # CI/CD workflows
```

### 🔨 Building Locally

```bash
# 📦 Production build (output to releases/)
python build/build.py

# 🧪 Dev build (auto-increment, output to releases/dev/)
python build/build.py --dev

# 📋 List APK contents
python build/build.py --list releases/io.runtipi_4.6.5_x86-64.apk
```

### 🧪 Dev Builds

Use `--dev` for local testing without modifying version or changelog:

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

---

## ✏️ Making Changes

### 🌿 Branch Naming

| Prefix | Usage |
|--------|-------|
| `feature/` | New features |
| `fix/` | Bug fixes |
| `docs/` | Documentation updates |
| `refactor/` | Code refactoring |

### 💬 Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```bash
feat: add Cloudflare DNS challenge support
fix: resolve CRLF line ending issue in scripts
docs: update README with backup instructions
chore: update dependencies
```

### 📝 Updating the Changelog

Add your changes to `build/package-notes.md` under `## Current`:

```markdown
## Current
- Added: Your new feature
- Fixed: Bug you fixed
- Improved: Enhancement description
```

> 💡 The changelog is auto-generated during build.

---

## 📤 Pull Request Process

### Workflow

1. 🌿 **Create a feature branch** from `main`
2. ✏️ **Make your changes** following the coding standards
3. 📝 **Update `build/package-notes.md`** with your changes
4. 🧪 **Test locally** with `python build/build.py --dev`
5. 📤 **Push and create a PR**
6. ⏳ **Wait for CI checks** to pass
7. 👀 **Request review** from maintainers

### ✅ PR Checklist

| Check | Description |
|-------|-------------|
| 🐚 POSIX/sh | Code follows POSIX/sh compatibility for shell scripts |
| 📊 Logging | Uses unified logging (`log_info`, `log_success`, etc.) |
| 📄 Line endings | All scripts have Unix line endings (LF, not CRLF) |
| 📋 config.json | Valid JSON format |
| 🔨 Build | Build succeeds locally (`python build/build.py --dev`) |
| 📝 Changelog | Updated (`build/package-notes.md`) |
| 📚 Docs | Documentation updated if needed |

---

## 📏 Coding Standards

### 🐚 Shell Scripts (POSIX/sh)

All scripts in `apk/CONTROL/` must be POSIX compatible for ADM 5.x BusyBox:

#### ✅ Good - POSIX Compatible

```bash
#!/bin/sh
set -eu

# Use common.sh for logging
. "${CONTROL_DIR}/common.sh"

log_info "Starting operation"
log_success "Operation completed"

if [ -f "$file" ]; then
  log_warn "File exists"
fi
```

#### ❌ Bad - Bash-specific

```bash
#!/bin/bash
declare -A array        # ❌ Bash arrays
[[ $var == "value" ]]   # ❌ Double brackets
echo -e "text"          # ❌ echo -e
```

### 📊 Logging Functions

Use the unified logging from `common.sh`:

| Function | Emoji | Usage |
|----------|-------|-------|
| `log_info` | ℹ️ | Information messages |
| `log_success` | ✅ | Success confirmations |
| `log_warn` | ⚠️ | Warnings |
| `log_error` | ❌ | Errors |
| `log_debug` | 🐛 | Debug (when enabled) |
| `log_section` | ═══ | Section headers |

### 🚫 Avoid

| Pattern | Reason | Alternative |
|---------|--------|-------------|
| `declare` | Bash-specific | Use plain variables |
| `[[ ]]` | Bash-specific | Use `[ ]` |
| Bash arrays | Not POSIX | Use simple strings |
| `source` | Not portable | Use `.` |
| `function` | Bash-specific | Just use `name()` |
| `echo -e` | Not portable | Use `printf` |

### 📋 config.json

| Setting | Value |
|---------|-------|
| Indentation | 4 spaces |
| Package name | `io.runtipi` |
| Architecture | `x86-64` or `arm64` |
| Firmware | `5.1.0` minimum |

---

## 🧪 Testing

### 🖥️ Local Testing

```bash
# 🔨 Build dev package
python build/build.py --dev

# 📤 Copy to NAS
scp releases/dev/*.apk admin@nas:/tmp/

# 📦 Install on NAS
ssh admin@nas "apkg install /tmp/io.runtipi_*.apk"
```

### ✅ Test Checklist

| Test | Description |
|------|-------------|
| 🆕 Fresh install | Install on clean ADM 5.x |
| ⬆️ Upgrade | Upgrade from previous version |
| ▶️ Start/Stop | Service lifecycle |
| 📋 Logs | Check `/share/Docker/RunTipi/logs/` |
| 🌐 Web UI | Verify accessible |
| 💾 Snapshot | Test backup/restore |
| 🗑️ Uninstall | Data should be preserved |

### 🤖 CI Testing

Pull requests automatically run:

| Check | Description |
|-------|-------------|
| 🐚 ShellCheck | Shell script linting |
| 📄 Line endings | CRLF → LF validation |
| 📋 config.json | JSON validation |
| 🖼️ Icon | Size validation (90x90) |
| 🔨 Build | Build test |

---

## ❓ Questions

| Resource | Link |
|----------|------|
| 🐛 Issues | [GitHub Issues](https://github.com/JigSawFr/asustor-runtipi/issues) |
| 🛠️ Developer Guide | [DEVELOPER.md](DEVELOPER.md) |
| 📚 Runtipi Docs | [runtipi.io/docs](https://runtipi.io/docs) |
| 📖 ASUSTOR Dev Guide | [developer.asustor.com](https://developer.asustor.com/) |
| 💬 Discord | [#asustor Channel](https://discord.gg/xPtEFWEcjT) |

---

## 🙏 Thank You!

Thank you for contributing to Runtipi for ASUSTOR! Your contributions help make self-hosting easier for the community. 🎉

---

*Last updated: November 2025*
