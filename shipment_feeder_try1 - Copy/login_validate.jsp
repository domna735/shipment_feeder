<%@ page import="hkapps.shipment_feeder.*"%>
<%@ page import="com.hkapps.util.*"%>
<%@ page import="java.net.URLEncoder"%>
<%@ page import="java.util.*"%>
<%@ page import="java.lang.*"%>
<%@ page import="java.net.*"%>
<%@ page import="java.sql.*"%>
<%@ page import="java.io.*"%>


<%@
out.println("debug: start<br>");
// 強化 CSP，允許 Google reCAPTCHA v3 及 gstatic style
response.setHeader("Content-Security-Policy",
  "default-src 'self'; " +
  "script-src 'self' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; " +
  "style-src 'self' https://www.gstatic.com/recaptcha/; " +
  "frame-src 'self' https://www.google.com/recaptcha/; " +
  "connect-src 'self' https://www.google.com/recaptcha/ https://www.gstatic.com/recaptcha/; " +
  "object-src 'none'; " +
  "frame-ancestors 'self'; " +
  "upgrade-insecure-requests; " +
  "block-all-mixed-content"
);
out.println("debug: after CSP<br>");
%>
<html>
<head>
<title>DHL Shipment Information Feeder</title>
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">
</head>
<body bgcolor=#ffffff><blockquote>
<script type="text/javascript" src="js/back.js"></script>
<form id="validateForm">
<%
out.println("debug: before referer check<br>");
String referpage = request.getHeader("referer");
Common common = new Common();
if (referpage == null) {
   out.println("debug: referpage null<br>");
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}
if (request.getQueryString() != null) {
   out.println("debug: query string not null<br>");
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}
URL referurl = new URL(referpage);
out.println("debug: referurl=" + referurl.getPath() + "<br>");
if (!referurl.getPath().equals("/shipment_feeder/login.html") && !referurl.getPath().equals("/shipment_feeder/login_ip.jsp") && !referurl.getPath().equals("/shipment_feeder/login_ip.html")) {
   out.println("debug: referurl not allowed<br>");
   response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
   if(true){return;}
}
if (referurl.getPath().equals("/shipment_feeder/login.html")) {
  out.println("debug: login.html flow<br>");
  if ((request.getParameter("emailadr") == null) || (request.getParameter("emailadr").equals("")) || 
    (request.getParameter("passwd") == null) || (request.getParameter("passwd").equals(""))) {
     out.println("debug: login.html param missing<br>");
     response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
     if(true){return;}
  }
  DataTypeUtil dtu = new DataTypeUtil();
  if ((!dtu.isValidEmail(request.getParameter("emailadr"),50)) || (!dtu.isValidPassword(request.getParameter("passwd"),6,16))) {
     out.println("debug: login.html param invalid<br>");
     response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
     if(true){return;}
  }
}
if (referurl.getPath().equals("/shipment_feeder/login_ip.html") || referurl.getPath().equals("/shipment_feeder/login_ip.jsp")) {
    out.println("debug: login_ip flow<br>");
    if ((request.getParameter("emailadr") == null) || (request.getParameter("emailadr").equals(""))) {
       out.println("debug: login_ip param missing<br>");
       response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
       if(true){return;}
    }
    DataTypeUtil dtu = new DataTypeUtil();
    if ((!dtu.isAlphaNumeric(request.getParameter("emailadr"))) || (request.getParameter("emailadr").length() != 4)) {
       out.println("debug: login_ip param invalid<br>");
       response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "index.html"));
       if(true){return;}
    }
}
// === Google reCAPTCHA v3 驗證區塊 ===
String recaptchaResponse = request.getParameter("g-recaptcha-response");
if (recaptchaResponse == null || recaptchaResponse.isEmpty()) {
    out.println("reCAPTCHA missing<br>");
    response.sendRedirect("login_ip.html");
    return;
}
try {
    Properties prop = new Properties();
    FileInputStream ip = new FileInputStream(System.getProperty("catalina.base") + "/webapps/config.properties");
    prop.load(ip);
    String secret = prop.getProperty("captcha_secretKey_v3");
    ip.close();
    String url = "https://www.google.com/recaptcha/api/siteverify";
    String params = "secret=" + URLEncoder.encode(secret, "UTF-8") +
                    "&response=" + URLEncoder.encode(recaptchaResponse, "UTF-8") +
                    "&remoteip=" + request.getRemoteAddr();
    java.net.URL obj = new java.net.URL(url);
    java.net.HttpURLConnection con = (java.net.HttpURLConnection) obj.openConnection();
    con.setRequestMethod("POST");
    con.setDoOutput(true);
    java.io.DataOutputStream wr = new java.io.DataOutputStream(con.getOutputStream());
    wr.writeBytes(params);
    wr.flush();
    wr.close();
    java.io.BufferedReader in = new java.io.BufferedReader(new java.io.InputStreamReader(con.getInputStream()));
    String inputLine;
    StringBuffer responseStr = new StringBuffer();
    while ((inputLine = in.readLine()) != null) {
        responseStr.append(inputLine);
    }
    in.close();
    boolean captchaSuccess = responseStr.toString().contains("\"success\": true");
    if (!captchaSuccess) {
        out.println("reCAPTCHA failed<br>");
        response.sendRedirect("login_ip.html");
        return;
    }
} catch (Exception e) {
    out.println("reCAPTCHA verify error: " + e.getMessage() + "<br>");
    response.sendRedirect("login_ip.html");
    return;
}
out.println("debug: before overAttempt<br>");
Shipment_feeder sf = new Shipment_feeder();
if (sf.overAttempt(10, request.getParameter("emailadr"))) {
   out.println("debug: overAttempt<br>");
   out.println("<font size=2 face=\"Frutiger, Arial\"><b>Please contact your sales representative.</b></font>");
} else {
  out.println("debug: before getCust<br>");
  Customer cust = sf.getCust(request.getParameter("emailadr"), request.getParameter("passwd"));
  out.println("debug: after getCust<br>");
  JdbcConn myJdbc = new JdbcConn("webdb_ds");
  String sql_str="";
  if (cust.grp_id == null) {
    out.println("debug: cust.grp_id null<br>");
    sql_str = "insert into sf_customer_login (email, passwd, login_time) values ('" + request.getParameter("emailadr") + "', '" + request.getParameter("passwd") + "', current)";
    myJdbc.exeUpdateTrans(sql_str);
    response.sendError(HttpServletResponse.SC_UNAUTHORIZED, "Invalid login credentials");
    return;
  } else {
    out.println("debug: cust.grp_id not null<br>");
    sql_str = "delete from sf_customer_login where email = '" + request.getParameter("emailadr") + "'";
    myJdbc.exeUpdateTrans(sql_str);
    // Prevent session fixation: Invalidate old session and create a new one after successful login
    out.println("debug: before session.invalidate<br>");
    session.invalidate();
    out.println("debug: after session.invalidate<br>");
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
    out.println("debug: after set session, df_menu=" + df_menu + "<br>");
    if (df_menu.equals("ip")) {
      out.println("debug: redirect to input_print/toMain.jsp<br>");
      response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "input_print/toMain.jsp"));
      return;
    } else {
      if (df_menu.equals("f2")) {
        out.println("debug: redirect to feed_print2/toMain.jsp<br>");
        response.sendRedirect(common.convert_path(request.getServerPort(), (request.getRequestURL()).toString(), request.getServletPath(), "feed_print2/toMain.jsp"));
        return;
      } 
    }
    // 建立 /appl/service/webapps/shipment_feeder/sessions/SESSIONID 檔案
    try {
        String sessionId = newSession.getId();
        java.io.File sessionDir = new java.io.File("/appl/service/webapps/shipment_feeder/sessions");
        if (!sessionDir.exists()) sessionDir.mkdirs();
        java.io.File sessionFile = new java.io.File(sessionDir, sessionId);
        java.io.FileWriter fw = new java.io.FileWriter(sessionFile);
        fw.write("emailadr=" + request.getParameter("emailadr") + "\n");
        fw.write("grp_id=" + cust.grp_id + "\n");
        fw.write("contact_name=" + cust.contact_name + "\n");
        fw.write("login_time=" + (new java.util.Date()) + "\n");
        fw.close();
        out.println("debug: session file created<br>");
    } catch (Exception e) {
        // log error
        out.println("Session file error: " + e.getMessage());
    }
  }
}
out.println("debug: end<br>");
%>
</form>
</blockquote></body></html>
