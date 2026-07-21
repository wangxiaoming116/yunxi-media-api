#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
云析 API - Python 调用示例
平台: https://syapi.chuangye.site/
文档: https://syapi.chuangye.site/home/doc

支持: 抖音 / 快手 / 小红书 / 微博 / 皮皮虾 / 视频号 / 豆包 / 即梦 / 实况 等短视频与图集解析。
请勿将真实 KEY 写入代码仓库。
"""

from __future__ import annotations

import json
import os
import sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = os.getenv("YUNXI_API_BASE", "https://syapi.chuangye.site/home/api")
UID = os.getenv("YUNXI_UID", "YOUR_UID")
KEY = os.getenv("YUNXI_KEY", "YOUR_KEY")
PRODUCT_TYPE = os.getenv("YUNXI_TYPE", "dsp")


def parse_media(share_url: str, *, uid: str = UID, key: str = KEY, product_type: str = PRODUCT_TYPE) -> dict:
    """调用去水印 / 多媒体解析接口，返回 JSON 字典。"""
    if uid == "YOUR_UID" or key == "YOUR_KEY":
        raise SystemExit(
            "请设置环境变量 YUNXI_UID / YUNXI_KEY。\n"
            "免费注册: https://syapi.chuangye.site/user/login/register"
        )

    query = urlencode(
        {
            "type": product_type,
            "uid": uid,
            "key": key,
            "url": share_url,
        }
    )
    req = Request(f"{API_BASE}?{query}", headers={"User-Agent": "yunxi-api-demo/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))


def main() -> None:
    share_url = sys.argv[1] if len(sys.argv) > 1 else "https://www.douyin.com/video/xxxxxxxx"
    data = parse_media(share_url)
    print(json.dumps(data, ensure_ascii=False, indent=2))

    code = str(data.get("code", ""))
    if code in ("0001", "200"):
        print("\n解析成功。常见字段: playAddr / pics / title 等，以实际返回为准。")
    else:
        print(f"\n未成功: code={code}, msg={data.get('msg')}")


if __name__ == "__main__":
    main()
