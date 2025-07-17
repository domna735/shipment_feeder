<html>

<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");
%>

<head><title></title>
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
</head>

<script src="../js_client/rollovers.js" type="text/javascript"></script>


<%
if (session.getAttribute("emailadr") == null) {
    response.sendRedirect("../toLogin.html");
    return;
}

out.println("<script language=\"JavaScript\" type=\"text/javascript\" src=\"../js/feed_print2/fp_Top.js\" head=\"Change Password\" logo=\"" + session.getAttribute("logo_filename") + "\" cname=\"" + session.getAttribute("contact_name") + "\"></script>");

%>

</html>
