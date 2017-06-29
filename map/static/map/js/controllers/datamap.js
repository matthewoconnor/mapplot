(function(){
	angular.module("MapApplication")
		.controller('DataMapController', function($scope, $log, $http, $interval, $datamaps) {

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

	  		$scope.toggleVisibility = function() {
	  			if($scope.isVisible) {
	  				$scope._show();
	  			}else{
	  				$scope._hide();
	  			}
	  		}

	  		$scope.setGeometry = function() {
	  			$scope.isLoading = true;

	  			$scope.datamap.getGeometry()
	  				.then($scope.datamap.setCesiumGeometry)
	  				.then(function(areabins){
	  					$scope.datamap.addToCesiumMap($scope.cesium);
	  				})
	  				.then($scope.datamap.setMetadataCounts)
	  				.then($scope.datamap.setCesiumEntitiesColor)
	  				.then(function(){
	  					$scope.isLoading = false;
	  					$scope.isLoaded = true;
	  					$scope.isVisible = true;
	  					$scope.$apply();
	  					$scope.datamap.flyToCesiumEntities($scope.cesium);
	  				});
	  		}

	  		$scope._hide = function() {
	  			$scope.datamap.hideCesiumEntities();
	  		}

	  		$scope._show = function() {
	  			$scope.datamap.showCesiumEntities().then(function(entities){
	  				$scope.datamap.flyToCesiumEntities($scope.cesium, entities);
	  			});
	  		}

	  		$scope.edit = function() {
	  			$datamaps.editDatamap($scope.datamap.id);
	  			$scope.navigate("create_datamap");
	  		}

	  		// ON INIT
	  		if($scope.datamap.task_ids) {
	  			$datamaps.watchImportProgress($scope.datamap.id);
	  		}

	  	});
})();
