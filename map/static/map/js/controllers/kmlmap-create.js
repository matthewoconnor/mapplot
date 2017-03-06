(function(){
  angular.module("MapApplication")
  	.controller('DataMapCreateController', function($scope, $log, $http) {
  		
    		$scope.kmlmap = {};
        $scope.metadata = {};

        $scope.current_tab = "basic-info"; // "basic-info", "settings", "import"

        $scope.change_tab = function(tab_name) {
          $scope.current_tab = tab_name;
        }

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