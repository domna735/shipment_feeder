<%@ page import="java.net.URLEncoder"%>

<% 
    if (cust.grp_id == null) {
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid login credentials");
    return;
    }
%>
<html>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");
%>


<SCRIPT LANGUAGE="javascript" SRC="../js_client/formCheck.js"></SCRIPT>

<body>
	<script src="../js/input_print/toMain.js" type="text/javascript"></script>

</body>

</html>

<%
response.setHeader("Cache-Control", "no-cache, no-store, must-revalidate");
response.setHeader("Pragma", "no-cache");
response.setDateHeader("Expires", 0);
%>

<%
if (session.getAttribute("emailadr") == null) {
    response.sendRedirect("toLogin.html");
    return;
}
%>
