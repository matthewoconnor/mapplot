(function(){
	angular.module("MapApplication")
		.controller("MapApplicationController", function ($scope, $http, $mdSidenav, $log) {

			$scope.cesium = new Cesium.Viewer("worldmap");
			$scope.kmlfiles = [];
			$scope.isLoading = false;

			$scope.toggleLeftMenu = buildToggler('left');
			$scope.view = "map";
		
			$scope.fetchData = function(){
				$scope.isLoading = true;
				$log.debug("fetchingData");
				$http.get("/kmlmap/list/json/")
					.then(function(response){
						$scope.kmlfiles = response.data.kmlfiles;
						$scope.isLoading = false;
					});
			}

			$scope.navigate = function(viewname) {
				$scope.view = viewname;
			};

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
