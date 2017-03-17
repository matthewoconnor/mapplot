(function(){
  angular.module("MapApplication")
  	.controller('DataMapCreateController', function($scope, $log, $http, $datamaps) {
  		
    		$scope.datamap = {};
        $scope.metadata = {};

        $scope.current_tab = "basic-info"; // "basic-info", "settings", "import"

        $scope.change_tab = function(tab_name) {
          $scope.current_tab = tab_name;
        }

        $scope.$on("datamaps:updated", function(event, data) {
          if ($scope.datamap.id) {
            $scope.datamaps = $datamaps.getById($scope.datamap.id);
          }
        });

        $scope.get_metadata = function() {
          var url = "/app/kmlmap/"+$scope.kmlmap.id+"/metadata/";
          $http.get(url)
            .then(function(response){
              $scope.metadata = response.data;
            });
        };

    	});
})();