#!/bin/sh
# ============================================================================
# CLEANUP-DOCKER.SH - Clean unused Docker resources
# ============================================================================
set -eu

echo "🧹 Docker cleanup started"

echo ""
echo "Removing unused images..."
docker image prune -af 2>/dev/null && echo "✅ Images cleaned" || echo "⚠️  Failed"

echo ""
echo "Removing unused volumes..."
docker volume prune -f 2>/dev/null && echo "✅ Volumes cleaned" || echo "⚠️  Failed"

echo ""
echo "Removing unused networks..."
docker network prune -f 2>/dev/null && echo "✅ Networks cleaned" || echo "⚠️  Failed"

echo ""
echo "🎉 Cleanup complete"
exit 0
