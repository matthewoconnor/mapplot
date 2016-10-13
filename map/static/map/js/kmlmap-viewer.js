$(function(){

	var viewer = new Cesium.Viewer("worldmap");

	$("#maplist .selectable-list").on("click", "a", function(event){
		var dataSource = $(event.target).data("dataSource");

		if(dataSource) {
			viewer.flyTo(dataSource.entities);
		} else {
			var url = $(event.target).attr("data-source");
			dataSource = Cesium.KmlDataSource.load(
				url, {
		        	camera: viewer.camera,
		        	canvas: viewer.canvas
		        });
			viewer.dataSources.add(dataSource).then( function (kmlData) { //success
				$(event.target).data("dataSource", kmlData);
                viewer.flyTo(kmlData.entities);
            });
		}

	});

});