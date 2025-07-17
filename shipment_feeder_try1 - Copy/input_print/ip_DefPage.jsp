<%@ page import="java.net.URLEncoder"%>

<html>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'self'; upgrade-insecure-requests; block-all-mixed-content");
%>

<head>
<title>DHL Shipment Information Feeder</title>
</head>

<frameset cols=187,* frameborder=0 framespacing=0 frameborder=0>

<%
Common common = new Common();
if (session.getAttribute("emailadr") == null) {
    response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "../toLogin.html"));
    if(true){return;}
}

out.println("<frame src=\"ip_menu.jsp\" name=menu marginheight=0 marginwidth=0 scrolling=no>");
out.println("<frameset rows=130,* frameborder=0 framespacing=0 border=0>");
out.println("<frame src=\"ip_Top.jsp\" scrolling=off marginheight=0 marginwidth=0 name=\"head\">");
out.println("<frame src=\"main.jsp\" scrolling=auto name=\"main\">");

%>
	
</frameset>

</frameset>



</html>
