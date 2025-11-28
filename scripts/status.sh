#!/bin/sh
# ============================================================================
# STATUS.SH - Show Runtipi status
# ============================================================================
set -eu

RUNTIPI_PATH="/share/Docker/RunTipi"
PKG_DIR="${APKG_PKG_DIR:-/usr/local/AppCentral/runtipi}"

echo "📋 Runtipi Status Report"
echo "========================"
echo ""

# Version
if [ -f "$PKG_DIR/VERSION" ]; then
    echo "Version: $(cat "$PKG_DIR/VERSION")"
else
    echo "Version: unknown"
fi

# Service status
if pgrep -f runtipi-cli >/dev/null 2>&1; then
    echo "Service: ✅ running"
else
    echo "Service: ⏹️  stopped"
fi

# Docker containers
echo ""
echo "Docker Containers:"
docker ps --filter "name=runtipi" --format "  {{.Names}}: {{.Status}}" 2>/dev/null || echo "  (unable to check)"

# Critical files
echo ""
echo "Configuration:"
for f in "$PKG_DIR/.env" "$RUNTIPI_PATH/.env" "$RUNTIPI_PATH/state/settings.json"; do
    if [ -f "$f" ]; then
        echo "  ✅ $f"
    else
        echo "  ❌ $f (missing)"
    fi
done

# Disk usage
echo ""
echo "Disk Usage:"
if [ -d "$RUNTIPI_PATH" ]; then
    du -sh "$RUNTIPI_PATH" 2>/dev/null | awk '{print "  RunTipi: " $1}'
fi

# Last log entries
echo ""
echo "Recent Package Logs:"
if [ -f "$RUNTIPI_PATH/logs/runtipi-package.log" ]; then
    tail -n 5 "$RUNTIPI_PATH/logs/runtipi-package.log" | sed 's/^/  /'
else
    echo "  (no logs found)"
fi

exit 0
