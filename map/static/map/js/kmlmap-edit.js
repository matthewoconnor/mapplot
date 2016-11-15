angular
	.module('KmpMapEditor', ['ngMaterial', 'ngMessages'])
	.controller('KmlMapForm', function($scope) {
		$scope.kmlmap = $("form", "KmlMapForm").serialize();
	})
	.config(function($mdThemingProvider) {

	// Configure a dark theme with primary foreground yellow

	$mdThemingProvider.theme('docs-dark', 'default')
      .primaryPalette('blue')
      .dark();
  	});

