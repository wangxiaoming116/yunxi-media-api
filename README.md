# 云析 API 调用示例 · 短视频 / 图集 / 实况去水印解析

[![官网](https://img.shields.io/badge/官网-syapi.chuangye.site-2563eb)](https://syapi.chuangye.site/)
[![文档](https://img.shields.io/badge/文档中心-立即查看-0ea5e9)](https://syapi.chuangye.site/home/doc)
[![注册](https://img.shields.io/badge/免费注册-获取_UID%2FKEY-16a34a)](https://syapi.chuangye.site/user/login/register)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

> **本仓库是什么？**  
> 面向开发者的 **公开调用示例 + 轻量 SDK 封装**，帮助你在几分钟内接入 [云析 API](https://syapi.chuangye.site/) 的多媒体解析能力。  
> **本仓库不是什么？**  
> 不包含服务端解析源码、不包含真实密钥、不逆向任何第三方 App。解析能力由云析开放平台提供。

**English:** [README.en.md](./README.en.md)

---

## 为什么选择云析 API？

| 能力 | 说明 |
|------|------|
| 覆盖广 | 支持 **80+** 主流平台短视频 / 图集 / 实况等解析场景 |
| 好接入 | 标准 HTTP GET，Python / Node / PHP / Java / curl 均可 |
| 稳 | 面向生产环境，文档与在线调试齐全 |
| 计费清晰 | **成功扣点、失败不扣**；控制台可充值套餐 |

**官网首页：** https://syapi.chuangye.site/  
**接口文档：** https://syapi.chuangye.site/home/doc  
**免费注册：** https://syapi.chuangye.site/user/login/register  

---

## 支持方向（常用关键词）

适合做：去水印工具、素材采集、内容审核辅助、小程序/APP 后端聚合等。

- **短视频去水印**：抖音、快手、小红书、微博、皮皮虾、视频号、B 站 …
- **图集解析**：图文作品批量取无水印图
- **实况 / Live**：实况相关解析场景
- **AI 创作平台分享链**：豆包、即梦 等（以文档与实际上线能力为准）

完整清单见：[docs/PLATFORMS.md](./docs/PLATFORMS.md)  
**以官网文档为准，平台规则变化时服务端会持续适配。**

---

## 30 秒看懂接口

**网关地址**

```text
https://syapi.chuangye.site/home/api
```

**常用产品编码**

| type | 说明 |
|------|------|
| `dsp` | 短视频 / 图集 / 实况解析（本仓库默认示例） |

**请求参数**

| 参数 | 必填 | 说明 |
|------|------|------|
| `type` | 是 | 产品编码，如 `dsp` |
| `uid` | 是 | 控制台用户 UID |
| `key` | 是 | 控制台接口密钥（**勿提交到 Git**） |
| `url` | 是 | 待解析的分享链接 |

**成功码（常见）**：`code=0001` 或 `code=200`  
**资源字段（常见）**：`playAddr`（视频）、`pics`（图集）、`title` 等 —— **以实际 JSON 为准**。

---

## 快速开始

详细步骤：[docs/QUICKSTART.md](./docs/QUICKSTART.md)

### 1）注册拿密钥

打开 [免费注册](https://syapi.chuangye.site/user/login/register) → 登录控制台 → 个人信息复制 `UID` / `KEY`。

### 2）配置环境变量（推荐）

```bash
cp .env.example .env
export YUNXI_UID=你的UID
export YUNXI_KEY=你的KEY
```

### 3）发起调用

**curl**

```bash
curl -G "https://syapi.chuangye.site/home/api" \
  --data-urlencode "type=dsp" \
  --data-urlencode "uid=$YUNXI_UID" \
  --data-urlencode "key=$YUNXI_KEY" \
  --data-urlencode "url=这里粘贴抖音/快手/小红书等分享链接"
```

**Python**

```bash
python examples/python/demo.py "分享链接"
```

**Node.js 18+**

```bash
node examples/nodejs/demo.js "分享链接"
```

**PHP**

```bash
php examples/php/demo.php "分享链接"
```

**Java**

```bash
# 先设置环境变量 YUNXI_UID / YUNXI_KEY
javac examples/java/Demo.java && java -cp examples/java Demo "分享链接"
```

更多示例目录：

```text
examples/
  curl/demo.sh
  python/demo.py
  nodejs/demo.js
  php/demo.php
  java/Demo.java
```

---

## 轻量 SDK（可选）

仅封装 HTTP，**零服务端逻辑**。

### Python

```bash
cd sdk/python && pip install -e .
```

```python
from yunxi_api import YunxiClient

client = YunxiClient(uid="YOUR_UID", key="YOUR_KEY")
data = client.parse_ok("https://www.douyin.com/video/xxxxxxxx")
print(data.get("playAddr") or data.get("pics"))
```

### Node.js

```bash
cd sdk/nodejs
node -e "const {YunxiClient}=require('./'); (async()=>{ const c=new YunxiClient({uid:process.env.YUNXI_UID,key:process.env.YUNXI_KEY}); console.log(await c.parseOk(process.argv[1])); })()" "分享链接"
```

---

## 返回示例（结构示意）

> 以下为示意，字段名以你账号实际返回为准。

```json
{
  "code": "0001",
  "msg": "解析成功",
  "title": "作品标题",
  "playAddr": "https://example.com/video.mp4",
  "pics": []
}
```

在线调试（登录后自动填密钥）：  
进入 [文档中心](https://syapi.chuangye.site/home/doc) → 选择产品 → 在线调试。

---

## 计费说明（摘要）

- 默认按次计费（`dsp` 常见为成功扣点）  
- **解析成功扣点，失败不扣点**  
- 支持包点 / 包月等套餐，登录控制台充值购买  

套餐与价格以官网控制台为准：https://syapi.chuangye.site/

---

## 安全须知（必读）

1. **永远不要**把真实 `KEY` 写进前端页面或公开仓库  
2. 推荐服务端持有密钥，前端只传业务参数  
3. 可在控制台定期「更换秘钥」  
4. 本仓库示例一律使用 `YOUR_UID` / `YOUR_KEY` 占位符  

---

## 仓库结构

```text
├── README.md                 # 本说明（引流 / 接入文档）
├── README.en.md
├── LICENSE
├── .env.example              # 环境变量模板（无真实密钥）
├── docs/
│   ├── QUICKSTART.md         # 5 分钟接入
│   └── PLATFORMS.md          # 平台方向说明
├── examples/                 # 多语言最小可运行示例
└── sdk/                      # Python / Node 轻量客户端
```

---

## 常见问题

**Q: 和本仓库同名的“去水印源码站”有什么区别？**  
A: 本仓库只教你 **如何调用云析开放接口**。解析算法与适配维护在云析服务端，你无需自建爬虫集群。

**Q: 小程序能直接调吗？**  
A: 不建议把 KEY 放在小程序端。请走你自己的后端转发，或按控制台安全建议配置。

**Q: 某平台偶发失败？**  
A: 平台页面结构会变更。失败通常不扣点；可换链接重试，或联系官网客服。文档与工单入口见：https://syapi.chuangye.site/

**Q: 如何联系 / 商务合作？**  
A: 官网「联系我们」：https://syapi.chuangye.site/

---


## Star & 反馈

如果本示例帮你快速跑通接口，欢迎 Star。  
问题与需求优先走官网文档与客服通道，便于同步到正式产品线。

**立即开始：** [https://syapi.chuangye.site/](https://syapi.chuangye.site/)
