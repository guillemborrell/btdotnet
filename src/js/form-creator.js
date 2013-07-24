var beTweet = new function(){
  this.fields = [1];
};

function createBet($scope){
  $scope.choices = [new Choice()];
  $scope.hashtag = "";
  $scope.addChoice = function(){
    beTweet.fields.push(beTweet.fields[beTweet.fields.length-1] + 1);
    $scope.choices.push(new Choice());
  };
  
  $scope.preview = function(){
    message = "#" + $scope.hashtag;
    return message;
  }
  $scope.count = function(){
    return 140 - message.length;
  }
}


function Choice(){
  this.bet_type = "select";
  this.bet_name = "field" + beTweet.fields[beTweet.fields.length-1];
  
  
}

function betSelect(){
  this.bet_options = new array();
  this.add_option = function(){
    
  }
}

function betInput(){
  this.bet_value = "";
  this.bet_size = 3;
}
