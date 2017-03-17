(function(){
  angular.module("MapApplication")
    .factory('$datamaps', ['$http', '$log', '$interval', '$rootScope', function($http, $log, $interval, $rootScope) {

    var service = {};

    service.data = [];

    service.fetchAll = function(callback) {
      // fetch all datamaps from server
      $log.debug("fetchAll");
      $http.get("/kmlmap/list/json/")
        .then(function(response){
          service.data = response.data.kmlfiles // make these datamap objects?
          $rootScope.$broadcast('datamaps:updated', service.data);
          callback();
        });
    };

    service.findByAttr = function(attr, val) {
      var result = service.data.find(function(datamap){
        return datamap[attr] == val;
      });
      return result
    };

    service.getById = function(datamap_id) {
      return service.findByAttr("id", datamap_id);
    };

    service.watchImportProgress = function(datamap_id) {
      var datamap = service.getById(datamap_id);

      var taskwatcher = $interval(function(){
        $http.get("/app/task/progress/", {"params":{"task_ids":datamap.task_ids}}).then(function(response){
          if(response.data.status == "PROGRESS") {
            datamap.watchingProgress = true;
            datamap.taskPending = false;
            datamap.progressValue = response.data.complete * 100.0;
          }else if(response.data.status == "PENDING"){
            datamap.taskPending = true;
            datamap.watchingProgress = false
          }else{
            $interval.cancel(taskwatcher);
            datamap.progressValue = 100;
            datamap.taskPending = false;
            datamap.watchingProgress = false;
          }
        });
      }, 1000);
    };

    return service;

  }]);
})();

// function Datamap(options) {

//   options = options || {};

//   this.id = options.id;

//   this.name = options.name;
//   this.data_source = options.data_source;
//   this.dataset_identifier = options.dataset_identifier;
//   this.area_map = options.area_map;

//   this.categorize_type = options.categorize_type;
//   this.latitude_key = options.latitude_key;
//   this.longitude_key = options.longitude_key;
//   this.point_key = options.point_key;
//   this.join_key = options.join_key;

//   this.weight_type = options.weight_type;
//   this.value_key = options.value_key;
//   this.querystring = options.querystring;
//   this.join_key = options.join_key;

//   this.importState = {};

//   this.import = function() {
//     // make a request to trigger import of data
//   };

//   this.pollImportState = function() {
//     // make a request to poll state of import
//   };


// }
