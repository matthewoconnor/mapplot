angular
	.module("MapApplication", ["ngMaterial"])
	.config(function($interpolateProvider, $httpProvider) {
	    $interpolateProvider.startSymbol('{$');
	    $interpolateProvider.endSymbol('$}'); 

	    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
		$httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
	});
