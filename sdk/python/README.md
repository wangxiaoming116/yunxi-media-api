# Yunxi API Python SDK

轻量 HTTP 封装，不含任何服务端解析实现。

```bash
cd sdk/python
pip install -e .
```

```python
import os
from yunxi_api import YunxiClient

os.environ["YUNXI_UID"] = "YOUR_UID"
os.environ["YUNXI_KEY"] = "YOUR_KEY"

client = YunxiClient()
data = client.parse_ok("https://www.douyin.com/video/xxxxxxxx")
print(data.get("playAddr") or data.get("pics"))
```

完整文档与充值: https://syapi.chuangye.site/
