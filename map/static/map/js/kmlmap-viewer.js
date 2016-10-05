$(function(){

	var viewer = new Cesium.Viewer("worldmap");

	$("#maplist .selectable-list").on("click", "a", function(event){
		var url = $(event.target).attr("data-source")
		viewer.dataSources.add(Cesium.KmlDataSource.load(
			url, {
	        	camera: viewer.camera,
	        	canvas: viewer.canvas
	        }));
	});

});