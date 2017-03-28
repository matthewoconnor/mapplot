(function(){
	angular.module("MapApplication")
		.controller('DataMapController', function($scope, $log, $http, $interval, $datamaps) {

			$scope.data = null;

	  		$scope.isLoading = false;
	  		$scope.isLoaded = false;
	  		$scope.isVisible = false;

	  		$scope.watchingProgress = false;
	  		$scope.taskPending = false;
	  		$scope.progressValue = 12.0;

	  		$scope.showKmlData = function(){
	  			$scope.isLoading = true;
	  			if(!$scope.kmldata) {
	  				$scope.kmldata = Cesium.KmlDataSource.load(
						$scope.datamap.source, {
				        	camera: $scope.cesium.camera,
				        	canvas: $scope.cesium.canvas
				        });
	  			}
	  			$scope.addKmlDataToCesiumViewer($scope.kmldata);
	  		}

	  		$scope.hideKmlData = function(){
	  			if($scope.kmldata) {
	  				$scope.cesium.dataSources.remove($scope.kmldata)
	  				$scope.isVisible = false;
	  			}
	  		}

	  		$scope.addKmlDataToCesiumViewer = function(kmldata) {
	  			if (!$scope.cesium.dataSources.contains($scope.kmldata)) {
  					$scope.cesium.dataSources.add($scope.kmldata).then(function(kmlData){
  						$scope.kmldata = kmlData;
  						$scope.isLoading = false;
						$scope.isLoaded = true;
						$scope.isVisible = true;
						$scope.cesium.flyTo(kmlData.entities);
						try {
							$scope.$apply();
						} catch (err) {}
						
  					})
  				}else{
  					$scope.isLoading = false;
	  				$scope.isVisible = true;
	  				$scope.cesium.flyTo($scope.kmldata.entities);
  				}
	  		}

	  		$scope.toggleVisibility = function(isvisible) {
	  			if(isvisible) {
	  				$scope.showKmlData();
	  			}else{
	  				$scope.hideKmlData();
	  			}
	  		}

	  		$scope.setGeometry = function() {
	  			$scope.isLoading = true;

	  			$scope.datamap.getGeometry()
	  				.then($scope.datamap.setCesiumGeometry)
	  				.then(function(areabins){
	  					$scope.datamap.addToCesiumMap($scope.cesium);
	  					$scope.isLoading = false;
	  				});
	  		}

	  		// ON INIT
	  		if($scope.datamap.task_ids) {
	  			$scope.watchTaskProgress($scope.datamap.task_ids.join(","));
	  		}

	  	});
})();
