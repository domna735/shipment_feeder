var msie3=false;

browserVer=parseInt( navigator.appVersion );
if( browserVer == 2 && navigator.appName == "Microsoft Internet Explorer" ) {
  browserVer++;
  msie3=true;
}

function MM_findObj(n, d) { //v4.0
  var p,i,x;  if(!d) d=document; if((p=n.indexOf("?"))>0&&parent.frames.length) {
      d=parent.frames[n.substring(p+1)].document; n=n.substring(0,p);}
        if(!(x=d[n])&&d.all) x=d.all[n]; for (i=0;!x&&i<d.forms.length;i++) x=d.forms[i][n];
          for(i=0;!x&&d.layers&&i<d.layers.length;i++) x=MM_findObj(n,d.layers[i].document);
            if(!x && document.getElementById) x=document.getElementById(n); return x;
}

function MM_validateForm() { //v4.0
var i,p,q,nm,test,num,min,max,errors='',args=MM_validateForm.arguments;

for (i=0; i<(args.length-2); i+=3) 
{
 test=args[i+2]; val=MM_findObj(args[i]);

 if (val) { 
     nm=val.name;
     if (nm == "emailadr") showname="Authentication code";
     if ((val=val.value)!="") {
	 if (test.indexOf('isEmail')!=-1)
	 { 
	  //p=val.indexOf('@');
	  //if (p<1 || p==(val.length-1)) errors+='- '+showname+' is invalid.\n';
	  if (!isEmail(val)) errors+='- '+showname+' is invalid.\n';	   
	 } else if (test!='R') {
	   if (isNaN(val)) errors+='- '+showname+' must contain a number.\n';
	   if (test.indexOf('inRange') != -1) 
	    { p=test.indexOf(':');
	      min=test.substring(8,p); max=test.substring(p+1);
	      if (val<min || max<val) 
	        errors+='- '+showname+' must contain a number between '+min+' and '+max+'.\n';
	    } 
	 } // else if
	 
	 if (nm == "passwd") {
	 	if (!isPassword(val)) errors+='- '+showname+' is invalid.\n';
	 }
	 
	 if (nm == "emailadr") {
	    	if (!isLoginID(val)) errors+='- '+showname+' is invalid.\n';
	 }
	 
      }
         else if ((test.charAt(0) == 'R') || (test.indexOf('isEmail')!=-1)) errors += '- '+showname+' is required.\n'; 
         
      }
} //for 

if (errors) alert('The following error(s) occurred:\n'+errors);

document.MM_returnValue = (errors == '');
}

window.onload=function(){
    document.getElementById("formLogin").addEventListener("submit", function() {
        event.preventDefault();
        MM_validateForm('emailadr','','R');
        if (document.MM_returnValue) {
            document.getElementById("formLogin").submit();
        }
    });
}
