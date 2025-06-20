<HTML>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");
%>

if (session.getAttribute("emailadr") == null) {
    response.sendRedirect("../toLogin.html");
    return;
}

<head>
<title>DHL Shipment Information Feeder</title>
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>

<SCRIPT LANGUAGE="javascript" SRC="js_client/formCheck.js"></SCRIPT>
<script src="js/logout.js" type="text/javascript"></script>

<%

File sessionFile = new File("/tmp/sessions/" + session.getId());
if (sessionFile.exists()) sessionFile.delete();

// Invalidate the session to securely log out the user
session.invalidate();
// Optionally, redirect to login page after logout
response.sendRedirect("toLogin.html");
return;
%>


<body><script src="js/logout.js" type="text/javascript"></script></body>

</HTML>
