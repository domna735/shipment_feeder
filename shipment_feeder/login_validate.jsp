<%@ page import="hkapps.shipment_feeder.*"%>
<%@ page import="com.hkapps.util.*"%>
<%@ page import="java.net.URLEncoder"%>
<%@ page import="java.util.*"%>
<%@ page import="java.lang.*"%>
<%@ page import="java.net.*"%>

Cookie sessionCookie = new Cookie("SESSIONID", newSession.getId());
sessionCookie.setHttpOnly(true);
sessionCookie.setSecure(true);
sessionCookie.setPath("/");
sessionCookie.setMaxAge(1800);
// Add SameSite manually (Java doesn't support it directly)
response.setHeader("Set-Cookie", sessionCookie.getName() + "=" + sessionCookie.getValue() + "; HttpOnly; Secure; SameSite=Strict; Path=/");



<html>
<%
response.setHeader("Content-Security-Policy", "default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content");
%>

<head>
<title>DHL Shipment Information Feeder</title>
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">

</head>

<body bgcolor=#ffffff><blockquote>
<script type="text/javascript" src="js/back.js"></script>
<form>

<%
String referpage = request.getHeader("referer");

Common common = new Common();
//out.println(referpage);


if (referpage == null) {
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}

if (request.getQueryString() != null) {
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}

URL referurl = new URL(referpage);
//if (!(referpage.substring(referpage.length()-26,referpage.length()).equals("shipment_feeder/login.html"))) {
if (!referurl.getPath().equals("/shipment_feeder/login.html") && !referurl.getPath().equals("/shipment_feeder/login_ip.html")) {
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}

if (referurl.getPath().equals("/shipment_feeder/login.html")) {
	
	if ((request.getParameter("emailadr") == null) || (request.getParameter("emailadr").equals("")) || 
		(request.getParameter("passwd") == null) || (request.getParameter("passwd").equals(""))) {
	   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
	   if(true){return;}
	}

	DataTypeUtil dtu = new DataTypeUtil();

	if ((!dtu.isValidEmail(request.getParameter("emailadr"),50)) || (!dtu.isValidPassword(request.getParameter("passwd"),6,16))) {
	   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
	   if(true){return;}
	}

}

if (referurl.getPath().equals("/shipment_feeder/login_ip.html")) {
	
	if ((request.getParameter("emailadr") == null) || (request.getParameter("emailadr").equals("")) || 
		(request.getParameter("passwd") == null) || (!request.getParameter("passwd").equals(""))) {
	   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
	   if(true){return;}
	}

	DataTypeUtil dtu = new DataTypeUtil();

	if ((!dtu.isAlphaNumeric(request.getParameter("emailadr"))) || (request.getParameter("emailadr").length() != 4)) {
	   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
	   if(true){return;}
	}

}



Shipment_feeder sf = new Shipment_feeder();
//out.println(sf.overAttempt(10, request.getParameter("emailadr")));
if (sf.overAttempt(10, request.getParameter("emailadr"))) {
   out.println("<font size=2 face=\"Frutiger, Arial\"><b>Please contact your sales representative.</b></font>");
} else {

  Customer cust = sf.getCust(request.getParameter("emailadr"), request.getParameter("passwd"));
    JdbcConn myJdbc = new JdbcConn("webdb_ds");
    String sql_str="";

  if (cust.grp_id == null) {
    sql_str = "insert into sf_customer_login values ('" + request.getParameter("emailadr") + "','" + request.getParameter("passwd") + "',current)";
    myJdbc.exeUpdateTrans(sql_str);

	if (cust.grp_id == null) {
    // Invalid login
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid login credentials");
    return;
	}


	response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid login credentials");
	return;


    // out.println("<br><br><input type=\"button\" name=\"back\" value=\"Back\" id=\"backButton\">");
    
  } else {
    sql_str = "delete from sf_customer_login where email = '" + request.getParameter("emailadr") + "'";
    myJdbc.exeUpdateTrans(sql_str);

	  // Prevent session fixation: Invalidate old session and create a new one after successful login
	session.invalidate();
	HttpSession newSession = request.getSession(true);
	newSession.setAttribute("emailadr", request.getParameter("emailadr"));
	newSession.setAttribute("grp_id", cust.grp_id);
	newSession.setAttribute("contact_name", cust.contact_name);
	newSession.setAttribute("logo_filename", cust.logo_filename);
	newSession.setAttribute("default_charset", cust.default_charset);
	newSession.setAttribute("opt_charset", cust.opt_charset);
	newSession.setAttribute("default_sub_grp_id", cust.default_sub_grp_id);
	newSession.setAttribute("opt_sub_grp", cust.opt_sub_grp);
	newSession.setAttribute("authenticated", true);
	// Assign user role based on group or logic (example: admin if grp_id == 'admin')
	String userRole = "user";
	if ("admin".equalsIgnoreCase(cust.grp_id)) {
		userRole = "admin";
	}
newSession.setAttribute("role", userRole);
	  
	  String df_menu = sf.getDefaultMenu(cust.grp_id);

	  
	  if (df_menu.equals("ip")) {
	    //response.sendRedirect("input_print/toMain.jsp");
		response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "input_print/toMain.jsp"));
	    return;
      } else {
		if (df_menu.equals("f2")) {
	      //response.sendRedirect("feed_print2/toMain.jsp");
		  response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "feed_print2/toMain.jsp"));
		  return;
	    } 
	  }
	  
  }
}
   
%>
</form>
</blockquote></body></html>

