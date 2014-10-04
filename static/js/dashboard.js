var loadDashboard= function($scope){
  $scope.loggedIn = true;
  service.getUser(function(response){
    $scope.userId = response.id;
    $scope.userName = response.first_name + ' ' + response.last_name;

    loadWho($scope);
    loadWhat($scope);
  });
};

var loadWhat = function($scope){
  service.getWhat($scope.userId, function(response){
    $scope.what = response;
    charting.drawBarChart(response.list, '#what-chart');
    
  });
};

var loadWho = function($scope){
  service.getWho($scope.userId, function(response){

    var toArray = transformWhoData(response['to']);
    charting.drawDonutChart(toArray, '#who-chart-to');

    var fromArray = transformWhoData(response['from']);
    charting.drawDonutChart(fromArray, '#who-chart-from');

  });
};

var transformWhoData = function(toArray){
   var whoData = [];
   for (var key in toArray) {
      if (toArray.hasOwnProperty(key)) {
         whoData.push(
             {
               "label": key, 
               "value": toArray[key]
             });
      }
   }  
   debugger;
   return whoData;
};

