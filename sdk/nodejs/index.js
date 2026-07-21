/**
 * 云析 API Node.js 轻量客户端（仅 HTTP 封装，无服务端逻辑）
 * Docs: https://syapi.chuangye.site/home/doc
 */

class YunxiError extends Error {
  constructor(message, { code, payload } = {}) {
    super(message);
    this.name = 'YunxiError';
    this.code = code;
    this.payload = payload;
  }
}

class YunxiClient {
  constructor(options = {}) {
    this.uid = options.uid || process.env.YUNXI_UID || '';
    this.key = options.key || process.env.YUNXI_KEY || '';
    this.baseUrl = (options.baseUrl || process.env.YUNXI_API_BASE || 'https://syapi.chuangye.site/home/api').replace(
      /\?$/,
      ''
    );
    this.productType = options.productType || process.env.YUNXI_TYPE || 'dsp';
    this.timeoutMs = options.timeoutMs || 30000;

    if (!this.uid || !this.key || this.uid === 'YOUR_UID' || this.key === 'YOUR_KEY') {
      throw new YunxiError(
        '缺少 UID/KEY。注册获取: https://syapi.chuangye.site/user/login/register'
      );
    }
  }

  async parse(shareUrl, extra = {}) {
    const qs = new URLSearchParams({
      type: this.productType,
      uid: this.uid,
      key: this.key,
      url: shareUrl,
      ...extra,
    });

    const controller = new AbortController();
    const timer = setTimeout(() => controller.abort(), this.timeoutMs);
    try {
      const res = await fetch(`${this.baseUrl}?${qs.toString()}`, {
        headers: { 'User-Agent': 'yunxi-api-sdk/1.0.0' },
        signal: controller.signal,
      });
      if (!res.ok) {
        throw new YunxiError(`HTTP ${res.status}`, { code: String(res.status) });
      }
      return await res.json();
    } finally {
      clearTimeout(timer);
    }
  }

  async parseOk(shareUrl, extra = {}) {
    const data = await this.parse(shareUrl, extra);
    const code = String(data.code ?? '');
    if (code !== '0001' && code !== '200') {
      throw new YunxiError(data.msg || '解析失败', { code, payload: data });
    }
    return data;
  }
}

module.exports = { YunxiClient, YunxiError };
