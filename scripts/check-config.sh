#!/bin/sh
# ============================================================================
# CHECK-CONFIG.SH - Validate Runtipi configuration
# ============================================================================
set -eu

RUNTIPI_PATH="/share/Docker/RunTipi"
PKG_DIR="${APKG_PKG_DIR:-/usr/local/AppCentral/runtipi}"
ERRORS=0

echo "🔎 Runtipi Configuration Check"
echo "==============================="
echo ""

check_file() {
    if [ -f "$1" ]; then
        echo "✅ $2"
    else
        echo "❌ $2 (missing: $1)"
        ERRORS=$((ERRORS + 1))
    fi
}

check_dir() {
    if [ -d "$1" ]; then
        echo "✅ $2"
    else
        echo "❌ $2 (missing: $1)"
        ERRORS=$((ERRORS + 1))
    fi
}

check_env_var() {
    if [ -f "$PKG_DIR/.env" ]; then
        if grep -q "^$1=" "$PKG_DIR/.env"; then
            val=$(grep "^$1=" "$PKG_DIR/.env" | cut -d'=' -f2-)
            if [ -n "$val" ]; then
                echo "✅ $1 = $val"
            else
                echo "⚠️  $1 is empty"
            fi
        else
            echo "❌ $1 missing in .env"
            ERRORS=$((ERRORS + 1))
        fi
    fi
}

echo "Files:"
check_file "$PKG_DIR/.env" ".env (package)"
check_file "$RUNTIPI_PATH/.env" ".env (data)"
check_file "$RUNTIPI_PATH/state/settings.json" "settings.json"
check_file "$PKG_DIR/runtipi-cli" "runtipi-cli"

echo ""
echo "Directories:"
check_dir "$RUNTIPI_PATH" "RunTipi data"
check_dir "$RUNTIPI_PATH/logs" "Logs"

echo ""
echo "Environment Variables:"
check_env_var "INTERNAL_IP"
check_env_var "NGINX_PORT"
check_env_var "NGINX_PORT_SSL"
check_env_var "DOMAIN"

echo ""
echo "Dependencies:"
for cmd in docker jq curl openssl git; do
    if command -v "$cmd" >/dev/null 2>&1; then
        echo "✅ $cmd"
    else
        echo "❌ $cmd (not installed)"
        ERRORS=$((ERRORS + 1))
    fi
done

echo ""
if [ "$ERRORS" -eq 0 ]; then
    echo "✅ Configuration OK"
else
    echo "❌ Found $ERRORS error(s)"
fi

exit $ERRORS
