/**
 * 云析 API - Node.js 调用示例
 * 平台: https://syapi.chuangye.site/
 * 文档: https://syapi.chuangye.site/home/doc
 *
 * 支持抖音、快手、小红书、微博、皮皮虾、视频号、豆包、即梦、实况等。
 * 请勿把真实 KEY 提交到 Git。
 */

const API_BASE = process.env.YUNXI_API_BASE || 'https://syapi.chuangye.site/home/api';
const UID = process.env.YUNXI_UID || 'YOUR_UID';
const KEY = process.env.YUNXI_KEY || 'YOUR_KEY';
const TYPE = process.env.YUNXI_TYPE || 'dsp';

async function parseMedia(shareUrl) {
  if (UID === 'YOUR_UID' || KEY === 'YOUR_KEY') {
    throw new Error(
      '请设置环境变量 YUNXI_UID / YUNXI_KEY。注册: https://syapi.chuangye.site/user/login/register'
    );
  }

  const qs = new URLSearchParams({
    type: TYPE,
    uid: UID,
    key: KEY,
    url: shareUrl,
  });

  const res = await fetch(`${API_BASE}?${qs.toString()}`, {
    headers: { 'User-Agent': 'yunxi-api-demo/1.0' },
  });
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}

async function main() {
  const shareUrl = process.argv[2] || 'https://www.douyin.com/video/xxxxxxxx';
  const data = await parseMedia(shareUrl);
  console.log(JSON.stringify(data, null, 2));

  const code = String(data.code ?? '');
  if (code === '0001' || code === '200') {
    console.log('\n解析成功。可读取 playAddr / pics 等字段（以实际返回为准）。');
  } else {
    console.log(`\n未成功: code=${code}, msg=${data.msg || ''}`);
  }
}

main().catch((err) => {
  console.error(err.message || err);
  process.exit(1);
});
