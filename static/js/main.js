/**
 *  * Main AngularJS Web Application
 *   */
var app = angular.module('swearJar', [
]);

SCOPE = null;

app.controller('SwearJarController', function($scope){
  angular.element(document).ready(function(){
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

};

