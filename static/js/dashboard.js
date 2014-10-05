var loadDashboard= function($scope){
  $scope.loggedIn = true;
  
  service.getUser(function(response){
    $scope.$apply(function() {
      $scope.message = 'Fetched after 3 seconds'; 
      console.log('message:' + $scope.message);
    });
    $scope.userId = response.id;
    $scope.userName = response.first_name + ' ' + response.last_name;
      loadWho($scope);
      loadWhat($scope);
      loadWhy($scope);

    $scope.$apply();
    
  });
 $scope.popWordCloud = function(x){
   debugger;
   $('body').append(
      '<div class="modal fade">' +
        'hi' +
      '</div>'
   );
 };
  
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
   return whoData;
};


var loadWhy = function($scope){
  service.getWhy($scope.userId, function(response){
    $scope.why = response;
    charting.drawWordCloud(response.list, 'why-chart');
  });
};
