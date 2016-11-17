angular
	.module("MapApplication", ["ngMaterial"])
	.config(function($interpolateProvider) {
	    $interpolateProvider.startSymbol('{$');
	    $interpolateProvider.endSymbol('$}');

	    // $httpProvider
	    // $httpProvider.defaults.xsrfCookieName = 'csrftoken';
	    // $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	})
	
 //  	.controller('KmlMapNavigationController', function ($scope, $timeout, $mdSidenav, $log) {

	//     $scope.close = function () {
	//       $mdSidenav('left').close()
	//         .then(function () {
	//           $log.debug("close LEFT is done");
	//         });
	//     };

	// })