# 微信小程序做去水印：为什么 KEY 不能放前端 + 后端转发示例

> **导语**  
> 很多同学做「去水印小程序」时，会把解析接口的 `uid/key` 直接写进小程序代码。这非常危险：包体可被解包，密钥泄漏后点数会被刷光。本文说明正确架构，并给出一个最小的后端转发示例（Node / Python 任选其一即可）。

---

## 1. 错误做法 vs 正确做法

### 错误：小程序直连开放 API

```text
用户 → 小程序(内置 KEY) → https://syapi.chuangye.site/home/api
```

风险：

- KEY 泄露  
- 被人刷解析额度  
- 无法做登录鉴权、频控、审计  

### 正确：自有后端持有密钥

```text
用户 → 小程序(登录态) → 你的后端 → 云析 API
```

小程序只传「分享文本/链接」，后端校验用户身份后再调用云析。

云析官网：https://syapi.chuangye.site/  
文档：https://syapi.chuangye.site/home/doc  
注册：https://syapi.chuangye.site/user/login/register  

---

## 2. 小程序端伪代码

```javascript
// 仅示例：把剪贴板内容交给你自己的后端
wx.getClipboardData({
  success: async (res) => {
    const shareText = res.data;
    const r = await wx.request({
      url: 'https://your-api.com/parse',
      method: 'POST',
      header: { Authorization: 'Bearer ' + wx.getStorageSync('token') },
      data: { text: shareText },
    });
    // 根据 r.data 展示视频或图片
  },
});
```

注意：

- 请求域名需在小程序后台配置 request 合法域名（你的后端域名）  
- **不要**把 `syapi.chuangye.site` 和 KEY 配进小程序  

---

## 3. 后端转发示例（Node.js）

```javascript
// server.js 示意
const express = require('express');
const app = express();
app.use(express.json());

const API = 'https://syapi.chuangye.site/home/api';
const UID = process.env.YUNXI_UID; // 服务器环境变量
const KEY = process.env.YUNXI_KEY;

function extractUrl(text = '') {
  const m = String(text).match(/https?:\/\/[^\s]+/i);
  return m ? m[0] : '';
}

app.post('/parse', async (req, res) => {
  // TODO: 校验登录态、每日次数、敏感词等
  const url = extractUrl(req.body.text || req.body.url || '');
  if (!url) return res.status(400).json({ msg: '未识别到链接' });

  const qs = new URLSearchParams({ type: 'dsp', uid: UID, key: KEY, url });
  const upstream = await fetch(`${API}?${qs}`);
  const data = await upstream.json();
  // 可只把前端需要的字段返回，避免透传多余信息
  res.json(data);
});

app.listen(3000);
```

---

## 4. 后端转发示例（Python Flask）

```python
import os, re, json
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from flask import Flask, request, jsonify

app = Flask(__name__)
API = "https://syapi.chuangye.site/home/api"
UID = os.environ["YUNXI_UID"]
KEY = os.environ["YUNXI_KEY"]

def extract_url(text: str) -> str:
    m = re.search(r"https?://\S+", text or "")
    return m.group(0) if m else ""

@app.post("/parse")
def parse():
    # TODO: 登录校验 / 限流
    body = request.get_json(force=True, silent=True) or {}
    url = extract_url(body.get("text") or body.get("url") or "")
    if not url:
        return jsonify({"msg": "未识别到链接"}), 400
    qs = urlencode({"type": "dsp", "uid": UID, "key": KEY, "url": url})
    req = Request(f"{API}?{qs}", headers={"User-Agent": "mp-backend/1.0"})
    with urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return jsonify(data)
```

---

## 5. 小程序侧还要注意什么

1. **保存到相册**：需用户授权；注意 iOS/安卓差异  
2. **域名与 https**：正式环境必须 https  
3. **内容合规**：工具类目、用户协议、敏感内容处理  
4. **体验**：解析中加 loading；失败提示「链接无效或暂不支持」  
5. **计费**：云析侧常见「成功扣点失败不扣」；你还可以按会员次数做二次计费  

完整多语言示例与 SDK：  
https://gitee.com/wzzdq8/yunxi-media-api  

---

## 6. 架构小结

| 层级 | 职责 |
|------|------|
| 小程序 | UI、剪贴板、展示结果、登录 |
| 你的后端 | 鉴权、限流、持有 KEY、调用云析 |
| 云析 API | 多平台解析、计费、稳定性 |

这样即使小程序被逆向，也拿不到你的开放平台密钥。

---

## 下一步

1. 注册云析账号并充值测试点：https://syapi.chuangye.site/  
2. 用文档中心在线调试先跑通一条链接  
3. 把转发接口接到小程序  

需要「Java Spring Boot 转发版」或「PHP ThinkPHP 转发版」可以评论区留言，我按需补文。

---

**标签建议：** 微信小程序, 去水印, API, 后端, 安全, Node.js, Python
