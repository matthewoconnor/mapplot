(function(){
	angular.module("MapApplication")
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
})();
