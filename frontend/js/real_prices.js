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
    $scope.mode = 'choose_shop';
    $scope.connection_error = false;
    $scope.selected_shop_id = undefined;
    $scope.selected_shop_name = undefined;
    $http.get(domain + '/shops').success(function(response){
        $scope.shops = response;
    }).error(function(response){
        $log.error(response);
        $scope.connection_error = true;
        $scope.connection_error_message = response;
    });

    $scope.choose_shop = function (id, name) {
        $log.info("Choosed shop: " + id + " " + name);
        $scope.selected_shop_id = id;
        $scope.selected_shop_name = name;
        $scope.mode = 'products';
    };

    $scope.search_products = function (query){
        $http.get(domain + '/products',
            { params: { shop_id: $scope.selected_shop_id, query: query }}).success(function (response){
            $scope.products = response;
        }).error(function (response) {
            $log.error(response);
            $scope.connection_error = true;
            $scope.connection_error_message = response;
        });
    };

    $scope.back_to_choose_shop_mode = function() {
        $scope.selected_shop_id = undefined;
        $scope.selected_shop_name = undefined;
        $scope.mode = 'choose_shop';
        $scope.products = [];
    };
});
