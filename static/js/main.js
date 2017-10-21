window.fbAsyncInit = function() {
  window.FB.init({
    appId            : 124172418273424,
    autoLogAppEvents : true,
    xfbml            : true,
    version          : 'v2.10'
  });
  window.FB.AppEvents.logPageView();
};

var finished_rendering = function() {
console.log("finished rendering plugins");
var spinner = document.getElementById("spinner");
spinner.removeAttribute("style");
spinner.removeChild(spinner.childNodes[0]);
}
window.FB.Event.subscribe('xfbml.render', finished_rendering);

(function(d, s, id){
   var js, fjs = d.getElementsByTagName(s)[0];
   if (d.getElementById(id)) {return;}
   js = d.createElement(s); js.id = id;
   js.src = "https://connect.facebook.net/en_US/sdk.js";
   fjs.parentNode.insertBefore(js, fjs);
 }(document, 'script', 'facebook-jssdk'));

// // initialize Account Kit with CSRF protection
// AccountKit_OnInteractive = function(){
//    AccountKit.init(
//      {
//        appId:124172418273424,
//        state:0929,
//        version:"{{ACCOUNT_KIT_API_VERSION}}",
//        fbAppEventsEnabled:true,
//        redirect:"https://www.google.com"
//      }
//    );
// };
//
// // login callback
// function loginCallback(response) {
//    if (response.status === "PARTIALLY_AUTHENTICATED") {
//      var code = response.code;
//      var csrf = response.state;
//      // Send code to server to exchange for access token
//    }
//    else if (response.status === "NOT_AUTHENTICATED") {
//      // handle authentication failure
//    }
//    else if (response.status === "BAD_PARAMS") {
//      // handle bad parameters
//    }
// }
//
// // email form submission handler
// function emailLogin() {
//    var emailAddress = document.getElementById("email").value;
//       AccountKit.login(
//         'EMAIL',
//         loginCallback
//       );
// }
