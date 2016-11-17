(function(){
  angular.module("MapApplication")
  	.controller('KmlMapCreateController', function($scope, $log, $http) {
  		
    		$scope.kmlmap = {};

        $scope.areaMapAutocomplete = {
          searchText : "",
          getMatches : function(query) {
            return $http.get("/app/areamap/autocomplete/", {"query":query}).then(function(response){
              return response.data.results
            });
          },
          selectedItemChanged : function(item) {
            $scope.kmlmap.area_map = item.id;
          }
        }

    	});
})();