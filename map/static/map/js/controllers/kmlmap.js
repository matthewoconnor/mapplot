(function(){
	angular.module("MapApplication")
		.controller('KmlMapController', function($scope, $log, $http, $interval) {

	  		$scope.kmldata = null;

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

	  			var taskwatcher = $interval(function(){
	  				$http.get("/app/task/progress/", {"params":{"task_ids":task_ids_string}}).then(function(response){
		  				if(response.data.status == "PROGRESS") {
		  					$scope.watchingProgress = true;
		  					$scope.taskPending = false;
		  					$scope.progressValue = response.data.complete * 100.0;
		  				}else if(response.data.status == "PENDING"){
		  					$scope.taskPending = true;
		  					$scope.watchingProgress = false
		  				}else{
		  					$interval.cancel(taskwatcher);
		  					$scope.progressValue = 100;
		  					$scope.taskPending = false;
		  					$scope.watchingProgress = false;

		  					// refetch at the end 
		  					$scope.fetchKmlMap();
		  				}
		  			});
	  			}, 1000);

	  		}

	  		$scope.fetchKmlMap = function() {

	  			$scope.isLoading = true;

	  			$http.get("/kmlmap/list/json/", {"params":{"ids":$scope.kmlfile.id}})
					.then(function(response){
						if(response.data.kmlfiles){
							$scope.kmlfile = response.data.kmlfiles[0];	
						}
						$scope.isLoading = false;
					});
	  		}


	  		// ON INIT
	  		if($scope.kmlfile.task_ids) {
	  			$scope.watchTaskProgress($scope.kmlfile.task_ids.join(","));
	  		}

	  	});
})();
