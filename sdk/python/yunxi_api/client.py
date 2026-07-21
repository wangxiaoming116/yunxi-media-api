from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen


class YunxiError(Exception):
    """API 或网络异常。"""

    def __init__(self, message: str, *, code: Optional[str] = None, payload: Any = None):
        super().__init__(message)
        self.code = code
        self.payload = payload


class YunxiClient:
    """
    云析多媒体解析 API 轻量客户端。

    仅封装公开 HTTP 调用，不包含任何服务端解析逻辑。
    文档: https://syapi.chuangye.site/home/doc
    """

    def __init__(
        self,
        uid: Optional[str] = None,
        key: Optional[str] = None,
        *,
        base_url: Optional[str] = None,
        product_type: str = "dsp",
        timeout: int = 30,
    ) -> None:
        self.uid = uid or os.getenv("YUNXI_UID", "")
        self.key = key or os.getenv("YUNXI_KEY", "")
        self.base_url = (base_url or os.getenv("YUNXI_API_BASE") or "https://syapi.chuangye.site/home/api").rstrip(
            "?"
        )
        self.product_type = product_type or os.getenv("YUNXI_TYPE", "dsp")
        self.timeout = timeout

        if not self.uid or not self.key or self.uid == "YOUR_UID" or self.key == "YOUR_KEY":
            raise YunxiError(
                "缺少 UID/KEY。请在控制台获取后传入，或设置环境变量 YUNXI_UID / YUNXI_KEY。"
                " 注册: https://syapi.chuangye.site/user/login/register"
            )

    def parse(self, share_url: str, **extra: Any) -> Dict[str, Any]:
        """解析分享链接，返回接口 JSON。"""
        params: Dict[str, Any] = {
            "type": self.product_type,
            "uid": self.uid,
            "key": self.key,
            "url": share_url,
        }
        params.update(extra)
        query = urlencode(params)
        req = Request(
            f"{self.base_url}?{query}",
            headers={"User-Agent": "yunxi-api-sdk/1.0.0"},
        )
        try:
            with urlopen(req, timeout=self.timeout) as resp:
                raw = resp.read().decode("utf-8")
        except HTTPError as e:
            raise YunxiError(f"HTTP {e.code}", code=str(e.code)) from e
        except URLError as e:
            raise YunxiError(f"网络错误: {e.reason}") from e

        try:
            data = json.loads(raw)
        except json.JSONDecodeError as e:
            raise YunxiError("响应不是合法 JSON", payload=raw) from e
        return data

    def parse_ok(self, share_url: str, **extra: Any) -> Dict[str, Any]:
        """解析并校验成功码（0001 / 200），失败则抛 YunxiError。"""
        data = self.parse(share_url, **extra)
        code = str(data.get("code", ""))
        if code not in ("0001", "200"):
            raise YunxiError(str(data.get("msg") or "解析失败"), code=code, payload=data)
        return data
