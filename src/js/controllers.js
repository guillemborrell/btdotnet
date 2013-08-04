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
	$scope.authenticated = 0;
	$scope.info = "";
	
	$scope.count = function(){
		return $scope.description.length + $scope.hashtag.length +2;
	}
	
	$scope.fields = [];
	
	$scope.addField = function() {
		$scope.fields.push({Descr: $scope.formDescription,
							Val: Process($scope.formValue),
							Marked: false}
							);
		document.forms['fieldform'].description.value="";
		document.forms['fieldform'].value.value="";
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
			creator: document.forms['data'].username.value,
			key: document.forms['data'].key.value,
			description: $scope.description,
			duration: $scope.duration,
			hashtag: $scope.hashtag,
			fields: cleanFields,
			info: $scope.info,
			authenticated: $scope.authenticated
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
	username = document.forms['auth'].username.value;
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
	$scope.get_data2 = $http.get(
		"http://betweetdotnet.appspot.com/restform/last"
		).success(function(data,status,headers,config) {
			$scope.last = data;
		})
	}

function anonIndexCtrl($scope, $http){
	$scope.get_data2 = $http.get(
			"http://betweetdotnet.appspot.com/restform/last"
			).success(function(data,status,headers,config) {
				$scope.last = data;
			})	
}

function fieldCtrl($scope, $http){
	$scope.get_data = $http.get(
			"http://betweetdotnet.appspot.com/restform/allbets?key="+document.forms['bet'].form_key.value
		).success(function(data,status,headers,config) {
			$scope.bets = data;
		}).error(function(data,status,headers,config) {
			$scope.bets = [];
		})
	
	$scope.submitBet = function() {
		fields = [];
		numforms = parseInt(document.forms['bet'].numfields.value);
		form_key = document.forms['bet'].form_key.value;
		username = document.forms['bet'].username.value;
		auth = parseInt(document.forms['bet'].auth.value);
		
		for (i=4; i< 4+numforms; i++){
			fields.push([document.forms['bet'][i].name, document.forms['bet'][i].value]);
		}
		data = {form_key: form_key,
				user: username,
				fields: fields,
				auth: auth};
		
		$http.post(
			"http://betweetdotnet.appspot.com/restbet",data
			).success(function(data,status,headers,config) {
				window.location = "http://betweetdotnet.appspot.com";
			}).error(function(data,status,headers,config) {
				window.location = document.URL;
			})
	
	}
}

