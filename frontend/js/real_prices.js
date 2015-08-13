var realPricesApp = angular.module('realPricesApp', []);
var domain = 'http://localhost:8000';

realPricesApp.config(function ( $httpProvider) {
        delete $httpProvider.defaults.headers.common['X-Requested-With'];
    }).factory('featuresData', function ($http) {
        return{
            doCrossDomainGet: function() {
                return $http({
                    url:'http://localhost:8000',
                    method: 'GET'
                })
            }
        }
});

realPricesApp.controller('IndexController', function ($scope, $http, $log){
    $http.get(domain + '/shops').success(function(response){
        $scope.shops = response;
    }).error(function(response){
        $log.error(response);
    });
});
