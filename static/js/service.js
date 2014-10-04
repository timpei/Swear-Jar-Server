var service = {};
service.getUser = function(onSuccess){
  FB.api('/me', {fields: 'first_name, last_name'}, onSuccess);
};

service.getWhat = function(userId, onSuccess){
  //function(){
  result = {
        list : [{'word': 'Duck', 'count': 123},
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
    success: onSuccess
     
  });
};

