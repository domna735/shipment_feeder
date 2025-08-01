#!/usr/bin/perl

use lib '/appl/service/webapps/cgi-bin/';
use db_con;
use CGI;


use CGI::Cookie;

my %cookies = CGI::Cookie->fetch;
my $session_token = $cookies{'SESSIONID'} ? $cookies{'SESSIONID'}->value : '';

# Validate session token (you need to implement this function)
unless (is_valid_session($session_token)) {
    my $q = CGI->new;
    print $q->redirect('toLogin.html');
    exit;
}

my $session_id = $ENV{'HTTP_COOKIE'} =~ /SESSIONID=([^;]+)/;
unless (is_valid_session($session_id)) {
    print "Status: 401 Unauthorized\n\n";
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
	$value =~ s/^%09/<dd>/g;
	$value =~ s/%0D/<br>%0D/g;
	if (($ENV{'HTTP_REFERER'} ne '') && (index($ENV{'HTTP_REFERER'}, "?") == -1)) {
	   $value =~ tr/+/ /;
	}
	$value =~ s/%(..)/pack("c", hex($1))/eg;
	$Form{$name} = $value;
}

if (!defined $ENV{'HTTP_REFERER'}) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if (($ENV{'HTTP_REFERER'} eq '') || (index($ENV{'HTTP_REFERER'}, "?") != -1) || 
       (($ENV{'HTTP_REFERER'} ne 'https://apps.dhl.com.hk/cgi-bin/cservice.cgi') &&
        ($ENV{'HTTP_REFERER'} ne 'https://mykullstc000536.apis.dhl.com/cgi-bin/hkapp/cservice.cgi'))) {	       
	
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
  #$d=1;
 } else {
	if ($Form{dhl_acc_no} =~ /\D/) {
	  $d=1;
	} else {
	  if (substr($Form{dhl_acc_no},0,1) ne "6") {
		my $q = CGI->new;	
		print $q->redirect('sender.cgi');
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
  #$d=1;
 } else {
	if ($Form{charge_to_account} =~ /\D/) {
	  $d=1;
	} else {
	  if (substr($Form{charge_to_account},0,1) ne "6") {
		my $q = CGI->new;	
		print $q->redirect('sender.cgi');
		exit();
	  }
	}
 }
}

if (!defined $Form{consign_country}) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if (($Form{send_name} eq '') || ($Form{send_company} eq '') || ($Form{send_address1} eq '') || ($Form{send_media} eq '') || ($Form{send_tel} eq '') || 
   ($Form{consign_company} eq '') || ($Form{consign_address1} eq '') || ($Form{consign_country} eq '') || ($Form{consign_person} eq '') || 
   ($Form{consign_media} eq '') || ($Form{consign_tel} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{consign_city} eq '') && ($Form{consign_pc} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
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
  (($Form{consign_pc} ne '.') && ((length($Form{consign_pc}) > 12) || ($Form{consign_pc} =~ m/[^a-zA-Z0-9 \-]/))) ||
  (($Form{consign_city} ne '') && ((length($Form{consign_city}) > 35) || ($Form{consign_city} =~ m/[^a-zA-Z0-9\/ &()\-_',.]/))) ||
  (($Form{consign_country} ne '') && ((length($Form{consign_country}) != 2) || ($Form{consign_country} =~ m/[^A-Z]/))) ||
  (($Form{consign_tel} ne '') && ((length($Form{consign_tel}) > 18) || ($Form{consign_tel} =~ m/[^0-9\/ ()\-+]/))) ||
  (($Form{consign_email} ne '') && ((length($Form{consign_email}) > 45) || ($Form{consign_email} =~ m/[^a-zA-Z0-9@&\-_.]/))) ) {
	   
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
  
}

#block AF and SD shipment
if (($country_code eq 'AF') || ($country_code eq 'SD')) {
  my $q = CGI->new;	
  print $q->redirect('sender.cgi');
  exit();
}


if (($Form{ship_product} ne 'DOCUMENT') && ($Form{ship_product} ne 'DUTIABLE PARCEL')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if ((uc($Form{ship_product}) eq 'DUTIABLE PARCEL') && (isEU(uc($Form{consign_country})) == 1)) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if ((uc($Form{ship_product}) eq 'DUTIABLE PARCEL') && (uc($Form{consign_country}) eq 'ID')) {
  my $q = CGI->new;	
  print $q->redirect('sender.cgi');
  exit();
}

if (($Form{ship_product_dtl} ne 'EXPRESS WORLDWIDE') && ($Form{ship_product_dtl} ne 'EXPRESS 0900') && ($Form{ship_product_dtl} ne 'EXPRESS 1030') && ($Form{ship_product_dtl} ne 'EXPRESS 1200') && ($Form{ship_product_dtl} ne 'EXPRESS EASY')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
}

if (($Form{contents_desc_doc} ne '') && 
(($Form{contents_desc_doc} ne 'BILL OF LADING') && 
 ($Form{contents_desc_doc} ne 'CERTIFICATE') && 
 ($Form{contents_desc_doc} ne 'CHECK/CHEQUE') && 
 ($Form{contents_desc_doc} ne 'CONTRACT') && 
 ($Form{contents_desc_doc} ne 'CREDIT NOTE') && 
 ($Form{contents_desc_doc} ne 'CREDIT/DEBIT CARD') && 
 ($Form{contents_desc_doc} ne 'DIPLOMATIC MAIL') && 
 ($Form{contents_desc_doc} ne 'DOCUMENTATION') && 
 ($Form{contents_desc_doc} ne 'DOCUMENTS') && 
 ($Form{contents_desc_doc} ne 'IDENTITY DOCUMENT') && 
 ($Form{contents_desc_doc} ne 'JOURNAL') && 
 ($Form{contents_desc_doc} ne 'LETTER') && 
 ($Form{contents_desc_doc} ne 'PRINTED MATTER') && 
 ($Form{contents_desc_doc} ne 'OTHERS'))) {
  
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{contents_desc_doc} eq 'OTHERS') && ($Form{contents_desc_doc_oth} eq '')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{ship_product} eq 'DUTIABLE PARCEL') && ($Form{contents_desc} eq '')) {
    my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{'declare_currency'} ne '') && (($Form{'declare_currency'} ne 'HKD') && ($Form{'declare_currency'} ne 'USD') && ($Form{'declare_currency'} ne 'EUR') && ($Form{'declare_currency'} ne 'JPY') && ($Form{'declare_currency'} ne 'GBP') && ($Form{'declare_currency'} ne 'NZD') && ($Form{'declare_currency'} ne 'AUD') && ($Form{'declare_currency'} ne 'CNY'))) {
    my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}    

if (($Form{'declare_value'} ne '') && !($Form{declare_value} =~ /^-?\d+\.?\d*$/)) {
   my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}    

if (($Form{'dest_duties'} ne '') && (($Form{'dest_duties'} ne 'Sender') && ($Form{'dest_duties'} ne 'Receiver') && ($Form{'dest_duties'} ne 'Other'))) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
} 

if ($Form{dest_other} ne '') {
 $Form{dest_other} = uc($Form{dest_other});
 if ((length($Form{dest_other}) > 9) || ($Form{dest_other} =~ m/[^A-Z0-9]/)) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
 }
}

if (($Form{'ship_insurance'} ne '') && ($Form{'ship_insurance'} ne 'ON')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{'ext'} ne '') && ($Form{'ext'} ne 'ON')) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($Form{'ship_insur_value'} ne '') && !($Form{ship_insur_value} =~ /^-?\d+\.?\d*$/)) {
    my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if ($Form{ship_qty} =~ /\D/) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (!($Form{ship_weight} =~ /^-?\d+\.?\d*$/)) {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if ($Form{ship_product} eq 'DUTIABLE PARCEL') {
  if ($Form{item_list} eq '') {
	my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  if (($Form{print_inv} ne 'Y') && ($Form{print_inv} ne 'N')) {
    my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  if (($Form{'inv_ty'} ne '') && (($Form{'inv_ty'} ne 'proforma') && ($Form{'inv_ty'} ne 'commercial'))) {
  	my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  if (($Form{inv_num} ne '') && ((length($Form{inv_num}) > 15) || ($Form{inv_num} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) {
    my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  if (($Form{export_reason} ne '') && ((length($Form{export_reason}) > 40) || ($Form{export_reason} =~ m/[^a-zA-Z0-9\/ `~!@#^&()\-_+{}:',.]/))) {
    my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  if (($Form{'export_ty'} ne 'Permanent') && ($Form{'export_ty'} ne 'Temporary') && ($Form{'export_ty'} ne 'Repair/Return')) {
  	my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
  
  if (($Form{incoterm} ne '') && 
	(($Form{incoterm} ne 'CIP') && 
	 ($Form{incoterm} ne 'CPT') && 
	 ($Form{incoterm} ne 'DAP') && 
	 ($Form{incoterm} ne 'DAT') && 
	 ($Form{incoterm} ne 'DDP') && 
	 ($Form{incoterm} ne 'DDU') && 
	 ($Form{incoterm} ne 'DEQ') && 
	 ($Form{incoterm} ne 'DES') && 
	 ($Form{incoterm} ne 'EXW') && 
	 ($Form{incoterm} ne 'FAS') && 
	 ($Form{incoterm} ne 'FCA') && 
	 ($Form{incoterm} ne 'FOB'))) {
	my $q = CGI->new;	
	print $q->redirect('csender.cgi');
	exit();
	#$d=1;
  }
}


if ($Form{agreetc} ne "Y") {
  my $q = CGI->new;	
  print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

##########

$home="../..";

%tel_cd_list = (
"+93"       => "AF", 
"+355"      => "AL", 
"+213"      => "DZ", 
"+1-684"    => "AS", 
"+376"      => "AD", 
"+244"      => "AO", 
"+1-264"    => "AI", 
"+1-268"    => "AG", 
"+54"       => "AR", 
"+374"      => "AM", 
"+297"      => "AW", 
"+61"       => "AU", 
"+43"       => "AT", 
"+994"      => "AZ", 
"+1-242"    => "BS", 
"+973"      => "BH", 
"+880"      => "BD", 
"+1-246"    => "BB", 
"+375"      => "BY", 
"+32"       => "BE", 
"+501"      => "BZ", 
"+229"      => "BJ", 
"+1-441"    => "BM", 
"+975"      => "BT", 
"+591"      => "BO", 
"+599"      => "XB", 
"+387"      => "BA", 
"+267"      => "BW", 
"+55"       => "BR", 
"+673"      => "BN", 
"+359"      => "BG", 
"+226"      => "BF", 
"+257"      => "BI", 
"+855"      => "KH", 
"+237"      => "CM", 
"+1"        => "CA", 
"+34"       => "IC", 
"+238"      => "CV", 
"+1-345"    => "KY", 
"+236"      => "CF", 
"+235"      => "TD", 
"+56"       => "CL", 
"+86"       => "CN", 
"+57"       => "CO", 
"+1-670"    => "MP", 
"+269"      => "KM", 
"+242"      => "CG", 
"+243"      => "CD", 
"+682"      => "CK", 
"+506"      => "CR", 
"+225"      => "CI", 
"+385"      => "HR", 
"+53"       => "CU", 
"+599"      => "XC", 
"+357"      => "CY", 
"+420"      => "CZ", 
"+45"       => "DK", 
"+253"      => "DJ", 
"1-767"     => "DM", 
"+1-809"    => "DO", 
"+1-829"    => "DO", 
"+1-849"    => "DO", 
"+670"      => "TL", 
"+593"      => "EC", 
"+20"       => "EG", 
"+503"      => "SV", 
"+291"      => "ER", 
"+372"      => "EE", 
"+251"      => "ET", 
"+500"      => "FK", 
"+298"      => "FO", 
"+679"      => "FJ", 
"+358"      => "FI", 
"+33"       => "FR", 
"+594"      => "GF", 
"+241"      => "GA", 
"+220"      => "GM", 
"+995"      => "GE", 
"+49"       => "DE", 
"+233"      => "GH", 
"+350"      => "GI", 
"+30"       => "GR", 
"+299"      => "GL", 
"+1-473"    => "GD", 
"+590"      => "GP", 
"+1-671"    => "GU", 
"+502"      => "GT", 
"+44-1481"  => "GG", 
"+224"      => "GN", 
"+245"      => "GW", 
"+240"      => "GQ", 
"+592"      => "GY", 
"+509"      => "HT", 
"+504"      => "HN", 
"+852"      => "HK", 
"+36"       => "HU", 
"+354"      => "IS", 
"+91"       => "IN", 
"+62"       => "ID", 
"+98"       => "IR", 
"+964"      => "IQ", 
"+353"      => "IE", 
"+972"      => "IL", 
"+39"       => "IT", 
"+1-876"    => "JM", 
"+81"       => "JP", 
"+44-1534"  => "JE", 
"+962"      => "JO", 
"+7"        => "KZ", 
"+254"      => "KE", 
"+686"      => "KI", 
"+82"       => "KR", 
"+850"      => "KP", 
"+383"      => "KV", 
"+965"      => "KW", 
"+996"      => "KG", 
"+856"      => "LA", 
"+371"      => "LV", 
"+961"      => "LB", 
"+266"      => "LS", 
"+231"      => "LR", 
"+218"      => "LY", 
"+423"      => "LI", 
"+370"      => "LT", 
"+352"      => "LU", 
"+853"      => "MO", 
"+389"      => "MK", 
"+261"      => "MG", 
"+265"      => "MW", 
"+60"       => "MY", 
"+960"      => "MV", 
"+223"      => "ML", 
"+356"      => "MT", 
"+692"      => "MH", 
"+596"      => "MQ", 
"+222"      => "MR", 
"+230"      => "MU", 
"+262"      => "YT", 
"+52"       => "MX", 
"+691"      => "FM", 
"+373"      => "MD", 
"+377"      => "MC", 
"+976"      => "MN", 
"+382"      => "ME", 
"+1-664"    => "MS", 
"+212"      => "MA", 
"+258"      => "MZ", 
"+95"       => "MM", 
"+264"      => "NA", 
"+674"      => "NR", 
"+977"      => "NP", 
"+599"      => "AN", 
"+31"       => "NL", 
"+1-869"    => "XN", 
"+687"      => "NC", 
"+64"       => "NZ", 
"+505"      => "NI", 
"+227"      => "NE", 
"+234"      => "NG", 
"+683"      => "NU", 
"+47"       => "NO", 
"+968"      => "OM", 
"+92"       => "PK", 
"+680"      => "PW", 
"+507"      => "PA", 
"+675"      => "PG", 
"+595"      => "PY", 
"+51"       => "PE", 
"+63"       => "PH", 
"+48"       => "PL", 
"+351"      => "PT", 
"+1-787"    => "PR", 
"+1-939"    => "PR", 
"+974"      => "QA", 
"+262"      => "RE", 
"+40"       => "RO", 
"+7"        => "RU", 
"+250"      => "RW", 
"+290"      => "SH", 
"+685"      => "WS", 
"+378"      => "SM", 
"+239"      => "ST", 
"+966"      => "SA", 
"+221"      => "SN", 
"+381"      => "RS", 
"+248"      => "SC", 
"+232"      => "SL", 
"+65"       => "SG", 
"+421"      => "SK", 
"+386"      => "SI", 
"+677"      => "SB", 
"+252"      => "SO", 
"+252"      => "XS", 
"+27"       => "ZA", 
"+211"      => "SS", 
"+34"       => "ES", 
"+94"       => "LK", 
"+590"      => "XY", 
"+599"      => "XE", 
"+1-869"    => "KN", 
"+1-758"    => "LC", 
"+1-721"    => "XM", 
"+1-784"    => "VC", 
"+249"      => "SD", 
"+597"      => "SR", 
"+268"      => "SZ", 
"+46"       => "SE", 
"+41"       => "CH", 
"+963"      => "SY", 
"+689"      => "PF", 
"+886"      => "TW", 
"+992"      => "TJ", 
"+255"      => "TZ", 
"+66"       => "TH", 
"+228"      => "TG", 
"+676"      => "TO", 
"+1-868"    => "TT", 
"+216"      => "TN", 
"+90"       => "TR", 
"+1-649"    => "TC", 
"+688"      => "TV", 
"+256"      => "UG", 
"+380"      => "UA", 
"+971"      => "AE", 
"+44"       => "GB", 
"+1"        => "US", 
"+598"      => "UY", 
"+998"      => "UZ", 
"+678"      => "VU", 
"+379"      => "VA", 
"+58"       => "VE", 
"+84"       => "VN", 
"+1-284"    => "VG", 
"+1-340"    => "VI", 
"+967"      => "YE", 
"+260"      => "ZM", 
"+263"      => "ZW");

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


print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


$err = 0;
$station_code='';

############ validation for direct posting (to be removed) ##############


if ($err == 0) {
    if (defined $Form{charge_to}) {
       if ($Form{'charge_to'} eq '') {
    	$err = 1;
    	$err_str = 'Please input charge to option.';
       } else {
       	  if ((uc($Form{'charge_to'}) ne 'SHIPPER') && (uc($Form{'charge_to'}) ne 'RECEIVER') && (uc($Form{'charge_to'}) ne 'OTHERS') && (uc($Form{'charge_to'}) ne 'CASH')) {
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
  if (uc($Form{'charge_to'}) eq 'SHIPPER') {
    if (defined $Form{dhl_acc_no}) {
       if ($Form{'dhl_acc_no'} eq '') {
    	$err = 1;
    	$err_str = 'Please input DHL account number.';
       }
    } else {
       $err = 1;
       $err_str = 'Please input DHL account number.';
    }
  } elsif ((uc($Form{'charge_to'}) eq 'RECEIVER') || (uc($Form{'charge_to'}) eq 'OTHERS')) {
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
   
   if ($Form{dhl_acc_no} ne "") {
   if ($Form{dhl_acc_no} =~ /\D/) {
     $Form{dhl_acc_no} = uc($Form{'dhl_acc_no'});
	 if (isFOC_CASH($Form{dhl_acc_no}) == 0) {
      $err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
     }
      
   } else {
     if (length($Form{dhl_acc_no}) != 9) {
     	$err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
     } else {
     	#if ((substr($Form{dhl_acc_no},0,2) ne '63') && (substr($Form{dhl_acc_no},0,2) ne '64') && (substr($Form{dhl_acc_no},0,2) ne '96') && (substr($Form{dhl_acc_no},0,2) ne '95') && (substr($Form{dhl_acc_no},0,2) ne '94')) {
		if ((substr($Form{dhl_acc_no},0,2) ne '63') && (substr($Form{dhl_acc_no},0,2) ne '64')) {
     	   $err_msg = $err_msg . "Sender account no. is invalid.<br><br>";
     	} else {
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
				#  if (validate_billed_ac($Form{dhl_acc_no}, $Form{origin}) == 0) {
				#    $err_msg = $err_msg . '由<b>2021年9月1日</b>起，此應用程式將不再支援 "<b>DHL 進口帳號</b>" (即字首為95/96的帳號) 作為寄件人帳號 。<br>請您使用"<b>DHL 出口帳號</b>" 作為寄件人帳號，或註冊使用網上工具 <a href="https://mydhl.express.dhl/hk/zh/ship/solutions.html" target="mydhl" rel="noopener noreferrer"><b>MyDHL+</b></a>製作你的提單。 (<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_TC_202107.pdf" target="reg_guide" rel="noopener noreferrer">註冊教學</a>)<br><br>';
				#	$err_msg = $err_msg . 'Effective from <b>1 September 2021</b>, this application will not support "<b>DHL Import Express</b>" account number (i.e. 95/96 prefix) as Shipper accounts.<br>Please use "<b>DHL Export</b>" account number as Shipper account, or please register our online tool <a href="https://mydhl.express.dhl/hk/en/ship/solutions.html" target="mydhl" rel="noopener noreferrer"><b>MyDHL+</b></a> to create your waybills. (<a href="https://shipping.dhl.com.hk/Global/FileLib/HongKong/MyDHL__Registration_Guide_EN_202107.pdf" target="reg_guide" rel="noopener noreferrer">Registration Guide</a>)<br><br>';
				#  }
			   #}
			   
			 }
		  }
     	}
     }
   }
  }
  			   
  
   if ($Form{charge_to_account} ne "") {
    if ($Form{charge_to_account} =~ /\D/) {
     $Form{charge_to_account} = uc($Form{'charge_to_account'});
     if (isFOC_CASH($Form{charge_to_account}) == 0) {
		 $err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
	 }
    } else {
     if (length($Form{charge_to_account}) != 9) {
     	$err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
     } else {
     	#if ((substr($Form{charge_to_account},0,2) ne '63') && (substr($Form{charge_to_account},0,2) ne '64') && (substr($Form{charge_to_account},0,2) ne '96') && (substr($Form{charge_to_account},0,2) ne '95') && (substr($Form{charge_to_account},0,2) ne '94')) {
		if ((substr($Form{charge_to_account},0,2) ne '63') && (substr($Form{charge_to_account},0,2) ne '64')) {
     	   $err_msg = $err_msg . "Payer account no. is invalid.<br><br>";
     	} else {
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

if (defined $Form{contents_desc_doc}) {
  if ($Form{'contents_desc_doc'} ne '') {
    if ($Form{'contents_desc_doc'} eq 'OTHERS') {
	  $Form{'contents_desc'} = $Form{contents_desc_doc_oth};
	} else {
	  $Form{'contents_desc'} = $Form{contents_desc_doc};
	}
  }
}

$contents_desc = $Form{'contents_desc'};
$contents_desc =~ s/<br><br>//g;
$contents_desc =~ s/<br>//g;
#$contents_desc =~ s/[\n]/ /g;
$contents_desc =~ s/[\n]//g;
$contents_desc =~ s/[\r]//g;
$contents_desc =~ s/[\t]//g;
$contents_desc =~ s/\|//g;
$contents_desc = trim($contents_desc);

if ($err == 0) {
    
    	if ((($Form{charge_to} ne '') && ($Form{charge_to} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) || 
	   (($Form{ship_insur_value} ne '') && ($Form{ship_insur_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{ship_insur_currency} ne '') && ($Form{ship_insur_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{reference} ne '') && ($Form{reference} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_name} ne '') && ($Form{send_name} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||   
	   (($Form{send_company} ne '') && ($Form{send_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address1} ne '') && ($Form{send_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address2} ne '') && ($Form{send_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_address3} ne '') && ($Form{send_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_pc} ne '') && ($Form{send_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{send_tel} ne '') && ($Form{send_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_pc} ne '') && ($Form{consign_pc} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_city} ne '') && ($Form{consign_city} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_state} ne '') && ($Form{consign_state} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country} ne '') && ($Form{consign_country} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_country_nm} ne '') && ($Form{consign_country_nm} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{consign_tel} ne '') && ($Form{consign_tel} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{contents_desc_doc_oth} ne '') && ($Form{contents_desc_doc_oth} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($contents_desc ne '') && ($contents_desc =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_currency} ne '') && ($Form{declare_currency} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{declare_value} ne '') && ($Form{declare_value} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_duties} ne '') && ($Form{dest_duties} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ||
	   (($Form{dest_other} ne '') && ($Form{dest_other} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/))  ||
	   (($Form{inv_num} ne '') && ($Form{inv_num} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) || 
	   (($Form{export_reason} ne '') && ($Form{export_reason} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) ) {
	    	
	    	$err = 1;
       		#$err_str = 'No Chinese character is allowed for DOCUMENT except Receiver company name, contact name and address line 1, 2 & 3. Please input again.';
       		$err_str = 'No Chinese character is allowed except Receiver company name, contact name and address line 1, 2 & 3. Please input again.';
       	}
    #}
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
		    } else {
			   if ($Form{contents_desc_doc_oth} ne '') {
					 if (onDG_lst($contents_desc_doc_oth) == 1) {
					   $err = 1;
					   $err_str = 'This application cannot support the preparation of shipment carrying &#8220;Lithium Batteries&#8221;.<br><br>Please contact your Sales Manager for assistance.';
					 } elsif (onRED_lst($contents_desc_doc_oth) == 1) {
					   $err = 1;
					   $err_str = 'Acceptable Goods Descriptions include complete information, providing sufficient detail about the precise nature of goods in plain language.<br><br>It should indicate what the goods are, for which purpose the goods are used and what is made of.';
					 } elsif (onPNR_lst($contents_desc_doc_oth) == 1) {
					   $err = 1;
					   $err_str = 'Your shipping items are either Prohibited or Restricted items, they will NOT be accepted for carriage by DHL or unless otherwise agreed to by DHL.<br><br>Please contact your Sales Manager for assistance.';
					 }

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

if ($err == 0) {
   if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
      if ((defined $Form{declare_value}) && (defined $Form{declare_currency})) {
      	 if (($Form{'declare_value'} eq '') || ($Form{'declare_currency'} eq '')) {
	     $err = 1;
	     $err_str = 'Please input declared value and currency for dutiable parcel.';
	 } else {
	     $Form{'declare_currency'}=uc($Form{'declare_currency'});
	     
	     if (($Form{'declare_currency'} ne 'HKD') && ($Form{'declare_currency'} ne 'USD') && ($Form{'declare_currency'} ne 'EUR') && ($Form{'declare_currency'} ne 'JPY') && ($Form{'declare_currency'} ne 'GBP') && ($Form{'declare_currency'} ne 'NZD') && ($Form{'declare_currency'} ne 'AUD') && ($Form{'declare_currency'} ne 'CNY')) {
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
     	     
     	     if (($Form{'declare_currency'} ne 'HKD') && ($Form{'declare_currency'} ne 'USD') && ($Form{'declare_currency'} ne 'EUR') && ($Form{'declare_currency'} ne 'JPY') && ($Form{'declare_currency'} ne 'GBP') && ($Form{'declare_currency'} ne 'NZD') && ($Form{'declare_currency'} ne 'AUD') && ($Form{'declare_currency'} ne 'CNY')) {	
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
	 	#  $err_str = 'Other account number for destination duties is invalid. Please input again';
	 	#}
	 	if ($Form{dest_other} =~ /\D/) {
	 	     $err = 1; 
		     $err_str = 'Other account number for destination duties is invalid. Please input again.';
		} else {
		     if (length($Form{dest_other}) != 9) {
		     	$err = 1;
		     	$err_str = 'Other account number for destination duties is invalid. Please input again.';
		     } else {
		     	#if ((substr($Form{dest_other},0,2) ne '63') && (substr($Form{dest_other},0,2) ne '64') && (substr($Form{dest_other},0,2) ne '96') && (substr($Form{dest_other},0,2) ne '95') && (substr($Form{dest_other},0,2) ne '94')) {
				if ((substr($Form{dest_other},0,2) ne '63') && (substr($Form{dest_other},0,2) ne '64')) {
		     	   $err = 1;
		     	   $err_str = 'Other account number for destination duties is invalid. Please input again.';
		     	} else {
		     	   if (isColoader($Form{dest_other}) == 1) {
				     $err = 1;
					 $err_str = 'You are not authorized to use this tool.';
				   } else {
				      if (isBlacklist($Form{dest_other}) == 1) {
					    $err = 1;
						$err_str = 'You are not authorized to use this account. Contact the account owner to obtain authorization.';
					  } else {
						 if (validate_ac($Form{dest_other}) == 0) {
						   $err = 1;
						   $err_str = 'Other account number for destination duties is invalid or has stopped credit. Please input again.';
						 }
					  }
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
   if (($Form{'ship_insurance'} eq 'ON') && ($Form{'ext'} eq 'ON')) {
	$err = 1;
	$err_str = 'Please select Extended Liability for DOCUMENT or Shipment Insurance for DUTIABLE PARCEL.';
   }
}

if ($err == 0) {
   if (($Form{'ship_product'} eq 'DOCUMENT') && ($Form{'ship_insurance'} eq 'ON')) {
   	$err = 1;
	$err_str = 'Shipment Insurance is for DUTIABLE PARCEL only.';
   } else {   
	if (($Form{'ship_product'} eq 'DUTIABLE PARCEL') && ($Form{'ext'} eq 'ON')) {
	   $err = 1;
	   $err_str = 'Extended Liability is for DOCUMENT only.';
	}
   }
}

if ($err == 0) {
   #if ((uc($Form{'ship_insurance'}) eq 'ON') || (uc($Form{'ship_insurance'}) eq 'Y')) {
   if ($Form{'ship_insurance'} eq 'ON'){
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


$Form{consign_city} = trim($Form{consign_city});
$Form{consign_city} = replace_spaces($Form{consign_city});

$Form{consign_pc} = trim($Form{consign_pc});
$Form{consign_pc} = replace_spaces($Form{consign_pc});


# get country code if only country name is provided
if ($err == 0) {
 if (($Form{consign_country} eq '') && ($Form{consign_country_nm} eq '')) {
  $err = 1;
	$err_str = 'Country/Territory code or name should be inputted, please input again.';
 } else {
	if ($Form{consign_country_nm} ne '') {
		 $in_cn_nm=uc($Form{consign_country_nm});
		 $country_code=`./label/get_cn_cd.sh \"$in_cn_nm\"`;
		 #$country_code='AB';
		 $country_code =~ s/\s+$//;

		 if ($country_code eq 'error') {
		 	$err = 1;
		 	$err_str = 'Invalid country/territory name, please input again.';
		 } else {
		     if ($Form{consign_country} ne '') {		     	       
		        if ($country_code ne uc($Form{consign_country})) {
		 	   $err = 1;
		 	   $err_str = 'Country/Territory name does not match with country/territory code, please input again.';
		 	}
		     }
		 }
			 
	} else {
		 $country_code = uc($Form{consign_country});		 
	}
 }
}

#block destination=HK if origin=HK
if ($Form{origin} eq '') {
  $origin_ctry='HK';
  $origin_city='HONG KONG';
  $Form{origin}='HKG';
} else {
  if ($Form{origin} eq 'MCA') {
    $origin_ctry='MO';
    $origin_city='MACAU';
  } else {
    $origin_ctry='HK';
    $origin_city='HONG KONG';
    $Form{origin}='HKG';    
  }
}

if ($err == 0) {
   if ($origin_ctry eq $country_code) {
      $err = 1;
      $err_str = "Sender and Receiver country/territory should not be the same for international shipment. Please input again.";
   }
}



# get station code
if ($err == 0) {
  $in_city='';
  
  if (defined $Form{consign_city}) {
    if ($Form{consign_city} ne '') {
  	$in_city=uc($Form{consign_city});
    }
  } else {
    if ($Form{consign_address3} ne '') {
  	$in_city=uc($Form{consign_address3});
    }
  }
  
  #$in_station='';
  #if ($Form{station_code} ne '') {
  #	$in_station=uc($Form{station_code});
  #}
  $in_pc='';
  if ($Form{consign_pc} ne '') {
     $in_pc=uc($Form{consign_pc});  
  } 
  
  #$station_code=`./label/get_stn.sh \"$country_code\" \"$in_pc\" \"$in_city\" \"$in_station\"`;
  #$station_code =~ s/\s+$//;
  
  #if (length($station_code) != 3) {
  #	$err = 1;
  #	$err_str = $station_code;			
  #}
	
}

if ($err == 0) {
 
   $param_pc=".";
   if ($in_pc ne '') {
     $param_pc = $in_pc;
   }

} 

#validate and get destination info thro GLS with the minimum data fields
if ($err == 0) {
  #$param_pc=".";
  $param_city=".";
  
  #if ($in_pc ne '') {
     #$param_pc = $in_pc;
  #}
  
  if ($in_city ne '') {
     $param_city = $in_city;
  }
  
  $param_str = $country_code."~".$param_pc."~".$param_city;
  $station_facility=`./label/gls_validate.sh \"$param_str\"`;
  $station_facility =~ s/\s+$//;
  
  #if (length($station_facility) != 7) {
  if ((length($station_facility) != 7) && (length($station_facility) != 4)) {  	
     $err = 1;
     #$err_str = $station_code;
     $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode' rel='noopener noreferrer'>list</a>.";
  } else {
     @cd = split(/\|/,$station_facility);
     $station_code = $cd[0];
     $facility_code = $cd[1];
     if ($station_code eq "") {
     	$err = 1;
        $err_str = "Sorry, the city or the postcode you entered is incorrect. Please input a valid City and Postcode (if applicable).<br><br>You may take a reference in this <a href='../../postcode2/$country_code.html' target='postcode' rel='noopener noreferrer'>list</a>.";
     }
  }
  
}

#validate and build invoice item list
$str_item_list="";
$str_item_list_gls="";
$com_val = 0;
$com_wght = 0;

if ($err == 0) {
  if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
    
     if (defined $Form{'item_list'}) {
        if ($Form{'item_list'} ne "") {
          @itemlist = split(/\^\^/,$Form{'item_list'});
          $itemlistsize=0;
          $pre_itemlistsize=@itemlist;
          if ($pre_itemlistsize > 0) {
           for ($i=0;$i<@itemlist;$i++) {
            if ($itemlist[$i] ne "") {
              @item_arr = split(/\^\~/,$itemlist[$i]);
              $item_arr_size = @item_arr;              
              if (($item_arr_size == 6) || ($item_arr_size == 7)) {
              	#validate fields
              	$chk_com=check_commodity($itemlist[$i]);
              	if ($chk_com eq "") {
              	  $itemlistsize++;
                  $str_item_list=$str_item_list."|".$item_arr[1]."|".$item_arr[2]."|".$item_arr[4]."|".$item_arr[3]."|".$item_arr[5]."|".$item_arr[0]."|".$item_arr[6];
                  if ($str_item_list_gls eq "") {
                     $str_item_list_gls=$item_arr[0]."^~".$item_arr[1]."^~".$item_arr[2]."^~".$item_arr[3]."^~".$item_arr[4]."^~".$country_list{$item_arr[5]}."^~".$item_arr[6];
                  } else {
                     $str_item_list_gls=$str_item_list_gls."^^".$item_arr[0]."^~".$item_arr[1]."^~".$item_arr[2]."^~".$item_arr[3]."^~".$item_arr[4]."^~".$country_list{$item_arr[5]}."^~".$item_arr[6];
                  }
                  
                  #$com_val = $com_val + ($item_arr[1]*$item_arr[3]);
                  $com_val = $com_val + (round_up(($item_arr[1]*$item_arr[3]),2));
                  $com_wght = $com_wght + (round_up(($item_arr[1]*$item_arr[4]),3));
                  
                } else {
                  $err = 1;
	          $err_str = $chk_com;
	          $i=@itemlist;
                }	
              } else {
                $err = 1;
	        $err_str = 'Please input commodity item information for dutiable parcel in valid format.';
	        $i=@itemlist;
              } 
            } else {
              $err = 1;
	      $err_str = 'Please input commodity item information for dutiable parcel.';
	      $i=@itemlist;
            }
          }
          $com_val = round_up($com_val,2);
          $com_wght = round_up($com_wght,3);
          
          if ($err == 0) {              
            $com_val_num = sprintf '%.2f', round_up($com_val,2);
            $declare_value_num = sprintf '%.2f', round_up($Form{'declare_value'},2);
            $com_wght_num = sprintf '%.3f', round_up($com_wght,3);
            $ship_weight_num = sprintf '%.3f', round_up($Form{'ship_weight'},3);
            
            #if (round_up($com_val,2) ne round_up($Form{'declare_value'},2)) {
            if ($com_val_num != $declare_value_num) {
              $err = 1;
	      $err_str = 'Shipment declared value does not match with total customs value of commodity item(s). Please input again.';
            } else {
            	
              if ($com_wght_num > $ship_weight_num) {
                $err = 1;
	        $err_str = 'Shipment weight does not match with total weight of commodity item(s). Please input again.'; 	
              } else {
            	$str_item_list="".$itemlistsize.$str_item_list;
              }
            }
          }
          
         } else {
           $err = 1;
	   $err_str = 'Please input commodity item information for dutiable parcel.';
         }  
          
        } else {
                $err = 1;
	   	$err_str = 'Please input commodity item information for dutiable parcel.';
        }  	
     } else {
           $err = 1;
	   $err_str = 'Please input commodity item information for dutiable parcel.';
     }     	
  } else {
     $str_item_list="0";
  }
}

if ($err == 0) {
  if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
    if ($Form{'print_inv'} eq 'Y') {
  	if (($Form{'inv_ty'} ne 'proforma') && ($Form{'inv_ty'} ne 'commercial')) {
  	    $err = 1;
            $err_str = 'Please input valid invoice type.';
  	}
  	
  	if ((lc($Form{'export_ty'}) ne 'permanent') && (lc($Form{'export_ty'}) ne 'temporary') && (lc($Form{'export_ty'}) ne 'repair/return')) {
  	    $err = 1;
            $err_str = 'Please input valid export type.';
  	}
    }
  }
}

if ($err == 0) {
  if ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
    if ($Form{'print_inv'} eq 'Y') {
    	
$incoterm_valid = "0";
@incoterm_arr = (
'',
'CIP',
'CPT',
'DAP',
'DAT',
'DDP',
'DDU',
'DEQ',
'DES',
'EXW',
'FAS',
'FCA',
'FOB');

	  foreach $t (@incoterm_arr) {
	     if ($t eq $Form{incoterm}) {
	     	$incoterm_valid = "1";
	     }
	  }
	  
	  if ($incoterm_valid eq "0") {
	     $err = 1;
	     $err_str = 'Please input valid incoterm.';
	  }
    }
  }
}


if ($err == 1) {
  #if (length($station_code) > 3) {
  #   $station_code = '';
  #} else {

print <<END1;

<html>
<head><title>DHL Waybill Printing</title>
<meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
<!--<meta http-equiv="Content-Security-Policy" content="default-src 'self'; script-src 'self'">-->
</head>

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
  t7his.MouseOver = private_MouseOver;
}

objPIC5 = new objMouseChangeImg('PIC5', back2.src, back1.src);
</script>

<body bgcolor=white>
<center><br><br><b>
<font face="Arial" size="2">$err_str</font>
</b><br><br>
<a href="javascript:history.go(-1);" onMouseOver="objPIC5.MouseOver()" onMouseOut ="objPIC5.MouseOut()"><img src="../../images/back1.gif" border=0 name=PIC5></a>
</center>
</body>
</html>

END1

exit();
 #}
}

########### Remaining section is for printing label ##########

$dhl_acc_no = $Form{dhl_acc_no};
if (($dhl_acc_no =~ /\D/) || (length($dhl_acc_no) != 9)){
	$dhl_acc_no = "";
}

if ($Form{origin} eq 'MCA') {
  $filename = "./temp_mca/airwaybill.txt";
} else {
  $filename = "./temp/airwaybill.txt";
}

##### dedicated awb range for specific a/c
if (($Form{origin} ne 'MCA') && ($dhl_acc_no ne "")) {
   $af=`./temp/getfile.sh "$dhl_acc_no".txt`;      
   if ($af ne "") {
   	$filename = "./temp/" . $dhl_acc_no . ".txt";
   }
}

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

#if ($Form{origin} eq 'MCA') {
#  $limit_factor = 0.1;
#} else {	
  $limit_factor = 1;
#}

if ($airway_limit <= 3000 * $limit_factor) {
   if ($airway_limit % (1000 * $limit_factor) == 0){
     $tosend = 1;
   } else {
     if ($airway_limit <= 100){
       if ($airway_limit % 50 == 0) {
        $tosend = 1;
       }
     }
   }
 
 #if ($Form{origin} eq 'MCA') {
   #if ($airway_limit > 100) {
   #   $tosend = 0;
   #}
 #}
 
 if ($tosend == 1) {
   $subject = '['.$Form{origin}.']'.' Only '.$airway_limit.' Waybill Number can be used!';
   $email = 'hkgwebadm@dhl.com';
   
   $> = $<;
   $) = $(;

   open( OUT ,'|-', '/usr/lib/sendmail -t -oi');
      print OUT "To\: $receiver\n";
      print OUT "From: $email\n";
      print OUT "Subject: $subject\n";
      print OUT "\n";
      print OUT "Please monitor the update of waybill number range files. For MCA, pls check to put the fixed range as spare range.";
   $> = $<;
   $) = $(;
   
   close(OUT);
 }
}

#if ($airway_limit == 0 ) {
if ($airway_limit <= 0 ) {
  #switch to use spare awb range file
  if ($Form{origin} eq 'MCA') {
    $sw=`./temp_mca/switchfile.sh`;
  } else {
    $sw=`./temp/switchfile.sh`;
  }
}
&unlock_file ($filename);
if ($airway_id > $max_air_id){
   print "<html><body bgcolor=white><center>\n";
   print "<br><h2>Please contact DHL for further information.</h2>\n";
   print "</center></body></html>\n";
   exit();
}

##### get piece ID from range

#for ($sq = 1; $sq <= $Form{ship_qty}; ++$sq) {

if ($Form{origin} eq 'MCA') {
  $filename = "./temp_mca/piece.txt";
} else {
  $filename = "./temp/piece.txt";
}

$> = $<;
$) = $(;

&lock_file ($filename, 20) || die "Can't lock $filename";
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
   
 if ($Form{origin} eq 'MCA') {
   if ($piece_limit > 300) {
      $tosend = 0;
   } else {
      $receiver = 'charmaine.chow@dhl.com';
   }
 }
   
  if ($tosend == 1) {
   $subject = '['.$Form{origin}.']'.' Only '.$piece_limit.' piece ID can be used!';
   $email = 'hkgwebadm@dhl.com';
   
   $> = $<;
   $) = $(;

   open( OUT , '|-', "/usr/lib/sendmail -t -oi");
      print OUT "To\: $receiver\n";
      print OUT "From: $email\n";
      print OUT "Subject: $subject\n";
      print OUT "\n";
      #print OUT "Please go to the server /cgi-bin/temp directory to update the piece.txt";
      print OUT "Please monitor the update of piece ID range files. For MCA, pls request for a new piece ID range if it's not done.";
   $> = $<;
   $) = $(;
   close(OUT);
  }
}

if ($piece_limit <= 200 ) {
  #switch to use spare awb range file
  if ($Form{origin} eq 'MCA') {
    $sw=`./temp_mca/switchfile_pcs.sh`;
  } else {
    $sw=`./temp/switchfile_pcs.sh`;
  }
}
&unlock_file ($filename);
if ($piece_id > $max_piece_id){
   print "<html><body bgcolor=white><center>\n";
   print "<br><h2>Please contact DHL for further information.</h2>\n";
   print "</center></body></html>\n";
   exit();
}


if (($Form{dhl_acc_no} eq "") && ($Form{'charge_to'} ne 'CASH')) {
  $Form{'dhl_acc_no'} = $Form{'charge_to_account'};
}

$dhl_acc_no = $Form{'dhl_acc_no'};

if ($Form{'ship_product'} eq 'DOCUMENT') {
	if ($Form{'ship_product_dtl'} eq 'OTHER SERVICE') {
		if ($dhl_acc_no eq ""){
			#$dhl_acc_no = "CASH";
			#$dhl_acc_no = "CASHHKG";
			if ($Form{origin} eq 'MCA') {
			  $dhl_acc_no = "CASHMOMCA";
			} else {
			  $dhl_acc_no = "CASHHKHKG";
			}			
    }
  } else {
    if ($dhl_acc_no eq ""){
			#$dhl_acc_no = "CASH";
			#$dhl_acc_no = "CASHHKG";
			if ($Form{origin} eq 'MCA') {
			  $dhl_acc_no = "CASHMOMCA";
			} else {
			  $dhl_acc_no = "CASHHKHKG";
			}			
    }
	
  }

  $DutiFlag = 'N';
  	
} elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
	if ($dhl_acc_no eq ""){
		#$dhl_acc_no = "SPXCASH";
		if ($Form{origin} eq 'MCA') {
			  $dhl_acc_no = "CASHMOMCA";
		} else {
			  $dhl_acc_no = "CASHHKHKG";
		}			
  }
  
  $DutiFlag = 'Y';
}

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
		$ProdCode = 'P';
	}
} elsif ($Form{'ship_product_dtl'} eq 'ECONOMY SELECT') {
   $ProdCode = 'H';
    
} elsif ($Form{'ship_product_dtl'} eq 'EXPRESS EASY') {
  if ($Form{'ship_product'} eq 'DOCUMENT') {    
		$ProdCode = '7';
  } elsif ($Form{'ship_product'} eq 'DUTIABLE PARCEL') {
		$ProdCode = '8';   
  }
}


if ($Form{'ship_insurance'} eq 'ON'){
  $insurance = $Form{'ship_insur_value'};
}
else{
  $insurance = "0";
}

#$Form{send_media} = "tel";
$Form{consign_media} = "Tel";

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
$Form{consign_company} =~ s/[\n]/ /g;
$Form{consign_company} =~ s/[\r]//g;
$Form{consign_company} =~ s/<br><br>//g;
$Form{consign_company} =~ s/<br>//g;
$Form{consign_company} = trim($Form{consign_company});
$Form{consign_person} =~ s/[\t]//g;
$Form{consign_person} =~ s/\|//g;
$Form{consign_person} =~ s/[\n]/ /g;
$Form{consign_person} =~ s/[\r]//g;
$Form{consign_person} =~ s/<br><br>//g;
$Form{consign_person} =~ s/<br>//g;
$Form{consign_person} = trim($Form{consign_person});
$Form{consign_address1} =~ s/[\t]//g;
$Form{consign_address1} =~ s/\|//g;
$Form{consign_address1} =~ s/[\n]/ /g;
$Form{consign_address1} =~ s/[\r]//g;
$Form{consign_address1} =~ s/<br><br>//g;
$Form{consign_address1} =~ s/<br>//g;
$Form{consign_address1} = trim($Form{consign_address1});
$Form{consign_address2} =~ s/[\t]//g;
$Form{consign_address2} =~ s/\|//g;
$Form{consign_address2} =~ s/[\n]/ /g;
$Form{consign_address2} =~ s/[\r]//g;
$Form{consign_address2} =~ s/<br><br>//g;
$Form{consign_address2} =~ s/<br>//g;
$Form{consign_address2} = trim($Form{consign_address2});
$Form{consign_address3} =~ s/[\t]//g;
$Form{consign_address3} =~ s/\|//g;
$Form{consign_address3} =~ s/[\n]/ /g;
$Form{consign_address3} =~ s/[\r]//g;
$Form{consign_address3} =~ s/<br><br>//g;
$Form{consign_address3} =~ s/<br>//g;
$Form{consign_address3} = trim($Form{consign_address3});

$Form{consign_city} =~ s/[\t]//g;
$Form{consign_city} =~ s/\|//g;
$Form{consign_city} = trim($Form{consign_city});
$Form{consign_media} =~ s/[\t]//g;
$Form{consign_media} =~ s/\|//g;
$Form{consign_media} = trim($Form{consign_media});
$Form{consign_tel} =~ s/[\t]//g;
$Form{consign_tel} =~ s/\|//g;
$Form{consign_tel} = trim($Form{consign_tel});
$Form{consign_email} =~ s/[\t]//g;
$Form{consign_email} =~ s/\|//g;
$Form{consign_email} = trim($Form{consign_email});
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


if ($Form{consign_country_nm} ne '') {
   $cnty_data = $Form{consign_country_nm};
} else {
   $cnty_data = $country_list{uc($Form{consign_country})};
}



$srv_cat="";
if ((uc($Form{'dest_duties'}) eq 'SENDER') || (uc($Form{'dest_duties'}) eq 'OTHER')) {
	$srv_cat = "DTP";
}
#if (uc($Form{'dest_duties'}) eq 'SENDER'){
#	$srv_cat = "DDP";
#}
#if (uc($Form{'dest_duties'}) eq 'OTHER'){
	#$srv_cat = "NDS";
#	$srv_cat = "DDP";
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



$gls_file_name = $home.'/web_files/awb/gls/work/'.$airway_no.'.gls';

$awb_string = $airway_no."|".$origin_ctry."|".$origin_city."|".$ProdCode."|".
		$Form{send_company}."|".$Form{send_name}."|".$Form{send_address1}."|".$Form{send_address2}."|".$Form{send_address3}."|".
		$Form{send_media}."|".$Form{send_tel}."|".
		$Form{consign_company}."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$Form{consign_address3}."|".
		$param_pc."|".$in_city."|"."|".$cnty_data."|".$country_code."|".
		$Form{consign_person}."|".$Form{consign_media}."|".$Form{consign_tel}."|".
		$dhl_acc_no_dis."|".$Form{reference}."|".$Form{declare_currency}."|".$Form{declare_value}."|".
		$Form{ship_qty}."|".$Form{ship_weight}."|".
		$Form{charge_to_account}."|".$srv_cat."|".$Form{ext}."|".$Form{dest_other}."|".$contents_desc."|".
		$insurance."|".$export."|".$Form{commodity_code}."|".$piece_id_next;
		
$> = $<;
$) = $(;

open(AWB, '>', "$gls_file_name") || die "Can't create gls interface file.\n";
print AWB "$awb_string";
$> = $<;
$) = $(;

close(AWB);


$pr_cust_cp = get_cust_cp($Form{sub_grp_id});

#$gls_result=`./label/gls_label.sh \"$airway_no\" \"$Form{paper_ty}\" \"y\" \"www.dhl.com.hk\"`;

$gls_result=`./label/gls_label.sh \"$airway_no\" \"$Form{paper_ty}\" \"$pr_cust_cp\" \"www.dhl.com.hk\"`;

$gls_result =~ s/\s+$//;
if ($gls_result ne 'true') {
  print "<html><body bgcolor=white><center>\n";
  print "<br><h2>Please contact DHL for further information.</h2>\n";
  print "<br><br><br>Error Code: $airway_no\n";
  print "</center></body></html>\n";  
} else {

	
  print "<html><body bgcolor=white>\n";
  print "<br><b>Please download and print the following WAYBILL DOC and Invoice (if applicable).\n";
  print "<br><br>Please keep one WAYBILL DOC (out of two) for your own record and as your shipment receipt.</b><br><br>\n";
  #print '<a href="./label/download_pdf.cgi?download_filename='.$airway_no.'.pdf">Waybill DOC</a>';
  print '<script type="text/javascript">';
  print 'window.open("./label/download_pdf.cgi?download_filename='.$airway_no.'.pdf", "Waybill", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=600,height=400,left=600,top=300").focus();';
  #print '</script></html>'; 
  #generate invoice
  
%incoterm_list = (
"" => "",
"CIP" => "CIP - Carriage & Insurance Paid",
"CPT" => "CPT - Carriage Paid To",
"DAP" => "DAP - Delivered At Place",
"DAT" => "DAT - Delivered At Terminal",
"DDP" => "DDP - Delivered Duty Paid",
"DDU" => "DDU - Delivered Duty Unpaid",
"DEQ" => "DEQ - Delivered Ex Quay",
"DES" => "DES - Delivered Ex Ship",
"EXW" => "EXW - Ex Works",
"FAS" => "FAS - Free Alongside Ship",
"FCA" => "FCA - Free Carrier",
"FOB" => "FOB - Free On Board");

    
if (($Form{'ship_product'} eq 'DUTIABLE PARCEL') && ($str_item_list_gls ne '')) {
 if ($Form{'print_inv'} eq 'Y') {
  $p_copy=0;
  $c_copy=0;
  if ($Form{'inv_ty'} eq 'proforma') {
    $p_copy = 2;
  }
  if ($Form{'inv_ty'} eq 'commercial') {
    $c_copy = 2;
  }
  
  #if (($Form{'proforma'} eq "1") || ($Form{'commercial'} eq "1")) {
  if (($p_copy > 0) || ($c_copy > 0)) {
    $inv_file_name = $home.'/web_files/awb/gls/work/'.$airway_no.'.inv.gls';

    $inv_string = $airway_no."|".$origin_ctry."|".$origin_city."|".
		$Form{send_company}."|".$Form{send_name}."|".$Form{send_address1}."|".$Form{send_address2}."|".$Form{send_address3}."|".
		$Form{send_media}."|".$Form{send_tel}."|".
		$Form{consign_company}."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$Form{consign_address3}."|".
		$param_pc."|".$in_city."|"."|".$cnty_data."|".
		$Form{consign_person}."|".$Form{consign_media}."|".$Form{consign_tel}."|".
		$Form{reference}."|".$Form{declare_currency}."|".$Form{inv_num}."|".$Form{export_ty}."|".$Form{export_reason}."|".
		$incoterm_list{$Form{incoterm}}."|".$str_item_list_gls;
		
		
	
	#print $inv_file_name;
	#print $inv_string;
			
$> = $<;
$) = $(;
open(INV, '>', "$inv_file_name") || die "Can't create gls inv interface file.\n";
print INV "$inv_string";
$> = $<;
$) = $(;
close(INV);

   $inv_result=`./label/gls_invoice.sh \"${airway_no}.inv\" \"$p_copy\" \"$c_copy\"`;
   $inv_result =~ s/\s+$//;
   if ($inv_result eq 'true') {
	   #print 'window.open("../../gls/'.$airway_no.'.inv.pdf", "Invoice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=600,height=400,left=600,top=300").focus();';
	   print 'invwin=window.open("./label/download_pdf.cgi?download_filename='.$airway_no.'.inv.pdf", "Invoice", "toolbar=0,scrollbars=0,location=0,statusbar=0,menubar=0,resizable=0,width=1,height=1,left=600,top=300").focus();';
	   print 'invwin.close();';
	   
	   #print '<br><a href="./label/download_pdf.cgi?download_filename='.$airway_no.'.inv.pdf">Invoice</a>\n';
	   #$d=0;
   }
   	 
  }
 } 
}  
  
print '</script>';
print '</html>'; 

#if (isProd()) {
#print 'window.location="https://apps.dhl.com.hk/gls/'.$airway_no.'.pdf";';
#} else {
    #print 'window.location="https://mykullstc000536.apis.dhl.com/gls/'.$airway_no.'.pdf";';
    #print 'window.open("./label/download_pdf.cgi?download_filename='.$airway_no.'.pdf", "Waybill", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=600,height=400,left=600,top=300").focus();';
     
    #}
  #print 'window.open("../../info/notice.html", "notice", "toolbar=0,scrollbars=1,location=0,statusbar=0,menubar=0,resizable=1,width=300,height=200,left=600,top=300").focus();</script>';
  

$str_send_company = $Form{send_company};
$str_send_name = $Form{send_name};
$str_send_address1 = $Form{send_address1};
$str_send_address2 = $Form{send_address2};
$str_send_address3 = $Form{send_address3};

#$str_consign_company = $Form{consign_company};
#$str_consign_person = $Form{consign_person};
#$str_consign_address1 = $Form{consign_address1};
#$str_consign_address2 = $Form{consign_address2};
#$str_consign_address3 = $Form{consign_address3};
#$str_consign_city = $Form{consign_city};
$str_contents_desc = $contents_desc;

 #replace value
 if (($Form{send_company} ne '') && ($Form{send_company} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_send_company = ".";
 }
 if (($Form{send_name} ne '') && ($Form{send_name} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_send_name = ".";
 }
 if (($Form{send_address1} ne '') && ($Form{send_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_send_address1 = ".";
 }
 if (($Form{send_address2} ne '') && ($Form{send_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_send_address2 = ".";
 }
 if (($Form{send_address3} ne '') && ($Form{send_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_send_address3 = ".";
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
 #if (($Form{consign_address3} ne '') && ($Form{consign_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_address3 = "."; 
 #}  
 #if (($Form{consign_city} ne '') && ($Form{consign_city} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()-=_+{};:'",.<>?]/)) {
 #  $str_consign_city = ".";
 #}
 
 if (($contents_desc ne '') && ($contents_desc =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
   $str_contents_desc = ".";
 }

if (!defined $Form{consign_city}) {
    $Form{consign_city} = $Form{consign_address3};    
}

if (($Form{consign_city} ne '') && ($Form{consign_city} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) {
    $Form{consign_city} = ".";
}
 

    if ($Form{origin} eq 'MCA') {
      $awb_file_name = $home.'/web_files/awb_mca/work/'.$airway_no.'.awb';
    } else {
      $awb_file_name = $home.'/web_files/awb/work/'.$airway_no.'.awb';
      
      $pf_rand = int(rand(3)) + 1;
    	if (($pf_rand > 0) || ($pf_rand < 4)) {
    	   $awb_file_name = $home.'/web_files/awb/work'.$pf_rand.'/'.$airway_no.'.awb';    	
    	} 
    }
    $awb_string = $airway_no."|".$dhl_acc_no."|".$str_send_company."|".$Form{reference}."|".$str_send_name."|".
		$str_send_address1."|".$str_send_address2."|".$str_send_address3."|".$Form{send_media}."|".$Form{send_tel}."|".
		$Form{consign_company}."|".$Form{consign_person}."|".$Form{consign_address1}."|".$Form{consign_address2}."|".$Form{consign_city}."|".
		$cnty_data."|".$Form{consign_media}."|".$Form{consign_tel}."|".$param_pc."|".$ProdCode."|".
		$DutiFlag."|".$Form{ship_qty}."|".$Form{ship_weight}."|".$insurance."|".$Form{declare_currency}."|".
		$Form{declare_value}."|".$str_contents_desc."|".$Form{dest_other}."|".$d1."|".$t1."|".
		$Form{charge_to_account}."|".$station_code."|".$country_code."|"."JD01".$piece_id_next."|".$srv_cat."|".
		$Form{NDS}."|".$Form{consign_address3}."|".$Form{origin}."|"."|".$Form{ext}."|".
		$ENV{'HTTP_REFERER'}."|".$Form{consign_email}."|".$facility_code."|".$str_item_list."|".$Form{auth_cd}."|".
                "grp_id:".$Form{sub_grp_id}."|1";
		
		$> = $<;
		$) = $(;
		open(AWB, '>', "$awb_file_name") || die "Can't create awb_file.\n";
    print AWB "$awb_string";
    $> = $<;
    $) = $(;
    close(AWB);
    
#create interface file for CN team for pre-sorting shipment with Chinese receiver address 
if ($country_code eq 'CN') { 
 if ((($Form{consign_address1} ne '') && ($Form{consign_address1} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) || 
	 (($Form{consign_address2} ne '') && ($Form{consign_address2} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/)) || 
	 (($Form{consign_address3} ne '') && ($Form{consign_address3} =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/))) {
	 
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
   #local ($lc_total) = @_;
   local $lc_total = $_[0];
   local $decimal_place = $_[1];
   
   $chk_num = 1;
   for ($r=1; $r<=$decimal_place; $r++) {
      $chk_num=$chk_num * 10;
   }
   $chk_num=$chk_num - 1;
	
	@amt = split(/\./,$lc_total);
	if ($amt[1] != ''){
		#$head = substr($amt[1], 0, 1);
		#$second = substr($amt[1], 1, 1);
		$head = substr($amt[1], 0, $decimal_place);
		$second = substr($amt[1], $decimal_place, 1);
		if ($second >= 5){
			#if ($head == 9){
			if ($head == $chk_num){
				$amt[0] = $amt[0] + 1;
				$head = 0;
			}
			else{
				$head = $head + 1;
			}
		   $fmt="%0".$decimal_place."d";
		   $head = sprintf $fmt,$head;
		}
		$lc_total = "$amt[0]\.$head";
		
		
	}
	
	return $lc_total;
}

sub validate_ac{
   
   $in_ac = $_[0];
   $check_result = 0;
   
   &get_connect("wcmf");

   #$sql_ac_str="select count(*) from invoicing_info where accnt_no = '" . $in_ac . "' and cr_status_cd = 'O'";
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

sub get_cust_cp{
   
   $sub_grp_id = $_[0];
   $cust_cp = 0;
   
   &get_connect("webdb");

   $sql_custcp_str="select pr_cust_cp ". 
	"from sf_print_setup ". 
	"where grp_id = '" . $sub_grp_id . "'";

   $sql_custcp=$web_db->prepare($sql_custcp_str) or die "Couldn't select from sf_print_setup";
   $sql_custcp->execute();
	
   @custcp_data = $sql_custcp->fetchrow_array;
   $cust_cp = $custcp_data[0];
   
   return $cust_cp;

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
        
        if ($in_str =~ m/[^a-zA-Z0-9 \-]/) {
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

sub check_commodity{
  
  $in_itemlst = $_[0];
  $out_chk_com = "";
  
  @in_item_arr = split(/\^\~/,$in_itemlst);
  
   if ((trim($in_item_arr[0]) eq "") || (trim($in_item_arr[1]) eq "") || (trim($in_item_arr[2]) eq "") || (trim($in_item_arr[3]) eq "") || (trim($in_item_arr[4]) eq "") || (trim($in_item_arr[5]) eq "")) {  
    	$out_chk_com = "Part of mandatory commodity information is missing. Please input.";
   } elsif (($in_item_arr[0] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) || 
   	($in_item_arr[1] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) ||
   	($in_item_arr[2] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) ||
   	($in_item_arr[3] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) ||
   	($in_item_arr[4] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) ||
   	($in_item_arr[5] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/) ||
   	((trim($in_item_arr[6]) ne '') && ($in_item_arr[6] =~ m/[^a-zA-Z0-9\\\/ `~!@#\$\%^&*()\-=_+{};:'",.<>?]/))) {
   	
   	$out_chk_com = "No Chinese character is allowed. Please input again.";
   
   } elsif ($in_item_arr[1] =~ /\D/) {
   	$out_chk_com = "Please input valid commodity quantity.";
   #} elsif (($in_item_arr[1] <= 0) || ($in_item_arr[1] > 999)) {
   #	$out_chk_com = "Please input at least 1 and less than 1000 commodity quantity.";
   } elsif ($in_item_arr[1] <= 0) {
   	$out_chk_com = "Please input at least 1 commodity quantity.";
   } elsif (!($in_item_arr[3] =~ /^-?\d+\.?\d*$/)) {
   	$out_chk_com = "Please input valid commodity unit value.";
   } elsif ($in_item_arr[3] <= 0) {
   	$out_chk_com = "Please input valid commodity unit value.";
   } elsif (!($in_item_arr[4] =~ /^-?\d+\.?\d*$/)) {
   	$out_chk_com = "Please input valid commodity unit weight.";
   } elsif ($in_item_arr[4] <= 0) {
   	$out_chk_com = "Please input valid commodity unit weight.";
   } elsif ($country_list{$in_item_arr[5]} eq "") {
   	$out_chk_com = "Please input valid commodity or territory country of origin.";
   }
   
   return $out_chk_com;  

}

sub auth_chk{
   
   $auth_cd = $_[0];
   $cust_cnt = 0;
   
   &get_connect("webdb");

   $sql_cust_str="select count(*) ". 
	"from sf_customer ". 
	"where grp_id = '" . $auth_cd . "'";

   $sql_cust=$web_db->prepare($sql_cust_str) or die "Couldn't select from sf_print_setup";
   $sql_cust->execute();
	
   @cust_data = $sql_cust->fetchrow_array;
   $cust_cnt = $cust_data[0];
   
   return $cust_cnt;

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
