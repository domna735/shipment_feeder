#!/usr/bin/perl

use CGI::Cookie;
my %cookies = CGI::Cookie->fetch;
my $session_token = $cookies{'SESSIONID'} ? $cookies{'SESSIONID'}->value : '';
unless (is_valid_session($session_token)) {
    my $q = CGI->new;
    print $q->redirect('toLogin.html');
    exit;
}


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

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


use lib '/appl/service/webapps/cgi-bin/';
use db_con;
use CGI;
$> =$<;
$) = $(;

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
	$value =~ s/\"/&quot;/g;
	$Form{$name} = $value;
}

if (!defined $ENV{'HTTP_REFERER'}) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if (($ENV{'HTTP_REFERER'} eq '') || (index($ENV{'HTTP_REFERER'}, "?") != -1) || 
        (($ENV{'HTTP_REFERER'} ne 'https://apps.dhl.com.hk/cgi-bin/csender.cgi') &&
         ($ENV{'HTTP_REFERER'} ne 'https://mykullstc000536.apis.dhl.com/cgi-bin/hkapp/csender.cgi'))) {	
  	
	 my $q = CGI->new;	
     print $q->redirect('csender.cgi');
	 exit();
	 #$d=1;
}

if ($ENV{'QUERY_STRING'} ne '') {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
  
}

#input validation

if (($Form{charge_to} ne 'SHIPPER') && ($Form{charge_to} ne 'RECEIVER') && ($Form{charge_to} ne 'OTHERS') && ($Form{charge_to} ne 'CASH')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if ($Form{charge_to} ne 'CASH') {
 if (($Form{dhl_acc_no} eq '') && ($Form{charge_to_account} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
 }
}

if ($Form{dhl_acc_no} ne '') {
 $Form{dhl_acc_no} = uc($Form{'dhl_acc_no'});
 if ((length($Form{dhl_acc_no}) > 9) || ($Form{dhl_acc_no} =~ m/[^A-Z0-9]/)) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
 } else {
	if ($Form{dhl_acc_no} =~ /\D/) {
	  $d=1;
	} else {
	  if (substr($Form{dhl_acc_no},0,1) ne "6") {
		my $q = CGI->new;
		print $q->redirect('csender.cgi');
		exit();
	  }
	}
 }
}



if ($Form{charge_to_account} ne '') {
 $Form{charge_to_account} = uc($Form{'charge_to_account'});
 if ((length($Form{charge_to_account}) > 9) || ($Form{charge_to_account} =~ m/[^A-Z0-9]/)) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
 } else {
	if ($Form{charge_to_account} =~ /\D/) {
	  $d=1;
	} else {
	  if (substr($Form{charge_to_account},0,1) ne "6") {
		my $q = CGI->new;	
		print $q->redirect('csender.cgi');
		exit();
	  }
	} 
 }
 
}

if (($Form{send_name} eq '') || ($Form{send_company} eq '') || ($Form{send_address1} eq '') || ($Form{send_media} eq '') || ($Form{send_tel} eq '') || 
   ($Form{consign_company} eq '') || ($Form{consign_address1} eq '') || ($Form{consign_country} eq '') || ($Form{consign_person} eq '') || 
   ($Form{consign_media} eq '') || ($Form{consign_tel_cd} eq '') || ($Form{consign_tel} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if (($Form{consign_city} eq '') && ($Form{consign_pc} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}


if ((($Form{reference} ne '') && ((length($Form{reference}) > 36) || ($Form{reference} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_name} ne '') && ((length($Form{send_name}) > 45) || ($Form{send_name} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_company} ne '') && ((length($Form{send_company}) > 45) || ($Form{send_company} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_address1} ne '') && ((length($Form{send_address1}) > 45) || ($Form{send_address1} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_address2} ne '') && ((length($Form{send_address2}) > 45) || ($Form{send_address2} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_address3} ne '') && ((length($Form{send_address3}) > 45) || ($Form{send_address3} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) ||
  (($Form{send_tel} ne '') && ($Form{send_media} ne 'Email') && ((length($Form{send_tel}) > 18) || ($Form{send_tel} =~ m/[^0-9\/ ()\-+]/))) ||
  (($Form{send_tel} ne '') && ($Form{send_media} eq 'Email') && ((length($Form{send_tel}) > 25) || ($Form{send_tel} =~ m/[^a-zA-Z0-9@&\-_.]/))) ||
  #(($Form{consign_person} ne '') && ((length($Form{consign_person}) > 45) || ($Form{consign_person} =~ m/[^a-zA-Z0-9\/ `~!@#^&()-_+{}:',.]/))) ||
  #(($Form{consign_company} ne '') && ((length($Form{consign_company}) > 45) || ($Form{consign_company} =~ m/[^a-zA-Z0-9\/ `~!@#^&()-_+{}:',.]/))) ||
  #(($Form{consign_address1} ne '') && ((length($Form{consign_address1}) > 45) || ($Form{consign_address1} =~ m/[^a-zA-Z0-9\/ `~!@#^&()-_+{}:',.]/))) ||
  #(($Form{consign_address2} ne '') && ((length($Form{consign_address2}) > 45) || ($Form{consign_address2} =~ m/[^a-zA-Z0-9\/ `~!@#^&()-_+{}:',.]/))) ||
  #(($Form{consign_address3} ne '') && ((length($Form{consign_address3}) > 45) || ($Form{consign_address3} =~ m/[^a-zA-Z0-9\/ `~!@#^&()-_+{}:',.]/))) ||
  (($Form{consign_pc} ne '') && ((length($Form{consign_pc}) > 12) || ($Form{consign_pc} =~ m/[^a-zA-Z0-9 \-]/))) ||
  (($Form{consign_city} ne '') && ((length($Form{consign_city}) > 35) || ($Form{consign_city} =~ m/[^a-zA-Z0-9\/ &()\-_',.]/))) ||
  (($Form{consign_country} ne '') && ((length($Form{consign_country}) != 2) || ($Form{consign_country} =~ m/[^A-Z]/))) ||
  (($Form{consign_tel_cd} ne '') && ((length($Form{consign_tel_cd}) > 8) || ($Form{consign_tel_cd} =~ m/[^0-9\-+]/))) ||
  (($Form{consign_tel} ne '') && (length($Form{consign_tel_cd}) + length($Form{consign_tel_cd}) > 18)) ||
  (($Form{consign_tel} ne '') && ($Form{consign_tel} =~ m/[^0-9\/ ()\-+]/)) ||
  (($Form{consign_email} ne '') && ((length($Form{consign_email}) > 45) || ($Form{consign_email} =~ m/[^a-zA-Z0-9@&\-_.]/))) ) {
	   
  my $q = CGI->new;
  print $q->redirect('csender.cgi');
  exit();
}  

if (($Form{consign_address1} ne '') && ($Form{consign_address1} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/)) {
	if ($Form{consign_address1} =~ m/[\$%\*\=\;\<\>\?\\\"]/) {
	my $q = CGI->new;
	print $q->redirect('csender.cgi');
	exit();
	  } 
}

if (($Form{consign_address2} ne '') && ($Form{consign_address2} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/)) {
  if ($Form{consign_address2} =~ m/[\$%\*\=\;\<\>\?\\\"]/) {
	my $q = CGI->new;
    print $q->redirect('csender.cgi');
    exit();
  } 
}

if (($Form{consign_address3} ne '') && ($Form{consign_address3} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/)) {
  if ($Form{consign_address3} =~ m/[\$%\*\=\;\<\>\?\\\"]/) {
	my $q = CGI->new;
    print $q->redirect('csender.cgi');
    exit();
  } 
}

if (($Form{consign_country} ne 'CN') && ($Form{consign_country} ne 'TW') && ($Form{consign_country} ne 'MO') && ($Form{consign_country} ne 'HK')) {
	my $q = CGI->new;
    print $q->redirect('csender.cgi');
    exit();
}

##########

@new_arr = (
'AL',
'DZ',
'AS',
'AD',
'AO',
'AI',
'AG',
'AR',
'AM',
'AW',
'AU',
'AT',
'AZ',
'BS',
'BH',
'BD',
'BB',
'BY',
'BE',
'BZ',
'BJ',
'BM',
'BT',
'BO',
'XB',
'BA',
'BW',
'BR',
'BN',
'BG',
'BF',
'BI',
'KH',
'CM',
'CA',
'IC',
'CV',
'KY',
'CF',
'TD',
'CL',
'CN',
'CO',
'KM',
'CG',
'CD',
'CK',
'CR',
'CI',
'HR',
'CU',
'XC',
'CY',
'CZ',
'DK',
'DJ',
'DM',
'DO',
'TL',
'EC',
'EG',
'SV',
'ER',
'EE',
'ET',
'FK',
'FO',
'FJ',
'FI',
'FR',
'GF',
'GA',
'GM',
'GE',
'DE',
'GH',
'GI',
'GR',
'GL',
'GD',
'GP',
'GU',
'GT',
'GG',
'GN',
'GW',
'GQ',
'GY',
'HT',
'HN',
'HK',
'HU',
'IS',
'IN',
'ID',
'IR',
'IQ',
'IE',
'IL',
'IT',
'JM',
'JP',
'JE',
'JO',
'KZ',
'KE',
'KI',
'KR',
'KV',
'KW',
'KG',
'LA',
'LV',
'LB',
'LS',
'LR',
'LY',
'LI',
'LT',
'LU',
'MO',
'MK',
'MG',
'MW',
'MY',
'MV',
'ML',
'MT',
'MH',
'MQ',
'MR',
'MU',
'YT',
'MX',
'FM',
'MD',
'MC',
'MN',
'ME',
'MS',
'MA',
'MZ',
'MM',
'NA',
'NR',
'NP',
'NL',
'XN',
'NC',
'NZ',
'NI',
'NE',
'NG',
'NU',
'KP',
'NO',
'OM',
'PK',
'PW',
'PA',
'PG',
'PY',
'PE',
'PH',
'PL',
'PT',
'PR',
'QA',
'RE',
'RO',
'RU',
'RW',
'MP',
'WS',
'SM',
'ST',
'SA',
'SN',
'RS',
'SC',
'SL',
'SG',
'SK',
'SI',
'SB',
'SO',
'XS',
'ZA',
'SS',
'ES',
'LK',
'XY',
'XE',
'KN',
'LC',
'XM',
'VC',
'SR',
'SZ',
'SE',
'CH',
'SY',
'PF',
'TW',
'TJ',
'TZ',
'TH',
'TG',
'TO',
'TT',
'TN',
'TR',
'TC',
'TV',
'UG',
'UA',
'AE',
'GB',
'US',
'UY',
'UZ',
'VU',
'VE',
'VN',
'VG',
'VI',
'YE',
'ZM',
'ZW');

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
"TJ" => "Tajikistan",
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

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


#check if non-numeric sender a/c and payer a/c are on pre-defined account list

$err_msg = "";

if ($Form{dhl_acc_no} ne "") {
 if ($Form{dhl_acc_no} =~ /\D/) { 
  $Form{dhl_acc_no} = uc($Form{'dhl_acc_no'});
  if (isFOC_CASH($Form{dhl_acc_no}) == 0) {
      $err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
  }
 } else {
  #if (!(($Form{origin} eq "MCA") && (substr($Form{dhl_acc_no},0,2) eq "64"))) {
   if (isColoader($Form{dhl_acc_no}) == 1) {
      $err_msg = $err_msg . "You are not authorized to use this tool.<br><br>";
   } else {
	  if (isBlacklist($Form{dhl_acc_no}) == 1) {
		$err_msg = $err_msg . "You are not authorized to use this account. Contact the account owner to obtain authorization.<br><br>";
	  } else {	    
	   if (validate_ac($Form{dhl_acc_no}) == 0) {
		  $err_msg = $err_msg . "Sender account no. is invalid or has stopped credit.<br><br>";
	   } 
	   # else {	     
	   #   if (validate_billed_ac($Form{dhl_acc_no}, $Form{origin}) == 0) {
	   #     $err_msg = $err_msg . '由<b>2021年9月1日</b>起，此應用程式將不再支援 "<b>DHL 進口帳號</b>" (即字首為95/96的帳號) 作為寄件人帳號 。<br>請您使用"<b>DHL 出口帳號</b>" 作為寄件人帳號，或註冊使用網上工具 <a href="https://mydhl.express.dhl/hk/zh/ship/solutions.html" target="mydhl" rel="noopener noreferrer"><b>MyDHL+</b></a>製作你的提單。 (<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf" target="reg_guide" rel="noopener noreferrer">註冊教學</a>)<br><br>';
	   #     $err_msg = $err_msg . 'Effective from <b>1 September 2021</b>, this application will not support "<b>DHL Import Express</b>" account number (i.e. 95/96 prefix) as Shipper accounts.<br>Please use "<b>DHL Export</b>" account number as Shipper account, or please register our online tool <a href="https://mydhl.express.dhl/hk/en/ship/solutions.html" target="mydhl" rel="noopener noreferrer"><b>MyDHL+</b></a> to create your waybills. (<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf" target="reg_guide" rel="noopener noreferrer">Registration Guide</a>)<br><br>';
	   #   }
	   #}
	   
	  }
   }
  #} 
 }
}

if ($Form{charge_to_account} ne "") {
 if ($Form{charge_to_account} =~ /\D/) { 
  $Form{charge_to_account} = uc($Form{'charge_to_account'});
  if (isFOC_CASH($Form{charge_to_account}) == 0) {
      $err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
  }
 } else {
  #if (!(($Form{origin} eq "MCA") && (substr($Form{charge_to_account},0,2) eq "64"))) {
   if (isColoader($Form{charge_to_account}) == 1) {
      $err_msg = $err_msg . "You are not authorized to use this tool.<br><br>";
   } else {
	  if (isBlacklist($Form{charge_to_account}) == 1) {
		$err_msg = $err_msg . "You are not authorized to use this account. Contact the account owner to obtain authorization.<br><br>";
	  } else {
	   if (validate_ac($Form{charge_to_account}) == 0) {
		  $err_msg = $err_msg . "Payer account no. is invalid or has stopped credit.<br><br>";
	   }
	  }
   }
  #} 
 }
}


#check if destination code can be generated
$err = 0;

$country_code = uc($Form{consign_country});

$Form{consign_city} = trim($Form{consign_city});
$Form{consign_city} = replace_spaces($Form{consign_city});

$Form{consign_pc} = trim($Form{consign_pc});
$Form{consign_pc} = replace_spaces($Form{consign_pc});

$in_city='';
#if ($Form{consign_address3} ne '') {
#  $in_city=uc($Form{consign_address3});
#}

if ($Form{consign_city} ne '') {
  $in_city=uc($Form{consign_city});
}

$in_pc='';
if ($Form{consign_pc} ne '') {
  $in_pc=uc($Form{consign_pc});  
}

#$in_station='';

#$station_code=`./label/get_stn.sh \"$country_code\" \"$in_pc\" \"$in_city\" \"$in_station\"`;
#$station_code =~ s/\s+$//;
	
#if (length($station_code) != 3) {
  #$err = 1;
  #$err_str = $station_code. "<br>Please input valid postcode of the country if it's available and city name.<br><br><input type=button name=back value=Back onClick='javascript:history.go(-1);'";
#}

#pre check for CN

if ($country_code eq 'CN') {
   if (($in_pc eq '') && ($in_city eq '')) {
   	$err = 1;
   } else {
      if ($in_pc ne '') {
      	 $chk_result = pre_check($country_code, $in_pc);
      	 if ($chk_result == 0) {
      	    $err = 1;
      	 }
      }
   }

}

#validate postcode pattern
if ($err == 0) {
  $param_pc=".";
  
  #check if the country has no postcode
  $with_pc = chk_ctry_pc($country_code);
  
  if ($in_pc ne '') {
     if ($with_pc eq 'Y') {
     	
       #validate postcode pattern and reformat postcode with no pattern  
       $param_pc = reformat_pc($country_code, $in_pc);
       if ($param_pc eq 'error') {
       	  $err = 1;
       }
     } else {
       $err = 1;
     }
  	
  } else {
     if ($with_pc eq 'Y') {
      	 $err = 1;
     }
  }

}

#validate and get destination info thro GLS with the minimum data fields
if ($err == 0) {
  
  $param_city=".";
  
  if ($in_city ne '') {
     $param_city = $in_city;
  }
  
  $param_str = $country_code."~".$param_pc."~".$param_city;
  $station_facility=`./label/gls_validate.sh \"$param_str\"`;
  $station_facility =~ s/\s+$//;
  
  #if ($validate_result ne 'true') {
  if ((length($station_facility) != 7) && (length($station_facility) != 4)) {
     $err = 1;
     $err_str = $station_facility;
  } else {
     @cd = split(/\|/,$station_facility);
     $station_code = $cd[0];
     $facility_code = $cd[1];
     if ($station_code eq "") {
     	$err = 1;
        $err_str = $station_facility;
     }
  }
  
  
  
}


#if ($err == 1) {
if (($err == 1) || ($err_msg ne "")) {
	
print <<END1;

<html>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<script language="JavaScript">
back1 = new Image
back2 = new Image

back1.src = '../../images/back1.gif'
back2.src = '../../images/back2.gif'

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

objPIC5 = new objMouseChangeImg('PIC5', back2.src, back1.src);
</script>

<body bgcolor=white>
<center><br><Br><b>
<!--$err_str-->
<font face="Arial" size="2">
END1

if ($err_msg ne "") {
   print $err_msg;
}

if ($err == 1) {
print <<END1;
Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).
<br><br>
You may take a reference in this <a href="../../postcode2/$country_code.html" target='postcode' rel="noopener noreferrer">list</a>.
<br><br>
END1
}
print <<END1;
</font>
</b>
<!--<input type=button name=back value=Back onClick='javascript:history.go(-1);'>-->
<a href="javascript:history.go(-1);" onMouseOver="objPIC5.MouseOver()" onMouseOut ="objPIC5.MouseOut()"><img src="../../images/back1.gif" border=0 name=PIC5></a>
</center>
</body>
<script LANGUAGE="javascript" SRC="../../js_client/copyright_a.js"></script>
</html>

END1

exit();
}

print <<END1;

<html>
<head><title>DHL Waybill Printing</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
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
<!--<script LANGUAGE="javascript" SRC="../../js_client_eng_hws/eng_bp_FormCheck.js"></script>-->

<script language="JavaScript">

<!--

if (browserOK) {
printa1 = new Image
printa2 = new Image
reset_1 = new Image
reset_2 = new Image
printc1 = new Image
printc2 = new Image
receiver1 = new Image
receiver2 = new Image
back1 = new Image
back2 = new Image
com1 = new Image
com2 = new Image

printa1.src = '../../images/confirm1.jpg'
printa2.src = '../../images/confirm2.jpg'
reset_1.src = '../../images/reset_1.gif'
reset_2.src = '../../images/reset_2.gif'
printc1.src = '../../images/printc1.gif'
printc2.src = '../../images/printc2.gif'
receiver1.src = '../../images/awb/receiver1.gif'
receiver2.src = '../../images/awb/receiver2.gif'
back1.src = '../../images/back1.gif'
back2.src = '../../images/back2.gif'
com1.src = '../../images/addupd_com1.jpg'
com2.src = '../../images/addupd_com2.jpg'
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

objPIC1 = new objMouseChangeImg('PIC1', printc2.src, printc1.src);
objPIC2 = new objMouseChangeImg('PIC2', reset_2.src, reset_1.src);
objPIC3 = new objMouseChangeImg('PIC3', printa2.src, printa1.src);
objPIC4 = new objMouseChangeImg('PIC4', receiver2.src, receiver1.src);
objPIC5 = new objMouseChangeImg('PIC5', back2.src, back1.src);
objPIC6 = new objMouseChangeImg('PIC6', com2.src, com1.src);

function disable_duties(flag) {
END1

  if ($Form{charge_to} ne "CASH") {
print <<END1;
  	
  var radios = document.dhl.dest_duties;

  for (var i=0, iLen=radios.length; i<iLen; i++) {
    radios[i].disabled = flag;
    if (flag) {
      radios[i].checked = false;
    }
  }
  document.dhl.dest_other.disabled=flag;
  if (flag) {
      document.dhl.dest_other.value="";
  }
END1
  } else {
print <<END1;       
  document.dhl.dest_duties.disabled=flag;
  if (flag) {
    document.dhl.dest_duties.checked = false;
  }
END1
  }
print <<END1;
}

function disable_declare(flag) {
   
  if (flag) {
    document.dhl.declare_value.value="";
    document.dhl.declare_currency.selectedIndex=0;
  }
  
  document.dhl.declare_value.disabled=flag;
  document.dhl.declare_currency.disabled=flag;

}

function switch_insur(sel_prod) {
	if (sel_prod == "D") {
	    document.getElementById('ext_display').style.visibility='visible';
	    document.getElementById('ship_insurance').checked=false;
	    document.getElementById('ship_insur_value').value='';
	    document.getElementById('sii_display').style.visibility='hidden';
		document.getElementById('contents_desc').value='';
	} else {
	    document.getElementById('sii_display').style.visibility='visible';
	    document.getElementById('ext').checked=false;
	    document.getElementById('ext_display').style.visibility='hidden';
		document.getElementById('contents_desc_doc_oth').value="";
        document.getElementById('contents_desc_doc_oth').disabled=true;
	    document.getElementById("contents_desc_doc").selectedIndex = 0;		
	}		
}	

function showfield(sel_desc){
  if(sel_desc=='OTHERS') {    
    document.getElementById('contents_desc_doc_oth').disabled=false;
  } else {
    document.getElementById('contents_desc_doc_oth').value="";
    document.getElementById('contents_desc_doc_oth').disabled=true;
  }	
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

function isNumAndDecimal(passedVal) {
    var decimal = ""
    for (var c = 0; c < passedVal.length; c++){
    	var oneChar = passedVal.charAt(c)
    	if (oneChar == "." && c == 0) {
        	return false
        }
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

function popWindow(){
	URL = '../../faq/airwaybill.html'
	remote = window.open(URL, 'remote', 'width=640,height=620,scrollbars=yes');
}

function checkEmpty(theField)
{
    v = theField.value;
	v = v.replace(/[\\n\\r]+/g,'');
    while(''+v.charAt(0)==' ')v=v.substring(1,v.length);
    while(v.charAt(v.length-1)+''==' ')v=v.substring(0,v.length-1);

    if ((v=='.') || (v==',') || (v=='')) return false;
    else return true;
}

function onDC_lst(instr)
{
 DC_lst = create_DG_lst ();
 var textfound=0;
 for (var i=0; i<DC_lst.length; i++) {
	if (myTrim(instr.toLowerCase()).indexOf(myTrim(DC_lst[i].toLowerCase())) != -1) {
		i=DC_lst.length;
		textfound=1;
	}
 }
 return textfound;
}

function onRED_lst(instr)
{
 RED_lst = create_RED_lst ();
 var textfound=0;
 for (var i=0; i<RED_lst.length; i++) {
	//if (myTrim(instr.toLowerCase()).indexOf(RED_lst[i].toLowerCase()) != -1) {
	if (myTrim(instr.toLowerCase()) == myTrim(RED_lst[i].toLowerCase())) {
		i=RED_lst.length;
		textfound=1;
	}
 }
 return textfound;
}

function onPNR_lst(instr)
{
 PNR_lst = create_PNR_lst ();
 var textfound=0;
 for (var i=0; i<PNR_lst.length; i++) {
	//if (myTrim(instr.toLowerCase()).indexOf(PNR_lst[i].toLowerCase()) != -1) {
	if (myTrim(instr.toLowerCase()) == myTrim(PNR_lst[i].toLowerCase())) {
		i=PNR_lst.length;
		textfound=1;
	}
 }
 return textfound;
}

function checking(form) {
	var flag = 'true'
   	var getit = -1
   	var getit2 = -1

 var flag = 'true'
 
 if (form.consign_country.value=="IQ") {
   if (form.ship_product_dtl[form.ship_product_dtl.selectedIndex].value != "EXPRESS WORLDWIDE") {
      return dhl_alert("", "Invalid Value", "Only Express Worldwide is available for Iraq, please select service again.", 180);
   }
 }

END1

print <<END1;
    for (j=0; j<form.ship_product.length; j++) {
      if (form.ship_product[j].checked) {
	getit = j
      }
    }

    if (getit == -1) {
        form.ship_product[0].focus()
		dhl_alert("useless", "Service is missing", "Please select International Document or Non-Document for the service.", 180)
        flag = 'false'
    }
    else if (!isNumAndDecimal(form.ship_insur_value.value)) {
		form.ship_insur_value.focus()
		form.ship_insur_value.select()
		dhl_alert("useless", "Invalid insurance value", "Please enter the insurance value in numbers.", 180)
		flag = 'false'
    }
    else if ((!(form.ship_insurance.checked)) && (form.ship_insur_value.value != "")) {
	form.ship_insurance.focus()
	form.ship_insurance.select()
	dhl_alert("useless", "The tick box is not marked", "Please click 'Yes' tick box for shipment insurance.", 180)
	flag = 'false'
    }
    else if (((form.ship_insurance.checked)) && (form.ship_insur_value.value == "")) {
	form.ship_insurance.focus()
	form.ship_insurance.select()
	dhl_alert("useless", "The insured value is not entered", "Please enter insured value.", 180)
	flag = 'false'
    }
	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc").selectedIndex == 0)) {
	  document.getElementById("contents_desc_doc").focus()
	  dhl_alert("useless", "Full description of content is not selected", "Please select full description of content.", 180)
	  flag = 'false'
	}

	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc")[document.getElementById("contents_desc_doc").selectedIndex].value == "OTHERS") && (!checkEmpty(form.contents_desc_doc_oth))) {
	  document.getElementById("contents_desc_doc_oth").focus()
	  dhl_alert("useless", "Full description of content is missing", "Please enter the full description of content.", 180)
	  flag = 'false'
	}
	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc")[document.getElementById("contents_desc_doc").selectedIndex].value == "OTHERS") && (!isAlphaNum(form.contents_desc_doc_oth.value))) {
	  document.getElementById("contents_desc_doc_oth").focus()
	  dhl_alert("useless", "Full description of content is invalid", "Please enter the full description of content in English with no tabs.", 180)
	  flag = 'false'
	}
	
	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc")[document.getElementById("contents_desc_doc").selectedIndex].value == "OTHERS") && (onDC_lst(form.contents_desc_doc_oth.value) == 1)) {
		document.getElementById("contents_desc_doc_oth").focus()
		dhl_alert("useless", "Full description of content is invalid", "This application cannot support the preparation of shipment carrying &#8220;Lithium Batteries&#8221;.<br><br>Please contact your Sales Manager for assistance.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc")[document.getElementById("contents_desc_doc").selectedIndex].value == "OTHERS") && (onRED_lst(form.contents_desc_doc_oth.value) == 1)) {
		document.getElementById("contents_desc_doc_oth").focus()
		dhl_alert("useless", "Full description of content is invalid", "Acceptable Goods Descriptions include complete information, providing sufficient detail about the precise nature of goods in plain language.<br><br>It should indicate what the goods are, for which purpose the goods are used and what is made of.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[0].checked) && (document.getElementById("contents_desc_doc")[document.getElementById("contents_desc_doc").selectedIndex].value == "OTHERS") && (onPNR_lst(form.contents_desc_doc_oth.value) == 1)) {
		document.getElementById("contents_desc_doc_oth").focus()
		dhl_alert("useless", "Full description of content is invalid", "Your shipping items are either Prohibited or Restricted items, they will NOT be accepted for carriage by DHL or unless otherwise agreed to by DHL.<br><br>Please contact your Sales Manager for assistance.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[1].checked) && (!checkEmpty(form.contents_desc))){
	    form.contents_desc.focus()
	    form.contents_desc.select()
	    dhl_alert("useless", "Full description of content is missing", "Please enter the full description of contents.", 180)
	    flag = 'false'
	}
    else if ((form.ship_product[1].checked) && (!(isAlphaNum(form.contents_desc.value)))) {
	form.contents_desc.focus()
	form.contents_desc.select()
	dhl_alert("useless", "Full description of content is invalid", "Please enter the full description of content in English with no tabs.", 180 )
	flag = 'false'
    }
	else if ((form.ship_product[1].checked) && (form.contents_desc.value.replace(/[\\n\\r]+/g,'').length > 120)) {
	form.contents_desc.focus()
	form.contents_desc.select()
	dhl_alert("useless", "Full description of content is invalid", "Please enter the full description of content no longer than maximum limit of 120 characters.", 180 )
	flag = 'false'
	}
	
	else if ((form.ship_product[1].checked) && (onDC_lst(form.contents_desc.value) == 1)) {
		form.contents_desc.focus()
		form.contents_desc.select()
		dhl_alert("useless", "Full description of content is invalid", "This application cannot support the preparation of shipment carrying &#8220;Lithium Batteries&#8221;.<br><br>Please contact your Sales Manager for assistance.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[1].checked) && (onRED_lst(form.contents_desc.value) == 1)) {
		form.contents_desc.focus()
		form.contents_desc.select()
		dhl_alert("useless", "Full description of content is invalid", "Acceptable Goods Descriptions include complete information, providing sufficient detail about the precise nature of goods in plain language.<br><br>It should indicate what the goods are, for which purpose the goods are used and what is made of.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[1].checked) && (onPNR_lst(form.contents_desc.value) == 1)) {
		form.contents_desc.focus()
		form.contents_desc.select()
		dhl_alert("useless", "Full description of content is invalid", "Your shipping items are either Prohibited or Restricted items, they will NOT be accepted for carriage by DHL or unless otherwise agreed to by DHL.<br><br>Please contact your Sales Manager for assistance.", 260 )
		flag = 'false'
	}
	
	else if ((form.ship_product[1].checked) && (!checkEmpty(form.declare_value))){
	    form.declare_value.focus()
	    form.declare_value.select()
	    dhl_alert("useless", "Declared Value is missing", "Please enter the declared value.", 180)
	    flag = 'false'
	}    
	//else if (!isNum(document.dhl.declare_value.value)){
	else if (!isNumAndDecimal(document.dhl.declare_value.value)){
		form.declare_value.focus()
		form.declare_value.select()
		dhl_alert("useless", "Invalid declared value", "Please enter the declared value in numbers.", 180)
		flag = 'false'
	}
	else if ((!isEmpty(document.dhl.declare_value.value)) && (isNumAndDecimal(document.dhl.declare_value.value)) && (document.dhl.declare_value.value <= 0)) {
		form.declare_value.focus()
		form.declare_value.select()
		dhl_alert("useless", "Invalid declared value", "Please enter the declared value.", 180)
		flag = 'false'
	}
END1

print <<END1;
	
	else if (!(isAlphaNum(form.commodity_code.value))) {
	    	form.commodity_code.focus()
		form.commodity_code.select()
		dhl_alert("useless", "Harmonised commodity code is invalid", "Please enter a valid harmonised commodity code", 180 )
		flag = 'false'
	}
	else if ((form.dest_duties[2] != null) && (!form.dest_duties[2].checked) && (checkEmpty(form.dest_other))){
		form.dest_other.focus()
	    form.dest_other.select()
	    dhl_alert("useless", "Destination Duties/Taxes option is invalid", "No need to input the field 'Other' of Destination Duties/Taxes if you do not select 'Other'.", 180)
	    flag = 'false'
	}
	else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (!checkEmpty(form.dest_other))){
	    form.dest_other.focus()
	    form.dest_other.select()
	    dhl_alert("useless", "Field 'Other' of Destination Duties/Taxes is missing", "Please enter the field 'Other' of Destination Duties/Taxes.", 180)
	    flag = 'false'
	}
	else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (checkEmpty(form.dest_other)) && (!(isNum(form.dest_other.value)))){
	   	    form.dest_other.focus()
		    form.dest_other.select()
		    dhl_alert("useless", "Field 'Other' of Destination Duties/Taxes is invalid", "Please enter a valid DHL Account Number in the field 'Other' of Destination Duties/Taxes.", 180)
		    flag = 'false'
	}

END1

if ($Form{origin} eq 'MCA') {
  #print "else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (checkEmpty(form.dest_other)) && ((isNum(form.dest_other.value))) && (!((form.dest_other.value.substring(0,2)== '64') || (form.dest_other.value.substring(0,2) == '96') || (form.dest_other.value.substring(0,2) == '95') || (form.dest_other.value.substring(0,2) == '94')))) {";
  print "else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (checkEmpty(form.dest_other)) && ((isNum(form.dest_other.value))) && (!(form.dest_other.value.substring(0,2)== '64'))) {";
} else {
  #print "else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (checkEmpty(form.dest_other)) && ((isNum(form.dest_other.value))) && (!((form.dest_other.value.substring(0,2)== '63') || (form.dest_other.value.substring(0,2) == '96') || (form.dest_other.value.substring(0,2) == '95') || (form.dest_other.value.substring(0,2) == '94')))) {";
  print "else if ((form.dest_duties[2] != null) && (form.dest_duties[2].checked) && (checkEmpty(form.dest_other)) && ((isNum(form.dest_other.value))) && (!(form.dest_other.value.substring(0,2)== '63'))) {";
}

print <<END1;	
	    form.dest_other.focus()
	    form.dest_other.select()
	    dhl_alert("useless", "Field 'Other' of Destination Duties/Taxes is invalid", "Please enter a valid DHL Account Number in the field 'Other' of Destination Duties/Taxes.", 180)
	    flag = 'false'		
	}
	
	
		else if (isEmpty(document.dhl.ship_qty.value)){
			form.ship_qty.focus()
			form.ship_qty.select()
			dhl_alert("useless", "The total number of packages is missing", "Please enter the total number of packages.", 180)
			flag = 'false'
		}
		else if (!isNum(document.dhl.ship_qty.value)){
			form.ship_qty.focus()
			form.ship_qty.select()
			dhl_alert("useless", "Invalid shipment packages", "Please enter shipment packages in numbers.", 180)
			flag = 'false'
		}
		else if ((isNum(document.dhl.ship_qty.value)) && (document.dhl.ship_qty.value <= 0)){
			form.ship_qty.focus()
			form.ship_qty.select()
			dhl_alert("useless", "Invalid shipment packages", "Please enter at least 1 shipment package.", 180)
			flag = 'false'
		}
END1

#if (substr($Form{sub_grp_id},0,3) eq 'PWC') {
if (($Form{sub_grp_id} eq 'PWC1') || ($Form{sub_grp_id} eq 'PWC2') || ($Form{sub_grp_id} eq 'PWC3')) {
print <<END1;
		else if ((isNum(document.dhl.ship_qty.value)) && (document.dhl.ship_qty.value > 1)){
			form.ship_qty.focus()
			form.ship_qty.select()
			dhl_alert("useless", "More than 1 shipment piece", "Please use other e-tool if total number of packages is more than 1 piece.", 180)
			flag = 'false'
		}
END1
}

print <<END1;
		
		else if (isEmpty(document.dhl.ship_weight.value)) {
			form.ship_weight.focus()
			form.ship_weight.select()
			dhl_alert("useless", "The total weight is missing", "Please enter the total weight.", 180)
			flag = 'false'
		}
		else if (!isNumAndDecimal(document.dhl.ship_weight.value)){
			form.ship_weight.focus()
			form.ship_weight.select()
			dhl_alert("useless", "Invalid shipment weight", "Please enter shipment weight in numbers.", 180)
			flag = 'false'
		}
		else if (document.dhl.ship_weight.value > 3000){
			form.ship_weight.focus()
			form.ship_weight.select()
			//dhl_alert("useless", "For shipment of 1000kg or above", "Please call our 24-hours Customer Service Hotline on 2400 3388 for special arrangement", 180)
			//dhl_alert("useless", "Invalid total weight", "The total weight cannot exceed 1000kg.", 180)
			dhl_alert("useless", "Invalid total weight", "The total weight cannot exceed 3000kg.", 180)
			flag = 'false'
		}
		else if (document.dhl.ship_qty.value <= 10) {
			var wght_limit = document.dhl.ship_qty.value * 300;
			if (document.dhl.ship_weight.value > wght_limit) {
				form.ship_weight.focus()
			    form.ship_weight.select()
			    dhl_alert("useless", "Invalid total weight", "The total weight cannot exceed " + wght_limit + "kg; For any piece's weight, it cannot exceed 300kg.", 180)
			    flag = 'false'
			}
		}
		
		
		if (flag == 'true') {
		  
		   	if (form.ship_product[1].checked) {
		   	    //if (!check_commodity()) {
		   	    if (form.item_list.value == "") {
		   	        dhl_alert("useless", "The commodity information is missing", "Please enter commodity information.", 180)
		   	    	flag = 'false'
			    } else {
			    	if (!chk_val_wght()) {
			    	    flag = 'false'
			    	} else {
			    	    if (!(isAlphaNum(document.getElementById("inv_num").value))) {
				   	document.getElementById("inv_num").focus()
				   	document.getElementById("inv_num").select()
					dhl_alert("useless", "The invoice number is invalid", "Please enter the invoice number in English with no tabs.", 180 )
					flag = 'false'
				    } else {
				    	if (!(isAlphaNum(document.getElementById("export_reason").value))) {
				   	  document.getElementById("export_reason").focus()
				   	  document.getElementById("export_reason").select()
					  dhl_alert("useless", "The reason of export is invalid", "Please enter the reason of export in English with no tabs.", 180 )
					  flag = 'false'
					}
				    } 
			    	
			        } 
			    	
			    }
		        }
		   
		}
		
		if (flag == 'true') {
		   if (form.agreetc.checked == false) {
		 	  form.agreetc.focus()
			  form.agreetc.select()
			  dhl_alert("useless", "Please tick the box if you have read and accept the Terms and Conditions, and Privacy Notice.", "Please enter again.", 180)
			  flag = 'false'
			 	
		   	
		   }
		}
	
END1

##

print <<END1;
   	if (flag == 'true') {
                        if (navigator.appName == "Netscape"){
                document.dhl.browser.value = "Netscape"
                        }
                        else{
                                document.dhl.browser.value = "IE"
                        }
                        document.dhl.submit()
        }
   //}
  //}
}

function show_rmk() {
  if (document.dhl.ship_product_dtl[document.dhl.ship_product_dtl.selectedIndex].value == "EXPRESS EASY") {
     document.getElementById('xe_rmk').style.visibility="visible";
  } else {
     document.getElementById('xe_rmk').style.visibility="hidden";
  }

}

//invoice item

function check_commodity() {
  
   var cflag = true;
  
   if (!checkEmpty(document.getElementById("item_desc"))) {
   	document.getElementById("item_desc").focus();
   	document.getElementById("item_desc").select();                
        dhl_alert("useless", "The commodity description is missing", "Please enter commodity description.", 180)
        cflag = false
   } else if (!(isAlphaNum(document.getElementById("item_desc").value))) {
   	document.getElementById("item_desc").focus();
   	document.getElementById("item_desc").select();                
	dhl_alert("useless", "The commodity description is invalid", "Please enter the commodity description in English with no tabs.", 180 )
	cflag = false
   } else if (isEmpty(document.getElementById("item_qty").value)) {
	document.getElementById("item_qty").focus();
   	document.getElementById("item_qty").select();
	dhl_alert("useless", "The commodity quantity is missing", "Please enter the commodity quantity.", 180)
	cflag = false
   } else if (!isNum(document.getElementById("item_qty").value)) {
	document.getElementById("item_qty").focus();
   	document.getElementById("item_qty").select();
	dhl_alert("useless", "Invalid commodity quantity", "Please enter commodity quantity in numbers.", 180)
	cflag = false
   } else if ((isNum(document.getElementById("item_qty").value)) && (document.getElementById("item_qty").value <= 0)){
	document.getElementById("item_qty").focus();
   	document.getElementById("item_qty").select();
	dhl_alert("useless", "Invalid commodity quantity", "Please enter at least 1 commodity quantity.", 180)
	cflag = false
   } else if (isEmpty(document.getElementById("unit_val").value)) {
	document.getElementById("unit_val").focus();
   	document.getElementById("unit_val").select();
	dhl_alert("useless", "The commodity unit value is missing", "Please enter the commodity unit value.", 180)
	cflag = false
   } else if (!isNumAndDecimal(document.getElementById("unit_val").value)){
	document.getElementById("unit_val").focus();
   	document.getElementById("unit_val").select();
	dhl_alert("useless", "Invalid commodity unit value", "Please enter the commodity unit value in numbers.", 180)
	cflag = false
   } else if ((isNumAndDecimal(document.getElementById("unit_val").value)) && (document.getElementById("unit_val").value <= 0)) {
	document.getElementById("unit_val").focus();
   	document.getElementById("unit_val").select();
	dhl_alert("useless", "Invalid commodity unit value", "Please enter valid commodity unit value.", 180)
	cflag = false
   } else if (isEmpty(document.getElementById("unit_wght").value)) {
	document.getElementById("unit_wght").focus();
   	document.getElementById("unit_wght").select();
	dhl_alert("useless", "The commodity unit weight is missing", "Please enter the commodity unit weight.", 180)
	cflag = false
   } else if (!isNumAndDecimal(document.getElementById("unit_wght").value)){
	document.getElementById("unit_wght").focus();
   	document.getElementById("unit_wght").select();
	dhl_alert("useless", "Invalid commodity unit weight", "Please enter the commodity unit weight in numbers.", 180)
	cflag = false
   } else if ((isNumAndDecimal(document.getElementById("unit_wght").value)) && (document.getElementById("unit_wght").value <= 0)) {
	document.getElementById("unit_wght").focus();
   	document.getElementById("unit_wght").select();
	dhl_alert("useless", "Invalid commodity unit weight", "Please enter valid commodity unit weight.", 180)
	cflag = false
   } else if (document.getElementById("item_origin").selectedIndex == 0) {
	document.getElementById("item_origin").focus();
   	//document.getElementById("item_origin").select();
   	dhl_alert("useless", "The commodity country or territory of origin is not selected", "Please select commodity country or territory of origin.", 180)
	cflag = false
   } else if (!(isAlphaNum(document.getElementById("item_commodity").value))) {
    	document.getElementById("item_commodity").focus();
   	document.getElementById("item_commodity").select();
	dhl_alert("useless", "The commodity code is invalid", "Please enter the commodity code in English with no tabs.", 180)
	cflag = false
   } else if ((document.getElementById("item_commodity").value.length != 0) && (document.getElementById("item_commodity").value.length < 2)) {
    	document.getElementById("item_commodity").focus();
   	document.getElementById("item_commodity").select();
	dhl_alert("useless", "The commodity code is invalid", "Please enter the commodity code with minimum 2 characters.", 180)
	cflag = false
   }
			   
   return cflag;
}	

function switch_inv(sel_prod) {
		
	if (sel_prod == "D") {
	    document.getElementById('div0').style.visibility='hidden';
	    
	    document.getElementById('item_list').value="";
	    document.getElementById('cur_item').value="";
	    
	    reloadTable();
	    
	    document.dhl.print_inv[0].checked=true;
	    document.dhl.print_inv[1].checked=false;
	    document.getElementById("inv_ty").selectedIndex = 0;
	    document.getElementById("inv_num").value = "";
	    document.getElementById("export_ty").selectedIndex = 0;
	    document.getElementById("export_reason").value = "";
	    document.getElementById("incoterm").selectedIndex = 3;
	    	    
	    document.getElementById('div2').style.position='absolute';
	    //document.getElementById('div2').style.top='300px';
	    document.getElementById('div2').style.top='200px';
	    
	} else {
	    //document.getElementById('div0').style.visibility='visible';
	    //document.getElementById('div0').style.position='relative';
	    //document.getElementById('div0').style.margin-left='5px';
	    
	    document.getElementById('div0').style.visibility='visible';
	    
	    document.getElementById('div2').style.visibility='visible';
	    document.getElementById('div2').style.position='relative';
	    document.getElementById('div2').style.top='0px';
	    document.getElementById("item_list").value = "";
	    
	    document.dhl.print_inv[0].checked=true;
	    document.dhl.print_inv[1].checked=false;
	    
	    
	}
}

function switch_incoterm(term_in) {
    for (t=0; t<document.getElementById("incoterm").options.length; t++) {
        if (document.getElementById("incoterm").options[t].value == term_in) {
          document.getElementById("incoterm").selectedIndex = t;
        }    
    }
}

function switch_dest_other() {
    
    if ((document.dhl.dest_duties[0].checked) || (document.dhl.dest_duties[1].checked)) {
	   document.dhl.dest_other.value="";
	   document.dhl.dest_other.disabled=true;
	} else {
	   document.dhl.dest_other.disabled=false;	
	}

}

function add_update() {
    
 //if ((document.getElementById("item_desc").value != "") && (document.getElementById("item_qty").value != "") && (document.getElementById("unit_val").value != "") && (document.getElementById("unit_wght").value != "")) {
 if (check_commodity()) {
   
    var itemArray = new Array();
    itemArray[0] = document.getElementById("item_desc").value;
    itemArray[1] = document.getElementById("item_qty").value;
    itemArray[2] = document.getElementById("unit_measure").options[document.getElementById("unit_measure").selectedIndex].value;
    itemArray[3] = document.getElementById("unit_val").value;
    itemArray[4] = document.getElementById("unit_wght").value;
    itemArray[5] = document.getElementById("item_origin").options[document.getElementById("item_origin").selectedIndex].value;
    itemArray[6] = document.getElementById("item_commodity").value;
 

    var itemString = itemArray.join("^~");
    //alert(itemString);
    
  
  if (document.getElementById("cur_item").value == "") {
    
    
    if (document.getElementById("item_list").value != "") {
       document.getElementById("item_list").value=document.getElementById("item_list").value + "^^" + itemString;
    } else {
       document.getElementById("item_list").value=itemString;
    }
    
    //alert(document.getElementById("item_list").value);
    
  
  } else {
  
    var itemlistArray = new Array();
    itemlistArray = document.getElementById("item_list").value.split("^^");
    itemlistArray[document.getElementById("cur_item").value] = itemString;
    
    document.getElementById("item_list").value=itemlistArray.join("^^");
    //alert(document.getElementById("item_list").value);
  
  }
  
  reloadTable();     
 } 
}

function edit (item_id) {

    //alert(item_id);
    
    document.getElementById("cur_item").value = item_id;
    
    var itemlistArray = new Array();
    itemlistArray = document.getElementById("item_list").value.split("^^");
    itemArray = itemlistArray[item_id].split("^~");
    
    document.getElementById("item_desc").value = itemArray[0];
    document.getElementById("item_qty").value = itemArray[1];
    
    
    for (u=0; u<document.getElementById("unit_measure").options.length; u++) {
        if (document.getElementById("unit_measure").options[u].value == itemArray[2]) {
          document.getElementById("unit_measure").selectedIndex = u;
        }
    
    }    
    
    document.getElementById("unit_val").value = itemArray[3]; 
    document.getElementById("unit_wght").value = itemArray[4];
    
    for (u=0; u<document.getElementById("item_origin").options.length; u++) {
        if (document.getElementById("item_origin").options[u].value == itemArray[5]) {
          document.getElementById("item_origin").selectedIndex = u;
        }
    
    }
    
    document.getElementById("item_commodity").value = itemArray[6];
    
    
}

function del (item_id) {

    //alert(item_id);
    
    var itemlistArray = new Array();
    itemlistArray = document.getElementById("item_list").value.split("^^");
    
    itemlistArray.splice(item_id,1)
    
    document.getElementById("item_list").value=itemlistArray.join("^^");
    
    //alert(document.getElementById("item_list").value);
    
    reloadTable();
    
}


function reloadTable () {
  
    var tbl_heading = "<table style='FONT-FAMILY:Arial;FONT-SIZE:12px;border: 1px solid #e4e4e4;padding:0px' rules='all' cellspacing='0' cellpadding='2' width='80%'><tr style='background-color : #F2F2F2;FONT-WEIGHT: bold;'><td valign='top'>Commodity Description</td><td valign='top'>Quantity</td><td valign='top'>Unit<br>Value<br>(<label id='unit_currency_hdr'>" + document.getElementById("declare_currency").value + "</label>)</td><td valign='top'>Sub-Total<br>Customs<br>Value<br>(<label id='unit_currency_sub_hdr'>" + document.getElementById("declare_currency").value + "</label>)</td><td valign='top'>Unit<br>Weight<br>(kg)</td><td valign='top' width=20>Edit Item</td><td valign='top' width=20>Delete Item</td></tr>";
    var tbl_end = "</table>";
    var tbl_content = "";
    var tbl_ttl = "";
      
    if (document.getElementById("item_list").value != "") {
      //var itemlistArray = new Array();
      itemlistArray = document.getElementById("item_list").value.split("^^");
      //alert(itemlistArray.length);
      
      var item_id = 0;
      var counter = 1;
      var tr = "";
      var ttl_qty = 0;
      var ttl_val = 0;
      var ttl_wght = 0;      
      
      for (var i=0; i<itemlistArray.length; i++) {
         
         itemArray = itemlistArray[i].split("^~");
         if (counter == 2) {
      		tr = "<tr style='background-color : #F2F2F2;'>";
      		counter = 1;
      	 } else {
      	 	tr = "<tr>";
      	 	counter++;
      	 	
      	 }
      	 
         tbl_content = tbl_content + tr + "<td>" + itemArray[0] + "</td><td>" + itemArray[1] + " " + itemArray[2] + "</td><td>" + itemArray[3] + "</td><td>" + Math.round((itemArray[1]*itemArray[3] * 100).toFixed(10)) /100 + "</td><td>" + itemArray[4] + "</td><td><a href='javascript:edit(" + item_id + ");'><img src='../../images/edit.png' border=0></a></td><td><a href='javascript:del(" + item_id + ");'><img src='../../images/del.png' border=0></a></td></tr>";
      	 item_id++;
      	 
      	 ttl_qty = ttl_qty + (itemArray[1]*1);
      	 
      	 ttl_val = ttl_val + (Math.round((itemArray[1]*itemArray[3] * 100).toFixed(10)) /100);
      	 ttl_wght = ttl_wght + (Math.round((itemArray[1]*itemArray[4] * 1000).toFixed(10)) /1000);
      	 
      }
      ttl_val = Math.round((ttl_val * 100).toFixed(10)) /100;
      ttl_wght = Math.round((ttl_wght * 1000).toFixed(10)) /1000;
      
    } else {
       tbl_content = "<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr>";
    }
    
    if (document.getElementById("item_list").value != "") {
       tbl_ttl = "<tr><td>&nbsp;</td><td colspan=3 nowrap>Total Customs Value: " + ttl_val + " <label id='ttl_currency'>" + document.getElementById("declare_currency").value + "</label></td><td colspan=3 nowrap>Total Weight: " + ttl_wght + " kg </td></tr>";
       tbl_ttl = tbl_ttl + "<tr><td>&nbsp;</td><td colspan=3 nowrap>Total Quantity: " + ttl_qty + "</td><td colspan=3>&nbsp;</td></tr>";
    }    
    
    document.getElementById('div1').innerHTML = tbl_heading + tbl_content + tbl_ttl + tbl_end;
     
    document.getElementById("item_desc").value = "";
    document.getElementById("item_qty").value = ""; 
    document.getElementById("cur_item").value = "";
    document.getElementById("unit_measure").selectedIndex = 9;
    document.getElementById("unit_val").value = ""; 
    document.getElementById("unit_wght").value = "";
    document.getElementById("item_origin").selectedIndex = 0;
    document.getElementById("item_commodity").value = "";
    
}

function upd_unit_currency () {
  document.getElementById("unit_currency").innerText = document.getElementById("declare_currency").value;
  document.getElementById("unit_currency_hdr").innerText = document.getElementById("declare_currency").value;
  document.getElementById("unit_currency_sub_hdr").innerText = document.getElementById("declare_currency").value;
  document.getElementById("ttl_currency").innerText = document.getElementById("declare_currency").value;
}



function chk_val_wght () {
   var com_val = 0;
   var com_wght = 0;
   var match_err = "";
   var shp_val = 0;
   var shp_wght = 0;
   var itemlistArray = new Array();
   var itemArray = new Array();
   
   if (document.dhl.ship_product[1].checked) {
   	if (document.getElementById("item_list").value != "") {
   	   itemlistArray = document.getElementById("item_list").value.split("^^");
   	   for (var i=0; i<itemlistArray.length; i++) {
   		itemArray = itemlistArray[i].split("^~");
   		com_val = com_val + (Math.round((itemArray[1]*itemArray[3] * 100).toFixed(10)) /100);
      	com_wght = com_wght + (Math.round((itemArray[1]*itemArray[4] * 1000).toFixed(10)) /1000);   		      	        
   	   }
	   com_val = Math.round((com_val * 100).toFixed(10)) /100;
       com_wght = Math.round((com_wght * 1000).toFixed(10)) /1000;
   	      
      	   shp_val = document.dhl.declare_value.value * 1;
      	   shp_wght = document.dhl.ship_weight.value * 1;
      	   
      	   //alert(com_val);
      	   //alert(shp_val);
      	   //alert(com_wght);
   	   //alert(shp_wght);
      	   
      	   if ((com_val != shp_val) && (com_wght > shp_wght)) {
      	     document.dhl.declare_value.focus();
	     document.dhl.declare_value.select();
      	     match_err = '<ul><li>"Shipment Declared Value" (in section 5) is not matched with "Invoice&#39;s Total Customs Value" (in section 7), please correct either one to give matched values.</li><br><br>';
      	     match_err += '<li>"Shipment Total Weight" (in section 6) is not matched with "Invoice&#39;s Total Weight" (in section 7), please correct either one to give matched values.</li></ul>';
      	     dhl_alert("useless", "Input Validation Alert", match_err, 320);
      	   
      	   } else {
      	     if (com_val != shp_val) {
      	   	document.dhl.declare_value.focus();
		document.dhl.declare_value.select();
      	   	match_err = '"Shipment Declared Value" (in section 5) is not matched with "Invoice&#39;s Total Customs Value" (in section 7), please correct either one to give matched values.';
      	   	dhl_alert("useless", "Input Validation Alert", match_err, 200);
      	     } 
      	   
      	     if (com_wght > shp_wght) {
      	   	document.dhl.ship_weight.focus();
		document.dhl.ship_weight.select();
      	   	match_err = '"Shipment Total Weight" (in section 6) is not matched with "Invoice&#39;s Total Weight" (in section 7), please correct either one to give matched values.';
      	   	dhl_alert("useless", "Input Validation Alert", match_err, 200);
      	     }
      	     
      	   }
      	   
   		
   	}   	
   }
    
   if (match_err != "") {
   	//match_err += " Please enter again.";
   	//dhl_alert("useless", "Input Validation Alert", match_err, 270);
   	return false;
   } else {
        return true;	
   }
   

}



//-->


</script>
</head>

<body bgcolor=white>
END1

print <<END1;
<form name=dhl action=./clabel.cgi method=post>
<input type=hidden name=from_where value="$Form{from_where}">
<input type=hidden name=paper_ty value="$Form{paper_ty}">
<input type=hidden name=origin value="$Form{origin}">
<input type=hidden name=dhl_acc_no value="$Form{dhl_acc_no}">
<input type=hidden name=send_name value="$Form{send_name}">
<input type=hidden name=reference value="$Form{reference}">
<input type=hidden name=send_company value="$Form{send_company}">
<input type=hidden name=send_address1 value="$Form{send_address1}">
<input type=hidden name=send_address2 value="$Form{send_address2}">
<input type=hidden name=send_address3 value="$Form{send_address3}">
<input type=hidden name=send_pc value="$Form{send_pc}">
<input type=hidden name=send_media value="$Form{send_media}">
<input type=hidden name=send_tel value="$Form{send_tel}">
<input type=hidden name=consign_company value="$Form{consign_company}">
<input type=hidden name=consign_address1 value="$Form{consign_address1}">
<input type=hidden name=consign_address2 value="$Form{consign_address2}">
<input type=hidden name=consign_address3 value="$Form{consign_address3}">
<input type=hidden name=consign_city value="$Form{consign_city}">
<input type=hidden name=consign_pc value="$param_pc">
<input type=hidden name=consign_country value="$Form{consign_country}">
<input type=hidden name=consign_person value="$Form{consign_person}">
<input type=hidden name=consign_media value="$Form{consign_media}">
<input type=hidden name=consign_tel value="$Form{consign_tel_cd}$Form{consign_tel}">
<input type=hidden name=consign_email value="$Form{consign_email}">
<input type=hidden name=charge_to_account value="$Form{charge_to_account}">
<input type=hidden name=charge_to value="$Form{charge_to}">
<input type=hidden name=charge_by value="$Form{charge_by}">
<!--<input type=hidden name=ship_insurance value="$Form{ship_insurance}">
<input type=hidden name=ship_insur_value value="$Form{ship_insur_value}">-->
<input type=hidden name=browser value="$Form{browser}">

<table border=0 cellspacing=0 cellpadding=0>
<tr valign="top">
<td><img src="../../images/DHL_Ex_RGB.jpg" border=0></td>
<td width=15px>&nbsp;</td>
<td><font face="Frutiger, Arial" size=5><b>Homepage Shipment Form</b></font></td>
</tr>
<tr><td colspan=3><font size="1">&nbsp;</font></td></tr>
</table>

<TABLE border=1 cellSpacing=0 cellPadding=0 style="BORDER: windowtext 0.5pt solid">
<tr valign="top"><td width=460px>

<TABLE border=0 cellSpacing=0 cellPadding=0 width=460px>
<tr valign="top"><td>


<table cellspacing=0 cellpadding=3 border=0 width=460px>
<tr>
	<td bgcolor=#a60018 width=3% align=center><font face="Frutiger, Arial"><font color=white>4</font></td>
	<td bgcolor=#000000 width=445><font color=white><font face="Frutiger, Arial">Shipment details<font size=-2>&nbsp;&nbsp;(Not all payment and service options are available in all countries)</font></td>
</tr>

<tr>
	<td colspan=2>
	<table cellspacing=0 cellpadding=0 border=0>
	
	<tr>
	
	<td valign=top><font face="Frutiger, Arial">

	<table cellspacing=0 cellpadding=0 border=0>
	<tr>
	
		<td valign="top" width="230px"><input type=radio name=ship_product value="DOCUMENT" onClick="javascript:disable_duties(true);disable_declare(true);switch_inv('D');switch_insur('D');"><font size=-1>International Document</font></td>
		<td valign="top" width="230p">
END1

if (isEU($Form{consign_country}) == 1) {
   print "<input disabled type=radio name=ship_product value=\"DUTIABLE PARCEL\" onClick=\"javascript:disable_duties(false);disable_declare(false);switch_inv('P');switch_insur('P');\">";
   print "<font size=-1>International Non-Document</font>";
   print "<br><font color=\"#FF0000\" size=-1>";
   #print "Not Applicable for EU Countries, please use <a href=\"https://mydhl.express.dhl/hk\" target=_blank rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create waybills for shipments to EU countries.</font>";   
   if ($Form{origin} eq 'MCA') {
     print "Not Applicable for EU Countries, please use <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=_blank rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create waybills for shipments to EU Countries.</font>";
   } else {
     print "Not Applicable for EU Countries, please use <a href=\"https://mydhl.express.dhl/hk\" target=_blank rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create waybills for shipments to EU Countries.</font>"; 
   }   
   
} elsif ($Form{consign_country} eq "ID") {
   #print "<div id='IDWPX' style='visibility:hidden'>";
   print "<input disabled type=radio name=ship_product value=\"DUTIABLE PARCEL\" onClick=\"javascript:disable_duties(false);disable_declare(false);switch_inv('P');switch_insur('P');\">";
   print "<font size=-1>International Non-Document</font>";
   #print "</div>";
   print "<br><font color=\"#FF0000\" size=-1>";
   
   if ($Form{origin} eq 'MCA') {
     print "Not Applicable for Indonesia, please use <a href=\"https://mydhl.express.dhl/mo/en/registration.html\" target=_blank rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create waybills for shipments to Indonesia.</font>";
   } else {
     print "Not Applicable for Indonesia, please use <a href=\"https://mydhl.express.dhl/hk\" target=_blank rel=\"noopener noreferrer\"><b>MyDHL+</b></a> to create waybills for shipments to Indonesia.</font>"; 
   }   
} else {
   print "<input type=radio name=ship_product value=\"DUTIABLE PARCEL\" onClick=\"javascript:disable_duties(false);disable_declare(false);switch_inv('P');switch_insur('P');\">";
   print "<font size=-1>International Non-Document</font>";
}


print <<END1;
		</td>
	</tr>
	</table>

	</td>
	
	</tr>
	
	<tr><td colspan=2></td></tr>
	
	<tr>
		<!--<td width=250 valign=top><font face="Frutiger, Arial"><b>Services</b><font size=-1>-->
		<td colspan=2 width=600 valign=top><font face="Frutiger, Arial"><font size=-1>Services
		(For details about DHL Express Services, please click <a href=\"http://www.dhl.com.hk/en/express/export_services.html\" target=_blank rel="noopener noreferrer">HERE</a>)<br>


<select name="ship_product_dtl" onchange="javascript:show_rmk();">
<option value="EXPRESS 0900">Express 9:00 #</option>
<option value="EXPRESS 1030">Express 10:30 #</option>
<option value="EXPRESS 1200">Express 12:00 #</option>
<option value="EXPRESS WORLDWIDE" selected>Express Worldwide</option>
<!--<option value="EXPRESS EASY">Express Easy (2-30KG)</option>-->
END1

if (($Form{charge_to} eq "CASH") || ((substr($Form{dhl_acc_no},0,4) eq "CASH") && ($Form{dhl_acc_no} ne "CASHHKGHX")) || ((substr($Form{charge_to_account},0,4) eq "CASH") && ($Form{charge_to_account} ne "CASHHKGHX"))) {
   print "<option value=\"EXPRESS EASY\">Express Easy (0.5-30KG) (^ see remark)</option>";
}

print <<END1;
</select>
<br><br>
#<i> Availability of the guaranteed services is subject to destination postcode, area name and shipment details.  Please call Customer Service Hotline at 2400-3388 to check for availability of service for your shipment.</i>
<div id="xe_rmk" align="left" style="visibility:hidden">
<br>^<i> Express Easy can only be used when you self-drop your shipment to DHL Express Service-Points. Please call Customer Service Hotline for any inquiry.</i>
</div>
</font></td>

  </tr>
	
	</table>
	</td>
</tr>

<tr><td colspan=2><font size=-1><font face="Frutiger, Arial">
<div id="ext_display" align="left" style="visibility:hidden">
<input type="checkbox" name="ext" id="ext" value="ON">Check this box to select Extended Liability (for Document only): In the rare event of physical loss or damage of your documents, DHL will compensate for the cost of recovery with a fixed lump sum of HKD3,500.00. Surcharge is applied with this service.
<br><br>
Full description of contents  *<br>
<select style='FONT-FAMILY : Arial;FONT-SIZE: 12px;' id="contents_desc_doc" name="contents_desc_doc" onchange="showfield(this.options[this.selectedIndex].value)">
<option value="">[Please select]</option>
<option value="BILL OF LADING">Bill of Lading</option>
<option value="CERTIFICATE">Certificate</option>
<option value="CHECK/CHEQUE">Check/Cheque</option>
<option value="CONTRACT">Contract</option>
<option value="CREDIT NOTE">Credit Note</option>
<option value="CREDIT/DEBIT CARD">Credit/Debit Card</option>
<option value="DIPLOMATIC MAIL">Diplomatic Mail</option>
<option value="DOCUMENTATION">Documentation</option>
<option value="DOCUMENTS">Documents</option>
<option value="IDENTITY DOCUMENT">Identity Document</option>
<option value="JOURNAL">Journal</option>
<option value="LETTER">Letter</option>
<option value="PRINTED MATTER">Printed Matter</option>
<option value="OTHERS">Others, please specify:</option>
</select>&nbsp;<input type="text" id="contents_desc_doc_oth" name="contents_desc_doc_oth" size="38" maxlength="120" disabled>

</div>
</font></td></tr>

<tr>
<td colspan=2><font size=-1><font face="Frutiger, Arial">

<div id="sii_display" align="left" style="visibility:hidden">
Shipment Insurance (for Non-Document)<br>
<input type="checkbox" name="ship_insurance" id="ship_insurance" value="ON"> Yes <i>Insured value </i><sup>##</sup>
&nbsp;&nbsp;&nbsp;<input type="text" name="ship_insur_value" id="ship_insur_value" size=30 maxlength=12>&nbsp;&nbsp; Local Currency
<br>
<sup>##</sup> <i>Please note that the "Insured Value" should be the same as the "Declared Value (see section 5)". Verify and convert the amount if the "Declared Value" is not using Local Currency (HKD).</i>
<br><br>
Full description of contents  *<br>
<textarea wrap=physical name="contents_desc" id="contents_desc" rows=3 style="width:423px"></textarea>
<img src="../../images/awb/i.gif" alt="Maximum input: 120 characters" title="Maximum input: 120 characters">
</div>

</font></td></tr>

</table>

</td></tr>
<tr valign="top"><td width=460px>


<table cellspacing=0 cellpadding=3 border=0 width=460>

<tr>
	<td bgcolor=#a60018 width=5 align=center><font face="Frutiger, Arial"><font color=white>5</font></td>
	<td bgcolor=#000000 width=445><font color=white><font face="Frutiger, Arial">Non-Document shipment only (Customs Requirements)</font></td>
</tr>

<tr>
	
	<td colspan=2>
	<font face="Frutiger, Arial"><!--<b>For International Non-Document only:</b><BR>-->
	<font size=-1><i>Attach two copies of a Proforma or Commercial invoice</i>
	</font></td>
</tr>
<tr>
	<td colspan=2>
	<table cellspacing=0 cellpadding=0 border=0>
	<tr>

	<td colspan=2><font face="Frutiger, Arial"><font size=-1>Declared Value for Customs <i>(as on commercial/proforma invoice)</i> *<br>
	<input type=text name=declare_value size=22 maxlength=12>
	<select name="declare_currency" id="declare_currency" onchange="javascript:upd_unit_currency();">
	<option value=HKD>HKD</option>
	<option value=USD>USD</option>
	<option value=EUR>EUR</option>
	<option value=JPY>JPY</option>
	<option value=GBP>GBP</option>
	<option value=NZD>NZD</option>
	<option value=AUD>AUD</option>
	<option value=CNY>CNY</option>
	</select>
	</font></td>
	
	
	<input type=hidden name=commodity_code value="">
	</tr>
	
	<input type=hidden name="export" value="">
	<tr>
		<td colspan=2><font face="Frutiger, Arial"><font size=-1>Destination duties/taxes
		<img src="../../images/awb/i.gif" alt="If left blank, then receiver pays duties/taxes." title="If left blank, then receiver pays duties/taxes.">
		
	</tr>
	<tr valign="top">
		<td><font face="Frutiger, Arial"><font size=-1>
		<input type=radio name="dest_duties" value=Receiver onClick="javascript:switch_incoterm('DAP');switch_dest_other();">Receiver&nbsp;&nbsp;&nbsp;&nbsp;
END1
	if ($Form{charge_to} ne "CASH") {

		print '<input type=radio name="dest_duties" value=Sender onClick="javascript:switch_incoterm(\'DDP\');switch_dest_other();">Sender&nbsp;&nbsp;&nbsp;&nbsp;';
		print '<input type=radio name="dest_duties" value=Other onClick="javascript:switch_incoterm(\'DDP\');switch_dest_other();">Other';
	}
		
	print'</font></td><td><font face="Frutiger, Arial">';
	
	if ($Form{charge_to} ne "CASH") {
		print '<input type=text name="dest_other" size=30 maxlength=9><br>';
		print '<font size=-2><i>Specify destination approved account number</i></font>';
	}

print <<END1;
		
		</td>			
	</tr>
	</table>
	</td>
</tr>
</table>


</td></tr></table>



</td>
<!-- size section-->
<td>

<table cellspacing=0 cellpadding=3 border=0 width=100%>
<tr>
        <td bgcolor=#a60018 width=5 align=center><font face="Frutiger, Arial"><font color=white>6</font></td>
        <td bgcolor=#000000 width=445><font face="Frutiger, Arial"><font color=white>Size and weight</font></td>
</tr>

<tr>
        <td colspan=2>
        <table cellspacing=0 cellpadding=0 border=0 width=100%>
        <tr>
                <td width=230><font face="Frutiger, Arial"><font size=-1><font face="Frutiger, Arial"><font size=-1>Total no. of Packages *<br><input type=text name=ship_qty size="33" maxlength=3></td>
                <td nowrap><font face="Frutiger, Arial"><font size=-1>Total Weight *<br><input type=text name=ship_weight size="30" maxlength=12>&nbsp;&nbsp;kg</td>
        </tr>
		<tr>
		<td colspan="2">
		<font face="Frutiger, Arial"><font size=-1><i>Each package must not over 300kg in weight and 300cm in Length/Width/Height.<br>Shipment not compliant to this will not be accepted.</i></font></font>
		</td>
		</tr>

        </table>
        </td>
</tr>

</table>


<br>


<div id="div0" style="position:relative;visibility:hidden">
<table cellspacing=0 cellpadding=3 border=0 width="100%">
<tr>
        <td bgcolor=#a60018 width=5 align=center><font face="Frutiger, Arial"><font color=white>7</font></td>
        <td bgcolor=#000000><font face="Frutiger, Arial"><font color=white>Commodity Information</font></td>
</tr>
</table>

<div id="div1" style="position:relative;margin-left:5px;margin-top:5px">
<table style='FONT-FAMILY:Arial;FONT-SIZE:12px;border: 1px solid #e4e4e4;padding:0px' rules='all' cellspacing='0' cellpadding='2'>
<tr style='background-color : #F2F2F2;FONT-WEIGHT: bold;'><td valign='top'>Commodity Description</td><td valign='top'>Quantity</td><td valign='top'>Unit<br>Value<br>(<label id='unit_currency_hdr'>HKD</label>)</td><td valign='top'>Sub-Total<br>Customs<br>Value<br>(<label id='unit_currency_sub_hdr'>HKD</label>)</td><td valign='top'>Unit<br>Weight<br>(kg)</td><td valign='top' width=20>Edit Item</td><td valign='top' width=20>Delete Item</td></tr>
<tr><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td><td>&nbsp;</td></tr></table>
</div>

<br>
<table border=0 style='FONT-FAMILY : Arial;FONT-SIZE: 12px;'>

<tr><td>Commodity Description *</td>
<td><input type="text" value="" name="item_desc" id="item_desc" size="45" maxlength="40"></td>
</tr>
<tr><td>Quantity *</td>
<td><input type="text" value="" name="item_qty" id="item_qty" maxlength="6">
<select style='FONT-FAMILY : Arial;FONT-SIZE: 12px;' id="unit_measure" name="unit_measure">
<option value="bag">bag</option>
<option value="box">box</option>
<option value="cm">cm</option>
<option value="doz">doz</option>
<option value="g">g</option>
<option value="kg">kg</option>
<option value="lb">lb</option>
<option value="m">m</option>
<option value="ml">ml</option>
<option value="pcs" selected>pcs</option>
</select>
</td>
</tr>

<tr><td>Unit Value *</td>
<td><input type="text" value="" name="unit_val" id="unit_val" maxlength="12"> <label id="unit_currency">HKD</label></td>
</tr>

<tr><td>Unit Weight *</td>
<td><input type="text" value="" name="unit_wght" id="unit_wght" maxlength="12"> kg</td>
</tr>


<tr><td>Country or Territory of Origin *</td>
<td>
<select id="item_origin" name="item_origin">
<option value="">[Please select]</option>
END1

$jjj = 0;
foreach $c (@new_arr){
	$tmp = $new_arr[$jjj];
	#if ($c eq "HK"){
	#	print "<option value=\"$c\" selected>$country_list{$tmp}</option>\n";
	#}
	#else{
		print "<option value=\"$c\">$country_list{$tmp}</option>\n";
	#}
	$jjj = $jjj + 1;
}

print <<END1;
</select>
</td>
</tr>


<tr><td>Commodity Code</td>
<td><input type="text" value="" name="item_commodity" id="item_commodity" maxlength="15"></td>
</tr>



<tr><td></td>
<td>
<a href="javascript:add_update()" onMouseOver="objPIC6.MouseOver()" onMouseOut ="objPIC6.MouseOut()"><img src="../../images/addupd_com1.jpg" border=0 name=PIC6></a>
</td>
</tr>
<tr><td></td><td></td></tr>
<tr><td colspan="2">Do you want to print out the Invoice?</td>
</tr>
<tr><td colspan="2"><i><font color="#FF0000"><b>Alert:</b></font> <font color="#0040FF">A commercial invoice/proforma invoice is required for Non-Document shipment.<br>You may print out the DHL generated Customs invoice for Customs clearance.</font></i></td>
</tr>

<tr><td colspan="2" align="left"><input type=radio name="print_inv" id="print_inv" value="Y" checked>Yes, I want to print the above commodity information as below Invoice Type.</td>
</tr>
<tr><td>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
<select style='FONT-FAMILY : Arial;FONT-SIZE: 12px;' id="inv_ty" name="inv_ty">
<option value="commercial">Commercial Invoice</option>
<option value="proforma">Proforma Invoice</option>
</select>
</td>
<td></td>
</tr>
<tr><td colspan="2" align="left"><input type=radio name="print_inv" id="print_inv" value="N">No, please use your own Invoice.</td>
</tr>
<tr><td>Invoice Number</td>
<td><input type="text" value="" name="inv_num" id="inv_num" maxlength="15"></td>
</tr>
<tr><td>Type of Export</td>
<td>
<select style='FONT-FAMILY : Arial;FONT-SIZE: 12px;' id="export_ty" name="export_ty">
<option value="Permanent">Permanent</option>
<option value="Temporary">Temporary</option>
<option value="Repair/Return">Repair/Return</option>
</select>
</td>
</tr>
<tr><td>Reason of Export</td>
<td><input type="text" value="" name="export_reason" id="export_reason" size="45" maxlength="40"></td>
</tr>
<tr><td>Incoterm</td>
<td>
<select style='FONT-FAMILY : Arial;FONT-SIZE: 12px;' id="incoterm" name="incoterm">
<option value="">[Please select]</option>
<option value="CIP">CIP - Carriage & Insurance Paid</option>
<option value="CPT">CPT - Carriage Paid To</option>
<option value="DAP" selected>DAP - Delivered At Place</option>
<option value="DAT">DAT - Delivered At Terminal</option>
<option value="DDP">DDP - Delivered Duty Paid</option>
<option value="DDU">DDU - Delivered Duty Unpaid</option>
<option value="DEQ">DEQ - Delivered Ex Quay</option>
<option value="DES">DES - Delivered Ex Ship</option>
<option value="EXW">EXW - Ex Works</option>
<option value="FAS">FAS - Free Alongside Ship</option>
<option value="FCA">FCA - Free Carrier</option>
<option value="FOB">FOB - Free On Board</option>
</select>
</td>
</tr>

</table>
<input type="hidden" name="cur_item" id="cur_item" value="">
<input type="hidden" name="item_list" id="item_list" value="">


</div>



<br>

<div id="div2" style="position: absolute; top: 200px;">

<table cellspacing=3 cellpadding=3 border=0 width=460>
<tr><td><font face="Frutiger, Arial" size="2">


<input type="checkbox" name="agreetc" value="Y">
END1

if ($Form{origin} eq 'MCA') {
 print 'I have read and accept the <a href="https://mydhl.express.dhl/mo/en/legal.html" target="_blank" rel="noopener noreferrer">Terms and Conditions</a>, and <a href="https://apps.dhl.com.hk/statement/eng_mo/pics.html" target="_blank" rel="noopener noreferrer">Personal Information Collection Statement</a>. *';
} else {
 print 'I have read and accept the <a href="https://mydhl.express.dhl/hk/en/legal.html" target="_blank" rel="noopener noreferrer">Terms and Conditions</a>, and <a href="https://apps.dhl.com.hk/statement/eng_hk/pics.html" target="_blank" rel="noopener noreferrer">Personal Information Collection Statement</a>. *';
}

print <<END1;	
</font></td></tr>
</table>

</div>
</td>
</tr>
</table>

<br>
<a href="javascript:history.go(-1);" onMouseOver="objPIC5.MouseOver()" onMouseOut ="objPIC5.MouseOut()"><img src="../../images/back1.gif" border=0 name=PIC5></a>
&nbsp;&nbsp;
<a href="javascript:checking(document.dhl)" onMouseOver="objPIC3.MouseOver()" onMouseOut ="objPIC3.MouseOut()"><img src="../../images/confirm1.jpg" border=0 name=PIC3></a>
<br><br><font size=-1><font face="Frutiger, Arial">* Mandatory input</font></font>
<input type="hidden" name="sub_grp_id" value="$Form{sub_grp_id}">
</form>

<table cellspacing=3 cellpadding=3 border=0 width=460>
<tr>
<td COLSPAN=5>
<table border=0 cellpadding="2">
<tr>
<td bgcolor="#CC0204"><font size="3" face="Arial Black" color="white">
&nbsp;&nbsp;Track DHL Express Shipments&nbsp;&nbsp;&nbsp;&nbsp;
</font>
</td>
</tr>
</table>

<p><font size="2" face="Frutiger, Arial">

if you would like to track your shipments, please track online at <a href="http://www.dhl.com.hk/en/express/tracking.html" target="track" rel="noopener noreferrer">http://www.dhl.com.hk/en/express/tracking.html</a> or<br>
by email using eTrack (more information here: <a href="http://www.dhl.com.hk/en/express/tracking/tracking_tools.html" target="etrack" rel="noopener noreferrer">http://www.dhl.com.hk/en/express/tracking/tracking_tools.html</a> ).<br><br>

</td>
</tr>
</table>

</body>
<script LANGUAGE="javascript" SRC="../../js_client/copyright_r.js"></script>
</html>

END1


sub get_exp_time{
	$gm_time = time();
	$gm_time = $gm_time + 315360000;
	$gm_time = gmtime($gm_time);

	@array = split(/ /,$gm_time);
	if ($array[2] == ''){
		$array[2] = 0;
		$gm_time = "$array[0] $array[1] $array[2]$array[3] $array[4] $array[5]";
		@array = split(/ /,$gm_time);
	}
	$array[4] = substr($array[4], 2, 2);
	$cook_time = "$array[0], $array[2]-$array[1]-$array[4] $array[3] GMT";
	return $cook_time;
}

sub chk_ctry_pc{
  
  $in_ctry = $_[0];
  $ctry_with_pc = "N";
  
  &get_connect("wcrd");
  $sql_ctry_pc_str="select count(*) from post_code_pattern where country_code = '" . $in_ctry . "'";
  	
  $sql_ctry_pc=$web_db->prepare($sql_ctry_pc_str) or die "Couldn't select from post_code_pattern";
  $sql_ctry_pc->execute();

  @ctry_pc_data = $sql_ctry_pc->fetchrow_array;
  if ($ctry_pc_data[0] > 0) {
  	$ctry_with_pc = "Y";
  }
  
  return $ctry_with_pc;
	
}
	
sub reformat_pc{
  
  $in_ctry = $_[0];
  $in_pc = $_[1];
  $out_pc = "";
  
  #reformat postcode if it exist in v_post_code table
  
  &get_connect("wcrd");

 if (($in_ctry eq 'IL') || ($in_ctry eq 'PT')) {
  $sql_pc_exist_str="select count(*) from v_post_code where country_code = '" . $in_ctry . "' and postal_code = '" . $in_pc . "' and length(postal_code) = 7";  
 } else {
  $sql_pc_exist_str="select count(*) from v_post_code where country_code = '" . $in_ctry . "' and postal_code = '" . $in_pc . "'";
 }
	
  $sql_pc_exist=$web_db->prepare($sql_pc_exist_str) or die "Couldn't select from v_post_code";
  $sql_pc_exist->execute();

  @pc_exist_data = $sql_pc_exist->fetchrow_array;
  if ($pc_exist_data[0] > 0) {
     #print "exist<br>";
     
     $sql_format_str="select format from post_code_pattern where country_code = '" . $in_ctry . "' and reformat = 'Y' and pc_val_len = " . length($in_pc);
     
     $sql_format=$web_db->prepare($sql_format_str) or die "Couldn't select from post_code_pattern";
     $sql_format->execute();

     if (@format_data = $sql_format->fetchrow_array()) {
     	#print "pattern found<br>";
     	#print $format_data[0] . "<br>";
     	
     	$pattern = $format_data[0];
     	
     	$in_pc_cur = 0;
     	
     	for ($i=0; $i < length($pattern); $i++) {
     	    #print substr($pattern,$i,1) . "\n";
     	    if ((substr($pattern,$i,1) ne " ") && (substr($pattern,$i,1) ne "-") && ($in_pc_cur < length($in_pc))) {
     	    	$out_pc = $out_pc . substr($in_pc, $in_pc_cur, 1);
     	    	$in_pc_cur++;
     	    } else {
     	    	$out_pc = $out_pc . substr($pattern, $i, 1);
     	    }
        }
     	
     	#$out_pc = $format_data[0];
     } else {
     	#print "pattern not found<br>";
     	$out_pc = $in_pc;
     }
     
  } else {
     #$out_pc = $in_pc;     
     
     #if ($in_str =~ m/[^a-zA-Z0-9]/) {
        
        if ($in_str =~ m/[^a-zA-Z0-9 -]/) {
           #for non-alphanumeric postcode with other characters besides " " and "-"
           $out_pc = "error";
	} else {
	   #convert postcode to pattern A9
	   $in_pc_pattern = "";
	   for ($i=0; $i < length($in_pc); $i++) {
	       	 
	     	 if (substr($in_pc,$i,1) =~ /[A-Z]/) {
	     	    $in_pc_pattern = $in_pc_pattern . "A";
	     	 }
	     	 if (substr($in_pc,$i,1) =~ /[0-9]/) {
	     	    $in_pc_pattern = $in_pc_pattern . "9";
	     	 }
	     	 if (substr($in_pc,$i,1) eq " ") {
	     	    $in_pc_pattern = $in_pc_pattern . " ";
	     	 }
	     	 if (substr($in_pc,$i,1) eq "-") {
	     	    $in_pc_pattern = $in_pc_pattern . "-";
	     	 }
	   }
	     
	   #validate pattern
	   $sql_pc_pattern_exist_str="select count(*) from post_code_pattern where country_code = '" . $in_ctry . "' and format = '" . $in_pc_pattern . "'";
	
	   $sql_pc_pattern_exist=$web_db->prepare($sql_pc_pattern_exist_str) or die "Couldn't select from post_code_pattern";
	   $sql_pc_pattern_exist->execute();
	
	   @pc_pattern_exist_data = $sql_pc_pattern_exist->fetchrow_array;
	   if ($pc_pattern_exist_data[0] == 0) {
	      $out_pc = "error";
	   } else {
	      $out_pc = $in_pc;
	   }
	}
       
     #} else {
        #for alphanumeric postcode without pattern but not found at v_post_code     	
     	#$out_pc = "error";
     #}
     
  }
   
  return $out_pc;
   
}

sub trim {
   $in_str = $_[0];
   
   #my $string = shift;
   $in_str =~ s/^\s+//;
   $in_str =~ s/\s+$//;
   return $in_str;
}

sub replace_spaces {
   $in_str = $_[0];
   
   #$in_str =~ tr/ +/ /;   
   #$in_str =~ s/ +/ /;
   $in_str =~ s/ +/ /g;

   return $in_str;
}


sub pre_check{
   
   $in_ctry = $_[0];
   $in_pc = $_[1];
   $check_result = 0;
   
   &get_connect("wcrd");

   $sql_pc_exist_str="select count(*) from v_post_code where country_code = '" . $in_ctry . "' and postal_code = '" . $in_pc . "'";
	
   $sql_pc_exist=$web_db->prepare($sql_pc_exist_str) or die "Couldn't select from v_post_code";
   $sql_pc_exist->execute();

   @pc_exist_data = $sql_pc_exist->fetchrow_array;
   if ($pc_exist_data[0] > 0) {
	$check_result = 1;
   }
   
   return $check_result;

}


sub validate_ac{
   
   $in_ac = $_[0];
   $check_result = 0;
   
   &get_connect("wcmf");
   
   $sql_ac_str="select count(*) from invoicing_info where accnt_no = '" . $in_ac . "' and cr_status_cd = 'O' and accnt_bill_ty != 'C'";
   
   $sql_ac=$web_db->prepare($sql_ac_str) or die "Couldn't select from invoicing_info";
   $sql_ac->execute();

   @ac_data = $sql_ac->fetchrow_array;
   if ($ac_data[0] > 0) {
	$check_result = 1;
   }
   return $check_result;
   

}

sub validate_billed_ac{
   
   $in_ac = $_[0];
   $in_stn = $_[1];
   $check_result = 0;
   $chk_cnty = "HK";
   
   if ($in_stn eq "MCA") {
	 $chk_cnty = "MO";
   }
   
   &get_connect("wcmf");

   $sql_ac_str="select count(*) from invoicing_info where accnt_no = '" . $in_ac . "' and cr_status_cd = 'O' and bill_country = '" . $chk_cnty . "'";
   	
   $sql_ac=$web_db->prepare($sql_ac_str) or die "Couldn't select from invoicing_info";
   $sql_ac->execute();

   @ac_data = $sql_ac->fetchrow_array;
   if ($ac_data[0] > 0) {
	$check_result = 1;
   }
   
   return $check_result;

}


sub isFOC_CASH{
   
   $in_ac = $_[0];
   $check_result = 0;
   $acc_cnt = 0;
   
   $acc_cnt=`grep $in_ac ./FOC_CASH_acc.lst|wc -l`; 
   
   if ($acc_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}

sub isColoader{
   
   $in_ac = $_[0];
   $check_result = 0;
   $acc_cnt = 0;
   
   $acc_cnt=`grep $in_ac ./coloader_acc.lst|wc -l`; 
   
   if ($acc_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}

sub isBlacklist{
   
   $in_ac = $_[0];
   $check_result = 0;
   $acc_cnt = 0;
   
   $acc_cnt=`grep $in_ac ./blacklist_acc.lst|wc -l`; 
   
   if ($acc_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}

sub isEU{
   
   $in_cnty = $_[0];
   $check_result = 0;
   $rec_cnt = 0;

   $rec_cnt=`grep $in_cnty ./EU.lst|wc -l`; 
   
   if ($rec_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}
