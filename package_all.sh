#!/usr/bin/env bash
# 把 skills/ 下每个 skill 打包成 dist/<name>.skill
#
# 依赖 Anthropic skill-creator 的 package_skill.py。
# 默认路径为 Claude 运行环境中的位置；本地/CI 环境请改 PACKAGER 指向你的 skill-creator。
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PACKAGER_DIR="${PACKAGER_DIR:-/mnt/skills/examples/skill-creator}"
OUT="$ROOT/dist"

mkdir -p "$OUT"

for skill in "$ROOT"/skills/*/; do
  name="$(basename "$skill")"
  echo "📦 打包 $name ..."
  ( cd "$PACKAGER_DIR" && python -m scripts.package_skill "$skill" "$OUT" )
done

echo "✅ 全部完成，产物在 $OUT/"
ls -la "$OUT"
