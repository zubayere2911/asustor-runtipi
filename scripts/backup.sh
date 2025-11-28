#!/bin/sh
# ============================================================================
# BACKUP.SH - Backup Runtipi configuration and data
# Usage: backup.sh [--full] [--destination DIR] [--max N] [--quiet]
# ============================================================================
set -eu

RUNTIPI_PATH="/share/Docker/RunTipi"
BACKUP_DIR="${RUNTIPI_BACKUP_PATH:-$RUNTIPI_PATH/backup}"
MAX_BACKUPS="${RUNTIPI_MAX_BACKUPS:-5}"
FULL_BACKUP=false
QUIET=false

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
  -d, --destination DIR   Backup directory (default: $BACKUP_DIR)
  -m, --max-backups N     Keep only last N backups (default: $MAX_BACKUPS)
  -f, --full              Full backup including app-data (large!)
  -q, --quiet             Quiet mode
  -h, --help              Show this help
EOF
    exit 0
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -d|--destination) BACKUP_DIR="$2"; shift 2;;
        -m|--max-backups) MAX_BACKUPS="$2"; shift 2;;
        -f|--full) FULL_BACKUP=true; shift;;
        -q|--quiet) QUIET=true; shift;;
        -h|--help) usage;;
        *) echo "Unknown option: $1"; usage;;
    esac
done

TS=$(date +%Y%m%d%H%M%S)
DEST="$BACKUP_DIR/runtipi-backup-$TS.tar.gz"
mkdir -p "$BACKUP_DIR"

[ "$QUIET" = false ] && echo "📦 Backup started: $TS"

# Check if data exists
if [ ! -d "$RUNTIPI_PATH" ]; then
    echo "❌ Runtipi directory not found: $RUNTIPI_PATH"
    exit 1
fi

# Build list of items
BACKUP_ITEMS=".env state user-config traefik logs"
[ "$FULL_BACKUP" = true ] && BACKUP_ITEMS="$BACKUP_ITEMS app-data apps repos"

# Find existing items
cd "$RUNTIPI_PATH"
EXISTING=""
for item in $BACKUP_ITEMS; do
    [ -e "$item" ] && EXISTING="$EXISTING $item"
done

if [ -z "$EXISTING" ]; then
    echo "❌ No items to backup"
    exit 1
fi

# Create backup
# shellcheck disable=SC2086
if tar czf "$DEST" $EXISTING 2>/dev/null; then
    SIZE=$(du -h "$DEST" | cut -f1)
    [ "$QUIET" = false ] && echo "✅ Backup created: $DEST ($SIZE)"
    
    # Cleanup old backups
    find "$BACKUP_DIR" -name "runtipi-backup-*.tar.gz" -type f 2>/dev/null | \
        sort -r | tail -n +"$((MAX_BACKUPS + 1))" | while read -r old; do rm -f "$old"; done
else
    echo "❌ Backup failed"
    exit 1
fi

exit 0
