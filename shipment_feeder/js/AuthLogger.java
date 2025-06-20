package hkapps.shipment_feeder;

import java.io.FileWriter;
import java.io.IOException;
import java.time.LocalDateTime;

public class AuthLogger {

    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
    throws IOException, ServletException {
    HttpServletRequest request = (HttpServletRequest) req;
    HttpServletResponse response = (HttpServletResponse) res;

    // Set CSP header
    response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");

    // ... your existing session checks ...

    chain.doFilter(req, res);
    }
    
    private static final String LOG_FILE = "/tmp/auth_attempts.log"; // Change path as needed

    public static void logUnauthorized(String username, String uri, String reason) {
        try (FileWriter fw = new FileWriter(LOG_FILE, true)) {
            fw.write(LocalDateTime.now() + " | User: " + username + " | URI: " + uri + " | Reason: " + reason + "\n");
        } catch (IOException e) {
            // Optionally handle logging failure
        }
    }
}
