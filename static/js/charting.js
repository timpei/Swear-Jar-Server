var charting = {};

charting.drawBarChart = function(list, targetId){
  chartFormat = [{key:'swear words',
    values: list}];

  var chart = nv.models.discreteBarChart() 
    .x(function(d) { return d.label })    //Specify the data accessors.
    .y(function(d) { return d.value })
    .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
    .tooltips(false)        //Don't show tooltips
    .showValues(true)       //...instead, show the bar value right on top of each bar.
    .transitionDuration(350);
  debugger;

  d3.select(targetId)
    .datum(chartFormat)
    .call(chart);
};

charting.drawDonutChart = function(list, targetId){
  var chart = nv.models.pieChart()
    .y(function(d) { return d.value })
    .x(function(d) { 
      var str = String(d.label);
      
      return str; })
    .showLabels(true)     //Display pie labels
    .labelThreshold(.05)  //Configure the minimum slice size for labels to show up
    .labelType("percent") //Configure what type of data to show in the label. Can be "key", "value" or "percent"
    .donut(true)          //Turn on Donut mode. Makes pie chart look tasty!
    .donutRatio(0.35)     //Configure how big you want the donut hole size to be.
    ;

  d3.select(targetId)
    .datum(list)
    .transition().duration(350)
    .call(chart); 
};


charting.drawWordCloud = function(list, targetId) {
  //WordCloud(document.getElementById(targetId), {'list': list });
  console.log("Drawing Cloud: ", list)
  var options = {
    list: list,
    //gridSize: Math.round(16 * $('#why-chart').width() / 1024),
    fontFamily: 'Times, serif',
    color: function (word, weight) {
      return (weight === 12) ? '#f02222' : '#c09292';
    },
    minSize: 5,
    shuffle: 1,
        //rotateRatio: 0.5,
    backgroundColor: '#E3E3E3'
  }

  WordCloud(document.getElementById(targetId), options);
};


charting.drawTimeseriesChart = function(list, targetId){
    var data = [{key: "Swearing to Others", values: list.slice(0,20), area: true}];
    var chart = nv.models.lineChart()
      .useInteractiveGuideline(true)
      .interpolate("basis")
      .x(function(d){ 
        return d.time; 
      })
      .y(function(d){ 
        return d.score;
      });
    chart.xAxis
      .axisLabel('Date')
      .tickFormat(function(d) {
        return d3.time.format('%x')(new Date(d))
                                  });
    chart.yAxis
      .axisLabel('Swear Volume');
    /*.xAxis.axisLabel('Date')
    .xAxis.tickFormat(function(d) {
        return d3.time.format('%x')(new Date(d))
    })
    .yAxis.axisLabel('Times Sworn')
    ;*/

    d3.select(targetId)
        .datum(data)
        .call(chart);

};
