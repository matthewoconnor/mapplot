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

        $scope.getSubmitData = function() {
          return {
            "name":$scope.datamap.name,
            "data_source":$scope.datamap.data_source, 
            "dataset_identifier":$scope.datamap.dataset_identifier, 
            "area_map":$scope.datamap.area_map.id
          }
        }

        $scope.submitForm = function() {

          var submitData = $.param($scope.getSubmitData());

          var config = {
              headers : {
                  'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8;'
              }
          }

          if($scope.datamap.id) {
            $scope._submitUpdate(submitData, config);
          }else{
            $scope._submitCreate(submitData, config);
          }
          
        }

        $scope._submitCreate = function(data, config) {
          $http.post("/app/datamap/create/", data, config).then(function(response){
            if(response.data.success && response.data.datamap_id){
              $scope.datamap.id = response.data.datamap_id;
              $scope.datamap = new Datamap($scope.datamap);
              $datamaps.data.unshift($scope.datamap);
              $scope.change_editing_state("edit");
              $scope.change_tab("settings");
            }
          });
        }

        $scope._submitUpdate = function(data, config) {
          $http.post("/app/datamap/"+$scope.datamap.id+"/update/", data, config).then(function(response){
            if(response.data.success && response.data.datamap_id){
              $scope.change_editing_state("edit");
              $scope.change_tab("settings");
            }
          });
        }
 
    });
})();

