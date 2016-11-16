(function(app) {

	angular
		.module("MapApplication", ["ngMaterial"])
		.config(function($interpolateProvider) {
		    $interpolateProvider.startSymbol('{$');
		    $interpolateProvider.endSymbol('$}');

		    // $httpProvider
		    // $httpProvider.defaults.xsrfCookieName = 'csrftoken';
		    // $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
		})
		.controller("MapApplicationController", function ($scope, $http, $mdSidenav, $log) {

			$scope.cesium = new Cesium.Viewer("worldmap");
		
			$scope.fetchData = function(){
				$scope.isLoading = true;
				$log.debug("fetchingData");
				$http.get("/kmlmap/list/json/")
					.then(function(response){
						$scope.kmlfiles = response.data.kmlfiles;
						$scope.isLoading = false;
					});
			}

			$scope.fetchData();

		  })
		// .controller("KmlMapList", function($scope, $http) {

		// 	$scope.kmlfiles  = []
		// 	$scope.isLoading = false;

		// 	$scope.fetchData = function(){
		// 		$scope.isLoading = true;
		// 		$log.debug("fetchingData");
		// 		$http.get("/kmlmap/list/json/")
		// 			.then(function(response){
		// 				$scope.kmlfiles = response.data.kmlfiles;
		// 				$scope.isLoading = false;
		// 			});
		// 	}
		// 	$scope.fetchData();
		// })
	  	.controller('KmlMapNavigationController', function ($scope, $timeout, $mdSidenav, $log) {

		    $scope.close = function () {
		      $mdSidenav('left').close()
		        .then(function () {
		          $log.debug("close LEFT is done");
		        });
		    };


		})
	  	.controller('KmlMapController', function($scope, $log) {
	  		$scope.kmldata = null;
	  		$scope.isLoading = false;

	  		$scope.showKmlData = function(){
	  			$scope.isLoading = true;
	  			if($scope.kmldata) {
	  				$scope.isLoading = false;
	  				$scope.cesium.flyTo($scope.kmldata.entities);
	  			}else{
	  				$scope.kmldata = Cesium.KmlDataSource.load(
						$scope.kmlfile.source, {
				        	camera: $scope.cesium.camera,
				        	canvas: $scope.cesium.canvas
				        });
					$scope.cesium.dataSources.add($scope.kmldata).then( function (kmlData) { //success
						$scope.kmldata = kmlData;
						$scope.isLoading = false;
		                $scope.cesium.flyTo(kmlData.entities);
		            });
	  			}
	  		}

	  	});


})(window.app || (window.app = {}));