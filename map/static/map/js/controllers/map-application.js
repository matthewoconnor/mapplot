(function(){
	angular.module("MapApplication")
		.controller("MapApplicationController", function ($scope, $http, $mdSidenav, $log, $datamaps) {

			Cesium.BingMapsApi.defaultKey = "ArHjacadQi3kS1tS5SF2COD2kB5dZVy0LN8pFxGLmkMMuEDHhhTIO22VYXZ2os5S";
			$scope.cesium = new Cesium.Viewer("worldmap");
			$scope.datamaps = $datamaps.data;
			$scope.isLoading = false;

			$scope.toggleLeftMenu = buildToggler('left');
			$scope.view = "map";
		
			$scope.fetchData = function(){
				$scope.isLoading = true;
				$datamaps.fetchAll(function(){
					$scope.isLoading = false;
				});
			}

			$scope.$on("datamaps:updated", function(event, data) {
				$scope.datamaps = data;
			});

			$scope.navigate = function(viewname) {
				$scope.view = viewname;
			};

			$scope.createNewDatamap = function() {
				$datamaps.newDatamap();
				$scope.navigate("create_datamap");
			}

			$scope.stopPropagation=function(ev){
		        // don't delete this method it is required for multiple checkbox in list item.
              	ev.stopPropagation();
		    };

			function buildToggler(navID) {
		      return function() {
		        // Component lookup should always be available since we are not using `ng-if`
		        $mdSidenav(navID)
		          .toggle()
		          .then(function () {
		            $log.debug("toggle " + navID + " is done");
		          });
		      }
		    };

			$scope.fetchData();
		});
})();
