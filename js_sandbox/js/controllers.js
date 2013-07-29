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

function FieldListCtrl($scope){
	$scope.hashtag = "";
	$scope.text = "";
	$scope.duration = "";
	$scope.urlID = "";
	
	$scope.count = function(){
		return $scope.text.length + $scope.hashtag.length +2;
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
}

