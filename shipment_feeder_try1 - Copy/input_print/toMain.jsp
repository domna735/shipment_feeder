<%@ page import="java.net.URLEncoder"%>
<%
if (session.getAttribute("emailadr") == null) {
    response.sendRedirect("toLogin.html");
    return;
}
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'self'; upgrade-insecure-requests; block-all-mixed-content");
response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
response.setHeader("Pragma", "no-cache");
response.setDateHeader("Expires", 0);
%>
<html>
<head></head>
<SCRIPT LANGUAGE="javascript" SRC="../js_client/formCheck.js"></SCRIPT>
<body>
<script src="../js/input_print/toMain.js" type="text/javascript"></script>
</body>
</html>
