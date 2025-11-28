#!/bin/sh
# ============================================================================
# RESTORE.SH - Restore Runtipi configuration from backup
# Usage: restore.sh [--file BACKUP] [--list] [--dry-run] [--quiet]
# ============================================================================
set -eu

RUNTIPI_PATH="/share/Docker/RunTipi"
BACKUP_DIR="${RUNTIPI_BACKUP_PATH:-$RUNTIPI_PATH/backup}"
BACKUP_FILE=""
DRY_RUN=false
QUIET=false

usage() {
    cat << EOF
Usage: $0 [OPTIONS]

Options:
  -s, --source DIR   Backup directory (default: $BACKUP_DIR)
  -f, --file FILE    Restore specific backup file
  -l, --list         List available backups
  -n, --dry-run      Show what would be restored
  -q, --quiet        Quiet mode
  -h, --help         Show this help
EOF
    exit 0
}

list_backups() {
    echo "📋 Available backups in $BACKUP_DIR:"
    if [ -d "$BACKUP_DIR" ]; then
        find "$BACKUP_DIR" -name "runtipi-*.tar.gz" -type f -exec ls -lh {} \; 2>/dev/null | \
            awk '{print "  " $NF " (" $5 ")"}'
    else
        echo "  No backup directory found"
    fi
    exit 0
}

# Parse arguments
while [ $# -gt 0 ]; do
    case "$1" in
        -s|--source) BACKUP_DIR="$2"; shift 2;;
        -f|--file) BACKUP_FILE="$2"; shift 2;;
        -l|--list) list_backups;;
        -n|--dry-run) DRY_RUN=true; shift;;
        -q|--quiet) QUIET=true; shift;;
        -h|--help) usage;;
        *) echo "Unknown option: $1"; usage;;
    esac
done

[ "$QUIET" = false ] && echo "♻️  Restore started: $(date)"

# Find backup to restore
if [ -z "$BACKUP_FILE" ]; then
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "❌ Backup directory not found: $BACKUP_DIR"
        exit 1
    fi
    BACKUP_FILE=$(find "$BACKUP_DIR" -name "runtipi-*.tar.gz" -type f 2>/dev/null | sort -r | head -n1 || true)
    if [ -z "$BACKUP_FILE" ]; then
        echo "❌ No backup found. Run '$0 --list' to see available backups"
        exit 1
    fi
    [ "$QUIET" = false ] && echo "📁 Latest backup: $BACKUP_FILE"
elif [ ! -f "$BACKUP_FILE" ]; then
    echo "❌ Backup file not found: $BACKUP_FILE"
    exit 1
fi

# Dry-run mode
if [ "$DRY_RUN" = true ]; then
    echo "🔍 Backup contents:"
    tar tzf "$BACKUP_FILE"
    echo "📁 Would restore to: $RUNTIPI_PATH"
    exit 0
fi

# Safety backup before restore
TS=$(date +%Y%m%d%H%M%S)
if [ -f "$RUNTIPI_PATH/.env" ]; then
    [ "$QUIET" = false ] && echo "📦 Creating safety backup..."
    mkdir -p "$BACKUP_DIR"
    cd "$RUNTIPI_PATH"
    tar czf "$BACKUP_DIR/runtipi-pre-restore-$TS.tar.gz" .env state traefik user-config 2>/dev/null || true
fi

# Restore
mkdir -p "$RUNTIPI_PATH"
if tar xzf "$BACKUP_FILE" -C "$RUNTIPI_PATH" 2>/dev/null; then
    chmod 600 "$RUNTIPI_PATH/.env" 2>/dev/null || true
    chmod 600 "$RUNTIPI_PATH/state/settings.json" 2>/dev/null || true
    [ "$QUIET" = false ] && echo "✅ Restore completed"
    [ "$QUIET" = false ] && echo "⚠️  Please restart Runtipi to apply changes"
else
    echo "❌ Restore failed"
    exit 1
fi

exit 0
