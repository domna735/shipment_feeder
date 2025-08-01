#!/usr/bin/perl


use lib '/appl/service/webapps/cgi-bin/';
use db_con;

use CGI::Cookie;

my %cookies = CGI::Cookie->fetch;
my $session_token = $cookies{'SESSIONID'} ? $cookies{'SESSIONID'}->value : '';
unless (is_valid_session($session_token)) {
    my $q = CGI->new;
    print $q->redirect('toLogin.html');
    exit;
}


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
	$> = $<;
        $) = $(;
	read (STDIN, $buffer, $ENV{'CONTENT_LENGTH'});
}
elsif ($ENV{'REQUEST_METHOD'} eq "GET" ){
	$buffer = $ENV{'QUERY_STRING'};
}

@pairs = split(/&/, $buffer);

foreach $pair (@pairs){
	($name, $value) = split (/=/, $pair);
	#$value =~ s/^%09/<dd>/g;
	$value =~ s/^%09/ /g;
	$value =~ s/%0D/<br>%0D/g;
	$value =~ tr/+/ /;
	$value =~ s/%(..)/pack("c", hex($1))/eg;
	$Form{$name} = $value;
}

#$home="/hkweb/apache-tomcat-7.0.41_prd";
#$home_test="/local/stage/hk";
$home="../.."; 
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


print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


$err = 0;
$station_code='';

############ validation ##############

#double check grp id to avoid direct post
if (defined $Form{grp_id}) {
   if ($Form{grp_id} eq "") {
      $err = 1;
      $err_str = 'Invalid access. Please make sure you access the correct URL.';
   } else {
	  if (validate_grp_id($Form{grp_id}) == 0) {
		 $err = 1;
		 $err_str = 'Invalid access.';
	  }
   }
} else {
   $err = 1;
   $err_str = 'Invalid access. Please make sure you access the correct URL.';   
}

if ($err == 0) {
    if (defined $Form{charge_to}) {
       if ($Form{'charge_to'} eq '') {
    	$err = 1;
    	$err_str = 'Please input charge to option.';
       } else {
       	  if ((uc($Form{'charge_to'}) ne 'SHIPPER') && (uc($Form{'charge_to'}) ne 'RECEIVER') && (uc($Form{'charge_to'}) ne 'OTHERS')) {
       	     $err = 1;
    	     $err_str = 'Charge to option is invalid. Please input again.';
    	  } else {
    	     $Form{'charge_to'} = uc($Form{'charge_to'});
    	  }
       }
    } else {
       $err = 1;
       $err_str = 'Please input charge to option.';
    }
}

if ($err == 0) {
    if (defined $Form{send_company}) {
       if ($Form{'send_company'} eq '') {
    	$err = 1;
    	$err_str = 'Please input sender company name.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input sender company name.';
    }
}

if ($err == 0) {
    if (defined $Form{send_name}) {
       if ($Form{'send_name'} eq '') {
    	$err = 1;
    	$err_str = 'Please input sender name.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input sender name.';
    }
}

if ($err == 0) {
    if (defined $Form{send_address1}) {
       if ($Form{'send_address1'} eq '') {
    	$err = 1;
    	$err_str = 'Please input sender address line1.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input sender address line1.';
    }
}

#if ($err == 0) {
#    if (defined $Form{send_address2}) {
#       if ($Form{'send_address2'} eq '') {
#    	$err = 1;
#    	$err_str = 'Please input sender address line2.';
#       }
#    } else {
#       $err = 1;
#       $err_str = 'Please input sender address line2.';
#    }
#}

if ($err == 0) {
    if (defined $Form{send_tel}) {
       if ($Form{'send_tel'} eq '') {
    	$err = 1;
    	$err_str = 'Please input sender phone.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input sender phone.';
    }
}

if ($err == 0) {
    if (defined $Form{consign_company}) {
       if ($Form{'consign_company'} eq '') {
    	$err = 1;
    	$err_str = 'Please input receiver company.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input receiver company.';
    }
}

if ($err == 0) {
    if (defined $Form{consign_person}) {
       if ($Form{'consign_person'} eq '') {
    	$err = 1;
    	$err_str = 'Please input receiver contact person.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input receiver contact person.';
    }
}

if ($err == 0) {
    if (defined $Form{consign_address1}) {
       if ($Form{'consign_address1'} eq '') {
    	$err = 1;
    	$err_str = 'Please input receiver address line1.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input receiver address line1.';
    }
}

#if ($err == 0) {
#    if (defined $Form{consign_address2}) {
#       if ($Form{'consign_address2'} eq '') {
#    	$err = 1;
#    	$err_str = 'Please input receiver address line2.';
#       }
#    } else {
#       $err = 1;
#       $err_str = 'Please input receiver address line2.';
#    }
#}


if ($err == 0) {
    if (defined $Form{consign_tel}) {
       if ($Form{'consign_tel'} eq '') {
    	$err = 1;
    	$err_str = 'Please input receiver phone.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input receiver phone.';
    }
}


if ($err == 0) {
    if (defined $Form{dhl_acc_no}) {
       if ($Form{'dhl_acc_no'} eq '') {
    	$err = 1;
    	$err_str = 'Please input DHL account number.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input DHL account number.';
    }
}


if ($err == 0) {
  if ((uc($Form{'charge_to'}) eq 'RECEIVER') || (uc($Form{'charge_to'}) eq 'OTHERS')) {
    if (defined $Form{charge_to_account}) {
       if ($Form{'charge_to_account'} eq '') {
    	$err = 1;
    	$err_str = 'Please input payer account number.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input payer account number.';
    }
  }
}


if ($err == 0) {
   
   $err_msg = "";
    
   #if (($Form{dhl_acc_no} ne "") && ($Form{dhl_acc_no} =~ /\D/)) {
   if ($Form{dhl_acc_no} =~ /\D/) {
     $err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
   } else {
     if (length($Form{dhl_acc_no}) != 9) {
     	$err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
     } else {
     	#if ((substr($Form{dhl_acc_no},0,2) ne '63') && (substr($Form{dhl_acc_no},0,2) ne '96') && (substr($Form{dhl_acc_no},0,2) ne '95') && (substr($Form{dhl_acc_no},0,2) ne '94')) {
		if ((substr($Form{dhl_acc_no},0,2) eq '96') || (substr($Form{dhl_acc_no},0,2) eq '95') || (substr($Form{dhl_acc_no},0,2) eq '94')) {
			$err_msg = $err_msg . "由<b>2021年12月1日</b>起，此應用程式將不再支援 &quot;<b>DHL 進口帳號</b>&quot; (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br>請您使用網上工具 <a href='https://mydhl.express.dhl/hk/zh/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a>製作你的提單。 (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf' target='reg_guide' rel='noopener noreferrer'>註冊教學</a>)<br><br>";
			$err_msg = $err_msg . "Effective from <b>1 December 2021</b>, this application will not support &quot;<b>DHL Import Express</b>&quot; account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br>Please use our online tool <a href='https://mydhl.express.dhl/hk/en/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a> to create your waybills. (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf' target='reg_guide' rel='noopener noreferrer'>Registration Guide</a>)<br><br>";
		} else {
		  if (substr($Form{dhl_acc_no},0,2) ne '63') {
     	    $err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
     	  } else {
     	    if (validate_ac($Form{dhl_acc_no}) == 0) {
      		 $err_msg = $err_msg . "Sender account no. is invalid or has stopped credit.<br><br>";
   	        } 
		    # else {
			#  if (validate_billed_ac($Form{dhl_acc_no}) == 0) {
			#	    $err_msg = $err_msg . "由<b>2021年9月1日</b>起，此應用程式將不再支援 &quot;<b>DHL 進口帳號</b>&quot; (即字首為95/96的帳號) 作為寄件人帳號 。<br>請您使用&quot;<b>DHL 出口帳號</b>&quot; 作為寄件人帳號，或註冊使用網上工具 <a href='https://mydhl.express.dhl/hk/zh/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a>製作你的提單。 (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf' target='reg_guide' rel='noopener noreferrer'>註冊教學</a>)<br><br>";
			#	    $err_msg = $err_msg . "Effective from <b>1 September 2021</b>, this application will not support &quot;<b>DHL Import Express</b>&quot; account number (i.e. 95/96 prefix) as Shipper accounts.<br>Please use &quot;<b>DHL Export</b>&quot; account number as Shipper account, or please register our online tool <a href='https://mydhl.express.dhl/hk/en/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a> to create your waybills. (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf' target='reg_guide' rel='noopener noreferrer'>Registration Guide</a>)<br><br>";					
			#  }
		    #}
		  } 
     	}
     }
   }
			   
   #if (($Form{charge_to_account} ne "") && ($Form{charge_to_account} =~ /\D/)) {
   if ($Form{charge_to_account} ne "") {
    if ($Form{charge_to_account} =~ /\D/) {
     $err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
    } else {
     if (length($Form{charge_to_account}) != 9) {
     	$err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
     } else {
     	#if ((substr($Form{charge_to_account},0,2) ne '63') && (substr($Form{charge_to_account},0,2) ne '96') && (substr($Form{charge_to_account},0,2) ne '95') && (substr($Form{charge_to_account},0,2) ne '94')) {
		if ((substr($Form{charge_to_account},0,2) eq '96') || (substr($Form{charge_to_account},0,2) eq '95') || (substr($Form{charge_to_account},0,2) eq '94')) {
			$err_msg = $err_msg . "由<b>2021年12月1日</b>起，此應用程式將不再支援 &quot;<b>DHL 進口帳號</b>&quot; (即字首為95/96的帳號) 作為寄件人和付款帳號 。<br>請您使用網上工具 <a href='https://mydhl.express.dhl/hk/zh/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a>製作你的提單。 (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf' target='reg_guide' rel='noopener noreferrer'>註冊教學</a>)<br><br>";
			$err_msg = $err_msg . "Effective from <b>1 December 2021</b>, this application will not support &quot;<b>DHL Import Express</b>&quot; account number (i.e. 95/96 prefix) as Shipper and Payer accounts.<br>Please use our online tool <a href='https://mydhl.express.dhl/hk/en/ship/solutions.html' target='mydhl' rel='noopener noreferrer'><b>MyDHL+</b></a> to create your waybills. (<a href='https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf' target='reg_guide' rel='noopener noreferrer'>Registration Guide</a>)<br><br>";
		} else {		
		  if (substr($Form{charge_to_account},0,2) ne '63') {
     	    $err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
     	  } else {
     	    if (validate_ac($Form{charge_to_account}) == 0) {
      		  $err_msg = $err_msg . "Payer account no. is invalid or has stopped credit.<br><br>";
   	        }
     	  }
		}
     }
    }
   }

   if ($err_msg ne "") {
   	$err = 1;
   	$err_str = $err_msg;
   }
}

if ($err == 0) {
 if (defined $Form{ship_product}) {
   if ($Form{'ship_product'} eq '') {
	$err = 1;
	$err_str = 'Please input DOCUMENT or DUTIABLE PARCEL for the service.';	
   } else {
   	$Form{'ship_product'} = uc($Form{'ship_product'});
   	if (($Form{'ship_product'} ne 'DOCUMENT') && ($Form{'ship_product'} ne 'DUTIABLE PARCEL')) {
   	    $err = 1;
	    $err_str = 'Please input DOCUMENT or DUTIABLE PARCEL for the service.';
	}
   }
 } else {
   $err = 1;
   $err_str = 'Please input DOCUMENT or DUTIABLE PARCEL for the service.';
 }
}

if ($err == 0) {
	if ((uc($Form{ship_product}) eq 'DUTIABLE PARCEL') && (isEU(uc($Form{consign_country})) == 1)) {
	  $err = 1;
	  $err_str = 'This shipping tool will no longer support the waybill creation for all non-Document shipments sending to European Union Countries.';
	}
}

if ($err == 0) {
	if ((uc($Form{ship_product}) eq 'DUTIABLE PARCEL') && (uc($Form{consign_country}) eq 'ID')) {
	  $err = 1;
	  $err_str = 'This shipping tool will no longer support the waybill creation for all non-Document shipments sending to Indonesia.';
	}
}

if ($err == 0) {
#set default for null ship product dtl selected
  if ($Form{'ship_product_dtl'} eq '') {
    $Form{'ship_product_dtl'} = 'EXPRESS WORLDWIDE';
  } else {
    $Form{'ship_product_dtl'} = uc($Form{'ship_product_dtl'});
    if (($Form{'ship_product_dtl'} ne 'EXPRESS WORLDWIDE') && ($Form{'ship_product_dtl'} ne 'EXPRESS 0900') && ($Form{'ship_product_dtl'} ne 'EXPRESS 1030') && ($Form{'ship_product_dtl'} ne 'EXPRESS 1200') && ($Form{'ship_product_dtl'} ne 'ECONOMY SELECT') && ($Form{'ship_product_dtl'} ne 'EXPRESS EASY')) {
       $err = 1;
       $err_str = 'Type of service is invalid. Please input again.';
    }
  }
}


$contents_desc = $Form{'contents_desc'};
$contents_desc =~ s/<br><br>//g;
$contents_desc =~ s/<br>//g;
$contents_desc =~ s/[\n]/ /g;
$contents_desc =~ s/[\r]//g;
$contents_desc =~ s/[\t]//g;
$contents_desc =~ s/\|//g;
$contents_desc = trim($contents_desc);

if ($err == 0) {  
    #if (($Form{'ship_product'} eq 'DUTIABLE PARCEL') && ($Form{inv_copy} == 0)) {
    if (($Form{'ship_product'} eq 'DUTIABLE PARCEL') && ($Form{skip_err} eq 'N')) {
	if ((($Form{charge_to} ne '') && ($Form{charge_to} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) || 
	   (($Form{ship_insur_value} ne '') && ($Form{ship_insur_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{ship_insur_currency} ne '') && ($Form{ship_insur_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{reference} ne '') && ($Form{reference} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_name} ne '') && ($Form{send_name} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||   
	   (($Form{send_company} ne '') && ($Form{send_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address1} ne '') && ($Form{send_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address2} ne '') && ($Form{send_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address3} ne '') && ($Form{send_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_pc} ne '') && ($Form{send_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_tel} ne '') && ($Form{send_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_person} ne '') && ($Form{consign_person} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_company} ne '') && ($Form{consign_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_address1} ne '') && ($Form{consign_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_address2} ne '') && ($Form{consign_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_address3} ne '') && ($Form{consign_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_pc} ne '') && ($Form{consign_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_city} ne '') && ($Form{consign_city} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_state} ne '') && ($Form{consign_state} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country} ne '') && ($Form{consign_country} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country_nm} ne '') && ($Form{consign_country_nm} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_tel} ne '') && ($Form{consign_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($contents_desc ne '') && ($contents_desc =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_currency} ne '') && ($Form{declare_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_value} ne '') && ($Form{declare_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_duties} ne '') && ($Form{dest_duties} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_other} ne '') && ($Form{dest_other} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/))  ) {
	    	
	    	$err = 1;
       		$err_str = 'No Chinese character is allowed for DUTIABLE PARCEL. Please input again.';
       	}
    } else {
    	if ((($Form{charge_to} ne '') && ($Form{charge_to} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) || 
	   (($Form{ship_insur_value} ne '') && ($Form{ship_insur_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{ship_insur_currency} ne '') && ($Form{ship_insur_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{reference} ne '') && ($Form{reference} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_name} ne '') && ($Form{send_name} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||   
	   (($Form{send_company} ne '') && ($Form{send_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address1} ne '') && ($Form{send_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address2} ne '') && ($Form{send_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address3} ne '') && ($Form{send_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_pc} ne '') && ($Form{send_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{send_tel} ne '') && ($Form{send_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_pc} ne '') && ($Form{consign_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_city} ne '') && ($Form{consign_city} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_state} ne '') && ($Form{consign_state} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country} ne '') && ($Form{consign_country} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country_nm} ne '') && ($Form{consign_country_nm} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_tel} ne '') && ($Form{consign_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($contents_desc ne '') && ($contents_desc =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_currency} ne '') && ($Form{declare_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_value} ne '') && ($Form{declare_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_duties} ne '') && ($Form{dest_duties} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_other} ne '') && ($Form{dest_other} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/))  ) {
	    	
	    	$err = 1;
       		#$err_str = 'No Chinese character is allowed for DOCUMENT except Receiver company name, contact name and address line 1, 2 & 3. Please input again.';
       		$err_str = 'No Chinese character is allowed except Receiver company name, contact name and address line 1, 2 & 3. Please input again.';
       	}
    }
  
}


if ($err == 0) {
   #if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
	if (defined $Form{contents_desc}) {
	   if ($Form{'contents_desc'} eq '') {
		$err = 1;
		#$err_str = 'Please input contents description for dutiable parcel.';
		$err_str = 'Please input contents description.';
	   } else {
	      if (length($contents_desc) > 120) {
	   	$err = 1;
	   	$err_str = 'Please input contents description within 120 characters.';
	      } else {
		    if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
			 if (onDG_lst($contents_desc) == 1) {
			   $err = 1;
			   $err_str = 'This application cannot support the preparation of shipment carrying &#8220;Lithium Batteries&#8221;.<br><br>Please contact your Sales Manager for assistance.';
			 } elsif (onRED_lst($contents_desc) == 1) {
			   $err = 1;
			   $err_str = 'Acceptable Goods Descriptions include complete information, providing sufficient detail about the precise nature of goods in plain language.<br><br>It should indicate what the goods are, for which purpose the goods are used and what is made of.';
			 } elsif (onPNR_lst($contents_desc) == 1) {
			   $err = 1;
			   $err_str = 'Your shipping items are either Prohibited or Restricted items, they will NOT be accepted for carriage by DHL or unless otherwise agreed to by DHL.<br><br>Please contact your Sales Manager for assistance.';
			 }
		    }
		  }
	   }
	} else {
	   $err = 1;
	   #$err_str = 'Please input contents description for dutiable parcel.';
	   $err_str = 'Please input contents description.';
	}
   #}
}


@currency_arr = (
'HKD',
'USD',
'AUD',
'JPY',
'EUR',
'CNY',
'GBP',
'NZD');
	
if ($err == 0) {
   if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
      if ((defined $Form{declare_value}) && (defined $Form{declare_currency})) {
      	 if (($Form{'declare_value'} eq '') || ($Form{'declare_currency'} eq '')) {
	     $err = 1;
	     $err_str = 'Please input declared value and currency for dutiable parcel.';
	 } else {
	     $Form{'declare_currency'}=uc($Form{'declare_currency'});
	     
	     $currency_valid = "0";
	     foreach $b (@currency_arr){
        	if ($b eq $Form{'declare_currency'}) {
        	   $currency_valid = "1";
	        }
	     }
	     
	     #if (($Form{'declare_currency'} ne 'HKD') && ($Form{'declare_currency'} ne 'USD')) {
	     if ($currency_valid eq "0") {
	     	$err = 1;
		$err_str = 'Please input a valid declared value currency.';
	     }
	     
	     if (!($Form{declare_value} =~ /^-?\d+\.?\d*$/)) {
	        $err = 1;
		$err_str = $err_str . '<br><br>Please input a valid declared value.';
	     } else {
	     	if ($Form{declare_value} <= 0) { 
	     	  $err = 1;
	          $err_str = $err_str . '<br><br>Please input a valid declared value for dutiable parcel.';
	 	}
	     }
	 }
      } else {
      	 $err = 1;
   	 $err_str = 'Please input declared value and currency for dutiable parcel.';
      }	
   }
}

if ($err == 0) {
  if ($Form{'declare_value'} ne '') {
     if ($Form{'declare_currency'} eq '') {
  	$err = 1;
	$err_str = 'Please input declared value currency.';
     } else {
     	     $Form{'declare_currency'}=uc($Form{'declare_currency'});
     	     
     	     $currency_valid = "0";
	     foreach $b (@currency_arr){
        	if ($b eq $Form{'declare_currency'}) {
        	   $currency_valid = "1";
	        }
	     }
	     
	     #if (($Form{'declare_currency'} ne 'HKD') && ($Form{'declare_currency'} ne 'USD')) {
	     if ($currency_valid eq "0") {
	     	$err = 1;
		$err_str = 'Please input a valid declared value currency.';
	     }
	     
     	     if (!($Form{declare_value} =~ /^-?\d+\.?\d*$/)) {
	        $err = 1;
		$err_str = $err_str . '<br><br>Please input a valid declared value.';
	     } else {
	     	if ($Form{declare_value} <= 0) { 
	     	  $err = 1;
	          $err_str = $err_str . '<br><br>Please input a valid declared value.';
	 	}
	     }
     }
  }
}

if ($err == 0) {
   if ($Form{'dest_duties'} ne '') {
   	if ((uc($Form{'dest_duties'}) ne 'SENDER') && (uc($Form{'dest_duties'}) ne 'RECEIVER') && (uc($Form{'dest_duties'}) ne 'OTHER')) {
   	   $err = 1;
   	   $err_str = 'Destination duties option is invalid. Please input again.';
   	}
   }
}
	
if ($err == 0) {
   if (uc($Form{'dest_duties'}) eq 'OTHER') {
      if (defined $Form{dest_other}) {
         if ($Form{'dest_other'} eq '') {
		$err = 1;
		$err_str = 'If you select other account number for destination duties, pleae input a valid DHL account number at destination duties account number.';
	 } else {
	 	#if ((length($Form{dest_other}) != 9) || ($Form{dest_other} =~ /\D/)) {
	 	#  $err = 1;
	 	#  $err_str = 'Other account number for destination duties is invalid. Please input again.';
	 	#}
	 	if ($Form{dest_other} =~ /\D/) {
	 	     $err = 1; 
		     $err_str = 'Other account number for destination duties is invalid. Please input again.';
		} else {
		     if (length($Form{dest_other}) != 9) {
		     	$err = 1;
		     	$err_str = 'Other account number for destination duties is invalid. Please input again.';
		     } else {
		     	#if ((substr($Form{dest_other},0,2) ne '63') && (substr($Form{dest_other},0,2) ne '96') && (substr($Form{dest_other},0,2) ne '95') && (substr($Form{dest_other},0,2) ne '94')) {
				if (substr($Form{dest_other},0,2) ne '63') {
		     	   $err = 1;
		     	   $err_str = 'Other account number for destination duties is invalid. Please input again.';
		     	} else {
		     	   if (validate_ac($Form{dest_other}) == 0) {
		      		$err = 1;
		      		$err_str = 'Other account number for destination duties is invalid or has stopped credit. Please input again.';
					}
		     	} 
		     }
		}
	 }
      } else {
	$err = 1;
	$err_str = 'If you select other account number for destination duties, pleae input a valid DHL account number at destination duties account number.';
      }
   }
}

if ($err == 0) {
   if ((uc($Form{'ship_insurance'}) eq 'ON') || (uc($Form{'ship_insurance'}) eq 'Y')) {
	if ($Form{'ship_insur_value'} eq '') {
	     $err = 1;
	     $err_str = 'Please input insured value.';
	} else {		
	     if (!($Form{ship_insur_value} =~ /^-?\d+\.?\d*$/)) {
	        $err = 1;
		$err_str = 'Please input a valid insured value.';
	     } else {
	     	if ($Form{ship_insur_value} <= 0) { 
	     	  $err = 1;
	          $err_str = 'Please input a valid insured value.';
	 	}
	     }
	}
   }	
}

if ($err == 0) {
 if (defined $Form{ship_weight}) {
  if ($Form{ship_weight} eq '') {
 	$err = 1;
	$err_str = 'Please input shipment weight.';
  } else {
     if (!($Form{ship_weight} =~ /^-?\d+\.?\d*$/)) {
        $err = 1;
	$err_str = 'Please input valid shipment weight.';
     } else {
     	#if (($Form{ship_weight} <= 0) || ($Form{ship_weight} >= 1000)) {
		#if (($Form{ship_weight} <= 0) || ($Form{ship_weight} > 1000)) {
		if (($Form{ship_weight} <= 0) || ($Form{ship_weight} > 3000)) {
     	  $err = 1;
          #$err_str = 'The total weight must be over 0kg and not exceed 1000kg, please input again.';
		  $err_str = 'The total weight must be over 0kg and not exceed 3000kg, please input again.';
 	    }
     }
  }
 } else {
   $err = 1;
   $err_str = 'Please input shipment weight.';	
 }
}


if ($err == 0) {
 if (defined $Form{ship_qty}) {
  if ($Form{ship_qty} eq '') {
 	$err = 1;
	$err_str = 'Please input shipment quantity.';
  } else {
     if ($Form{ship_qty} =~ /\D/) {
        $err = 1;
	$err_str = 'Please input a valid shipment quantity.';
     } else {
     	if (($Form{ship_qty} <= 0) || ($Form{ship_qty} > 999)) { 
     	  $err = 1;          
          $err_str = 'Shipment quantity must be at least 1 and less than 1000, please input again.';
 	} else {
 	  $Form{ship_qty} = $Form{ship_qty} / 1;
 	}
     }
   }
 } else {
   $err = 1;
   $err_str = 'Please input shipment quantity.';	
 }
 		
 #if ($Form{ship_qty} eq '0') {
 #  $err = 1;
 #  $err_str = 'Quantity should be at least 1, please input again.';
 #} else {	
 #  $no_qty = $Form{ship_qty} / 1;
 #  if (($no_qty == 0) && ($Form{ship_qty} ne '0')){
 #      $err = 1;
 #	$err_str = 'Quantity must be numeric, please input again.';
 #  }
 #}
}

if ($err == 0) {
   if ($Form{ship_qty} <=10) {
	$wght_limit = $Form{ship_qty} * 300;
	if ($Form{ship_weight} > $wght_limit) {
	   $err = 1;
       $err_str = "The total weight cannot exceed ".$wght_limit."kg, please input again.";
	}
   }  
#  if (($Form{ship_qty} == 1) && ($Form{ship_weight} > 300)) {
#      $err = 1;
#      $err_str = "The total weight cannot exceed 300kg, please input again.";
#  }
#  if (($Form{ship_qty} == 2) && ($Form{ship_weight} > 600)) {
#      $err = 1;
#      $err_str = "The total weight cannot exceed 600kg; For any piece's weight, it cannot exceed 300kg. Please input again.";
#  }
#  if (($Form{ship_qty} == 3) && ($Form{ship_weight} > 900)) {
#      $err = 1;
#      $err_str = "The total weight cannot exceed 900kg; For any piece's weight, it cannot exceed 300kg. Please input again.";
#  }
}

	
#existing feeder customer will use address line 3 as city name for station code generation
$is_old_cust = "N";
$old_cust_lst = "HA|HSBC|LF|SONY|AIA";
@old_cust_arr = split(/\|/,$old_cust_lst);
for $oc ( 0 .. $#old_cust_arr ) {
 #print $oc;
 #print $Form{grp_id};
 #print @old_cust_arr[$oc];
 if (@old_cust_arr[$oc] eq $Form{grp_id}) {
   $is_old_cust = "Y";
 }
} 	
#print $is_old_cust;

$Form{consign_city} = trim($Form{consign_city});
$Form{consign_city} = replace_spaces($Form{consign_city});  

$Form{consign_pc} = trim($Form{consign_pc});
$Form{consign_pc} = replace_spaces($Form{consign_pc});


# get country code if only country name is provided
if ($err == 0) {
 if (($Form{consign_country} eq '') && ($Form{consign_country_nm} eq '')) {
  $err = 1;
	$err_str = 'Country/territory code or name should be inputted, please input again.';
 } else {
	#check country name only if country code is not provided.
	#if ($Form{consign_country_nm} ne '') {
	if (($Form{consign_country} eq '') && ($Form{consign_country_nm} ne '')) {
		 $in_cn_nm=uc($Form{consign_country_nm});
		 $country_code=`./label/get_cn_cd.sh \"$in_cn_nm\"`;
		 #$country_code='AB';
		 $country_code =~ s/\s+$//;

		 if ($country_code eq 'error') {
		 	$err = 1;
		 	$err_str = 'Invalid country/territory name, please input again.';
		 }
		 #else {
		 #    if ($Form{consign_country} ne '') {		     	       
		 #       if ($country_code ne uc($Form{consign_country})) {
		 #	       $err = 1;
		 #	      $err_str = 'Country/Territory name does not match with country/territory code, please input again.';
		 #	    }
		 #   }
		 #}
			 
	} else {
		 $country_code = uc($Form{consign_country});
	}
 }
}


#block destination=HK if origin=HK
if ($Form{origin} eq '') {
  $origin_ctry='HK';
  $origin_city='HONG KONG';
}

if ($err == 0) {
   if ($country_code eq 'TJ') {
      $err = 1;
      $err_str = "DHL has a temporary restriction on shipments to the receiver country/territory. Please check your entries and input again.";
   }
   
   if (($country_code eq 'AF') || ($country_code eq 'SD')) {
      $err = 1;
      $err_str = "Shipments to the receiver country/territory are suspended. Please check your entries and input again.";
   }
   
   if (($origin_ctry eq 'HK') && ($country_code eq 'HK')) {
      $err = 1;
      $err_str = "Receiver country/territory should not be Hong Kong for international shipment. Please input again.";
   }
}


# get station code
if ($err == 0) {
  $in_city='';
  
  if ($is_old_cust eq 'Y') {  
    if ($Form{consign_address3} ne '') {
  	$in_city=uc($Form{consign_address3});  	
    }
  } else {
    if ($Form{consign_city} ne '') {
  	$in_city=uc($Form{consign_city});
    }	
  }
  $in_city=trim($in_city);
  $in_city=replace_spaces($in_city);

  
  #$in_station='';
  #if ($Form{station_code} ne '') {
  #	$in_station=uc($Form{station_code});
  #}
  $in_pc='';
  if ($Form{consign_pc} ne '') {
    $in_pc=uc($Form{consign_pc});
    $in_pc=trim($in_pc);
    $in_pc=replace_spaces($in_pc);
  } 

  #$station_code=`./label/get_stn.sh \"$country_code\" \"$in_pc\" \"$in_city\" \"$in_station\"`;
  #$station_code =~ s/\s+$//;
  
  #if (length($station_code) != 3) {
  # 	$err = 1;
  #	$err_str = $station_code;
  #}
	
}

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
   
   if ($err == 1){
     $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";     
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
       	  $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";       	  
       }
     } else {
       $err = 1;
       $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";
     }
  	
  } else {
     if ($with_pc eq 'Y') {
      	 $err = 1;
      	 $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";
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
  #if (length($station_facility) != 7) {
  if ((length($station_facility) != 7) && (length($station_facility) != 4)) {  	
     $err = 1;
     #$err_str = $station_code;
     #$err_str = "$station_code<br><br>Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";
     $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";
  } else {
     @cd = split(/\|/,$station_facility);
     $station_code = $cd[0];
     $facility_code = $cd[1];
     if ($station_code eq "") {
     	$err = 1;
        $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode'>list</a>.";
     }
  }
  
}


if ($err == 1){

$topage="";
if ($Form{skip_err} eq "Y") {
  $topage="skip_err.jsp";
} else {
  $topage="show_rec.jsp";
}

print <<END1;

<html>


<body bgcolor=white>
<center><br><Br><b>$err_str</b>
</center>

<form name="show_skip" method="post" action="../../../shipment_feeder/feed_print2/$topage" target="$Form{clientID}_toprint">
<input type="hidden" name="pagefrom" value="awb">
<input type="hidden" name="error_msg" value="$err_str">

<input type="hidden" name="awb_printer" value="$Form{awb_printer}">
<input type="hidden" name="clientID" value="$Form{clientID}">
<input type="hidden" name="awb_paper_ty" value="$Form{awb_paper_ty}">
<input type="hidden" name="grp_id" value="$Form{grp_id}">
<input type="hidden" name="cur_rec_id" value="$Form{cur_rec_id}">
<!--<input type="hidden" name="emailadr" value="$Form{emailadr}">-->
<input type="hidden" name="contact_name" value="$Form{contact_name}">
<input type="hidden" name="logo_filename" value="$Form{logo_filename}">
<input type="hidden" name="default_charset" value="$Form{default_charset}">
<!--<input type="hidden" name="opt_charset" value="$Form{opt_charset}">-->
<input type="hidden" name="sub_grp_id" value="$Form{sub_grp_id}">
<input type="hidden" name="awb_copy" value="$Form{awb_copy}">
<input type="hidden" name="inv_copy" value="$Form{inv_copy}">
<input type="hidden" name="inv_printer" value="$Form{inv_printer}">
<input type="hidden" name="cur_awb_copy" value="$Form{cur_awb_copy}">
<input type="hidden" name="cur_inv_copy" value="$Form{cur_inv_copy}">
<input type="hidden" name="success_rec" value="$Form{success_rec}">
<input type="hidden" name="fail_rec" value="$Form{fail_rec}">
<input type="hidden" name="fail_rec_id" value="$Form{fail_rec_id}">
<input type="hidden" name="ttl_rec" value="$Form{ttl_rec}">
<input type="hidden" name="param" value="$Form{param}">
<input type="hidden" name="pr_cust_cp" value="$Form{pr_cust_cp}">
<input type="hidden" name="scriptx" value="$Form{scriptx}">
<input type="hidden" name="skip_err" value="$Form{skip_err}">
</form>

</body>

<script language="JavaScript" src="https://mykullstc000536.apis.dhl.com/shipment_feeder/js/label_feeder2/show_skip.js"></script>

</html>

END1

exit();
}

########### Remaining section is for printing label ##########



$dhl_acc_no = $Form{dhl_acc_no};
if (($dhl_acc_no =~ /\D/) || (length($dhl_acc_no) != 9)){
	$dhl_acc_no = "";
}

if ($Form{awb_no} ne '') {
   $airway_no = $Form{awb_no};
} else {
	
   $filename = "./temp/airwaybill.txt";
   #$filename = "$home_test/webapps/cgi/temp/airwaybill.txt";
   ##### dedicated awb range for specific a/c
   #if ($dhl_acc_no ne "") {
   #   $af=`./temp/getfile.sh "$dhl_acc_no".txt`;
   #   if ($af ne "") {
   #   	$filename = "./temp/" . $dhl_acc_no . ".txt";
   #   }
   #}
   
   &lock_file ($filename, 20) || die "Can't lock $filename";
   $> = $<;
   $) = $(;
   unless ( open (FILE1, '<',  "$filename") ) {
      &unlock_file ($filename); 
      die "Can't open $filename for appending.";
   }
   $uu = 1;
   while (<FILE1>){
      chop;
      if ($uu == 1){
         $airway_id = $_ *1;
      }
      elsif ($uu == 2){
         $max_air_id = $_ *1;
      }
      $uu ++;
   }
   
   $> = $<;
   $) = $(;
   close (FILE1);
   
   #&unlock_file ($filename);
   
   if (length($airway_id) != 9) {
    print "<html><body bgcolor=white><center>\n";
    print "<br><h2>Please contact DHL for further information.</h2>\n";
    print "</center></body></html>\n";
    exit();
   }
   
   $airway_id = $airway_id + 1;
      
   #&lock_file ($filename, 10) || die "Can't lock $filename";
   $> = $<;
   $) = $(;
   unless ( open (FILE1, '>', "$filename") ) {
      &unlock_file ($filename); 
      die "Can't open $filename for appending.";
   }
   print FILE1 "$airway_id\n";
   print FILE1 "$max_air_id\n";
   $> = $<;
   $) = $(;
   close (FILE1);
   #&unlock_file ($filename);
   
   $remainder = $airway_id % 7;
   
   $airway_no = "$airway_id"."$remainder";
   
   #$jj = 0;
   #while ($jj < 10){
   #   $digit = substr($airway_no, $jj, 1);
   #   $dig_array[$jj] = $digit;
   #   $dig_gif[$jj] = "$digit".".gif";
   #   $jj++;
   #}
   
   $airway_limit = $max_air_id - $airway_id;
   
   #if ($airway_limit <= 100){
     #$receiver = 'hkgwebadm@dhl.com';
     $receiver = 'charmaine.chow@dhl.com';
     
   $tosend = 0;
   if ($airway_limit <= 3000) {   
      if ($airway_limit % 1000 == 0){
        $tosend = 1;
      } else {
        if ($airway_limit <= 100){
          if ($airway_limit % 50 == 0) {
           $tosend = 1;
          }
        }
      }
      
    if ($tosend == 1) {
      $subject = '['.$origin_ctry.']'.' Only '.$airway_limit.' Waybill Number can be used!';
      $email = 'hkgwebadm@dhl.com';
      
      $> = $<;
      $) = $(;
      open( OUT , '|-', "/usr/lib/sendmail -t -oi");
         print OUT "To\: $receiver\n";
         print OUT "From: $email\n";
         print OUT "Subject: $subject\n";
         print OUT "\n";
         print OUT "Please monitor the update of related awb range files at /cgi-bin/temp directory.";
      $> = $<;
      $) = $(;
      close(OUT);
    }
   }
   
   #if ($airway_limit == 0 ) {
   if ($airway_limit <= 0 ) {
     #switch to use spare awb range file
     $sw=`./temp/switchfile.sh`;     
     #$sw=`$home_test/webapps/cgi/temp/switchfile.sh`;
     
   }
   &unlock_file ($filename);
   if ($airway_id > $max_air_id){
      print "<html><body bgcolor=white><center>\n";
      print "<br><h2>Please contact DHL for further information.</h2>\n";
      print "</center></body></html>\n";
      exit();
   }
}

##### get piece ID from range

#for ($sq = 1; $sq <= $Form{ship_qty}; ++$sq) {
	
$filename = "./temp/piece.txt";
#$filename = "$home_test/webapps/cgi/temp/piece.txt";

&lock_file ($filename, 20) || die "Can't lock $filename";
$> = $<;
$) = $(;
unless ( open (FILE1, '<', "$filename") ) {
   &unlock_file ($filename); 
   die "Can't open $filename for appending.";
}
$uu = 1;
while (<FILE1>){
   chop;
   if ($uu == 1){
   	  $piece_id_str = $_;
   	  $piece_id = $_ *1;
   }
   elsif ($uu == 2){
      $max_piece_id = $_ *1;
   }
   $uu ++;
}
$> = $<;
$) = $(;
close (FILE1);
#&unlock_file ($filename);

if (length($piece_id_str) != 16) {
   print "<html><body bgcolor=white><center>\n";
   print "<br><h2>Please contact DHL for further information.</h2>\n";
   print "</center></body></html>\n";
   exit();
}

$piece_id_next = $piece_id+1;
$piece_id = $piece_id+$Form{ship_qty};

$piece_id_next = sprintf("%.1f", $piece_id_next);
$piece_id_next = sprintf("%s", $piece_id_next);
$piece_id_next =~ s/\.0//g;

$piece_id = sprintf("%.1f", $piece_id);
$piece_id = sprintf("%s", $piece_id);
$piece_id =~ s/\.0//g;

#$max_piece_id = sprintf("%0.00f", $max_piece_id);
$max_piece_id = sprintf("%.1f", $max_piece_id);
$max_piece_id = sprintf("%s", $max_piece_id);
$max_piece_id =~ s/\.0//g;

#&lock_file ($filename, 10) || die "Can't lock $filename";
$> = $<;
$) = $(;
unless ( open (FILE1, '>', "$filename") ) {
   &unlock_file ($filename); 
   die "Can't open $filename for appending.";
}
print FILE1 "$piece_id\n";
print FILE1 "$max_piece_id\n";
$> = $<;
$) = $(;
close (FILE1);
#&unlock_file ($filename);


$piece_limit = $max_piece_id - $piece_id;

$tosend = 0;
if ($piece_limit <= 5000){
   #if ($piece_limit % 1000 <= 200){
   if ($piece_limit % 1000 == 0){
     $tosend = 1;
   } else {
     if ($piece_limit <= 500){
       if ($piece_limit % 100 == 0) {
        $tosend = 1;
       }
     }
   }
      
  if ($tosend == 1) { 	   
   $subject = '['.$origin_ctry.']'.' Only '.$piece_limit.' piece ID can be used!';
   $email = 'hkgwebadm@dhl.com';
   
   $> = $<;
   $) = $(;
   open( OUT , '|-', "/usr/lib/sendmail -t -oi");
      print OUT "To\: $receiver\n";
      print OUT "From: $email\n";
      print OUT "Subject: $subject\n";
      print OUT "\n";
      #print OUT "Please go to the server /cgi-bin/temp directory to update the piece.txt";
      print OUT "Please monitor the update of related piece range files at /cgi-bin/temp directory.";
   $> = $<;
   $) = $(;
   close(OUT);
  }
}

if ($piece_limit <= 200 ) {
  #switch to use spare awb range file
  $sw=`./temp/switchfile_pcs.sh`;
  #$sw=`$home_test/webapps/cgi/temp/switchfile_pcs.sh`;
  
}
&unlock_file ($filename);
if ($piece_id > $max_piece_id){
   print "<html><body bgcolor=white><center>\n";
   print "<br><h2>Please contact DHL for further information.</h2>\n";
   print "</center></body></html>\n";
   exit();
}

#}



#$dhl_acc_no = $Form{dhl_acc_no};
#if (($dhl_acc_no =~ /\D/) || (length($dhl_acc_no) != 9)){
#	$dhl_acc_no = "";
#}

#$ProdCode = "";
#$DutiFlag = "";

if (($Form{dhl_acc_no} eq "") && ($Form{'charge_to'} ne 'CASH')) {
  $Form{'dhl_acc_no'} = $Form{'charge_to_account'};
}

$dhl_acc_no = $Form{'dhl_acc_no'};

if ($Form{'ship_product'} eq 'DOCUMENT') {
	#if ($Form{'ship_product_dtl'} eq 'OTHER SERVICE') {
	#	if ($dhl_acc_no eq ""){
	#		$dhl_acc_no = "CASHHKG";
  #  }
  #} else {
    if ($dhl_acc_no eq ""){
			#$dhl_acc_no = "CASHHKG";
			$dhl_acc_no = "CASHHKHKG";
    }
  #}
  
  $DutiFlag = 'N';
  	
} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
	if ($dhl_acc_no eq ""){
		#$dhl_acc_no = "SPXCASH";
		$dhl_acc_no = "CASHHKHKG";
  }
  
  $DutiFlag = 'Y';
}

#set default for null ship product dtl selected
#if ($Form{'ship_product_dtl'} eq '') {
#    $Form{'ship_product_dtl'} = 'EXPRESS WORLDWIDE';
#}

if ($Form{'ship_product_dtl'} eq 'EXPRESS 0900') {
	if ($Form{'ship_product'} eq 'DOCUMENT') {
    $ProdCode = 'K';
	} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
		$ProdCode = 'E';
	}
} elsif ($Form{'ship_product_dtl'} eq 'EXPRESS 1030') {
  if ($Form{'ship_product'} eq 'DOCUMENT') {
    $ProdCode = 'L';
	} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
		$ProdCode = 'M';
	}    		
} elsif ($Form{'ship_product_dtl'} eq 'EXPRESS 1200') {
  if ($Form{'ship_product'} eq 'DOCUMENT') {
    $ProdCode = 'T';
	} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
		$ProdCode = 'Y';
	}    
} elsif ($Form{'ship_product_dtl'} eq 'EXPRESS WORLDWIDE') {
  if ($Form{'ship_product'} eq 'DOCUMENT') {
    $ProdCode = 'D';
	} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
		#$ProdCode = 'S';
		$ProdCode = 'P';
	}
} elsif ($Form{'ship_product_dtl'} eq 'ECONOMY SELECT') {
  #$ProdCode = 'F'; 
  $ProdCode = 'H'; 
#} elsif ($Form{'ship_product_dtl'} eq 'OTHER SERVICE') {
} elsif ($Form{'ship_product_dtl'} eq 'EXPRESS EASY') {
  if ($Form{'ship_product'} eq 'DOCUMENT') {
  	#if ($Form{'other'} eq 'JUMBO BOX'){      
        ##$ProdCode = 'G';
        #$ProdCode = '7';
  	#} elsif ($Form{'other'} eq 'JUMBO JUNIOR'){
    	#$ProdCode = '7';
    	##$ProdCode = 'B';
    	#if ($Form{'other'} eq 'EXPRESS EASY'){      
    	   $ProdCode = '7';
        #}
    
  } elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
  	#if ($Form{'other'} eq 'JUMBO BOX'){      
         ##$ProdCode = 'J';
         #$ProdCode = '8';
  	#} elsif ($Form{'other'} eq 'JUMBO JUNIOR'){
    	#$ProdCode = '8';
    	##$ProdCode = 'W';
    	#if ($Form{'other'} eq 'EXPRESS EASY'){
    	   $ProdCode = '8';
        #}
    
  }
}



if ((uc($Form{'ship_insurance'}) eq 'ON') || (uc($Form{'ship_insurance'}) eq 'Y')) {
  $insurance = $Form{'ship_insur_value'};
}
else{
  $insurance = "0";
}

#$Form{send_media} = "tel";
#$Form{consign_media} = "tel";

#$contents_desc = $Form{'contents_desc'};
#$contents_desc =~ s/<br><br>//g;
#$contents_desc =~ s/<br>//g;
#$contents_desc =~ s/[\n]/ /g;
#$contents_desc =~ s/[\r]//g;
#$contents_desc =~ s/[\t]//g;
#$contents_desc =~ s/\|//g;
#$contents_desc = trim($contents_desc);

$Form{send_company} =~ s/[\t]//g;
$Form{send_company} =~ s/\|//g;
$Form{send_company} = trim($Form{send_company});
$Form{reference} =~ s/[\t]//g;
$Form{reference} =~ s/\|//g;
$Form{reference} = trim($Form{reference});
$Form{send_name} =~ s/[\t]//g;
$Form{send_name} =~ s/\|//g;
$Form{send_name} = trim($Form{send_name});
$Form{send_address1} =~ s/[\t]//g;
$Form{send_address1} =~ s/\|//g;
$Form{send_address1} = trim($Form{send_address1});
$Form{send_address2} =~ s/[\t]//g;
$Form{send_address2} =~ s/\|//g;
$Form{send_address2} = trim($Form{send_address2});
$Form{send_address3} =~ s/[\t]//g;
$Form{send_address3} =~ s/\|//g;
$Form{send_address3} = trim($Form{send_address3});
$Form{send_media} =~ s/[\t]//g;
$Form{send_media} =~ s/\|//g;
$Form{send_media} = trim($Form{send_media});
$Form{send_tel} =~ s/[\t]//g;
$Form{send_tel} =~ s/\|//g;
$Form{send_tel} = trim($Form{send_tel});
$Form{consign_company} =~ s/[\t]//g;
$Form{consign_company} =~ s/\|//g;
$Form{consign_company} = trim($Form{consign_company});
$Form{consign_person} =~ s/[\t]//g;
$Form{consign_person} =~ s/\|//g;
$Form{consign_person} = trim($Form{consign_person});
$Form{consign_address1} =~ s/[\t]//g;
$Form{consign_address1} =~ s/\|//g;
$Form{consign_address1} = trim($Form{consign_address1});
$Form{consign_address2} =~ s/[\t]//g;
$Form{consign_address2} =~ s/\|//g;
$Form{consign_address2} = trim($Form{consign_address2});
$Form{consign_address3} =~ s/[\t]//g;
$Form{consign_address3} =~ s/\|//g;
$Form{consign_address3} = trim($Form{consign_address3});
$Form{consign_city} =~ s/[\t]//g;
$Form{consign_city} =~ s/\|//g;
$Form{consign_city} = trim($Form{consign_city});
$Form{consign_state} =~ s/[\t]//g;
$Form{consign_state} =~ s/\|//g;
$Form{consign_state} = trim($Form{consign_state});
$Form{consign_media} =~ s/[\t]//g;
$Form{consign_media} =~ s/\|//g;
$Form{consign_media} = trim($Form{consign_media});
$Form{consign_tel} =~ s/[\t]//g;
$Form{consign_tel} =~ s/\|//g;
$Form{consign_tel} = trim($Form{consign_tel});
$Form{consign_pc} =~ s/[\t]//g;
$Form{consign_pc} =~ s/\|//g;
$Form{consign_pc} = trim($Form{consign_pc});
$Form{ship_qty} =~ s/[\t]//g;
$Form{ship_qty} =~ s/\|//g;
$Form{ship_qty} = trim($Form{ship_qty});
$Form{ship_weight} =~ s/[\t]//g;
$Form{ship_weight} =~ s/\|//g;
$Form{ship_weight} = trim($Form{ship_weight});
$Form{declare_currency} =~ s/[\t]//g;
$Form{declare_currency} =~ s/\|//g;
$Form{declare_currency} = trim($Form{declare_currency});
$Form{declare_value} =~ s/[\t]//g;
$Form{declare_value} =~ s/\|//g;
$Form{declare_value} = trim($Form{declare_value});
$Form{commodity_code} =~ s/[\t]//g;
$Form{commodity_code} =~ s/\|//g;
$Form{commodity_code} = trim($Form{commodity_code});
$Form{charge_to_account} =~ s/[\t]//g;
$Form{charge_to_account} =~ s/\|//g;
$Form{charge_to_account} = trim($Form{charge_to_account});


$d1=`date +%y%m%d`;
chomp($d1);

$t1=`date +%H%M`;
chomp($t1);

if ($Form{send_media} eq '') {
   $Form{send_media} = "Tel";
}

if ($Form{consign_media} eq '') {
   $Form{consign_media} = "Tel";
}

#used input country name only if country code is not provided
#if ($Form{consign_country_nm} ne '') {
if (($Form{consign_country} eq '') && ($Form{consign_country_nm} ne '')) {
   $cnty_data = $Form{consign_country_nm};
} else {
   $cnty_data = $country_list{uc($Form{consign_country})};
}

$srv_cat="";
if ((uc($Form{'dest_duties'}) eq 'SENDER') || (uc($Form{'dest_duties'}) eq 'OTHER')) {
#if (uc($Form{'dest_duties'}) eq 'SENDER') {
	$srv_cat = "DTP";
}

#if (uc($Form{'dest_duties'}) eq 'OTHER'){
	##$srv_cat = "NDS";
	#$srv_cat = "DDP";
#}

#create the awb file

#if (($Form{origin} eq '') && ($Form{siteID} eq '')) {
#if (($Form{origin} eq '') || ($Form{origin} eq 'HKG')) {



#create GLS interface file for creating request XML file for request submission
#- create request XML file based on the interface file
#- submit request to extract PDF awb from response XML
#- show PDF awb on browser

$dhl_acc_no_dis=$Form{dhl_acc_no};

#if (($Form{'charge_to'} eq 'CASH') && ($Form{dhl_acc_no} eq "")) {
if ($Form{'charge_to'} eq 'CASH') {
	#$dhl_acc_no_dis ='CASH&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
	$dhl_acc_no_dis ='CASH';
}

$export="";
if ($Form{'export'} eq 'PERMANENT'){
   $export="Permanent";
}
if ($Form{'export'} eq 'REPAIR/RETURN'){
   $export="Repair / Return";
}
if ($Form{'export'} eq 'TEMPORARY'){
   $export="Temporary";
}



#$gls_file_name = $home_test.'/web_files/awb/gls/work/'.$airway_no.'.gls';
$gls_file_name = $home.'/web_files/awb/gls/work/'.$airway_no.'.gls';

$awb_string = $airway_no."|".$origin_ctry."|".$origin_city."|".$ProdCode."|".
		$Form{send_company}."|".$Form{send_name}."|".$Form{send_address1}."|".$Form{send_address2}."|".$Form{send_address3}."|".
		$Form{send_media}."|".$Form{send_tel}."|".
		$Form{consign_company}."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$Form{consign_address3}."|".
		$param_pc."|".$in_city."|".$Form{consign_state}."|".$cnty_data."|".$country_code."|".
		$Form{consign_person}."|".$Form{consign_media}."|".$Form{consign_tel}."|".
		$dhl_acc_no_dis."|".$Form{reference}."|".$Form{declare_currency}."|".$Form{declare_value}."|".
		$Form{ship_qty}."|".$Form{ship_weight}."|".
		$Form{charge_to_account}."|".$srv_cat."||".$Form{dest_other}."|".$contents_desc."|".
		$insurance."|".$export."|".$Form{commodity_code}."|".$piece_id_next;
		
$> = $<;
$) = $(;
open(AWB, '>', "$gls_file_name") || die "Can't create gls interface file.\n";
print AWB "$awb_string";
$> = $<;
$) = $(;
close(AWB);

$gls_master_filename = $Form{clientID};

$gls_result=`./label/gls_feeder.sh \"$airway_no\" \"$Form{awb_paper_ty}\" \"$Form{pr_cust_cp}\" \"web feeder\" \"$gls_master_filename\"`;
#$gls_result=`$home_test/public_html/cgi-bin/label/gls_feeder.sh \"$airway_no\" \"$Form{awb_paper_ty}\" \"$Form{pr_cust_cp}\" \"web feeder\" \"$gls_master_filename\"`;
$gls_result =~ s/\s+$//;

if ($gls_result ne 'true') {	
  print "<html><body bgcolor=white><center>\n";
  print "<br><h2>Please contact DHL for further information.</h2>\n";
  #print "<br><br><br>Error Code: $airway_no,$Form{awb_paper_ty},$Form{pr_cust_cp},$gls_master_filename\n";
  print "<br><br><br>Error Code: $airway_no\n";
  print "</center></body></html>\n";
} else {

#$str_consign_company = $Form{consign_company};
#$str_consign_person = $Form{consign_person};
#$str_consign_address1 = $Form{consign_address1};
#$str_consign_address2 = $Form{consign_address2};
$str_consign_address3 = $Form{consign_address3};
$str_consign_state = $Form{consign_state};

if ($is_old_cust eq 'N') {
   $str_consign_address3 = $Form{consign_city};
}

#SPS 2.07 support transliteration 
 #if (($Form{consign_company} ne '') && ($Form{consign_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_company = "."; 
 #}
 #if (($Form{consign_person} ne '') && ($Form{consign_person} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_person = "."; 
 #}
 #if (($Form{consign_address1} ne '') && ($Form{consign_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_address1 = "In Chinese"; 
 #}
 #if (($Form{consign_address2} ne '') && ($Form{consign_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_address2 = "In Chinese"; 
 #}
 if (($str_consign_address3 ne '') && ($str_consign_address3 =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
   $str_consign_address3 = ".";
 }
 if (($Form{consign_state} ne '') && ($Form{consign_state} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
   $str_consign_state = "."; 
 }
 

    #$awb_file_name = $home_test.'/web_files/awb/work/'.$airway_no.'.awb';
    $awb_file_name = $home.'/web_files/awb/work/'.$airway_no.'.awb';
    
    $awb_string = $airway_no."|".$dhl_acc_no."|".$Form{send_company}."|".$Form{reference}."|".$Form{send_name}."|".
		$Form{send_address1}."|".$Form{send_address2}."|".$Form{send_address3}."|".$Form{send_media}."|".$Form{send_tel}."|".
		$Form{consign_company}."|".$Form{consign_person}."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$str_consign_address3."|".
		$cnty_data."|".$Form{consign_media}."|".$Form{consign_tel}."|".$param_pc."|".$ProdCode."|".
		$DutiFlag."|".$Form{ship_qty}."|".$Form{ship_weight}."|".$insurance."|".$Form{declare_currency}."|".
		$Form{declare_value}."|".$contents_desc."|".$Form{dest_other}."|".$d1."|".$t1."|".
		$Form{charge_to_account}."|".$station_code."|".$country_code."|"."JD01".$piece_id_next."|".$srv_cat."|".$Form{NDS}."||".$Form{origin}."|".
		$str_consign_state."|"."|".$ENV{'HTTP_REFERER'}."|"."|".$facility_code."|"."|1";
		
		$> = $<;
		$) = $(;
		open(AWB, '>', "$awb_file_name") || die "Can't create awb_file.\n";
    print AWB "$awb_string";
    $> = $<;
    $) = $(;
    close(AWB);
    


#create data file for loading to DB for checking pickup checkpoint
if (($Form{alert_email} ne '') || ($Form{email_template} ne '')) {
     #$awb_file_name_load = $home_test.'/web_files/awb/load_data/work/'.$airway_no.'.awb';
     $awb_file_name_load = $home.'/web_files/awb/load_data/work/'.$airway_no.'.awb';
     $in_d1=`date +%y\/%m\/%d`;
     chomp($in_d1);
     #$awb_string_load = "20".$in_d1."|".$airway_no."|".$dhl_acc_no."|".$Form{reference}."|".$Form{alert_email}."|".$Form{email_template}."|||N|N|||";
     #$awb_string_load = "20".$in_d1."|".$airway_no."|".$dhl_acc_no."|".$Form{reference}."|".$Form{alert_email}."|".$Form{email_template}."|||N|N||||";
     $awb_string_load = "20".$in_d1."|".$airway_no."|".$dhl_acc_no."|".$Form{reference}."|".$Form{alert_email}."|".$Form{email_template}."|||N|N||||".$contents_desc."|";

     $> = $<;
     $) = $(;
     open(AWB_load, '>', "$awb_file_name_load") || die "Can't create awb_load_file.\n";                 
     print AWB_load "$awb_string_load";
     $> = $<;
     $) = $(;
     close(AWB_load);
}


#create interface file for CN team for pre-sorting shipment with Chinese receiver address
#if ($Form{grp_id} eq 'AIA') {
if ($country_code eq 'CN') {
  if ((($Form{consign_address1} ne '') && ($Form{consign_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) || 
	 (($Form{consign_address2} ne '') && ($Form{consign_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) || 
	 (($Form{consign_address3} ne '') && ($Form{consign_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/))) {
	 
	$awb_file_name_chinese_addr = $home.'/web_files/awb/chi_addr/work/'.$airway_no.'.awb';
	
	$awb_string_chinese_addr = $airway_no."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$Form{consign_address3}."|";
	
	$> = $<;
        $) = $(;
	open(AWB_chinese_addr, '>', "$awb_file_name_chinese_addr") || die "Can't create chinese addr awb_file.\n";
 	print AWB_chinese_addr "$awb_string_chinese_addr";
 	$> = $<;
        $) = $(;
	close(AWB_chinese_addr);
	
  }
}

########### End of writing AWB files to Unix      ##########
	
	
  #print '<script type="text/javascript">window.location ="http://apps.dhl.com.hk/GLS_label/'.$airway_no.'.pdf"</script>';  

$awb_file_name_html = $home.'/webapps/awb_html/'.$Form{awb_filename};

$> = $<;
$) = $(;
open(AWB_html, '>', "$awb_file_name_html") || die "Can't create awb_html_file.\n"; 

print AWB_html <<END1;

<html>
<head>
<title>DHL Label</title>

<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">

<script language="JavaScript" src="https://mykullstc000536.apis.dhl.com/shipment_feeder/js/focus.js"></script>

</head>

<body>
<font face=Arial>

Waybill file is generated for the record.
 
<form name="toprint" method="post" action="../../../shipment_feeder/feed_print2/toprint.jsp" target="$Form{clientID}_toprint">
<input type="hidden" name="pagefrom" value="awb">
<input type="hidden" name="awb_no" value="$airway_no">
<input type="hidden" name="awb_filename" value="$Form{awb_filename}">

<input type="hidden" name="awb_printer" value="$Form{awb_printer}">
<input type="hidden" name="clientID" value="$Form{clientID}">
<input type="hidden" name="awb_paper_ty" value="$Form{awb_paper_ty}">
<input type="hidden" name="grp_id" value="$Form{grp_id}">
<input type="hidden" name="cur_rec_id" value="$Form{cur_rec_id}">
<!--<input type="hidden" name="emailadr" value="$Form{emailadr}">-->
<input type="hidden" name="contact_name" value="$Form{contact_name}">
<input type="hidden" name="logo_filename" value="$Form{logo_filename}">
<input type="hidden" name="default_charset" value="$Form{default_charset}">
<!--<input type="hidden" name="opt_charset" value="$Form{opt_charset}">-->
<input type="hidden" name="sub_grp_id" value="$Form{sub_grp_id}">
<input type="hidden" name="awb_copy" value="$Form{awb_copy}">
<input type="hidden" name="inv_copy" value="$Form{inv_copy}">
<input type="hidden" name="inv_printer" value="$Form{inv_printer}">
<input type="hidden" name="cur_awb_copy" value="$Form{cur_awb_copy}">
<input type="hidden" name="cur_inv_copy" value="$Form{cur_inv_copy}">
<input type="hidden" name="success_rec" value="$Form{success_rec}">
<input type="hidden" name="fail_rec" value="$Form{fail_rec}">
<input type="hidden" name="fail_rec_id" value="$Form{fail_rec_id}">
<input type="hidden" name="ttl_rec" value="$Form{ttl_rec}">
<input type="hidden" name="param" value="$Form{param}">
<input type="hidden" name="pr_cust_cp" value="$Form{pr_cust_cp}">
<input type="hidden" name="scriptx" value="$Form{scriptx}">
<input type="hidden" name="skip_err" value="$Form{skip_err}">
</form>

</font>
</body>

<script language="JavaScript" src="https://mykullstc000536.apis.dhl.com/shipment_feeder/js/label_feeder2/toprint.js"></script>

</html>

END1

$> = $<;
$) = $(;
close(AWB_html);

#redirect to html file
print <<END2;
<html>
<head>
<!--<meta http-equiv="Refresh" content="0; URL=../awb_html/$airway_no.html">
<script language="JavaScript" src="https://mykullstc000536.apis.dhl.com/shipment_feeder/js/label_feeder2/open.js" airway_no=\""+ $airway_no +"\"></script>
</head>
-->
Loading Waybill...
</html>

END2

}

exit();

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

sub lock_file {
   local ($file_name, $numtries) = @_;
   local ($i);
                
   ## try several times, waiting a second in between
   for ($i = 1; $i <= $numtries; ++$i) {
                
   ## true if the lock file was created
   $> = $<;
   $) = $(;
   if ( symlink ($file_name, $file_name . ".lck") ) {
   return 1;        # success!
   }
   sleep 1;
   }
   return 0;                # failure :-(
   }
                
sub unlock_file {
   local ($file_name) = @_;
   $> = $<;
   $) = $(;
   unlink ($file_name . ".lck");
}

sub round_up{
	local ($lc_total) = @_;
	@amt = split(/\./,$lc_total);
	if ($amt[1] != ''){
		$head = substr($amt[1], 0, 1);
		$second = substr($amt[1], 1, 1);
		if ($second >= 5){
			if ($head == 9){
				$amt[0] = $amt[0] + 1;
				$head = 0;
			}
			else{
				$head = $head + 1;
			}
		}
		$lc_total = "$amt[0]\.$head";
	}
	return $lc_total;
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
   $check_result = 0;
   
   &get_connect("wcmf");

   $sql_ac_str="select count(*) from invoicing_info where accnt_no = '" . $in_ac . "' and cr_status_cd = 'O' and bill_country = 'HK'";
   	
   $sql_ac=$web_db->prepare($sql_ac_str) or die "Couldn't select from invoicing_info";
   $sql_ac->execute();

   @ac_data = $sql_ac->fetchrow_array;
   if ($ac_data[0] > 0) {
	$check_result = 1;
   }
   
   return $check_result;

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

sub validate_grp_id{
   
   $in_grp_id = $_[0];
   $check_result = 0;
   
   &get_connect("webdb");

   $sql_grp_id_str="select count(*) from sf_customer where grp_id = '" . $in_grp_id . "'";
	
   $sql_grp_id=$web_db->prepare($sql_grp_id_str) or die "Couldn't select from sf_customer";
   $sql_grp_id->execute();

   @grp_id_data = $sql_grp_id->fetchrow_array;
   if ($grp_id_data[0] > 0) {
	$check_result = 1;
   }
   
   return $check_result;

}

sub onDG_lst{
   
   $in_desc = $_[0];
   $in_desc = trim(uc($in_desc));
   $check_result = 0;
   $rec_cnt = 0;

   $rec_cnt=`awk '{if (match("$in_desc", toupper(\$0))) {print \$0}}' < ./DG.lst|wc -l`;
   
   if ($rec_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}

sub onRED_lst{
   
   $in_desc = $_[0];
   $in_desc = trim(uc($in_desc));
   $check_result = 0;
   $rec_cnt = 0;

   $rec_cnt=`awk '{if (toupper(\$0) == "$in_desc") {print \$0}}' < ./RED.lst|wc -l`;
   if ($rec_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}

sub onPNR_lst{
   
   $in_desc = $_[0];
   $in_desc = trim(uc($in_desc));
   $check_result = 0;
   $rec_cnt = 0;

   $rec_cnt=`awk '{if (toupper(\$0) == "$in_desc") {print \$0}}' < ./PNR.lst|wc -l`;
   if ($rec_cnt > 0) {
	  $check_result = 1;
   }
   
   return $check_result;

}
