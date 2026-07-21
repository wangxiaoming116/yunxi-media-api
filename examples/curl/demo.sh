#!/usr/bin/env bash
# 云析 API - curl 快速调用示例
# 文档: https://syapi.chuangye.site/home/doc
# 注册获取 UID/KEY: https://syapi.chuangye.site/user/login/register

set -euo pipefail

API_BASE="${YUNXI_API_BASE:-https://syapi.chuangye.site/home/api}"
UID="${YUNXI_UID:-YOUR_UID}"
KEY="${YUNXI_KEY:-YOUR_KEY}"
TYPE="${YUNXI_TYPE:-dsp}"

# 替换为任意支持平台的分享链接（抖音 / 快手 / 小红书 / 微博 / 皮皮虾 / 视频号 / 豆包 / 即梦 等）
SHARE_URL="${1:-https://www.douyin.com/video/xxxxxxxx}"

if [[ "$UID" == "YOUR_UID" || "$KEY" == "YOUR_KEY" ]]; then
  echo "请先设置环境变量 YUNXI_UID / YUNXI_KEY，或复制 .env.example 为 .env 后填写。"
  echo "注册地址: https://syapi.chuangye.site/user/login/register"
  exit 1
fi

ENCODED_URL="$(python -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1], safe=''))" "$SHARE_URL" 2>/dev/null \
  || node -e "console.log(encodeURIComponent(process.argv[1]))" "$SHARE_URL")"

curl -sS -G "$API_BASE" \
  --data-urlencode "type=${TYPE}" \
  --data-urlencode "uid=${UID}" \
  --data-urlencode "key=${KEY}" \
  --data-urlencode "url=${SHARE_URL}" \
  | python -m json.tool 2>/dev/null || cat

echo
