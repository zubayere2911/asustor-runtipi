#!/bin/sh
# ============================================================================
# HELPER.SH - Periodic maintenance hook called by ADM
# This script must remain POSIX/sh compatible for ADM 5.x (BusyBox/ash)
# ============================================================================
# ADM calls this script periodically for maintenance tasks.
# All logic is in common.sh - this is just the entry point.
# ============================================================================

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ -f "$SCRIPT_DIR/common.sh" ]; then
    . "$SCRIPT_DIR/common.sh"
    rotate_logs
else
    # Minimal fallback if common.sh missing
    LOG="/share/Docker/RunTipi/logs/package.log"
    [ -f "$LOG" ] && {
        size=$(stat -c%s "$LOG" 2>/dev/null || echo 0)
        [ "$size" -gt 10485760 ] && tail -n 1000 "$LOG" > "$LOG.tmp" && mv "$LOG.tmp" "$LOG"
    }
fi

exit 0
