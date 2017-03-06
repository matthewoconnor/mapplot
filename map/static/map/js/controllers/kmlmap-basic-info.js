(function(){
  angular.module("MapApplication")
    .controller('DataMapBascInfoController', function($scope, $log, $http) {
        
        $scope.areaMapAutocomplete = {
          searchText : "",
          getMatches : function(query) {
            return $http.get(
              "/app/areamap/autocomplete/", 
              {"params":{"query":query}}
            ).then(function(response){
              return response.data.results
            });
          },
          selectedItemChanged : function(item) {
            $scope.kmlmap.area_map = item;
          }
        }

        $scope.submitForm =function() {

          // var submitData = angular.copy($scope.kmlmap);
          // submitData.area_map = $scope.kmlmap.area_map.id;
          // submitData = $.param(submitData);

          // var config = {
          //     headers : {
          //         'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
          //     }
          // }

          // $http.post("/app/datamap/create/", submitData, config).then(function(response){
          //   if(response.data.success && response.data.kmlmap){
          //     var newkmlmap = response.data.kmlmap;
          //     $scope.current_tab = "settings"
          //   }
          // });

           $scope.change_tab("settings");

        }

    });
})();

