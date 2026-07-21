import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.nio.charset.StandardCharsets;

/**
 * 云析 API - Java 调用示例
 * 平台: https://syapi.chuangye.site/
 * 文档: https://syapi.chuangye.site/home/doc
 *
 * 运行前请设置环境变量 YUNXI_UID / YUNXI_KEY（切勿把真实密钥写进源码）。
 */
public class Demo {
    public static void main(String[] args) throws Exception {
        String apiBase = env("YUNXI_API_BASE", "https://syapi.chuangye.site/home/api");
        String uid = env("YUNXI_UID", "YOUR_UID");
        String key = env("YUNXI_KEY", "YOUR_KEY");
        String type = env("YUNXI_TYPE", "dsp");
        String shareUrl = args.length > 0 ? args[0] : "https://www.douyin.com/video/xxxxxxxx";

        if ("YOUR_UID".equals(uid) || "YOUR_KEY".equals(key)) {
            System.err.println("请设置环境变量 YUNXI_UID / YUNXI_KEY");
            System.err.println("注册: https://syapi.chuangye.site/user/login/register");
            System.exit(1);
        }

        String qs = "type=" + enc(type)
                + "&uid=" + enc(uid)
                + "&key=" + enc(key)
                + "&url=" + enc(shareUrl);

        HttpURLConnection conn = (HttpURLConnection) new URL(apiBase + "?" + qs).openConnection();
        conn.setRequestMethod("GET");
        conn.setConnectTimeout(15000);
        conn.setReadTimeout(30000);
        conn.setRequestProperty("User-Agent", "yunxi-api-demo/1.0");

        StringBuilder sb = new StringBuilder();
        try (BufferedReader br = new BufferedReader(
                new InputStreamReader(conn.getInputStream(), StandardCharsets.UTF_8))) {
            String line;
            while ((line = br.readLine()) != null) {
                sb.append(line);
            }
        }
        System.out.println(sb);
    }

    private static String env(String name, String def) {
        String v = System.getenv(name);
        return v == null || v.isEmpty() ? def : v;
    }

    private static String enc(String s) {
        return URLEncoder.encode(s, StandardCharsets.UTF_8);
    }
}
