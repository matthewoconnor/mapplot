(function(){
  angular.module("MapApplication")
  	.controller('DataMapCreateController', function($scope, $log, $http) {
  		
    		$scope.kmlmap = {};
        $scope.metadata = {};

        $scope.get_metadata = function() {
          var url = "/app/kmlmap/"+$scope.kmlmap.id+"/metadata/";
          $http.get(url)
            .then(function(response){
              if(response.data.kmlfiles){
                $scope.kmlfile = response.data.kmlfiles[0]; 
              }
              $scope.metadata = response.data;
            });
        };

    	});
})();