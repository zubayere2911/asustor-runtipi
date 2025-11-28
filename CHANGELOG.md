# 📋 Changelog

> All notable changes to Runtipi for ASUSTOR are documented here.
> 
> This changelog is **auto-generated** during build from GitHub releases and package notes.

---

## [4.6.5] - 2025-11-28

### 🚀 Runtipi v4.6.5

- Update traefik to v3.6.1. This fixes an upstream issue that was preventing the use of latest Docker v29
- `./runtipi-cli update v4.6.5`

### 📦 ASUSTOR Package

#### 🎉 Initial Public Release

This is the **first public release** on GitHub!

#### ✨ Added

| Feature | Description |
|---------|-------------|
| 💾 Auto Backup | Automatic pre-upgrade backup before package updates |
| 🌐 Cloudflare DNS | Setup script (`scripts/cloudflare-setup.sh`) |
| 📦 Enhanced Backup | `--full`, `--destination`, `--max-backups` options |
| 🔄 Enhanced Restore | `--list`, `--dry-run`, `--file` options |
| 🏗️ ARM64 Support | For AS33xx, AS11xx, AS67xx series |
| ⚙️ Environment Variables | `RUNTIPI_BACKUP_PATH` and `RUNTIPI_MAX_BACKUPS` |
| 🔗 CLI Symlink | Symbolic link for runtipi-cli in `/usr/local/bin` |
| 🤖 GitHub Actions | CI/CD workflows for automation |
| 🔨 Build System | Cross-platform APK builder (build.py v1.5.0) |
| 🧪 Dev Builds | Dev build mode with auto-increment counter |

#### 🔧 Improved

| Area | Description |
|------|-------------|
| 📊 Logging | Separate log files - `package.log` for package, `cli.log` for CLI |
| 🎨 Emoji Logging | Unified emoji logging across all scripts |
| 📋 CLI Output | Parsed for clean logging |
| 📝 Changelog | Auto-generated from GitHub releases + package notes |
| 🐚 POSIX | POSIX/sh compatibility for all scripts (ADM 5.x BusyBox) |
| 🔍 Port Detection | Port conflict detection before service start |
| 🔐 Security | Sensitive variables masking in logs |
| 📚 Documentation | Comprehensive README with upgrade guide and Cloudflare setup |

#### 🐛 Fixed

| Issue | Description |
|-------|-------------|
| 📄 Line Endings | CRLF line endings in shell scripts (build validation) |
| 🖼️ Icon Size | Icon size validation (90x90 per ASUSTOR spec) |
| 📁 Paths | CONTROL_DIR paths in start-stop.sh |

---

## 📚 More Information

| Resource | Link |
|----------|------|
| 🚀 Full Runtipi Changelog | [GitHub Releases](https://github.com/runtipi/runtipi/releases) |
| 📦 Download Packages | [Releases](https://github.com/JigSawFr/asustor-runtipi/releases) |
| 🐛 Report Issues | [GitHub Issues](https://github.com/JigSawFr/asustor-runtipi/issues) |
| 💬 Community | [Discord #asustor](https://discord.gg/xPtEFWEcjT) |

---

*Last updated: November 2025*
