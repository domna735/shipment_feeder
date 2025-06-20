package hkapps.shipment_feeder;

import javax.servlet.*;
import javax.servlet.annotation.WebFilter;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import javax.servlet.http.HttpSession;
import java.io.IOException;



@WebFilter("/input_print/*") // Adjust this path to match protected resources


public class AuthFilter implements Filter {
    public void doFilter(ServletRequest req, ServletResponse res, FilterChain chain)
            throws IOException, ServletException {
        HttpServletRequest request = (HttpServletRequest) req;
        HttpServletResponse response = (HttpServletResponse) res;
        HttpSession session = request.getSession(false);

        response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");

        String uri = request.getRequestURI();
        String role = (session != null) ? (String) session.getAttribute("role") : null;
        String username = (session != null) ? (String) session.getAttribute("emailadr") : null;
        boolean isLoggedIn = (role != null && username != null);
        boolean isLoginPage = uri.endsWith("toLogin.html") || uri.endsWith("login_validate.jsp");

        // Example: Only admin can access /admin/*
        if (uri.contains("/admin/") && (!isLoggedIn || !"admin".equals(role))) {
            AuthLogger.logUnauthorized(username, uri, "Admin access required");
            response.sendRedirect(request.getContextPath() + "/toLogin.html");
            return;
        }
        // General authentication check
        if (!isLoggedIn && !isLoginPage) {
            AuthLogger.logUnauthorized(username, uri, "Not logged in");
            response.sendRedirect(request.getContextPath() + "/toLogin.html");
            return;
        }
        Boolean isAuthenticated = (Boolean) session.getAttribute("authenticated");
        if (isAuthenticated == null || !isAuthenticated) {
            response.sendRedirect("toLogin.html");
            return;
        }

        chain.doFilter(req, res);
    }
}
