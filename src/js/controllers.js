function Process(s){
	if (s.lastIndexOf(',') >= 0){
		return s.split(',');
	}
	if (s.lastIndexOf(':') >= 0){
		x = [];
		f = s.split(':')
		for (i=parseInt(f[0]); i<=parseInt(f[1]); i++ ){
			x.push(i);
		}
		return x;
	}
}

function FieldListCtrl($scope,$http){
	$scope.hashtag = "";
	$scope.description = "";
	$scope.duration = "";
	$scope.urlID = "";
	$scope.username = username;
	$scope.key = key;
	$scope.info = "";
	
	$scope.count = function(){
		return $scope.description.length + $scope.hashtag.length +2;
	}
	
	$scope.fields = [
	    {Descr:'Number of goals',
	     Val:[0,1,2,3,4,5],
	     Marked:false
	    },
	    {Descr:'Máximo goleador',
	     Val:['Arbeloa','Cristiano Ronaldo','Higuaín'],
	     Marked:false
	    },
	    {Descr:'Resultado',
	     Val:['Vencedor','Perdedor'],
	     Marked:false}
	    ];
	
	$scope.addField = function() {
		$scope.fields.push({Descr: $scope.formDescription,
							Val: Process($scope.formValue),
							Marked: false}
		);
	}
	
	$scope.cleanFields = function() {
		var oldFields = $scope.fields;
		$scope.fields = [];
		angular.forEach(oldFields, function(field) {
			if (!field.Marked) {
				$scope.fields.push(field);
				}
			}
		)
	}
	
	$scope.submitFields = function() {
		var cleanFields = [];
		angular.forEach($scope.fields, function(field){
				cleanFields.push({Descr: field.Descr,
									Val: field.Val});
			}
		)
		var data = {
			creator: username,
			description: $scope.description,
			duration: $scope.duration,
			hashtag: $scope.hashtag,
			fields: cleanFields,
			info: $scope.info,
			authenticated: 1
		};

		$http.post(
				"http://betweetdotnet.appspot.com/restform",data
				).success(function(data,status,headers,config) {
					window.location = "http://betweetdotnet.appspot.com";
				}).error(function(data,status,headers,config) {
					window.location = document.URL;
				})
	}
}

function indexCtrl($scope, $http){
	$scope.get_data = $http.get(
		"http://betweetdotnet.appspot.com/restform/fromcreator?creator="+username
		).success(function(data,status,headers,config) {
				$scope.forms = data	;
			}
		)
	$scope.get_data1 = $http.get(
		"http://betweetdotnet.appspot.com/restbet/fromuser?user="+username
		).success(function(data,status,headers,config) {
			$scope.bets = data;
		})
	}

function fieldCtrl($scope, $http){
	$scope.submitBet = function() {
		fields = [];
		numforms = parseInt(document.forms['bet'].numfields.value);
		form_key = document.forms['bet'].form_key.value;
		username = document.forms['bet'].username.value;
		
		for (i=3; i< 3+numforms; i++){
			fields.push([document.forms['bet'][i].name, document.forms['bet'][i].value]);
		}
		data = {form_key: form_key,
				user: username,
				fields: fields};
		
		console.log(data);
		
		$http.post(
			"http://betweetdotnet.appspot.com/restbet",data
			).success(function(data,status,headers,config) {
				window.location = "http://betweetdotnet.appspot.com";
			}).error(function(data,status,headers,config) {
				window.location = document.URL;
			})
	
	}
}

