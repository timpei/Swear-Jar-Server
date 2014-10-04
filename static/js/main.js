/**
 *  * Main AngularJS Web Application
 *   */
var app = angular.module('swearJar', [
]);

SCOPE = null;

app.controller('SwearJarController', function($scope){
  $scope.loggedIn = false;
  fbInit($scope);
  SCOPE = $scope;
  $scope.login = function() {
    console.log('login');
    FB.login(function(response){
      statusChangeCallback(response, $scope);
    });
  };
});


var statusChangeCallback = function(response, $scope){
  if(response.status == 'connected'){
    loadDashboard($scope);
  }
};
var fbInit = function($scope){
  window.fbAsyncInit = function() {
    FB.init({
      appId      : '661005694006952',
      xfbml      : true,
      version    : 'v2.1'
    });
    FB.getLoginStatus(function(response) {
      statusChangeCallback(response, $scope);
    });
  };

  (function(d, s, id){
    var js, fjs = d.getElementsByTagName(s)[0];
    debugger;
    if (d.getElementById(id)) {return;}
    js = d.createElement(s); js.id = id;
    js.src = "//connect.facebook.net/en_US/sdk.js";
    fjs.parentNode.insertBefore(js, fjs);
    
  }(document, 'script', 'facebook-jssdk'));
};

