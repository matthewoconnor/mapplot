function Datamap(options) {

  var self = this;

  options = options || {};

  this.id = options.id;

  this.name = options.name;
  this.data_source = options.data_source;
  this.dataset_identifier = options.dataset_identifier;
  this.area_map = options.area_map;

  this.categorize_type = options.categorize_type;
  this.latitude_key = options.latitude_key;
  this.longitude_key = options.longitude_key;
  this.point_key = options.point_key;
  this.join_key = options.join_key;

  this.weight_type = options.weight_type;
  this.value_key = options.value_key;
  this.querystring = options.querystring;

  // non-model fields
  this.import_state = {};
  this.geometry = [];
  this.areabins = [];

  this.import = function() {
    // make a request to trigger import of data
    	// returns a promise
  };

  this.pollImportState = function() {
    // make a request to poll state of import
    	// returns a promise
  };

  this.fetchGeometry = function() {
  	// conditionally fetch geometry if doesn't already have it
  		// returns a promise

  	// consider using $.get instead of $http angular service
		return $.get("/app/datamap/"+self.id+"/geometry/").then(function(response){
      if(response.success){
        self.geometry = response.data.geometry;
        return self.geometry
      }else{
        throw "Error!!"
      }
    });
  }

  this.getGeometry = function() {
  	// retrieve geometry data from server
  		// returns a promise
	  if(self.geometry && self.geometry.length) {
	    return Promise.resolve(self.geometry);
	  }else{
	    return self.fetchGeometry();
	  }
  }

  this.setCesiumGeometry = function() {
  	var areabins = []
		for(var i = 0; i < self.geometry.length; i++) {
			var areabin = self.geometry[i];
			var cesium_polygons = [];
			for(var j = 0; j < areabin.geometry.length; j++) {
				var g = areabin.geometry[j];
				var outer_polygon = Cesium.Cartesian3.fromDegreesArray([].concat.apply([], g.outer).map(parseFloat));
				var inner_polygons = []
				for(var k = 0; k < g.inner.length; k++) {
					var hole = g.inner[k];
					inner_polygons.push(Cesium.Cartesian3.fromDegreesArray([].concat.apply([], hole).map(parseFloat)));
				}
				polygonGeometry = {
					"hierarchy" : {
						"positions":outer_polygon,
						"holes":inner_polygons	
					},
					"extrudedHeight":areabin.count
				};
				cesium_polygons.push(polygonGeometry);
			}
			areabin.cesium = {}; 
			areabin.cesium.polygons = cesium_polygons;
			areabins.push(areabin);
		}
		self.areabins = areabins;
		return self.areabins;
  }

  this.addToCesiumMap = function(cesium) {

	  for (var i = 0; i < self.areabins.length; i++) {
	  	var areabin = self.areabins[i];
			areabin.cesium.entities = [];
			for (var j = 0; j < areabin.cesium.polygons.length; j++) {
				var polygon = areabin.cesium.polygons[j];
				var entity = cesium.entities.add({
					"name":areabin.name,
					"polygon": polygon
				});
				areabin.cesium.entities.push(entity);
			}
		}
  }

}