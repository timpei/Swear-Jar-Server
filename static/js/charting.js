var charting = {};

charting.drawBarChart = function(list, targetId){
  chartFormat = [{key:'swear words',
    values: list}];

  var chart = nv.models.discreteBarChart() 
    .x(function(d) { return d.word })    //Specify the data accessors.
    .y(function(d) { return d.count })
    .staggerLabels(true)    //Too many bars and not enough room? Try staggering labels.
    .tooltips(false)        //Don't show tooltips
    .showValues(true)       //...instead, show the bar value right on top of each bar.
    .transitionDuration(350);

  d3.select('#what-chart')
    .datum(chartFormat)
    .call(chart);
};

charting.drawDonutChart = function(list, targetId){
  var chart = nv.models.pieChart()
    .x(function(d) { return d.label })
    .y(function(d) { return d.value })
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
