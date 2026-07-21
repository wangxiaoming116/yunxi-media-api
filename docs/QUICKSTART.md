# 5 分钟快速接入

## 1. 注册并获取密钥

1. 打开 [云析 API](https://syapi.chuangye.site/)  
2. [免费注册](https://syapi.chuangye.site/user/login/register)  
3. 登录控制台 → **个人信息**，复制 `UID` 与 `KEY`

> 成功解析才扣点，失败不扣。可在控制台购买套餐充值。

## 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 YOUR_UID / YOUR_KEY
export YUNXI_UID=你的UID
export YUNXI_KEY=你的KEY
```

Windows PowerShell:

```powershell
$env:YUNXI_UID="你的UID"
$env:YUNXI_KEY="你的KEY"
```

## 3. 发起一次解析

### curl

```bash
curl -G "https://syapi.chuangye.site/home/api" \
  --data-urlencode "type=dsp" \
  --data-urlencode "uid=$YUNXI_UID" \
  --data-urlencode "key=$YUNXI_KEY" \
  --data-urlencode "url=这里粘贴分享链接"
```

### Python

```bash
python examples/python/demo.py "分享链接"
```

### Node.js (18+)

```bash
node examples/nodejs/demo.js "分享链接"
```

## 4. 判断成功

常见成功码：`code=0001` 或 `code=200`。  
资源字段可能为 `playAddr`（视频）、`pics`（图集）等，**以实际 JSON 为准**。

完整说明：https://syapi.chuangye.site/home/doc
