var loadDashboard= function($scope){
  $scope.loggedIn = true;
  service.getUser(function(response){
    $scope.$apply(function() {
      $scope.message = 'Fetched after 3 seconds'; 
      console.log('message:' + $scope.message);
    });
    $scope.userId = response.number;
    $scope.userName = response.name;
      loadWho($scope);
      loadWhat($scope);
      loadWhy($scope);
//      loadTimeseries($scope);

    $scope.$apply();
    
  });
  $scope.popWordCloud = function(x){
    $('#myModal').modal('toggle');
    $('#wordCloud').empty();
    service.getWhy($scope.userId, function(response){
      debugger;
      
      transformedFrom = transformDataArray(response.from);
      
      charting.drawWordCloud(transformed, 'wordCloud');
    });
  };
  
};


var loadWhat = function($scope){
  service.getWhat($scope.userId, function(response){
    $scope.what = transformData(response.freq);
    $scope.$apply();
    charting.drawBarChart($scope.what, '#what-chart');
  });
};

var loadWho = function($scope){
  service.getWho($scope.userId, function(response){

    var toArray = transformData(response['to']);
    charting.drawDonutChart(toArray, '#who-chart-to');

    var fromArray = transformData(response['from']);
    charting.drawDonutChart(fromArray, '#who-chart-from');

  });
};

var transformData = function(toArray){
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

var combineHashToArray = function(hash1, hash2){
};

var transformDataArray = function(toArray){
   var whoData = [];
   for (var key in toArray) {
      if (toArray.hasOwnProperty(key)) {
         whoData.push(
             [key, toArray[key]]);
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


var loadTimeseries = function($scope){
  service.getTimeseries($scope.userId, function(response){
    var dateArray = transformData(response);
//    charting.drawTimeseriesChart(dateArray,'#timeseries-chart');
  });
};
