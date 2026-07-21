# Yunxi Media Parse API Demo

Open-source **call examples & lightweight SDKs** for [Yunxi API](https://syapi.chuangye.site/) — short video / album / live-photo parsing across 80+ platforms (Douyin, Kuaishou, Xiaohongshu, Weibo, Pipixia, Channels, Doubao, Jimeng, and more).

> This repository only contains **HTTP client samples**. It does **not** include any server-side parsing logic or real API keys.

## Get credentials

1. Register: https://syapi.chuangye.site/user/login/register  
2. Copy `UID` / `KEY` from the console  
3. Docs: https://syapi.chuangye.site/home/doc  

## Quick call

```bash
export YUNXI_UID=YOUR_UID
export YUNXI_KEY=YOUR_KEY
curl -G "https://syapi.chuangye.site/home/api" \
  --data-urlencode "type=dsp" \
  --data-urlencode "uid=$YUNXI_UID" \
  --data-urlencode "key=$YUNXI_KEY" \
  --data-urlencode "url=SHARE_LINK"
```

See the Chinese [README.md](./README.md) for full platform list, billing notes, and multi-language examples.
