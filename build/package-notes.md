# ASUSTOR Package Notes

Package-specific notes used to generate the changelog.
These notes are combined with Runtipi GitHub release notes.

## 4.6.5.r1 (2025-12-10)

- Added: Compatible ASUSTOR models table in README
- Added: Auto-created tipi-compose.yml for correct Traefik volume mounts
- Changed: Docker minimum version lowered to 28.0.0 (was 28.1.1)
- Fixed: Traefik config path mounting via tipi-compose.yml
- Known Issue: memory-advice temporarily removed from config.json (ASUSTOR bug #91706)

## 4.6.5 (2025-11-28)

- Initial public release on GitHub
- Added: Automatic pre-upgrade backup before package updates
- Added: Cloudflare DNS challenge setup script (`scripts/cloudflare-setup.sh`)
- Added: Enhanced backup script with `--full`, `--destination`, `--max-backups` options
- Added: Enhanced restore script with `--list`, `--dry-run`, `--file` options
- Added: ARM64 (aarch64) package support for AS33xx, AS11xx, AS67xx series
- Added: RUNTIPI_BACKUP_PATH and RUNTIPI_MAX_BACKUPS environment variables
- Added: Symbolic link for runtipi-cli in /usr/local/bin
- Added: GitHub Actions workflows for CI/CD automation
- Added: Cross-platform APK builder (build.py v1.5.0)
- Added: Dev build mode with auto-increment counter
- Improved: Separate log files - package.log for package scripts, cli.log for CLI output
- Improved: Unified emoji logging across all scripts
- Improved: CLI output parsed for clean logging
- Improved: Auto-generated changelog from GitHub releases + package notes
- Improved: POSIX/sh compatibility for all scripts (ADM 5.x BusyBox)
- Improved: Port conflict detection before service start
- Improved: Sensitive variables masking in logs
- Improved: Comprehensive README with upgrade guide and Cloudflare setup
- Fixed: CRLF line endings in shell scripts (build validation)
- Fixed: Icon size validation (90x90 per ASUSTOR spec)
- Fixed: CONTROL_DIR paths in start-stop.sh
