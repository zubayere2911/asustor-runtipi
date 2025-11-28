#!/bin/sh
# ADM snapshot restore pre-hook for Runtipi
set -eu
RUNTIPI_LOG="/share/Docker/RunTipi/logs/package.log"
mkdir -p "$(dirname "$RUNTIPI_LOG")" 2>/dev/null || true

_timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log_info()    { echo "$(_timestamp) ℹ️  $1" >> "$RUNTIPI_LOG"; }
log_success() { echo "$(_timestamp) ✅ $1" >> "$RUNTIPI_LOG"; }
log_warn()    { echo "$(_timestamp) ⚠️  $1" >> "$RUNTIPI_LOG"; }

echo "" >> "$RUNTIPI_LOG"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "📸 PRE-SNAPSHOT-RESTORE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# Stop service before restore
if [ -x "$APKG_PKG_DIR/runtipi-cli" ]; then
    log_info "🛑 Stopping service before snapshot restore..."
    "$APKG_PKG_DIR/runtipi-cli" stop >/dev/null 2>&1 || true
    log_success "Service stopped"
fi

log_success "Pre-snapshot-restore completed"
exit 0