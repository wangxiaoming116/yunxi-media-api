# Python / Node.js 调用短视频去水印 API 完整示例（含 SDK）

> **导语**  
> 本文给出云析短视频解析接口的 Python、Node.js 完整调用示例，以及可本地 `pip install -e` / `require` 的轻量 SDK。适合想把「去水印」接到后端服务、脚本任务或内部中台的同学。

---

## 环境准备

1. 注册并获取 UID/KEY：https://syapi.chuangye.site/user/login/register  
2. 文档：https://syapi.chuangye.site/home/doc  
3. 示例仓库：  
   - https://gitee.com/wzzdq8/yunxi-media-api  
   - https://github.com/wangxiaoming116/yunxi-media-api  

```bash
export YUNXI_UID=YOUR_UID
export YUNXI_KEY=YOUR_KEY
```

PowerShell：

```powershell
$env:YUNXI_UID="YOUR_UID"
$env:YUNXI_KEY="YOUR_KEY"
```

接口地址：`https://syapi.chuangye.site/home/api`  
产品编码示例：`dsp`

---

## Python：标准库即可跑

仓库文件：`examples/python/demo.py`

```python
import json, os, sys
from urllib.parse import urlencode
from urllib.request import Request, urlopen

API_BASE = os.getenv("YUNXI_API_BASE", "https://syapi.chuangye.site/home/api")
UID = os.getenv("YUNXI_UID", "YOUR_UID")
KEY = os.getenv("YUNXI_KEY", "YOUR_KEY")

def parse_media(share_url: str) -> dict:
    qs = urlencode({"type": "dsp", "uid": UID, "key": KEY, "url": share_url})
    req = Request(f"{API_BASE}?{qs}", headers={"User-Agent": "yunxi-demo/1.0"})
    with urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode("utf-8"))

if __name__ == "__main__":
    url = sys.argv[1] if len(sys.argv) > 1 else "https://www.douyin.com/video/xxxxxxxx"
    data = parse_media(url)
    print(json.dumps(data, ensure_ascii=False, indent=2))
```

运行：

```bash
python examples/python/demo.py "分享链接"
```

### Python SDK（可选）

```bash
cd sdk/python
pip install -e .
```

```python
from yunxi_api import YunxiClient

client = YunxiClient()  # 读取环境变量 YUNXI_UID / YUNXI_KEY
data = client.parse_ok("分享链接")
print(data.get("playAddr") or data.get("pics"))
```

`parse_ok` 会在 `code` 非 `0001/200` 时抛错，方便写业务逻辑。

---

## Node.js 18+：原生 fetch

仓库文件：`examples/nodejs/demo.js`

```javascript
const API_BASE = process.env.YUNXI_API_BASE || 'https://syapi.chuangye.site/home/api';
const UID = process.env.YUNXI_UID || 'YOUR_UID';
const KEY = process.env.YUNXI_KEY || 'YOUR_KEY';

async function parseMedia(shareUrl) {
  const qs = new URLSearchParams({
    type: 'dsp',
    uid: UID,
    key: KEY,
    url: shareUrl,
  });
  const res = await fetch(`${API_BASE}?${qs}`);
  if (!res.ok) throw new Error(`HTTP ${res.status}`);
  return res.json();
}

const shareUrl = process.argv[2] || 'https://www.douyin.com/video/xxxxxxxx';
parseMedia(shareUrl).then((data) => console.log(JSON.stringify(data, null, 2)));
```

运行：

```bash
node examples/nodejs/demo.js "分享链接"
```

### Node SDK（可选）

```javascript
const { YunxiClient } = require('./sdk/nodejs');

(async () => {
  const client = new YunxiClient();
  const data = await client.parseOk(process.argv[2]);
  console.log(data.playAddr || data.pics);
})();
```

---

## 结果处理建议

```text
成功 code ∈ {0001, 200}
  ├─ playAddr → 视频
  └─ pics     → 图集数组
失败 → 读 msg，一般不扣点（以控制台规则为准）
```

生产环境补充：

- 超时 15～30s  
- 有限次重试（注意别把失败重试打成费用；失败通常不扣点，但仍要控 QPS）  
- 日志里打请求 id / 分享域，**不要**打完整 KEY  

---

## PHP / Java / curl

同仓库 `examples/` 目录还有：

- `examples/php/demo.php`  
- `examples/java/Demo.java`  
- `examples/curl/demo.sh`  

一套参数，多语言复用，减少团队协作成本。

---

## 总结

把「平台解析」交给云析，你的服务只做鉴权转发与业务封装，迭代会快很多。

- 官网：https://syapi.chuangye.site/  
- 注册：https://syapi.chuangye.site/user/login/register  
- 示例：https://gitee.com/wzzdq8/yunxi-media-api  

如果希望下一篇写 Spring Boot / NestJS 封装，评论区扣 1。

---

**标签建议：** Python, Node.js, API, 去水印, SDK, 短视频
