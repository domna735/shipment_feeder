<%@ page import="com.hkapps.util.*"%>
<%@ page import="hkapps.shipment_feeder.*"%>
<%@ page import="java.net.URLEncoder"%>

<html>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");
%>

<head><title></title></head>

<script src="../js_client/rollovers.js" type="text/javascript"></script>
<script src="../js_client/formCheck.js" type="text/javascript"></script>

<%
Common common = new Common();

if (session.getAttribute("emailadr") == null) {
    response.sendRedirect("toLogin.html");
    return;
}

Shipment_feeder sf = new Shipment_feeder();

String menu_lst = sf.getCustMenu(session.getAttribute("grp_id").toString());
String df_menu = sf.getDefaultMenu(session.getAttribute("grp_id").toString());

//get accessible menu items

out.println("<script type=\"text/javascript\" src=\"../js/feed_print2/fp_menu.js\" menu_lst=\"" + menu_lst + "\" df_menu=\"" + df_menu + "\"></script>");

%>

</html>
