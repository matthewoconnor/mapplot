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
          var datamaps = response.data.datamaps;
          for(var i = 0; i < datamaps.length; i++) {
            service.data.push(new Datamap(datamaps[i]))
          }
        
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
