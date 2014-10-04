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
    var chart = nv.models.discreteBarChart()
    .x(function(d) { return d.word })    //Specify the data accessors.
    .y(function(d) { return d.count })
    .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
    .tooltips(false)        //Don't show tooltips
    .showValues(true)       //...instead, show the bar value right on top of each bar.
    .transitionDuration(350);
  d3.select('#what-chart')
    .datum(response)
    .call(chart);

    
  });
};



