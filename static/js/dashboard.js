var loadDashboard= function($scope){
  $scope.loggedIn = true;
  service.getUser(function(response){
    $scope.userId = response.id;
    $scope.userName = response.first_name + ' ' + response.last_name;
    loadWhat($scope);
  });
};

var loadWhat = function($scope){
  service.getWhat($scope.userId, function(response){
    $scope.what = response;
  });
};



