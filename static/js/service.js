var service = {};
service.getUser = function(onSuccess){
  FB.api('/me', {fields: 'first_name, last_name'}, function(response){
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
    result = {
      from: {score: 3, time: 1412470224},
      to:   {score: 2, time: 1412470224}
    }; 
      onSuccess(result);
  // var url = '/data/timeseries/1111112221/0/1412496425512';
  // $.ajax({
  //   method: 'GET',
  //   url: url,
  //   success: onSuccess,
  //   error: function(){
  //     result = {
  //       from: {score: 3, time: 1412470224},
  //       to:   {score: 2, time: 1412470224}
  //     }; 
  //     onSuccess(result);
  //   }
  // });
};
