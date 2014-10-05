var service = {};
service.getUser = function(onSuccess){
  FB.api('/me', {fields: 'first_name, last_name'}, function(response){
    var url = '/data/member/' + response.id; 
    $.ajax({
      url: url,
      success: onSuccess,
      error: function(){}
    });
  });
  
};

service.getWhat = function(userId, onSuccess){
  /**
  //function(){
  result = {
        list : [{'word': 'Duck', 'count': 123},
		{'word': 'Crap', 'count': 45},
                {'word': 'Poop', 'count':145}]
      };
      onSuccess(result);
   // }
   // */

  var url = '/data/words/' + userId;
  $.ajax({
    url: url,
    success: onSuccess,
    error: function(){
      result = {
        list : [{'word': 'Duck', 'count': 123},
                {'word': 'Poop', 'count':145}]
      };
      onSuccess(result);
    }
  });
};


service.getWho = function(userId, onSuccess){

  var url = '/data/who/' + userId;
  $.ajax({
    method: 'GET',
    url: url,
    success: onSuccess,
    error: function(){
	result = {
	  'to' : { 
	    '1234512333' : 100,
	    '6507381234' : 50 
	   },
	  'from' : {
	    '1234512333' : 8,
	    '6507381234' : 2 
	   }
	};
        onSuccess(result);
    }
  });
};

service.getWhy = function(userId, onSuccess){

  var url = 'data/why/' + userId + '/ass';
  $.ajax({
    method: 'GET',
    url: url,
    success: onSuccess,
    error: function(){
      result = {
        list: [['duck', 21],['crap', 13],['poop', 16], ['frack', 5], ['jack', 17]]
        };
      onSuccess(result);
    }
  });
};


service.getTimeseries = function(userId, onSuccess){
  var url = 'data/timeseries/' + userId + '/' + (new Date().getTime()-(30*60*60*24))+ '/' + new Date().getTime();
  $.ajax({
    method: 'GET',
    url: url,
    success: onSuccess,
    error: function(){
      result = {
        '1412481668461': 23,
        '1412481663000': 22,
        '1412481500000': 21,
        '1412481400000': 22,
        '1412481300000': 23
        };
      onSuccess(result);
    }
  });
};
