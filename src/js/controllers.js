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
			authenticated: 1
		};
		$http.post("http://betweetdotnet.appspot.com/restform",data);
		window.location = "http://betweetdotnet.appspot.com";
	}
}

function indexCtrl($scope, $http){
	$scope.get_data = $http.get(
		"http://betweetdotnet.appspot.com/restform/fromcreator?creator="+username
		).success(function(data,status,headers,config) {
				$scope.forms = data	;
			}
		)
	}
