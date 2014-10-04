var service = {};
service.getUser = function(onSuccess){
  FB.api('/me', {fields: 'first_name, last_name'}, onSuccess);
};

service.getWhat = function(userId, onSuccess){
  //function(){
  result = {
        list : [{'word': 'Duck', 'count': 123},
		{'word': 'Crap', 'count': 45},
                {'word': 'Poop', 'count':145}]
      };
      onSuccess(result);
   // }

  /**
  var url = '/data/words/' + userId + '/' + new Date().getTime();
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
  **/
};


service.getWho = function(userId, onSuccess){

  var url = '/data/who/' + userId + '/' + new Date().getTime();
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

  var url = 'data/why/' + userId + '/' + new Date().getTime() + '/duck';
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
