(function(){
  angular.module("MapApplication")
  	.controller('DataMapImportSettingsController', function($scope, $log, $http) {

        $scope.submitForm =function() {

          // var submitData = angular.copy($scope.kmlmap);
          // submitData.area_map = $scope.kmlmap.area_map.id;
          // submitData = $.param(submitData);

          // var config = {
          //     headers : {
          //         'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
          //     }
          // }

          // $http.post("/app/datamap/import-settings/", submitData, config).then(function(response){
          //   if(response.data.success && response.data.kmlmap){
          //     var newkmlmap = response.data.kmlmap;
          //     newkmlmap.task_ids = response.data.task_ids;
          //     $scope.kmlfiles.unshift(newkmlmap);
          //     $scope.current_tab = "import"
          //   }
          // });

          $scope.change_tab("import");
    	}

	});
})();