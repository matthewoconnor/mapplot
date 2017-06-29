(function(){
  angular.module("MapApplication")
  	.controller('DataMapCreateController', function($scope, $log, $http, $datamaps) {
  		
    		$scope.datamap = {};
        $scope.metadata = {};

        $scope.current_tab = "basic-info"; // "basic-info", "settings", "import"
        $scope.editing_state = "new"; // new, edit, import

        $scope.change_tab = function(tab_name) {
          $scope.current_tab = tab_name;
        }

        $scope.change_editing_state = function(state) {
          $scope.editing_state = state;
        }

        $scope.$on("datamaps:updated", function(event, data) {
          if ($scope.datamap.id) {
            $scope.datamap = $datamaps.getById($scope.datamap.id);
          }
        });

        $scope.$on("datamaps:edit_datamap", function(event, datamap_id) {
          $scope.datamap = $datamaps.getById(datamap_id);
          $scope.datamap.setMetadataColumns().then(function(){
            $scope.current_tab = "basic-info";
            $scope.change_editing_state("edit");
            $scope.$apply();
          });
        });

        $scope.$on("datamaps:new_datamap", function(event, datamap_id) {
          $scope.datamap = {};
          $scope.current_tab = "basic-info";
          $scope.change_editing_state("new");
        });

        // $scope.get_metadata = function() {
        //   var url = "/app/kmlmap/"+$scope.kmlmap.id+"/metadata/";
        //   $http.get(url)
        //     .then(function(response){
        //       $scope.metadata = response.data;
        //     });
        // };

    	});
})();