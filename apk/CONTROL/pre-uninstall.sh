#!/bin/sh
# ============================================================================
# PRE-UNINSTALL.SH - Pre-uninstallation tasks for Runtipi
# This script must remain POSIX/sh compatible for ADM 5.x (BusyBox/ash)
# ============================================================================
set -eu

# Use same log location as other scripts
RUNTIPI_PATH="/share/Docker/RunTipi"
RUNTIPI_LOG="$RUNTIPI_PATH/logs/package.log"
mkdir -p "$RUNTIPI_PATH/logs" 2>/dev/null || true

_timestamp() { date '+%Y-%m-%d %H:%M:%S'; }
log_info()    { echo "$(_timestamp) ℹ️  $1" >> "$RUNTIPI_LOG"; }
log_success() { echo "$(_timestamp) ✅ $1" >> "$RUNTIPI_LOG"; }
log_warn()    { echo "$(_timestamp) ⚠️  $1" >> "$RUNTIPI_LOG"; }
log_error()   { echo "$(_timestamp) ❌ $1" >> "$RUNTIPI_LOG"; }

log_section() {
    echo "" >> "$RUNTIPI_LOG"
    echo "$(_timestamp) ╔══════════════════════════════════════════════════════════════╗" >> "$RUNTIPI_LOG"
    echo "$(_timestamp) ║  $1" >> "$RUNTIPI_LOG"
    echo "$(_timestamp) ╚══════════════════════════════════════════════════════════════╝" >> "$RUNTIPI_LOG"
}

log_section "🗑️  PRE-UNINSTALL - Runtipi v$APKG_PKG_VER"

# ============================================================================
# 🛑 STOP SERVICE
# ============================================================================
echo "" >> "$RUNTIPI_LOG"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "🛑 STOP SERVICE"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

if [ -x "$APKG_PKG_DIR/runtipi-cli" ]; then
    log_info "Stopping Runtipi service..."
    
    # Change to package directory (CLI needs this to find docker-compose.yml)
    cd "$APKG_PKG_DIR" || true
    
    # Stop the service silently
    "$APKG_PKG_DIR/runtipi-cli" stop >/dev/null 2>&1 || true
    
    # Fallback: stop containers directly with docker if CLI failed
    if docker ps --filter "name=runtipi" --format "{{.Names}}" 2>/dev/null | grep -q .; then
        log_warn "CLI stop may have failed, stopping containers directly..."
        docker stop runtipi runtipi-reverse-proxy runtipi-db runtipi-queue 2>/dev/null || true
        docker rm runtipi runtipi-reverse-proxy runtipi-db runtipi-queue 2>/dev/null || true
    fi
    
    log_success "Service stopped"
else
    log_info "CLI not found, skipping service stop"
fi

# ============================================================================
# 🧹 CLEANUP (preserve user data in /share/Docker/RunTipi)
# ============================================================================
echo "" >> "$RUNTIPI_LOG"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "🧹 CLEANUP PACKAGE FILES"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

log_info "Cleaning up package files..."

# Remove CLI and binaries
rm -f "$APKG_PKG_DIR/runtipi-cli" 2>/dev/null || true
rm -rf "$APKG_PKG_DIR/bin" 2>/dev/null || true

# Remove package config files (not user data)
rm -f "$APKG_PKG_DIR/.env" 2>/dev/null || true
rm -f "$APKG_PKG_DIR/VERSION" 2>/dev/null || true
rm -rf "$APKG_PKG_DIR/user-config" 2>/dev/null || true
rm -rf "$APKG_PKG_DIR/traefik" 2>/dev/null || true
rm -rf "$APKG_PKG_DIR/state" 2>/dev/null || true

# Remove old .env backups
find "$APKG_PKG_DIR" -maxdepth 1 -name '.env.bak.*' -type f -delete 2>/dev/null || true

# Remove temp files
rm -f "$APKG_PKG_DIR/runtipi-cli.tar.gz" 2>/dev/null || true

log_success "Package files cleaned up"

# ============================================================================
# ✅ COMPLETE
# ============================================================================
echo "" >> "$RUNTIPI_LOG"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_success "🎉 Pre-uninstall completed successfully!"
log_info "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
log_info "📂 User data preserved in: /share/Docker/RunTipi"
log_info "💡 To remove all data: rm -rf /share/Docker/RunTipi"
echo "" >> "$RUNTIPI_LOG"

exit 0
