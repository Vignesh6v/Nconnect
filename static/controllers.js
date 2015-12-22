
angular.module("myApp").controller("registerController",
  ["$scope", "$http" ,"$location",
  function ($scope, $http, $location) {

    $scope.register = function () {

      // initial values
      $scope.error = false;

      $http.post("/api/register", $scope.registerForm)
        .success(function(data,status){
          if(status === 200 && data.result && data.code == "200"){
            $location.path("/home");
            $rootScope.current_user = data.user.username;
            $rootScope.authenticated = true;
            console.log(data);
          }
          else{
            $scope.error = true;
            $scope.errorMessage = data.message;
          } 
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
    };
}]);

angular.module("myApp").controller("loginController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {

    $scope.login = function () {
      

       console.log($scope.loginForm);
      // initial values
      $scope.error = false;
      $scope.authenticated = false;
      $http.post("/api/login",$scope.loginForm)
        .success(function (data, status) {
          if(status === 200 && data.result && data.code == "200"){
            $location.path("/home");
            $scope.loginForm = {};
            $rootScope.current_user = data.user.username;
            console.log(data.user.username);
            console.log($rootScope.current_user);
            $rootScope.authenticated = true;
            console.log(data);
          }
          else{
            $scope.error = true;
            $scope.errorMessage = data.message;
            $scope.loginForm = {};
          }
        })
        .error(function(data){
          console.log("Error in return call");
          console.log(data);
        })
    };
}]);

angular.module('appMaps', ['uiGmapgoogle-maps'])
    .controller('mainCtrl', function($scope) {
        $scope.map = {center: {latitude: 51.219053, longitude: 4.404418 }, zoom: 14 };
        $scope.options = {scrollwheel: false};
    });

angular.module("myApp").controller("mapController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("first");

    $scope.initialize = function() {
        console.log("inside init");
        var mapCanvas = document.getElementById('map');
        var mapOptions = {
          center: new google.maps.LatLng(44.5403, -78.5463),
          zoom: 8,
          mapTypeId: google.maps.MapTypeId.ROADMAP
        }
        var map = new google.maps.Map(mapCanvas, mapOptions)
      }
      google.maps.event.addDomListener(window, 'load', initialize);
}]);


angular.module("myApp").controller("logoutController",
  ["$scope","$http", "$location",
  function ($scope, $http, $location) {

    $scope.logout = function () {

      $http.get("/api/logout")
        .success(function(data){
          $location.path("/login");
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
      
    };

}]);

angular.module("myApp").controller("blockController",
  ["$scope","$http","$rootScope","$location",
  function ($scope, $http, $rootScope, $location) {
      $scope.user = $rootScope.current_user;
      $http.get("/api/blockreq/"+ $scope.user)
        .success(function(data,status){
          console.log(data);
          $scope.posts = data.items;
           console.log($scope.posts);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("homeController",
  ["$scope","$http","$rootScope" ,"$location",
  function ($scope, $http,$rootScope, $location) {
     $scope.user = $rootScope.current_user;
     console.log($scope.user)
      $http.get("/api/hoodreq/"+ $scope.user)
        .success(function(data,status){
          console.log(data);
          $scope.posts = data.items;
           console.log($scope.posts);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("neighborController",
  ["$scope","$http","$rootScope" ,"$location",
  function ($scope, $http,$rootScope, $location) {
     $scope.user = $rootScope.current_user;
     console.log($scope.user)
      $http.get("/api/neigbhorreq/"+ $scope.user)
        .success(function(data,status){
          console.log(data);
          $scope.nposts = data.items;
           console.log($scope.nposts);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("allfrndController",
  ["$scope","$http","$rootScope" ,"$location",
  function ($scope, $http,$rootScope, $location) {
     $scope.user = $rootScope.current_user;
     console.log($scope.user)
      $http.get("/api/friendreq/"+ $scope.user)
        .success(function(data,status){
          console.log(data);
          $scope.fposts = data.items;
           console.log($scope.fposts);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("msgController",
  ["$scope","$http","$rootScope" ,"$location",
  function ($scope, $http,$rootScope, $location) {
     $scope.user = $rootScope.current_user;
     console.log($scope.user)
      $http.get("/api/private/"+ $scope.user)
        .success(function(data,status){
          console.log(data);
          $scope.mposts = data.items;
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("profileController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    $scope.profiles = [
      { name: "Varun Elango",description :"John", interest: "Tennis",  dob :"25", imageUrl:"./static/img/Dp_Pic.jpg"}
    ];
}]);

angular.module("myApp").controller("flistController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("friendcontrol block");
    $http.get("/api/pending/"+ $rootScope.current_user)
        .success(function(data){
          $scope.friends = data.pending;
          $scope.requested = data.requested;
          $scope.newlist = data.tobesent;
          console.log($scope.friends);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })

    $scope.frequest = function ($id) {
      console.log($id);
      var items = {uname: $rootScope.current_user, toid: $id};
      console.log (items);
      $http.post("/api/friendrequest",items)
        .success(function (data, status) {
            $location.path("/friends");
        })
        .error(function(data){
          console.log("Error in return call");
          console.log(data);
        })
    };        
}]);

angular.module("myApp").controller("friendlistController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("friendcontrol block");
    $http.get("/api/oldfriends/"+ $rootScope.current_user)
        .success(function(data){
          $scope.friends = data.items;
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })

}]);

angular.module("myApp").controller("viewprofileController",
  ["$scope","$http", "$rootScope", "$routeParams","$location",
  function ($scope, $http, $rootScope, $routeParams, $location) {
    console.log("viewprofile block");
    var currentid = $routeParams.item;
    $scope.profiles = [
      { name: "Varun Elango",description :"John", interest: "Tennis",  dob :"25" , imageUrl:"./static/img/Dp_Pic.jpg"}
    ];

    $scope.uploadfile = function(){
      $http.post('upload.ashx',$scope.files)
      .success(function(data){
        console.log('uploaded');
      })
      .error(function(data){
        console.log("error");
      })
    };
}]);

angular.module("myApp").controller("changeBController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("changeblock block");
    $scope.address = [
      { street :"John", apt: "1",  door :"25", zip:"12322", city:"New York"}
    ];
}]);

angular.module("myApp").controller("searchController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("search block");
      $scope.user = $rootScope.current_user;
      console.log($scope.searchtext);
      $http.get("/api/search/"+ $scope.user+"/"+$scope.searchtext)
        .success(function(data,status){
          console.log(data);
          $scope.posts = data.items;
           console.log($scope.posts);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("detailController",
  ["$scope","$http", "$rootScope", "$routeParams","$location",
  function ($scope, $http, $rootScope, $routeParams, $location) {
    console.log("detail block");
      var currentid = $routeParams.item;
      $scope.comments = {}
      $http.get("/api/comments/"+ currentid)
        .success(function(data,status){
            console.log(data);
            $scope.comments = data.items;
            $scope.posts = data.post;
             console.log($scope.posts);
             console.log($scope.comments);
        })
        .error(function(data){
          console.log("error");
          console.log(data);
        })
}]);

angular.module("myApp").controller("nbController",
  ["$scope","$http", "$rootScope", "$location",
  function ($scope, $http, $rootScope, $location) {
    console.log("NB block");
    $scope.nb = [
      { name :"nb1"}, { name :"nb2"}
    ];
}]);
