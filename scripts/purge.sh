#!/bin/sh
# ============================================================================
# PURGE.SH - Remove ALL Runtipi data (DANGEROUS!)
# Usage: purge.sh --yes-i-am-sure
# ============================================================================
set -eu

RUNTIPI_PATH="/share/Docker/RunTipi"
PKG_DIR="${APKG_PKG_DIR:-/usr/local/AppCentral/runtipi}"

# Safety check
if [ "$#" -ne 1 ] || [ "$1" != "--yes-i-am-sure" ]; then
    cat << EOF
⚠️  WARNING: This will DELETE ALL Runtipi data!

This includes:
  - All installed apps and their data
  - All configuration and settings
  - All backups
  - All logs

To proceed, run: $0 --yes-i-am-sure

EOF
    exit 1
fi

# Final confirmation
printf "Type YES to confirm deletion: "
read -r answer
if [ "$answer" != "YES" ]; then
    echo "❌ Aborted"
    exit 1
fi

echo "🗑️  Purging Runtipi..."

# Stop service
if [ -x "$PKG_DIR/runtipi-cli" ]; then
    "$PKG_DIR/runtipi-cli" stop 2>/dev/null || true
fi

# Remove all data
rm -rf "$RUNTIPI_PATH"/* 2>/dev/null || true
rm -f "$PKG_DIR/.env" "$PKG_DIR/.env.bak."* 2>/dev/null || true
rm -f /tmp/runtipi-*.log 2>/dev/null || true

echo "✅ Purge complete"
exit 0
