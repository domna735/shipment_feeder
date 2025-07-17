<%@ page contentType="text/html; charset=UTF-8" pageEncoding="UTF-8" %>
<html>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'self'; upgrade-insecure-requests; block-all-mixed-content");

String[] attrs = {
    "emailadr","grp_id","clientID","param","awb_copy","awb_paper_ty","awb_printer","inv_copy","inv_printer","default_printer",
    "cur_awb_copy","cur_inv_copy","cur_rec_id","ttl_rec","success_rec","fail_rec","fail_rec_id","pagefrom","rec_id_list",
    "cur_index","rec_count","email_tmpl_list","contact_name","logo_filename","default_charset","opt_charset",
    "default_sub_grp_id","opt_sub_grp","sub_grp_id"
};
for(String attr : attrs) session.removeAttribute(attr);

session.invalidate();
response.sendRedirect("toLogin.html");
return;
%>
<head>
<title>DHL Shipment Information Feeder</title>
<meta charset="UTF-8">
</head>
<body></body>
</html>
