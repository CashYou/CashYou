window.fbAsyncInit = function() {
  FB.init({
    appId            : 124172418273424,
    autoLogAppEvents : true,
    xfbml            : true,
    version          : 'v2.10'
  });
  FB.AppEvents.logPageView();
};

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "https://connect.facebook.net/en_US/sdk.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

 (function(d, s, id) {
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) return;
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

(function(d, s, id) {
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) return;
   js = d.createElement(s); js.id = id;
   js.src = "//connect.facebook.net/en_US/sdk.js#xfbml=1";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

// initialize Account Kit with CSRF protection
AccountKit_OnInteractive = function(){
   AccountKit.init(
     {
       appId:124172418273424,
       state:"{{csrf}}",
       version:"{{ACCOUNT_KIT_API_VERSION}}",
       fbAppEventsEnabled:true,
       redirect:"{{REDIRECT_URL}}"
     }
   );
};

// login callback
function loginCallback(response) {
   if (response.status === "PARTIALLY_AUTHENTICATED") {
     var code = response.code;
     var csrf = response.state;
     // Send code to server to exchange for access token
   }
   else if (response.status === "NOT_AUTHENTICATED") {
     // handle authentication failure
   }
   else if (response.status === "BAD_PARAMS") {
     // handle bad parameters
   }
}

// phone form submission handler
function smsLogin() {
   var countryCode = document.getElementById("country_code").value;
   var phoneNumber = document.getElementById("phone_number").value;
   AccountKit.login(
     'PHONE',
     {countryCode: countryCode, phoneNumber: phoneNumber}, // will use default values if not specified
     loginCallback
   );
}

// email form submission handler
function emailLogin() {
   var emailAddress = document.getElementById("email").value;
      AccountKit.login(
        'EMAIL',
        {emailAddress: emailAddress},
        loginCallback
      );
}
