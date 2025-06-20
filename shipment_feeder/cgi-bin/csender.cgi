#!/usr/bin/perl

use lib '/appl/service/webapps/cgi-bin/';
use db_con;
$> = $<;
$) = $(;


use CGI::Cookie;
my %cookies = CGI::Cookie->fetch;
my $session_token = $cookies{'SESSIONID'} ? $cookies{'SESSIONID'}->value : '';
unless (is_valid_session($session_token)) {
    print "Location: /shipment_feeder/toLogin.html\n\n";
    exit;
}

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


sub is_valid_session {
    my ($token) = @_;
    return 0 unless $token;

    my $session_file = "/tmp/sessions/$token";
    return 0 unless -e $session_file;

    # Optional: check session age (e.g., expire after 30 minutes)
    my $max_age = 1800; # 30 minutes
    my $mtime = (stat($session_file))[9];
    return 0 if (time - $mtime > $max_age);

    # Optional: validate session content (e.g., user ID or checksum)
    open my $fh, '<', $session_file or return 0;
    my $content = do { local $/; <$fh> };
    close $fh;

    return 0 unless $content =~ /emailadr=/; # or any expected marker

    return 1;
}

if ($ENV{'REQUEST_METHOD'} eq "POST" ){
	read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
elsif ($ENV{'REQUEST_METHOD'} eq "GET" ){
	$buffer = $ENV{'QUERY_STRING'};
}

@pairs = split(/&/, $buffer);

foreach $pair (@pairs){
	($name, $value) = split (/=/, $pair);
	$value =~ s/^%09/<dd>/g;
	$value =~ s/%0D/<br>%0D/g;
	$value =~ tr/+/ /;
	$value =~ s/%(..)/pack("c", hex($1))/eg;
	$Form{$name} = $value;
}

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";

#$Form{origin}='HKG';
#$Form{paper_ty}='A';
#$Form{sub_grp_id}='DHL1';

$to_show=1;
if ((!defined $Form{origin}) || (!defined $Form{sub_grp_id}) || (!defined $Form{paper_ty})) {
  $to_show=0;
} else {		
    if (($Form{origin} eq '') || ($Form{sub_grp_id} eq '') || ($Form{paper_ty} eq '')) {
	  $to_show=0;
    } else {
		if (($Form{origin} ne 'HKG') && ($Form{origin} ne 'MCA')) {
			$to_show=0;
		}
		if (($Form{paper_ty} ne 'A') && ($Form{paper_ty} ne 'L')) {
			$to_show=0;
		}
		if ((length($Form{sub_grp_id}) > 4) || ($Form{sub_grp_id} =~ m/[^A-Z0-9]/)) {
			$to_show=0;
	        }	
	
	}
}

if ($to_show == 0) {

print <<END1;
<html>
<head>
<meta http-equiv="Refresh" content="0; URL=../../print_waybill/">
</head>
</html>
END1
exit();
}

if ($Form{rload} ne "Y") {
 if (isProd()) {
   print '<html><body><form name="pre" method="post" action="https://apps.dhl.com.hk/cgi-bin/csender.cgi">';
 } else {
   print '<html><body><form name="pre" method="post" action="csender.cgi">';
 }
print <<END1;
<input type="hidden" name="rload" value="Y">
<input type="hidden" name="from_where" value="$Form{from_where}">
<input type="hidden" name="paper_ty" value="$Form{paper_ty}">
<input type="hidden" name="origin" value="$Form{origin}">
<input type="hidden" name="sub_grp_id" value="$Form{sub_grp_id}">
</form>
</body>
<script LANGUAGE="javascript">
document.pre.submit();
//alert(document.pre.from_where.value);
</script>
</html>

END1

} else {

if ($Form{origin} eq 'MCA') {

@tel_code = (
'+86',
'+852',
'+886');

} else {

@tel_code = (
'+86',
'+853',
'+886');

}
	
@new_arr = (
'CN',
'HK',
'MO',
'TW');

%country_list = (
"AF" => "Afghanistan",
"AL" => "Albania",
"DZ" => "Algeria",
"AS" => "American Samoa",
"AD" => "Andorra",
"AO" => "Angola",
"AI" => "Anguilla",
"AG" => "Antigua",
"AR" => "Argentina",
"AM" => "Armenia",
"AW" => "Aruba",
"AU" => "Australia",
"AT" => "Austria",
"AZ" => "Azerbaijan",
"BS" => "Bahamas",
"BH" => "Bahrain",
"BD" => "Bangladesh",
"BB" => "Barbados",
"BY" => "Belarus",
"BE" => "Belgium",
"BZ" => "Belize",
"BJ" => "Benin",
"BM" => "Bermuda",
"BT" => "Bhutan",
"BO" => "Bolivia",
"XB" => "Bonaire",
"BA" => "Bosnia and Herzegovina",
"BW" => "Botswana",
"BR" => "Brazil",
"BN" => "Brunei",
"BG" => "Bulgaria",
"BF" => "Burkina Faso",
"BI" => "Burundi",
"KH" => "Cambodia",
"CM" => "Cameroon",
"CA" => "Canada",
"IC" => "Canary Islands, The",
"CV" => "Cape Verde",
"KY" => "Cayman Islands",
"CF" => "Central African Republic",
"TD" => "Chad",
"CL" => "Chile",
"CN" => "China, People's Republic",
"CO" => "Colombia",
"KM" => "Comoros",
"CG" => "Congo",
"CD" => "Congo, The Democratic Republic of",
"CK" => "Cook Islands",
"CR" => "Costa Rica",
"CI" => "Cote d'Ivoire",
"HR" => "Croatia",
"CU" => "Cuba",
"XC" => "Curacao",
"CY" => "Cyprus",
"CZ" => "Czech Republic, The",
"DK" => "Denmark",
"DJ" => "Djibouti",
"DM" => "Dominica",
"DO" => "Dominican Republic",
"TL" => "East Timor",
"EC" => "Ecuador",
"EG" => "Egypt",
"SV" => "El Salvador",
"ER" => "Eritrea",
"EE" => "Estonia",
"ET" => "Ethiopia",
"FK" => "Falkland Islands",
"FO" => "Faroe Islands",
"FJ" => "Fiji",
"FI" => "Finland",
"FR" => "France",
"GF" => "French Guiana",
"GA" => "Gabon",
"GM" => "Gambia",
"GE" => "Georgia",
"DE" => "Germany",
"GH" => "Ghana",
"GI" => "Gibraltar",
"GR" => "Greece",
"GL" => "Greenland",
"GD" => "Grenada",
"GP" => "Guadeloupe",
"GU" => "Guam",
"GT" => "Guatemala",
"GG" => "Guernsey",
"GN" => "Guinea Republic",
"GW" => "Guinea-Bissau",
"GQ" => "Guinea-Equatorial",
"GY" => "Guyana (British)",
"HT" => "Haiti",
"HN" => "Honduras",
"HK" => "Hong Kong",
"HU" => "Hungary",
"IS" => "Iceland",
"IN" => "India",
"ID" => "Indonesia",
"IR" => "Iran (Islamic Republic of)",
"IQ" => "Iraq",
"IE" => "Ireland, Republic Of",
"IL" => "Israel",
"IT" => "Italy",
"JM" => "Jamaica",
"JP" => "Japan",
"JE" => "Jersey",
"JO" => "Jordan",
"KZ" => "Kazakhstan",
"KE" => "Kenya",
"KI" => "Kiribati",
"KR" => "Korea, Republic Of",
"KV" => "Kosovo",
"KW" => "Kuwait",
"KG" => "Kyrgyzstan",
"LA" => "Lao People's Democratic Republic",
"LV" => "Latvia",
"LB" => "Lebanon",
"LS" => "Lesotho",
"LR" => "Liberia",
"LY" => "Libya",
"LI" => "Liechtenstein",
"LT" => "Lithuania",
"LU" => "Luxembourg",
"MO" => "Macau",
"MK" => "Macedonia, Former Yugoslav Republic",
"MG" => "Madagascar",
"MW" => "Malawi",
"MY" => "Malaysia",
"MV" => "Maldives",
"ML" => "Mali",
"MT" => "Malta",
"MH" => "Marshall Islands",
"MQ" => "Martinique",
"MR" => "Mauritania",
"MU" => "Mauritius",
"YT" => "Mayotte",
"MX" => "Mexico",
"FM" => "Micronesia, Federated States of",
"MD" => "Moldova, Republic Of",
"MC" => "Monaco",
"MN" => "Mongolia",
"ME" => "Montenegro, Republic of",
"MS" => "Montserrat",
"MA" => "Morocco",
"MZ" => "Mozambique",
"MM" => "Myanmar",
"NA" => "Namibia",
"NR" => "Nauru, Republic Of",
"NP" => "Nepal",
"NL" => "Netherlands, The",
"XN" => "Nevis",
"NC" => "New Caledonia",
"NZ" => "New Zealand",
"NI" => "Nicaragua",
"NE" => "Niger",
"NG" => "Nigeria",
"NU" => "Niue",
"KP" => "North Korea",
"NO" => "Norway",
"OM" => "Oman",
"PK" => "Pakistan",
"PW" => "Palau",
"PA" => "Panama",
"PG" => "Papua New Guinea",
"PY" => "Paraguay",
"PE" => "Peru",
"PH" => "Philippines, The",
"PL" => "Poland",
"PT" => "Portugal",
"PR" => "Puerto Rico",
"QA" => "Qatar",
"RE" => "Reunion, Island Of",
"RO" => "Romania",
"RU" => "Russian Federation, The",
"RW" => "Rwanda",
"MP" => "Saipan",
"WS" => "Samoa",
"SM" => "San Marino",
"ST" => "Sao Tome and Principe",
"SA" => "Saudi Arabia",
"SN" => "Senegal",
"RS" => "Serbia, Republic of",
"SC" => "Seychelles",
"SL" => "Sierra Leone",
"SG" => "Singapore",
"SK" => "Slovakia",
"SI" => "Slovenia",
"SB" => "Solomon Islands",
"SO" => "Somalia",
"XS" => "Somaliland, Rep of (North Somalia)",
"ZA" => "South Africa",
"SS" => "South Sudan",
"ES" => "Spain",
"LK" => "Sri Lanka",
"XY" => "St. Barthelemy",
"XE" => "St. Eustatius",
"KN" => "St. Kitts",
"LC" => "St. Lucia",
"XM" => "St. Maarten",
"VC" => "St. Vincent",
"SD" => "Sudan",
"SR" => "Suriname",
"SZ" => "Swaziland",
"SE" => "Sweden",
"CH" => "Switzerland",
"SY" => "Syria",
"PF" => "Tahiti",
"TW" => "Taiwan",
"TZ" => "Tanzania",
"TH" => "Thailand",
"TG" => "Togo",
"TO" => "Tonga",
"TT" => "Trinidad and Tobago",
"TN" => "Tunisia",
"TR" => "Turkey",
"TC" => "Turks and Caicos Islands",
"TV" => "Tuvalu",
"UG" => "Uganda",
"UA" => "Ukraine",
"AE" => "United Arab Emirates",
"GB" => "United Kingdom",
"US" => "United States Of America",
"UY" => "Uruguay",
"UZ" => "Uzbekistan",
"VU" => "Vanuatu",
"VE" => "Venezuela",
"VN" => "Vietnam",
"VG" => "Virgin Islands (British)",
"VI" => "Virgin Islands (US)",
"YE" => "Yemen, Republic Of",
"ZM" => "Zambia",
"ZW" => "Zimbabwe");


print <<END1;

<html>
<head><title>DHL Waybill Printing</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
<script type="text/javascript" src="../../javascript/jquery.js"></script>
<!--<script type="text/javascript" src="../../javascript/jquery-3.7.0.js"></script>-->
<script type="text/javascript" src="../../javascript/jquery-migrate-1.4.1.js"></script>
<script type="text/javascript" src="../../javascript/jquery-migrate-3.4.1.js"></script>
  <script type="text/javascript" src="../../javascript/jquery.autocomplete.js"></script>
	<link rel="stylesheet" href="../../css/jquery.autocomplete.css" type="text/css" />
<script language="JavaScript">

<!-- hide

  // ok, we have a JavaScript browser
  var browserOK = false;
  var pics;

// -->

</script>

<script language="JavaScript1.1">

<!-- hide

  // JavaScript 1.1 browser - oh yes!
  browserOK = true;
  pics = new Array();

// -->

</script>

<script LANGUAGE="javascript" SRC="../../js_client/check.js"></script>
<script LANGUAGE="javascript" SRC="../../js_client/cd_init2.js"></script>

<script language="JavaScript">

<!--
END1

#if ($Form{origin} eq 'MCA') {
#	print 'window.open("../../info/notice_decomm_mo.html", "Decommission Notice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=750,height=400,left=0,top=0").focus();';
#} else {
#	print 'window.open("../../info/notice_decomm_cn.html", "Decommission Notice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=750,height=400,left=0,top=0").focus();';
#}


print <<END1;

if (browserOK) {
printa1 = new Image
printa2 = new Image

printa1.src = '../../images/next1a.gif'
printa2.src = '../../images/next2a.gif'

}
else {
}

function private_MouseOver() {
  if (document.images) {
    eval("document." + this.stImageName + ".src='" + this.stOverImage + "'");
  }
}

function private_MouseOut() {
  if (document.images) {
    eval("document." + this.stImageName + ".src='" + this.stOutImage + "'");
  }
}

function objMouseChangeImg(stImageName, stOverImage, stOutImage) {
  this.stImageName = stImageName;
  this.stOverImage = stOverImage;
  this.stOutImage = stOutImage;
  this.MouseOut = private_MouseOut;
  this.MouseOver = private_MouseOver;
}

function isNum(passedVal) {
	for (i=0; i<passedVal.length; i++) {
		if (passedVal.charAt(i) < "0") {
			return false
		}
		if (passedVal.charAt(i) > "9") {
			return false
		}
	}
	return true
}

function popWindow(){
	URL = '../../faq/airwaybill.html'
	remote = window.open(URL, 'remote', 'width=640,height=620,scrollbars=yes');
}


objPIC3 = new objMouseChangeImg('PIC3', printa2.src, printa1.src);

tel_cd_arr = create_tel_cd_lst ();


function checkEmpty(theField)
{
    v = theField.value;
    while(''+v.charAt(0)==' ')v=v.substring(1,v.length);
    while(v.charAt(v.length-1)+''==' ')v=v.substring(0,v.length-1);

    if ((v=='.') || (v==',') || (v=='')) return false;
    else return true;
}

function isNumAndDecimal(passedVal) {
	var decimal = ""
	for (var c = 0; c < passedVal.length; c++){
    	var oneChar = passedVal.charAt(c)
        if (oneChar == "."  && decimal == ""){
           	if (oneChar == "."){
          		decimal = "yes"
           	}
        	continue                                                
        }
        if (oneChar < "0" || oneChar > "9"){
        	return false
        }
    }
	return true
}

function isChinese (s) {
    
	if (containInvalidSymbol(s)) {
		return false;
	} else {
		if (isAlphaNum(s)) {
			return false;
		}
	}
    return true;
}

function containInvalidSymbol(s)
{
		var i;
		var InvalidSymbol = "\$\%\*\=\;\<\>\?\\\"";
		var InvalidSymbol2 = "\\\\";
		
		//allow +-() /
		
		for (i = 0; i < s.length; i++)
		{   
			var c = s.charAt(i);
			if (InvalidSymbol.indexOf(c) != -1) return true;
			if (InvalidSymbol2.indexOf(c) != -1) return true;
		}
		// All characters do not contain invalid symbol.
		return false;
}


function clear_acc() {
   document.getElementById('dhl_acc_no').value="";
   document.getElementById('dhl_acc_no').disabled=true;
   document.getElementById('charge_to_account').value="";
   document.getElementById('charge_to_account').disabled=true;
}

function enable_acc() {
   document.getElementById('dhl_acc_no').disabled=false;
   document.getElementById('charge_to_account').disabled=false;

}

function checking(form)
{
    var flag = 'true'
	
	charge_to_option = -1;
	for (i=form.charge_to.length-1; i > -1; i--) {
         if (form.charge_to[i].checked) {
			charge_to_option = i;
         }	
    }

	if (charge_to_option == -1) {
		dhl_alert("useless", "Information is missing", "Please select Charge to option.")
		flag = 'false'
	}
	
	else if ((charge_to_option != -1) && (form.charge_to[charge_to_option].value == "OTHERS") && (!checkEmpty(form.charge_to_account))) {
        	form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is missing", "Please enter a payer account no. if it's charged to 3rd party.", 180 )
		flag = 'false'
	}
	/*
	else if ((charge_to_option != -1) && (form.charge_to[charge_to_option].value == "CASH") && ((checkEmpty(form.dhl_acc_no)) || (checkEmpty(form.charge_to_account)))) {
        	form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The sender and payer account no. are not required", "Please do not enter send account no. and payer account no. if it's paid by cash.", 180 )
		flag = 'false'
	}
	*/
	else if ((!(isAlphaNum_acno(form.charge_to_account.value))) || (form.charge_to_account.value.substring(0,4).toUpperCase() == "TCPC")) {
	    	form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.charge_to_account)) && (!isNum(form.charge_to_account.value)) && (form.charge_to_account.value.length != 9)) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && ((!isInteger(form.charge_to_account.value)) || (form.charge_to_account.value.length != 9))) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && ((form.charge_to_account.value.substring(0,2) == '96') || (form.charge_to_account.value.substring(0,2) == '95') || (form.charge_to_account.value.substring(0,2) == '94'))) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
END1

if ($Form{origin} eq 'MCA') {
	print "dhl_alert('useless', 'The payer account no. is invalid', '由2021年12月1日起，此應用程式將不再支援 \"DHL 進口帳號\" (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br><br>請您使用網上工具 <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> 製作你的提單。<br><br>Effective from 1 December 2021, this application will not support \"DHL Import Express\" account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br><br>Please use our online tool <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create your waybills.', 350 )\n";
} else {
	print "dhl_alert('useless', 'The payer account no. is invalid', '由2021年12月1日起，此應用程式將不再支援 \"DHL 進口帳號\" (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br><br>請您使用網上工具 <a href=\"https://mydhl.express.dhl/hk/zh/ship/solutions.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> 製作你的提單。<br><br>Effective from 1 December 2021, this application will not support \"DHL Import Express\" account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br><br>Please use our online tool <a href=\"https://mydhl.express.dhl/hk/en/ship/solutions.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create your waybills.', 350 )\n";
}
		
print <<END1;
		flag = 'false'
	}
END1

if ($Form{origin} eq 'MCA') {
  #print "else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (!((form.charge_to_account.value.substring(0,2) == '64') || (form.charge_to_account.value.substring(0,2) == '96') || (form.charge_to_account.value.substring(0,2) == '95') || (form.charge_to_account.value.substring(0,2) == '94')))) {";
  print "else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (!(form.charge_to_account.value.substring(0,2) == '64'))) {";
} else {
  #print "else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (!((form.charge_to_account.value.substring(0,2) == '63') || (form.charge_to_account.value.substring(0,2) == '96') || (form.charge_to_account.value.substring(0,2) == '95') || (form.charge_to_account.value.substring(0,2) == '94')))) {";
  print "else if ((checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (!(form.charge_to_account.value.substring(0,2) == '63'))) {";
}

print <<END1;

		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}else if ((charge_to_option != -1)&& (form.charge_to[charge_to_option].value == "RECEIVER") && !checkEmpty(form.charge_to_account) ) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is missing", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}	
	/*
	else if ((charge_to_option != -1)&&(checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (form.charge_to[charge_to_option].value == "RECEIVER")  && (!((form.charge_to_account.value.substring(0,2) == '96') || (form.charge_to_account.value.substring(0,2) == '95') || (form.charge_to_account.value.substring(0,2) == '94')))) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}
	else if ((charge_to_option != -1) && (checkEmpty(form.charge_to_account)) && (isNum(form.charge_to_account.value)) && (form.charge_to[charge_to_option].value == "OTHERS")  && (!((form.charge_to_account.value.substring(0,2) == '96') || (form.charge_to_account.value.substring(0,2) == '95') || (form.charge_to_account.value.substring(0,2) == '94')))) {
		form.charge_to_account.focus()
		form.charge_to_account.select()
		dhl_alert("useless", "The payer account no. is invalid", "Please enter a valid payer account no.", 180 )
		flag = 'false'
	}
	*/
	else if (!checkEmpty(form.dhl_acc_no)) {
   	    form.dhl_acc_no.focus()
		form.dhl_acc_no.select()
		dhl_alert("useless", "The sender account no. is missing", "Please enter a sender account no.", 180 )
		flag = 'false'
	}
	else if ((!(isAlphaNum_acno(form.dhl_acc_no.value))) || (form.dhl_acc_no.value.substring(0,4).toUpperCase() == "TCPC")) {
	    	form.dhl_acc_no.focus()
		form.dhl_acc_no.select()
		dhl_alert("useless", "The sender account no. is invalid", "Please enter a valid sender account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.dhl_acc_no)) && (!isNum(form.dhl_acc_no.value)) && (form.dhl_acc_no.value.length != 9)) {
		form.dhl_acc_no.focus()
		form.dhl_acc_no.select()
		dhl_alert("useless", "The sender account no. is invalid", "Please enter a valid sender account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && ((!isInteger(form.dhl_acc_no.value)) || (form.dhl_acc_no.value.length != 9))) {
		form.dhl_acc_no.focus()
		form.dhl_acc_no.select()
		dhl_alert("useless", "The sender account no. is invalid", "Please enter a valid sender account no.", 180 )
		flag = 'false'
	}
	else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && ((form.dhl_acc_no.value.substring(0,2) == '96') || (form.dhl_acc_no.value.substring(0,2) == '95') || (form.dhl_acc_no.value.substring(0,2) == '94'))) {
		form.dhl_acc_no.focus()
		form.dhl_acc_no.select()

END1

if ($Form{origin} eq 'MCA') {
	print "dhl_alert('useless', 'The sender account no. is invalid', '由2021年12月1日起，此應用程式將不再支援 \"DHL 進口帳號\" (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br><br>請您使用網上工具 <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> 製作你的提單。<br><br>Effective from 1 December 2021, this application will not support \"DHL Import Express\" account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br><br>Please use our online tool <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create your waybills.', 350 )\n";
} else {
	print "dhl_alert('useless', 'The sender account no. is invalid', '由2021年12月1日起，此應用程式將不再支援 \"DHL 進口帳號\" (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br><br>請您使用網上工具 <a href=\"https://mydhl.express.dhl/hk/zh/ship/solutions.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> 製作你的提單。<br><br>Effective from 1 December 2021, this application will not support \"DHL Import Express\" account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br><br>Please use our online tool <a href=\"https://mydhl.express.dhl/hk/en/ship/solutions.html\" target=\"mydhl\" rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create your waybills.', 350 )\n";
}
		
print <<END1;		
		flag = 'false'
	}

END1

if ($Form{origin} eq 'MCA') {
  #print "else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && (!((form.dhl_acc_no.value.substring(0,2)== '64') || (form.dhl_acc_no.value.substring(0,2) == '96') || (form.dhl_acc_no.value.substring(0,2) == '95') || (form.dhl_acc_no.value.substring(0,2) == '94')))) {";
  print "else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && (!(form.dhl_acc_no.value.substring(0,2)== '64'))) {";
} else {
  #print "else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && (!((form.dhl_acc_no.value.substring(0,2)== '63') || (form.dhl_acc_no.value.substring(0,2) == '96') || (form.dhl_acc_no.value.substring(0,2) == '95') || (form.dhl_acc_no.value.substring(0,2) == '94')))) {";
  print "else if ((checkEmpty(form.dhl_acc_no)) && (isNum(form.dhl_acc_no.value)) && (!(form.dhl_acc_no.value.substring(0,2)== '63'))) {";
}

print <<END1;	
		form.dhl_acc_no.focus()
		form.dhl_acc_no.select()
		dhl_alert("useless", "The sender account no. is invalid", "Please enter a valid sender account no.", 180 )
		flag = 'false'
	}
        else if (!checkEmpty(form.send_name)) {
                form.send_name.focus()
                form.send_name.select()
		dhl_alert("useless", "The name of the sender is missing", "Please enter the name of the sender.", 180)
                flag = 'false'
        }

        else if (!(isAlphaNum(form.send_name.value))) {
	    	form.send_name.focus()
		form.send_name.select()
		dhl_alert("useless", "The name of the sender is invalid", "Please enter the name of the sender in English with no tabs.", 180 )
		flag = 'false'
	}

	else if (!(isAlphaNum(form.reference.value))) {
	    	form.reference.focus()
		form.reference.select()
		dhl_alert("useless", "The sender's reference is invalid", "Please enter a valid sender's reference.", 180 )
		flag = 'false'
	}
	else if (!checkEmpty(form.send_company)) {
                form.send_company.focus()
                form.send_company.select()
                dhl_alert("useless", "The sender company name is missing", "Please enter sender company name.", 180)
                flag = 'false'
        }

        else if (!(isAlphaNum(form.send_company.value))) {
	    	form.send_company.focus()
		form.send_company.select()
		dhl_alert("useless", "The sender company name is invalid", "Please enter the sender company name in English with no tabs.", 180 )
		flag = 'false'
	}

        else if (!checkEmpty(form.send_address1)) {
                form.send_address1.focus()
                form.send_address1.select()
                dhl_alert("useless", "The sender address on line 1 is missing", "Please start entry of sender address on line 1.", 180)
                flag = 'false'
        }

        else if (!(isAlphaNum(form.send_address1.value))) {
	    	form.send_address1.focus()
		form.send_address1.select()
		dhl_alert("useless", "The sender address on line 1 is invalid", "Please enter the sender address line 1 in English with no tabs.", 180 )
		flag = 'false'
	}
	/*
	else if ((charge_to_option == -1) && !(form.charge_by.checked) && !checkEmpty(form.dhl_acc_no) && !checkEmpty(form.charge_to_account)) {    
		dhl_alert("useless", "Information is missing", "Please fill in Charge to, Cash Shipments, Payer Account No. or Sender Account no.")
		flag = 'false'
	}
	*/
	else if (!(isAlphaNum(form.send_address2.value))) {
	    	form.send_address2.focus()
		form.send_address2.select()
		dhl_alert("useless", "The sender address on line 2 is invalid", "Please enter the sender address line 2 in English with no tabs.", 180 )
		flag = 'false'
	}
	else if (!(isAlphaNum(form.send_address3.value))) {
	    	form.send_address3.focus()
		form.send_address3.select()
		dhl_alert("useless", "The sender address on line 3 is invalid", "Please enter the sender address line 3 in English with no tabs.", 180 )
		flag = 'false'
	}

	
	else if (!(isAlphaNum(form.send_pc.value))) {
	    	form.send_pc.focus()
		form.send_pc.select()
		dhl_alert("useless", "The sender postcode is invalid", "Please enter a valid sender postcode.", 180 )
		flag = 'false'
	}
	else if (!checkEmpty(form.send_tel)) {
                form.send_tel.focus()
                form.send_tel.select()
                dhl_alert("useless", "Sender Phone/Fax/Email is missing", "Please enter the Sender Phone/Fax/Email.", 180)
                flag = 'false'
        }
        else if (!(isAlphaNum(form.send_tel.value))) {
	    	form.send_tel.focus()
		form.send_tel.select()
		dhl_alert("useless", "Sender Phone/Fax/Email is invalid", "Please enter a valid Sender Phone/Fax/Email.", 180 )
		flag = 'false'
	}
	else if ((!(isValidPhone(form.send_tel.value))) && (!(form.send_media[2].checked))) {
	    	form.send_tel.focus()
		form.send_tel.select()
		dhl_alert("useless", "Sender Phone/Fax is invalid", "Please enter a valid Sender Phone/Fax.", 180 )
		flag = 'false'		
	}
	else if ((form.send_tel.value.length > 18) && (!(form.send_media[2].checked))) {
	    	form.send_tel.focus()
		form.send_tel.select()
		dhl_alert("useless", "Sender Phone/Fax is invalid", "Please enter a Sender Phone/Fax no longer than 18 characters limit.", 180 )
		flag = 'false'		
	}
	else if ((!isEmail(form.send_tel.value)) && (form.send_media[2].checked)) {
	    	form.send_tel.focus()
		form.send_tel.select()
		dhl_alert("useless", "Sender Email is invalid", "Please enter a valid Sender Email.", 180 )
		flag = 'false'		
	}
	
	else if (!checkEmpty(form.consign_company)) {
                form.consign_company.focus()
                form.consign_company.select()
		dhl_alert("useless", "The receiver company name is missing", "Please enter the receiver company name.", 180)
                flag = 'false'
        }
        
    else if (containInvalidSymbol(form.consign_company.value)) {
                form.consign_company.focus()
                form.consign_company.select()
				dhl_alert("useless", "The receiver company name invalid", "Please enter the receiver company name with no invalid symbols.", 180)
                flag = 'false'
        }	
	
        else if ((!(isAlphaNum(form.consign_company.value))) && (form.consign_company.value.length > 25)) {
        	form.consign_company.focus()
		form.consign_company.select()
		dhl_alert("useless", "The receiver company name is invalid", "If you enter receiver company name in Chinese, please enter no longer than 25 characters limit.", 180 )
		flag = 'false'
	}
        
        /*
        else if (!(isAlphaNum(form.consign_company.value))) {
	    	form.consign_company.focus()
		form.consign_company.select()
		dhl_alert("useless", "The receiver company name is invalid", "Please enter the receiver company name in English with no tabs.", 180 )
		flag = 'false'
	}
	*/
        
	
       
        else if (!checkEmpty(form.consign_address1)) {
                form.consign_address1.focus()
                form.consign_address1.select()
		dhl_alert("useless", "The delivery address on line 1 is missing", "Please start entry of delivery address on line 1.", 180)
                flag = 'false'
        }
	/*	
		else if (!isChinese(form.consign_address1.value)) {
	    	form.consign_address1.focus()
		form.consign_address1.select()
		dhl_alert("useless", "The delivery address on line 1 is invalid", "Only Chinese delivery address line 1 is accepted.", 180 )
		flag = 'false'
	}
*/
		
		
        //else if ((!(isAlphaNum(form.consign_address1.value))) && (form.consign_address1.value.length > 25)) {
		else if (form.consign_address1.value.length > 25) {
        	form.consign_address1.focus()
		form.consign_address1.select()
		dhl_alert("useless", "The delivery address on line 1 is invalid", "Please enter no longer than 25 characters limit.", 180 )
		flag = 'false'
	}
/*	
	else if ((checkEmpty(form.consign_address2)) && (!isChinese(form.consign_address2.value))) {
	    	form.consign_address2.focus()
		form.consign_address2.select()
		dhl_alert("useless", "The delivery address on line 2 is invalid", "Only Chinese delivery address line 2 is accepted.", 180 )
		flag = 'false'
	}
*/
	
	//else if ((checkEmpty(form.consign_address2)) && (!(!isChinese(form.consign_address2.value))) && (form.consign_address2.value.length > 25)) {
	else if ((checkEmpty(form.consign_address2)) && (form.consign_address2.value.length > 25)) {
        	form.consign_address2.focus()
		form.consign_address2.select()
		dhl_alert("useless", "The delivery address on line 2 is invalid", "Please enter no longer than 25 characters limit.", 180 )
		flag = 'false'
	}
/*	
	else if ((checkEmpty(form.consign_address3)) && (!isChinese(form.consign_address3.value))) {
	    	form.consign_address3.focus()
		form.consign_address3.select()
		dhl_alert("useless", "The delivery address on line 3 is invalid", "Only Chinese delivery address line 3 is accepted.", 180 )
		flag = 'false'
	}
*/	
	//else if ((checkEmpty(form.consign_address3)) && (!(!isChinese(form.consign_address3.value))) && (form.consign_address3.value.length > 25)) {
	else if ((checkEmpty(form.consign_address3)) && (form.consign_address3.value.length > 25)) {
		form.consign_address3.focus()
		form.consign_address3.select()
		dhl_alert("useless", "The delivery address on line 3 is invalid", "Please enter no longer than 25 characters limit.", 180 )
		flag = 'false'
	}
        
    else if (!(isAlphaNum(form.consign_city.value))) {
	    	form.consign_city.focus()
		form.consign_city.select()
		dhl_alert("useless", "The city is invalid", "Please enter the city in English with no tabs.", 180 )
		flag = 'false'
	}
	
	else if (!(isAlphaNum(form.consign_pc.value))) {
	    	form.consign_pc.focus()
		form.consign_pc.select()
		dhl_alert("useless", "The postcode is invalid", "Please enter a valid postcode.", 180 )
		flag = 'false'
	}
	else if ((!checkEmpty(form.consign_city)) && (!checkEmpty(form.consign_pc))) {
		form.consign_city.focus()
		form.consign_city.select()
		dhl_alert("useless", "Both city and postcode are blank", "Please enter at least a postcode or a city.", 180 )
		flag = 'false'
	}	
	else if (!checkEmpty(form.consign_person)) {
                form.consign_person.focus()
                form.consign_person.select()
		dhl_alert("useless", "The name of the contact person is missing", "Please enter the name of the contact person.", 180)
                flag = 'false'
        }
	 else if (containInvalidSymbol(form.consign_person.value)) {
                form.consign_person.focus()
                form.consign_person.select()
				dhl_alert("useless", "The name of the contact person is invalid", "Please enter the contact name with no invalid symbols.", 180)
                flag = 'false'
        }	
		
        else if ((!(isAlphaNum(form.consign_person.value))) && (form.consign_person.value.length > 25)) {
        	form.consign_person.focus()
		form.consign_person.select()
		dhl_alert("useless", "The name of the contact person is invalid", "If you enter name of the contact person in Chinese, please enter no longer than 25 characters limit.", 180 )
		flag = 'false'
	}
        /*
        else if (!(isAlphaNum(form.consign_person.value))) {
	    	form.consign_person.focus()
		form.consign_person.select()
		dhl_alert("useless", "The name of the contact person is invalid", "Please enter the name of the contact person in English with no tabs.", 180 )
		flag = 'false'
	}	
	else if ((form.consign_tel.value.length > 18) && (!(form.consign_media[2].checked))) {
	    	form.consign_tel.focus()
		form.consign_tel.select()
		dhl_alert("useless", "Receiver Phone/Fax is invalid", "Please enter a Receiver Phone/Fax no longer than 18 characters limit.", 180 )
		flag = 'false'		
	}
	*/
	else if (!checkEmpty(form.consign_tel)) {
                form.consign_tel.focus()
                form.consign_tel.select()
		dhl_alert("useless", "Receiver Mobile/Landline is missing", "Please enter the Receiver Mobile/Landline.", 180)
                flag = 'false'
        }
        else if (!(isAlphaNum(form.consign_tel.value))) {        	
                form.consign_tel.focus()
                form.consign_tel.select()
		dhl_alert("useless", "Receiver Mobile/Landline is invalid", "Please enter a valid Receiver Mobile/Landline.", 180)
                flag = 'false'
        }
		else if (!(isValidPhone(form.consign_tel.value))) {        	
                form.consign_tel.focus()
                form.consign_tel.select()
		dhl_alert("useless", "Receiver Mobile/Landline is invalid", "Please enter a valid Receiver Mobile/Landline.", 180)
                flag = 'false'
        }             	
	else if ((form.consign_tel_cd[form.consign_tel_cd.selectedIndex].value + form.consign_tel.value).length > 18) {
		form.consign_tel.focus()
		form.consign_tel.select()
		dhl_alert("useless", "Receiver Mobile/Landline is invalid", "Please enter a Receiver Mobile/Landline including country code no longer than 18 characters limit.", 180 )
		flag = 'false'	
        }
	else if ((checkEmpty(form.consign_email)) && (!isEmail(form.consign_email.value))) {
	        form.consign_email.focus()
		form.consign_email.select()
		dhl_alert("useless", "Receiver Email is invalid", "Please enter a valid Receiver email.", 180 )
		flag = 'false'
        }
	
		
        if (flag == 'true') {
			if (navigator.appName == "Netscape"){
            	document.dhl.browser.value = "Netscape"
			}
			else{
				document.dhl.browser.value = "IE"
			}
			document.dhl.submit()
        }
}
// -->
function isInteger (s)

{   var i;
	var defaultEmptyOK;
	
    if (isEmpty(s)) 
       if (isInteger.arguments.length == 1) return defaultEmptyOK;
       else return (isInteger.arguments[1] == true);
    

    // Search through string's characters one by one
    // until we find a non-numeric character.
    // When we do, return false; if we don't, return true.

    for (i = 0; i < s.length; i++)
    {   
        // Check that current character is number.
        var c = s.charAt(i);

        if (!isDigit(c)) return false;
    }

    // All characters are numbers.
    return true;
}


function upd_tel_cd() {
  
  for (i=0; i<tel_cd_arr.length; i++){
     if (tel_cd_arr[i][0] == document.getElementById("consign_country").options[document.getElementById("consign_country").selectedIndex].value) {
        for (j=0; j<document.getElementById("consign_tel_cd").length; j++){
           if (document.getElementById("consign_tel_cd").options[j].value == tel_cd_arr[i][1]) {
              document.getElementById("consign_tel_cd").selectedIndex = j;
              j=document.getElementById("consign_tel_cd").length;
           }
        }
        
        i = tel_cd_arr.length;        
        
     }
  }

}




</script>
</head>

<body bgcolor=white>
<form name=dhl action=./cservice.cgi method=post>
<input type=hidden name=from_where value="not_dhl">
<input type=hidden name=paper_ty value="$Form{paper_ty}">
<input type=hidden name=origin value="$Form{origin}">
<input type=hidden name=sub_grp_id value="$Form{sub_grp_id}">
<input type=hidden name=browser>


END1

#get default value of the group
&get_connect("webdb");

$sql_def_str="select trim(charge_to),trim(charge_to_account),trim(dhl_acc_no),". 
	"trim(send_name),trim(send_company),trim(send_address1),trim(send_address2),trim(send_address3),trim(send_tel),trim(reference) ". 
	"from sf_default ". 
	"where grp_id = '" . $Form{sub_grp_id} . "'";

$sql_def=$web_db->prepare($sql_def_str) or die "Couldn't select from sf_default";
$sql_def->execute();

    $df_charge_to = "";
    $df_charge_to_account = "";
    $df_dhl_acc_no = "";
    $df_send_name = "";
    $df_send_company = "";
    $df_send_address1 = "";
    $df_send_address2 = "";
    $df_send_address3 = "";
    $df_send_tel = "";
    $df_send_ref = "";
    
    
while (@def_data=$sql_def->fetchrow_array()) {
  #for ($j=0; $j < @def_data; $j++) {
    $df_charge_to = $def_data[0];
    $df_charge_to_account = $def_data[1];
    $df_dhl_acc_no = $def_data[2];
    $df_send_name = $def_data[3];
    $df_send_company = $def_data[4];
    $df_send_address1 = $def_data[5];
    $df_send_address2 = $def_data[6];
    $df_send_address3 = $def_data[7];
    $df_send_tel = $def_data[8];
    $df_send_ref = $def_data[9];
  #}
}

print <<END1;

<table border=0 cellspacing=0 cellpadding=0>
<tr valign="top">
<td><img src="../../images/DHL_Ex_RGB.jpg" border=0></td>
<td width=15px>&nbsp;</td>
<td><font face="Frutiger, Arial" size=5><b>Homepage Shipment Form</b></font></td>
</tr>
<tr><td colspan=3><font size="1">&nbsp;</font></td></tr>
</table>

<!-- notice -->

<table border="0" width="915px">
<tr><td><font face="Frutiger, Arial" size="2">
<b><u>重要通告</u>: </b>
</font></td></tr>
<tr><td>
<font face="Frutiger, Arial" size="2" color="red"><b>
由於系統維​​護，此應用程式將於<u>2025年5月4日（星期日）上午8:00至9:00</u> 暫停使用。
</b></font><br><br>
<font face="Frutiger, Arial" size="2" color="red">
END1

if ($Form{origin} eq 'MCA') {
    print '此應用程式為舊有DHL系統，由2022年7月1日起，只接受寄往中國、香港或台灣的中文提單。';
} else {
	print '此應用程式為舊有DHL系統，由2022年7月1日起，只接受寄往中國、澳門或台灣的中文提單。';
}
print <<END1;
<br></font><font face="Frutiger, Arial" size="2">
此應用程式亦<b>不支援</b> "<b><u>DHL 進口帳號</u></b>" (即字首為95/96的帳號) 作為寄件或付款帳號 。<br><br>
如要享用全面服務，請立即註冊官方網上工具
END1

if ($Form{origin} eq 'MCA') {
    print '<a href="https://mydhl.express.dhl/mo/en/registration.html" target="mydhl" rel="noopener noreferrer">';
} else {
	print '<a href="https://mydhl.express.dhl/hk/zh/ship/solutions.html" target="mydhl" rel="noopener noreferrer">';
}

print <<END1;
<b>MyDHL+</b></a> 以製作你的提單。(<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf" target="reg_guide" rel="noopener noreferrer">註冊教學</a>)<br>
*如有任何疑問，請聯繫你的銷售代表或致電我們的技術支援熱線。*
</font></td></tr>
<tr><td><font face="Frutiger, Arial" size="2"><br>
<b><u>Important Notice</u>:</b>
</font></td></tr>
<tr><td>
<font face="Frutiger, Arial" size="2" color="red"><b>
Due to system maintenance, this application will be temporarily unavailable <u>from 8:00 a.m. to 9:00 a.m. on 4th May, 2025 (Sunday)</u>.
</b></font><br><br>
<font face="Frutiger, Arial" size="2" color="red">
END1
if ($Form{origin} eq 'MCA') {
    print 'With effective from 1st Jul, 2022, this legacy shipping application will ONLY support Chinese shipments to China, Hong Kong or Taiwan.';
} else {
	print 'With effective from 1st Jul, 2022, this legacy shipping application will ONLY support Chinese shipments to China, Macau or Taiwan.';
}
print <<END1;
<br></font><font face="Frutiger, Arial" size="2">
Also, this application <b>DOES NOT</b> support "<b><u>DHL Import Express</u></b>" account number (i.e. 95/96 prefix) as Shipper Account & Payer account.<br><br>
To enjoy the full service, please register our official online tool 
END1

if ($Form{origin} eq 'MCA') {
    print '<a href="https://mydhl.express.dhl/mo/en/registration.html" target="mydhl" rel="noopener noreferrer">';
} else {
	print '<a href="https://mydhl.express.dhl/hk/en/ship/solutions.html" target="mydhl" rel="noopener noreferrer">';
}

print <<END1;
<b>MyDHL+</b></a> to create your waybills. (<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf" target="reg_guide" rel="noopener noreferrer">Registration Guide</a>)<br>
*If there is any queries, please feel free to contact your sales representatives or our ESS hotline.*
</font></td></tr>
</table>
<br>
<!-- notice end -->

<TABLE border=1 cellSpacing=0 cellPadding=0 style="BORDER: windowtext 0.5pt solid">
<tr valign="top"><td width=450px>

<TABLE border=0 cellSpacing=0 cellPadding=0 width=450px>
<tr valign="top"><td height=80px>

<table cellspacing=0 cellpadding=3 border=0 width=100%>
<tr>
	<td bgcolor=#a60018 width=5 align=center><font color=white>1</font></td>
	<td bgcolor=#000000 width=445><font color=white><font face="Frutiger, Arial">Payment account number</font></td>
</tr>
<tr>
	<td colspan=2>
	<table cellspacing=0 cellpadding=0 border=0 height=20px>
	<tr>
		<td width=70><font size=-1><font face="Frutiger, Arial">Charge to</td>
		<td><font size=-1><font face="Frutiger, Arial">
END1
	if ($df_charge_to eq "SHIPPER") {
	   print '<input type=radio name=charge_to value="SHIPPER" checked onClick="javascript:enable_acc();"> Shipper ';
	} else {
	   print '<input type=radio name=charge_to value="SHIPPER" onClick="javascript:enable_acc();"> Shipper ';
	}
	
	if ($df_charge_to eq "RECEIVER") {
	   print '<input type=radio name=charge_to value="RECEIVER" checked onClick="javascript:enable_acc();"> Receiver ';
	} else {
	   print '<input type=radio name=charge_to value="RECEIVER" onClick="javascript:enable_acc();"> Receiver ';
	}
	
	if ($df_charge_to eq "OTHERS") {
	   print '<input type=radio name=charge_to value="OTHERS" checked onClick="javascript:enable_acc();"> 3rd party ';
	} else {
	   print '<input type=radio name=charge_to value="OTHERS" onClick="javascript:enable_acc();"> 3rd party ';
	}
	###cash shipments option is removed on 20200316 START
	#if ($df_charge_by eq "CASH") {
	#   print '<input type=radio name="charge_to" value="CASH" checked onClick="javascript:clear_acc();"> Cash Shipments';
	#} else {
	#   print '<input type=radio name="charge_to" value="CASH" onClick="javascript:clear_acc();"> Cash Shipments';
	#}
  ###cash shipments option is removed on 20200316 END	
print <<END1;
</font></font></td>
	</tr>
	</table>
	
	<table cellspacing=0 cellpadding=0 border=0 height=30px>
	<tr>
		<td width=125><font size=-1><font face="Frutiger, Arial">Payer Account No.</font></td>
		<td><font size=-1><font face="Frutiger, Arial">
END1
	if ($df_charge_to_account ne "") {
	  print '<input type=text name=charge_to_account size=45 maxlength=9 value="'.$df_charge_to_account.'" autocomplete="off">';
        } else {
          print '<input type=text name=charge_to_account size=45 maxlength=9 autocomplete="off">';
        }
print <<END1;		
</font></td>
	</tr>
	
	
	<tr>
		<td colspan=2><font size=-1><font face="Frutiger, Arial"></font></td>
	</tr>
	
	</table>
	</td>
</tr>
</table>

</td></tr>
<tr valign="top"><td width=450px>

<table cellspacing=0 cellpadding=3 border=0 width=450>
<tr>
	<td bgcolor=#a60018 width=5 align=center><font face="Frutiger, Arial"><font color=white>2</font></td>
	<td bgcolor=#000000 width=445><font color=white><font face="Frutiger, Arial">From (Sender) (in English)</font></td>
</tr>
<tr>
	<td colspan=2>
	<table cellspacing=0 cellpadding=0 border=0 width>
	<tr>
		<td><font size=-1><font face="Frutiger, Arial">Account No. *<br>

END1
		if ($df_dhl_acc_no ne "") {
		  print '<input type=text name="dhl_acc_no" size="28" maxlength=9 value="'.$df_dhl_acc_no.'" autocomplete="off">&nbsp;&nbsp;</td>';
		} else {
		  print '<input type=text name="dhl_acc_no" size="28" maxlength=9 autocomplete="off">&nbsp;&nbsp;</td>';
		}
print <<END1;
		
		<td align="right"><font size=-1><font face="Frutiger, Arial"><div align="left">Sender's Name *</div>

END1
		if ($df_send_name ne "") {
		  print '<input type=text name="send_name" size="30" maxlength=35 value="'.$df_send_name.'">&nbsp;';
		} else {
		  print '<input type=text name="send_name" size="30" maxlength=35>&nbsp;';
		}
print <<END1;
		
		<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"></td>
	</tr>
	<tr>
		<td colspan=2><font size=-1><font face="Frutiger, Arial">Sender's Reference<br>
END1
		if ($df_send_ref ne "") {
		  print '<input type=text name="reference" size="66" maxlength=36 value="'.$df_send_ref.'">&nbsp;';
		} else {
		  print '<input type=text name="reference" size="66" maxlength=36>&nbsp;';
		}
print <<END1;
		<img src="../../images/awb/i.gif" alt="Maximum input: 36 characters. The first 12 characters will be shown on invoice." title="Maximum input: 36 characters. The first 12 characters will be shown on invoice."></td>
	</tr>
	<tr>
		<td colspan=2><font size=-1><font face="Frutiger, Arial">Company Name *<br>
END1
		if ($df_send_company ne "") {
		  print '<input type=text name="send_company" size="66" maxlength=35 value="'.$df_send_company.'">&nbsp;';
		} else {
		  print '<input type=text name="send_company" size="66" maxlength=35>&nbsp;';
		}
print <<END1;		
		<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"></td>
	</tr>
	<tr>
		<td colspan=2><font size=-1><font face="Frutiger, Arial">Address *<br>

END1
		if ($df_send_address1 ne "") {
		  print '<input type=text name="send_address1" size="66" maxlength="35" value="'.$df_send_address1.'">&nbsp;';
		} else {
		  print '<input type=text name="send_address1" size="66" maxlength="35">&nbsp;';
		}
	        print '<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"><br>';
	        if ($df_send_address2 ne "") {
		  print '<input type=text name="send_address2" size="66" maxlength="35" value="'.$df_send_address2.'">&nbsp;';
		} else {
		  print '<input type=text name="send_address2" size="66" maxlength="35">&nbsp;';
		}
		print '<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"><br>';
		if ($df_send_address3 ne "") {
		  print '<input type=text name="send_address3" size="66" maxlength="35" value="'.$df_send_address3.'">&nbsp;';
		} else {
		  print '<input type=text name="send_address3" size="66" maxlength="35">&nbsp;';
		}
		print '<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"><br>';

if ($Form{origin} eq 'MCA') {
  print "Macau";
} else {
  print "Hong Kong";
}
print <<END1;
		</td>
	</tr>
	
	<input type="hidden" name="send_pc" value="">
	<tr>
		<td valign=bottom colspan=2><font size=-1><font face="Frutiger, Arial">
		<input type=radio name="send_media" value="Tel" checked onClick="javascript:document.getElementById('send_tel_div').style.visibility='visible';">Phone
		<input type=radio name="send_media" value="Fax" onClick="javascript:document.getElementById('send_tel_div').style.visibility='visible';">Fax
		<input type=radio name="send_media" value="Email" onClick="javascript:document.getElementById('send_tel_div').style.visibility='hidden';">Email *
		<br>
END1
		if ($df_send_tel ne "") {
		 print '<input type=text name="send_tel" size="66" maxlength=25 value="'.$df_send_tel.'">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 18 characters for Phone/Fax; 25 characters for Email" title="Maximum input: 18 characters for Phone/Fax; 25 characters for Email">';
		} else {
		  print '<input type=text name="send_tel" size="66" maxlength=25>&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 18 characters for Phone/Fax; 25 characters for Email" title="Maximum input: 18 characters for Phone/Fax; 25 characters for Email">';
		}
print <<END1;


<div id="send_tel_div" style="visibility:visible">
<font size=-2><i>(country code + phone number e.g. +852 XXXX XXXX)</i></font>
</div>
		</td>
	</tr>
	</table>
	</td>
</tr>
</table>

</td></tr>
</table>


</td>
<td>


END1

print "<table cellspacing=0 cellpadding=3 border=0 width=100%>\n";
	print "<tr>\n";
	print "<td bgcolor=#a60018 width=5 align=center><font face=\"Frutiger, Arial\"><font color=white>3</font></td>\n";
	print "<td bgcolor=#000000 width=445><font face=\"Frutiger, Arial\"><font color=white>To (Receiver)</font></td>\n";
	print "</tr>\n";
	print "</table>\n";

print <<END1;

	
	<table cellspacing=0 cellpadding=3 border=0 width=450>
	<tr>
		<td colspan=2>
		<table cellspacing=0 cellpadding=0 border=0 width>
		<tr>
			<td colspan=2><font face="Frutiger, Arial"><font size=-1>Company Name *<br>
			<input type=text name="consign_company" size="66" maxlength=45 value="$company1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 45 characters for English; 25 characters for Chinese" title="Maximum input: 45 characters for English; 25 characters for Chinese">
			</td>
		</tr>
		<tr>
			<td colspan=2><font face="Frutiger, Arial"><font size=-1>Delivery Address * <i>&nbsp;&nbsp;&nbsp;&nbsp;<font color=#a60018>DHL cannot deliver to a PO Box</font></i><br>
			<input type=text name=consign_address1 size="66" maxlength=45 value="$address11">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 25 characters for Chinese" title="Maximum input: 25 characters for Chinese"><br>
			<input type=text name=consign_address2 size="66" maxlength=45 value="$address21">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 25 characters for Chinese" title="Maximum input: 25 characters for Chinese"><br>
			<input type=text name=consign_address3 size="66" maxlength=45 value="$address31">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 25 characters for Chinese" title="Maximum input: 25 characters for Chinese"><br>
		</td>
		</tr>
		<tr>				
			<td colspan=2 valign="bottom" align="left"><font face="Frutiger, Arial"><font size=-1><div align="left">Country or Territory *</div><select id="consign_country" name="consign_country" onChange="javascript:upd_tel_cd();">
END1

$jjj = 0;

foreach $c (@new_arr){	
	$tmp = $new_arr[$jjj];
	$toskip = 0;
	if (($tmp eq "HK") && ($Form{origin} eq 'HKG')) {
	  $toskip = 1;
	}
	if (($tmp eq "MO") && ($Form{origin} eq 'MCA')) {
	  $toskip = 1;
	}
	
     if ($toskip == 0) {  
	if ($c eq "$country1"){
		print "<option value=\"$c\" selected>$country_list{$tmp}</option>\n";
	}
	else{
		print "<option value=\"$c\">$country_list{$tmp}</option>\n";
	}
     }
	$jjj = $jjj + 1;
}

print <<END1;

			</select>&nbsp;&nbsp;</td>
		</tr>
		
		<tr><td colspan=2><font face="Frutiger, Arial"><font size=-1>
			City (in English)<br>
			<input type=text text id="consign_city" name="consign_city" size="66" maxlength=35 value="$city1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 35 characters" title="Maximum input: 35 characters"></td>
		</tr>
		<tr>
			<td colspan=2><font face="Frutiger, Arial"><font size=-1>Postcode (in English)<br>			    
			<input type=text id="consign_pc" name="consign_pc" size="20" maxlength=12 value="$pc1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum search result is 1000 records. Pls narrow down the searching by inputting more characters." title="Maximum search result is 1000 records. Pls narrow down the searching by inputting more characters."></td>
			
		</tr>

		<tr valign="top">
			<td valign="bottom"><font face="Frutiger, Arial">
			<font size=-1>Contact Person *<br><input type=text name="consign_person" size="20" maxlength=45 value="$person1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 45 characters for English; 25 characters for Chinese" title="Maximum input: 45 characters for English; 25 characters for Chinese">&nbsp;
			</td>

END1

print <<END1;
<td align="left"><input type="hidden" name="consign_media" value="Tel">
<font size=-1><font face="Frutiger, Arial">Mobile (preferred) / Landline *</font></font><br>
			<select name="consign_tel_cd" id="consign_tel_cd">
END1

foreach $t (@tel_code){
	if ($t eq "$tel_cd1"){
	     print "<option value=\"$t\" selected>$t</option>\n";
	} else {
	     print "<option value=\"$t\">$t</option>\n";	
	}
}
print <<END1;		
			</select>
			<input type=text name="consign_tel" size="23" maxlength=16 value="$tel1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 18 characters" title="Maximum input: 18 characters"></td></tr>
			<tr><td></td><td>

<font size=-1><font face="Frutiger, Arial">Email</font></font><br>
<input type=text name="consign_email" size="39" maxlength="45" value="$email1">&nbsp;<img src="../../images/awb/i.gif" alt="Maximum input: 45 characters" title="Maximum input: 45 characters">

		</td>
		</tr>
		</table>
		</td>
	</tr>
	</table>


</td></tr>
</table>


<br>
<a href="javascript:checking(document.dhl)" onMouseOver="objPIC3.MouseOver()" onMouseOut ="objPIC3.MouseOut()"><img src="../../images/next1a.gif" border=0 name=PIC3></a>
<br><br><font size=-1><font face="Frutiger, Arial">* Mandatory input</font></font>

<input type="hidden" name="sub_grp_id" value="$Form{sub_grp_id}">


</form>
</body>
<script LANGUAGE="javascript" SRC="../../js_client/copyright_r.js"></script>


<script type="text/javascript">
  function findValue(li) {
  	if( li == null ) return alert("No match!");

  	// if coming from an AJAX call, let's use the CityId as the value
  	if( !!li.extra ) var sid = li.extra[0];

  	// otherwise, let's just display the value in the text box
  	else var sValue = li.selectValue;

\$('#consign_pc').val(sid);
\$('#consign_city').val(li.selectValue);
  	//alert("The value you selected was: " + li.selectValue);
  }
  function findValue2(li) {
  	if( li == null ) return alert("No match!");

  	// if coming from an AJAX call, let's use the CityId as the value
  	if( !!li.extra ) var sid = li.extra[0];

  	// otherwise, let's just display the value in the text box
  	else var sValue = li.selectValue;

\$('#consign_city').val(sid);
\$('#consign_pc').val(li.selectValue);
  	//alert("The value you selected was: " + li.selectValue);
  }
  function selectItem(li) {
    	findValue(li);
  }
function selectItem2(li) {
    	findValue2(li);
  }
  function formatItem(row) {
//return row[0] ;
    	return row[0] + " : " + row[1] + "";
  }

    function formatItem2(row) {
	//return row[0] ;
    	return row[1] + " : " + row[0] + "";
  }
  function lookupAjax(){
  	var oSuggest = \$("#consign_city")[0].autocompleter;
    oSuggest.findValue();
  	return false;
  }

  function lookupLocal(){
    	var oSuggest = \$("#consign_city")[0].autocompleter;

    	oSuggest.findValue();

    	return false;
  }
  


\$(function(){
  


    \$("#consign_country").change(function(){
        \$("#consign_city").autocomplete(
      "states.cgi?type=C&country="+document.dhl.consign_country.value,
      {
  			delay:400,
  			minChars:2,
  			matchSubset:false,
  			matchContains:1,
  			cacheLength:1,
  			onItemSelect:selectItem,
  			onFindValue:findValue,
  			formatItem:formatItem,
			maxItemsToShow:1000,
			foundInCache:false,
  			autoFill:false
  		}
    );
	 \$("#consign_pc").autocomplete(
      "states.cgi?type=P&country="+document.dhl.consign_country.value,
      {
  			delay:400,
  			minChars:1,
  			matchSubset:false,
  			matchContains:1,
  			cacheLength:1,
  			onItemSelect:selectItem2,
  			onFindValue:findValue2,
  			formatItem:formatItem2,
			maxItemsToShow:1000,
			foundInCache:false,
  			autoFill:false
  		}
    );
    }).change();
});
END1

if ($Form{origin} eq 'MCA') {
    print 'window.open("../../info/notice_decomm_mo.html", "Decommission Notice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=750,height=400,left=0,top=0").focus();';
} else {
    print 'window.open("../../info/notice_decomm_cn.html", "Decommission Notice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=750,height=400,left=0,top=0").focus();';
}

print <<END1;

</script>

</html>

END1

}

