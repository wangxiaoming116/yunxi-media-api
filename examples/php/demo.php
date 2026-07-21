<?php
/**
 * 云析 API - PHP 调用示例
 * 平台: https://syapi.chuangye.site/
 * 文档: https://syapi.chuangye.site/home/doc
 *
 * 用法: php demo.php "分享链接"
 * 环境变量: YUNXI_UID / YUNXI_KEY / YUNXI_TYPE / YUNXI_API_BASE
 */

$apiBase = getenv('YUNXI_API_BASE') ?: 'https://syapi.chuangye.site/home/api';
$uid = getenv('YUNXI_UID') ?: 'YOUR_UID';
$key = getenv('YUNXI_KEY') ?: 'YOUR_KEY';
$type = getenv('YUNXI_TYPE') ?: 'dsp';
$shareUrl = $argv[1] ?? 'https://www.douyin.com/video/xxxxxxxx';

if ($uid === 'YOUR_UID' || $key === 'YOUR_KEY') {
    fwrite(STDERR, "请设置 YUNXI_UID / YUNXI_KEY\n注册: https://syapi.chuangye.site/user/login/register\n");
    exit(1);
}

$query = http_build_query([
    'type' => $type,
    'uid'  => $uid,
    'key'  => $key,
    'url'  => $shareUrl,
]);

$ch = curl_init($apiBase . '?' . $query);
curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_TIMEOUT => 30,
    CURLOPT_HTTPHEADER => ['User-Agent: yunxi-api-demo/1.0'],
]);
$body = curl_exec($ch);
if ($body === false) {
    fwrite(STDERR, '请求失败: ' . curl_error($ch) . PHP_EOL);
    exit(1);
}
curl_close($ch);

$data = json_decode($body, true);
echo json_encode($data, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT) . PHP_EOL;

$code = (string)($data['code'] ?? '');
if ($code === '0001' || $code === '200') {
    echo PHP_EOL . '解析成功。' . PHP_EOL;
} else {
    echo PHP_EOL . '未成功: code=' . $code . ', msg=' . ($data['msg'] ?? '') . PHP_EOL;
}
