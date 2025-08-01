#!/usr/bin/perl
use lib '/appl/service/webapps/cgi-bin/';

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


print <<END1;

<html>
<head><title>AWB Printing</title>
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

<script language="JavaScript">

<!--

if (browserOK) {
printa1 = new Image
printa2 = new Image
reset_1 = new Image
reset_2 = new Image
printc1 = new Image
printc2 = new Image
service1 = new Image
service2 = new Image

printa1.src = '../images/prepare1.gif'
printa2.src = '../images/prepare2.gif'
reset_1.src = '../images/reset_1.gif'
reset_2.src = '../images/reset_2.gif'
printc1.src = '../images/printc1.gif'
printc2.src = '../images/printc2.gif'
service1.src = '../images/awb/service1.gif'
service2.src = '../images/awb/service2.gif'
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


objPIC3 = new objMouseChangeImg('PIC3', printa2.src, printa1.src);

function checking(form){
	document.dhl.submit()
}

// -->

</script>
</head>
<body bgcolor=white><center>
<form name=dhl method=post action=./inv.cgi target=new>
<input type=hidden name=from_where value="$Form{from_where}">
<input type=hidden name=dhl_acc_no value="$Form{dhl_acc_no}">
<input type=hidden name=send_name value="$Form{send_name}">
<input type=hidden name=reference value="$Form{reference}">
<input type=hidden name=send_company value="$Form{send_company}">
<input type=hidden name=send_address1 value="$Form{send_address1}">
<input type=hidden name=send_address2 value="$Form{send_address2}">
<input type=hidden name=send_address3 value="$Form{send_address3}">
<input type=hidden name=send_media value="$Form{send_media}">
<input type=hidden name=send_tel value="$Form{send_tel}">
<input type=hidden name=consign_company value="$Form{consign_company}">
<input type=hidden name=consign_address1 value="$Form{consign_address1}">
<input type=hidden name=consign_address2 value="$Form{consign_address2}">
<input type=hidden name=consign_address3 value="$Form{consign_address3}">
<input type=hidden name=consign_pc value="$Form{consign_pc}">
<input type=hidden name=consign_country value="$Form{consign_country}">
<input type=hidden name=consign_person value="$Form{consign_person}">
<input type=hidden name=consign_media value="$Form{consign_media}">
<input type=hidden name=consign_tel value="$Form{consign_tel}">
<input type=hidden name=awb_no value="$Form{awb_no}">
<input type=hidden name=ship_qty value="$Form{ship_qty}">
<input type=hidden name=ship_weight value="$Form{ship_weight}">
</form>
END1

if ($Form{print_inv} eq 'yes')
{
print <<END1;
<table border="0" width="100%">
  <tr>
    <td width="70%">
    <b><font FACE="Frutiger, Arial" COLOR="#000000">Please note that </b></font>
    <font FACE="Frutiger, Arial" COLOR="#951314" SIZE="+2">&nbsp; 2 Copies &nbsp;</font>
    <b><font FACE="Frutiger, Arial" COLOR="#000000">of Airwaybill and </b></font>
    <font FACE="Frutiger, Arial" COLOR="#951314" SIZE="+2">&nbsp; 2 Copies &nbsp;</font>
    <b><font FACE="Frutiger, Arial" COLOR="#000000">of invoice are required for courier pick-up and customs declaration when you prepare the document.</b></td>
    <td width="30%"><img src="../images/awb4.jpg" width="135" height="177"
    alt="awb3_new2.gif (23373 bytes)"></td>
  </tr>
</table>
<br>
<a href="javascript:checking(document.dhl)" onMouseOver="objPIC3.MouseOver()" onMouseOut ="objPIC3.MouseOut()"><img src="../images/prepare1.gif" border=0 name=PIC3></a>
END1
}
else
{
print <<END1;
<table border="0" width="100%">
  <tr>
    <td width="70%">
    <b><font FACE="Frutiger, Arial" COLOR="#000000">For printing of Airwaybill, please note that</b></font>
    <font FACE="Frutiger, Arial" COLOR="#951314" SIZE="+2">&nbsp; 2 Copies &nbsp;</font>
    <b><font FACE="Frutiger, Arial" COLOR="#000000">are required for courier pick-up and customs declaration.</font></b></td>
    <td width="30%"><img src="../images/awb3.jpg" width="135" height="177"
    alt="awb3_new2.gif (23373 bytes)"></td>    
  </tr>
  <tr>
    <td colspan=2>
    <b><font FACE="Frutiger, Arial" COLOR="#000000">Please use your browser's printing function (e.g. File > Print) to print out the airwaybills.</b></font>
    </td>
  </tr>
</table>
END1
}

print <<END1;

</center>
</body>
</html>

END1
