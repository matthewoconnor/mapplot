(function(){
  angular.module("MapApplication")
  	.controller('DataMapImportSettingsController', function($scope, $log, $http, $datamaps) {

      $scope.submitForm =function() {

        var submitData = $.param($scope.getSubmitData());

        var config = {
            headers : {
                'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
            }
        }

        $http.post("/app/datamap/"+$scope.datamap.id+"/import-settings/", submitData, config).then(function(response){
          if(response.data.success && response.data.task_ids){
            $scope.datamap.task_ids = response.data.task_ids.join(",");
            $datamaps.watchImportProgress($scope.datamap.id);
            $scope.change_editing_state("import");
            $scope.change_tab("import");
          }

        });
    	}

      $scope.getSubmitData = function() {
          return {
            "weight_type":$scope.datamap.weight_type,
            "categorize_type":$scope.datamap.categorize_type, 
            "point_key":$scope.datamap.point_key, 
            "latitude_key":$scope.datamap.latitude_key,
            "longitude_key":$scope.datamap.longitude_key,
            "join_key":$scope.datamap.join_key,
            "value_key":$scope.datamap.value_key,
            "querystring":$scope.datamap.querystring
          }
        }

	});
})();