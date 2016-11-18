(function(){
	angular.module("MapApplication")
		.controller('KmlMapController', function($scope, $log) {

	  		$scope.kmldata = null;

	  		$scope.isLoading = false;
	  		$scope.isLoaded = false;
	  		$scope.isVisible = false;

	  		$scope.watchingProgress = false;
	  		$scope.progressValue = 0.0; 

	  		$scope.showKmlData = function(){
	  			$scope.isLoading = true;
	  			if(!$scope.kmldata) {
	  				$scope.kmldata = Cesium.KmlDataSource.load(
						$scope.kmlfile.source, {
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

	  		$scope.watchTaskProgress = function(task_ids_string) {

	  			var taskwatcher = setInterval(function(){
	  				$http.get("/app/task/progress/", {"params":{"task_ids":task_ids_string}}).then(function(response){
		  				if(response.data.status == "PROGRESS") {
		  					$scope.progressValue = float(response.data.complete) * 100;
		  				}else{
		  					clearInterval(taskwatcher);
		  					$scope.progressValue = 100;
		  					$scope.watchingProgress = false;
		  				}
		  			});
	  			}, 1000);

	  		}

	  	});
})();
