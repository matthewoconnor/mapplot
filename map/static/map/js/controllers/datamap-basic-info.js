(function(){
  angular.module("MapApplication")
    .controller('DataMapBascInfoController', function($scope, $log, $http, $datamaps) {
        
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
            $scope.datamap.area_map = item;
          }
        }

        $scope.submitForm =function() {

          var submitData = angular.copy($scope.datamap);
          submitData.area_map = $scope.datamap.area_map.id;
          submitData = $.param(submitData);

          var config = {
              headers : {
                  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
              }
          }

          $http.post("/app/datamap/create/", submitData, config).then(function(response){
            if(response.data.success && response.data.datamap_id){
              $scope.datamap.id = response.data.datamap_id;
              $datamaps.data.unshift($scope.datamap);
              $scope.change_tab("settings");
            }
          });
          
        }

    });
})();

