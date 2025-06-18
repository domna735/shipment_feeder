function createElementFromHTML(htmlString) {
    const div = document.createElement('div');
    div.innerHTML = htmlString.trim();
    return div.firstChild;
}

function loadTop(head, logo, cname) {
    const headElement = document.head;
    const body = document.body;

    // Add stylesheet
    const link = document.createElement('link');
    link.rel = 'stylesheet';
    link.type = 'text/css';
    link.href = '../common.css';
    headElement.appendChild(link);

    // Create top bar
    const table = document.createElement('table');
    table.style.width = '100%';
    table.cellSpacing = 0;
    table.cellPadding = 0;

    const row = table.insertRow();
    const cell = row.insertCell();
    cell.colSpan = 2;

    const innerTable = document.createElement('table');
    innerTable.style.width = '100%';
    innerTable.cellSpacing = 0;
    innerTable.cellPadding = 0;

    const innerRow = innerTable.insertRow();
    innerRow.bgColor = '#CC0000';
    const innerCell = innerRow.insertCell();
    innerCell.innerHTML = `<font color="#FFFFFF" size="4" face="Arial"><b>${head}</b></font>`;

    const rightCell = innerRow.insertCell();
    rightCell.align = 'right';
    rightCell.innerHTML = `<font color="#FFFFFF" size="2" face="Arial"><b>${cname ? 'Hello ' + cname : ''}</b></font>`;

    innerRow.appendChild(innerCell);
    innerRow.appendChild(rightCell);
    innerTable.appendChild(innerRow);
    cell.appendChild(innerTable);
    row.appendChild(cell);

    if (logo && logo !== 'null') {
        const logoCell = row.insertCell();
        const img = document.createElement('img');
        img.src = `../images/logo/${logo}`;
        img.alt = 'Logo';
        logoCell.appendChild(img);
    }

    body.appendChild(table);
}


function loadTop_frontpage()
{
document.write('<link rel="STYLESHEET" type="text/css" href="common.css">');	
document.write('<BODY BGCOLOR="#FFFFFF" TEXT="#000000" topmargin="0" leftmargin="0" rightmargin="0" marginheight="0" marginwidth="0" SCROLL="NO">');

document.write('<table width="100%" border="0" CELLSPACING=0 CELLPADDING=0>');
document.write('<tr bgcolor="#FFCC00"><td height="75px" width="15%"><a href="http://www.dhl.com.hk" target=_blank rel="noopener noreferrer"><img src="images/logo.gif" border=0 alt="DHL"></a></td><td>');
document.write('<table width="100%" border="0" CELLSPACING=0 CELLPADDING=0>');
document.write('<tr bgcolor="#FFCC00"><td>&nbsp;</td></tr>');
document.write('<tr bgcolor="#CC0000" valign="bottom"><td height="60px">');
document.write('<table height="100%" width="100%" border="0">');
document.write('<tr valign="bottom"><td width="2%">&nbsp;</td><td><font color="#FFFFFF" size="4" face="Arial"><b>Shipment Information Feeder</b></font></td></tr>');
document.write('</table>');
document.write('</td></tr>');
document.write('</table>');

document.write('</td></tr></table>');
document.write('<div id="Layer2">');
document.write('<table width="100%" border="0" CELLSPACING=0 CELLPADDING=0>');
document.write('<tr><td><img src="images/headline.jpg" align="right" hspace="0"></td></tr>');
document.write('</table>');
document.write('</div>');
document.write('</body>');
}


function loadMenu(menu_lst, default_menu) {
var menu_arr = new Array();
menu_arr = menu_lst.split('|');
document.write('<link rel="STYLESHEET" type="text/css" href="../common.css">');
document.write('<link rel="STYLESHEET" type="text/css" href="../menu.css">');
document.write('<link rel="STYLESHEET" type="text/css" href="../styles.css">');

document.write('<BODY topmargin="0" leftmargin="0" rightmargin="0" marginheight="0" marginwidth="0"><font face="Arial" size="2">');

document.write('<table border="0" CELLSPACING=0 CELLPADDING=0 width="187" height="100%"><tr><td colspan="2" valign=top height="5%">');

document.write('<table border="0" CELLSPACING=0 CELLPADDING=0 width="187">');

document.write('<tr><td width="12">&nbsp;</td><td bgcolor="#FFCC00" align="center" height="65px"><a href="http://www.dhl.com.hk" target=_blank rel="noopener noreferrer"><img src="../images/logo.gif" border=0 alt="DHL"></a></td></tr>');
document.write('<tr><td colspan=2></td></tr></table>');


for (a in menu_arr) {
    if (menu_arr[a] == "f2") {
	document.write('<a id="defPageButton" href="javascript:void(0);" class="menuItem">Feed & Print');
	document.getElementById("defPageButton").addEventListener("click", function() {
		nextpage('../feed_print2/fp_DefPage.jsp', false);
	});
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
	document.write('<a href="../feed_print2/download_processed.jsp" target=_blank rel="noopener noreferrer" class="submenuItem"><img src="../images/arrow_r.gif" border="0" alt="" width="9" height="9"><font size=1>Last Processed File</font>&nbsp;</a>');
    } else if (menu_arr[a] == "ip") {
    	document.write('<a id="defPageButton" href="javascript:void(0);" class="menuItem">Print Waybill');
	document.getElementById("defPageButton").addEventListener("click", function() {
		nextpage('../input_print/ip_DefPage.jsp',false);
	});
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');

    } 
	
    /*
    if (menu_arr[a] == "fp") {
	document.write('<a href="javascript:nextpage(\'../feed_print/fp_DefPage.jsp\',false);" class="menuItem">Feed & Print');
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
	document.write('<a href="../feed_print/download_processed.jsp" target=_blank rel="noopener noreferrer" class="submenuItem"><img src="../images/arrow_r.gif" border="0" alt="" width="9" height="9"><font size=1>Last Processed File</font>&nbsp;</a>');
	  	
    } else if (menu_arr[a] == "f2") {
	document.write('<a href="javascript:nextpage(\'../feed_print2/fp_DefPage.jsp\',false);" class="menuItem">Feed & Print');
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
	document.write('<a href="../feed_print2/download_processed.jsp" target=_blank rel="noopener noreferrer" class="submenuItem"><img src="../images/arrow_r.gif" border="0" alt="" width="9" height="9"><font size=1>Last Processed File</font>&nbsp;</a>');
		
    } else if (menu_arr[a] == "ip") {
    	document.write('<a href="javascript:nextpage(\'../input_print/ip_DefPage.jsp\',false);" class="menuItem">Print Waybill');
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
    } else if (menu_arr[a] == "i2") {
    	document.write('<a href="javascript:nextpage(\'../input_print2/ip_DefPage.jsp\',false);" class="menuItem">Type & Print');
	document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');    
    }
	*/
	
}

if (menu_lst != "ip") {
  document.write('<a id="changePasswordButton" href="javascript:void(0);" class="menuItem">Change Password');
  document.getElementById("changePasswordButton").addEventListener("click", function() {
	nextpage('../change_password/cp_DefPage.jsp',false);
  });
  document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
}

if (default_menu == "ip") {
  document.write('<a id="logoutButton" href="javascript:void(0);" class="menuItem">Logout');
  document.getElementById("logoutButton").addEventListener("click", function() {
	nextpage('../../print_waybill/logout.jsp',false);
  });
  document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
} else {
  document.write('<a id="logoutButton" href="javascript:void(0);" class="menuItem">Logout');
  document.getElementById("logoutButton").addEventListener("click", function() {
	nextpage('../logout.jsp',false);
  });
  document.write('<img src="../images/arrow_r.gif" border="0" vspace="6" alt="" width="9" height="9"></a>');
}

document.write('</td></tr>');

document.write('<tr><td colspan=2>');
document.write('<table border="0" CELLSPACING=0 CELLPADDING=0 width="187" height="100%">');
document.write('<tr><td width="12">&nbsp;</td><td nowrap bgcolor="#FFCC00">&nbsp;</td></tr></table>');
document.write('</td></tr>');

document.write('<tr><td colspan=2 valign=bottom height=5%>');

document.write('<table border="0" CELLSPACING=0 CELLPADDING=0 width="187">');
document.write('<tr><td width="12">&nbsp;</td><td nowrap bgcolor="#FFCC00" align="left" valign="bottom">');
document.write('<div align="center"><a href="http://www.dpdhl.com/" target=_blank rel="noopener noreferrer"><img src="../images/dpwn.jpg" border=0 alt="Deutsche Post World Net"></a></div>');
var currentTime = new Date();
var currentyear = currentTime.getFullYear();
document.write('<font class="footer-text"><br>&copy;' + currentyear + ' &#25958;&#35946;&#22283;&#38555;&#36895;&#36958;(&#39321;&#28207;)&#26377;&#38480;&#20844;&#21496;<br>&#29256;&#27402;&#25152;&#26377;&#65292;&#19981;&#24471;&#36681;&#36617;&#12290;<br>&copy;' + currentyear + ' DHL Express (Hong Kong) Limited<br>All rights reserved.<br>&nbsp;</font>');
document.write('</td></tr>');
document.write('<tr><td colspan=2></td></tr></table>');
document.write('</td></tr></table>');
document.write('</body>');

}





function doPopup(url) {
    const scrWt = screen.availWidth || 800;
    const scrHt = screen.availHeight || 600;
    const winWt = Math.min(660, scrWt - 100);
    const winHt = Math.min(488, scrHt - 75);
    const posLinks = ((scrWt - winWt) / 2) + 20;
    const posTop = ((scrHt - winHt) / 2 - 20) + 20;

    window.open(url, 'bps', `width=${winWt},height=${winHt},left=${posLinks},top=${posTop},location=no,menubar=no,toolbar=no,scrollbars=yes,resizable=yes`);
}


var image = new Object();


const image = {};

function preloadImage(name, state, src) {
    if (!image[name]) image[name] = {};
    image[name][state] = new Image();
    image[name][state].src = src;
}

function swapImageById(imgId, name, state) {
    if (image[name]) {
        const img = document.getElementById(imgId);
        if (img) img.src = image[name][state].src;
    }
}

// Preload common images
preloadImage('arrow', 'off', '../images/arrow_r.gif');



