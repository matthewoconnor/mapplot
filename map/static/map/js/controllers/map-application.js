(function(){
	angular.module("MapApplication")
		.controller("MapApplicationController", function ($scope, $http, $mdSidenav, $log) {

			$scope.cesium = new Cesium.Viewer("worldmap");
			$scope.kmlfiles = [];
			$scope.isLoading = false;
		
			$scope.fetchData = function(){
				$scope.isLoading = true;
				$log.debug("fetchingData");
				$http.get("/kmlmap/list/json/")
					.then(function(response){
						$scope.kmlfiles = response.data.kmlfiles;
						$scope.isLoading = false;
					});
			}


			$scope.$on($viewControllerLoaded)
			$scope.fetchData();
		});
})();
