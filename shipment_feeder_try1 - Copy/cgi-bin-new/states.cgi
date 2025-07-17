#!/usr/bin/perl

use lib '/appl/service/webapps/cgi-bin/';
use db_con;
use CGI;
use CGI::Cookie;

my $cgi = CGI->new;
my %cookies = CGI::Cookie->fetch;
my $session_token = '';

# 1. 從 cookie 取
$session_token = $cookies{'SESSIONID'}->value if $cookies{'SESSIONID'};

# 2. 從 URL/POST 取
$session_token ||= $cgi->param('SESSIONID');

# 3. 驗證 session
unless (is_valid_session($session_token)) {
    print $cgi->redirect('/shipment_feeder/toLogin.html');
    exit;
}

sub is_valid_session {
    my ($token) = @_;
    return 0 unless $token;
    my $session_file = "/tmp/sessions/$token";
    return 0 unless -e $session_file;
    my $max_age = 1800; # 30 minutes
    my $mtime = (stat($session_file))[9];
    return 0 if (time - $mtime > $max_age);
    open my $fh, '<', $session_file or return 0;
    my $content = do { local $/; <$fh> };
    close $fh;
    return 0 unless $content =~ /emailadr=/;
    return 1;
}

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";

# ...existing code...

if (!defined $ENV{'HTTP_REFERER'}) {
	my $q = CGI->new;	
	print $q->redirect('csender.cgi');
  exit();
  #$d=1;
}

if (($ENV{'HTTP_REFERER'} eq '') || 
  	(($ENV{'HTTP_REFERER'} ne 'https://apps.dhl.com.hk/cgi-bin/csender.cgi') &&
	 ($ENV{'HTTP_REFERER'} ne 'https://mykullstc000536.apis.dhl.com/cgi-bin/hkapp/csender.cgi'))) {  
	
 my $q = CGI->new;	
 print $q->redirect('csender.cgi');
 exit();
 #$d=1;
}

my $cgi = new CGI;
my $type = $cgi->param("type");
my $country = $cgi->param("country");
my $q = $cgi->param("q");

#input validation

if (($type eq '') || ($country eq '')) {
	my $q = CGI->new;
	print $q->redirect('csender.cgi');
	#print "\n1";
}

if (($type ne 'C') && ($type ne 'P')) {
	my $q = CGI->new;
	print $q->redirect('csender.cgi');
}

if ((length($country) != 2) || ($country =~ m/[^A-Z]/)) {
	my $q = CGI->new;
	print $q->redirect('csender.cgi');
}

##########

print "Content-type: text/html\n";
print "Content-Security-Policy: default-src 'self'; object-src 'none'; frame-ancestors 'none'; upgrade-insecure-requests; block-all-mixed-content\n\n";


print <<END1;

END1
&get_connect("wcrd");

$count=0;

if ($country eq 'KR') {
	if ($type eq 'C'){
	   $sql_def_str="select FIRST 4000 distinct   city_name,postal_code from v_post_code  where city_name LIKE upper('".  $q."%') and country_code  ='".$country."' and length(postal_code) = 5 ";
	}else{
	   $sql_def_str="select  FIRST 4000 distinct  postal_code,city_name from v_post_code  where postal_code LIKE upper('".  $q."%') and country_code  ='".$country."' and length(postal_code) = 5 ";
	}
	
} else {
   if (($country eq 'IL') || ($country eq 'PT')) {
	if ($type eq 'C'){
	   $sql_def_str="select FIRST 4000 distinct   city_name,postal_code from v_post_code  where city_name LIKE upper('".  $q."%') and country_code  ='".$country."' and length(postal_code) = 7 ";
	}else{
	   $sql_def_str="select  FIRST 4000 distinct  postal_code,city_name from v_post_code  where postal_code LIKE upper('".  $q."%') and country_code  ='".$country."' and length(postal_code) = 7 ";
	}	
   } else {
	if ($type eq 'C'){
	   $sql_def_str="select FIRST 4000 distinct   city_name,postal_code from v_post_code  where city_name LIKE upper('".  $q."%') and country_code  ='".$country."' ";
	}else{
	   $sql_def_str="select  FIRST 4000 distinct  postal_code,city_name from v_post_code  where postal_code LIKE upper('".  $q."%') and country_code  ='".$country."' ";
	}
   }
}

$sql_def=$web_db->prepare($sql_def_str) or die "Couldn't select from v_post_code";
$sql_def->execute();

while (@def_data=$sql_def->fetchrow_array()) {
print  trim($def_data[0])."|".trim($def_data[1])."\n";
$count=1;
}

if ($count==0){
if ($type eq 'C'){
$sql_def_str="select FIRST 4000 distinct city_name  from v_post_range where city_name LIKE upper('".  $q."%') and country_code  ='".$country."' ";
	
	$sql_def=$web_db->prepare($sql_def_str) or die "Couldn't select from v_post_range";
	$sql_def->execute();

	while (@def_data=$sql_def->fetchrow_array()) {
	print  trim($def_data[0])."|"."\n";
}
}
}
$web_db->disconnect;


sub trim($)
{
	my $string = shift;
	$string =~ s/^\s+//;
	$string =~ s/\s+$//;
	return $string;
}


