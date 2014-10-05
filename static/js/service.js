var service = {};
service.getUser = function(onSuccess){
  FB.api('/me', {fields: 'first_name, last_name'}, function(response){
    debugger;
    var url = '/data/member/' + response.id; 
    $.ajax({
      url: url,
      success: onSuccess,
      error: function(){
        var response = {id :'123', name : 'Clement', number: '12345'};
        onSuccess(response);
      }
    });
  });
  
};

service.getWhat = function(userId, onSuccess){
  
  // result = {
  //       "freq": {
  //           "ass": 1, 
  //           "fuck": 2, 
  //           "shit": 2
  //       }
  //     };
  // onSuccess(result);
  
  var url = '/data/words/' + userId;
  $.ajax({
    url: url,
    success: onSuccess,
    error: function(){
      result = {
        "freq": {
            "ass": 1, 
            "fuck": 2, 
            "shit": 2
        }
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

service.getWhy = function(userId, word, onSuccess){

  
  // result = {
  //       from: {'ass': 23, 'fat': 21, 'you': 14},
  //       to  : { 'ass': 12, 'poop':12}
  //     };
  // onSuccess(result);
  
  var url = '/data/why/' + userId + '/' + word;
  $.ajax({
    method: 'GET',
    url: url,
    success: onSuccess,
    error: function(){
      result = {
        from: {'ass': 23, 'fat': 21, 'you': 14},
        to  : { 'ass': 12}
      };
      onSuccess(result);
    }
  });
};


service.getTimeseries = function(userId, onSuccess){
  var url = '/data/timeseries/' + userId + '/' + (new Date().getTime()-(30*60*60*24))+ '/' + new Date().getTime();
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
