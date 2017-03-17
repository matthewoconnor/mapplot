(function(){
  angular.module("MapApplication")
  	.controller('DataMapImportSettingsController', function($scope, $log, $http, $datamaps) {

        $scope.submitForm =function() {

          var submitData = angular.copy($scope.datamap);
          submitData.area_map = $scope.datamap.area_map.id;
          submitData = $.param(submitData);

          var config = {
              headers : {
                  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
              }
          }

          $http.post("/app/datamap/"+$scope.datamap.id+"/import-settings/", submitData, config).then(function(response){
            if(response.data.success && response.data.task_ids){
              $scope.datamap.task_ids = response.data.task_ids.join(",");
              $datamaps.watchImportProgress($scope.datamap.id);
              $scope.current_tab = "import";
            }
          });

          $scope.change_tab("import");
    	}

	});
})();