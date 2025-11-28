#!/bin/sh
# Automated test script for Runtipi ADM package
# Usage: sh scripts/test.sh

set -eu
log="/tmp/runtipi-test-logs.txt"
echo "🧪 Runtipi ADM package test started: $(date)" > "$log"

# Notify ADM admin on critical error (if notify_admin available)
notify_admin() {
  if command -v notify_admin >/dev/null 2>&1; then
    notify_admin -t "Runtipi" -m "$1"
  fi
}

# Check dependencies
for dep in docker jq git curl openssl; do
  if ! command -v $dep >/dev/null 2>&1; then
    echo "❌ Missing dependency: $dep" >> "$log"
    notify_admin "Runtipi test failed: missing dependency $dep."
    exit 1
  fi
done

echo "✓ All dependencies found" >> "$log"

# Test service start/stop
if [ -x "$APKG_PKG_DIR/bin/runtipi-cli" ]; then
  "$APKG_PKG_DIR/bin/runtipi-cli" start >> "$log" 2>&1 && echo "✓ Service started" >> "$log"
  sleep 2
  "$APKG_PKG_DIR/bin/runtipi-cli" stop >> "$log" 2>&1 && echo "✓ Service stopped" >> "$log"
else
  echo "❌ runtipi-cli not found or not executable" >> "$log"
  notify_admin "Runtipi test failed: runtipi-cli not found or not executable."
  exit 1
fi

# Test persistent file sync
if [ -f "$APKG_PKG_DIR/.env" ] && [ -d "/share/Docker/RunTipi" ]; then
  echo "✓ Persistent files present" >> "$log"
else
  echo "❌ Persistent files missing" >> "$log"
  notify_admin "Runtipi test failed: persistent files missing."
  exit 1
fi

# Test log rotation
sh "$APKG_PKG_DIR/CONTROL/helper.sh"
echo "✓ Log rotation script executed" >> "$log"

echo "✅ All tests passed: $(date)" >> "$log"
exit 0
