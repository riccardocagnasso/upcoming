'use strict'

###*
 # @ngdoc overview
 # @name frontendApp
 # @description
 # # frontendApp
 #
 # Main module of the application.
###
module = angular.module('frontendApp', [
        'ngAnimate',
        'ngCookies',
        'ngResource',
        'ngRoute',
        'ngSanitize',
        'ngTouch',
        'LocalStorageModule',
        'config',
        'directive.g+signin',
        'djds4rce.angular-socialshare'
    ]).config ($routeProvider, $locationProvider) ->
        $routeProvider
            .when '/',
                templateUrl: 'views/main.html'
                controller: 'MainCtrl'
            .when '/about',
                templateUrl: 'views/about.html'
                controller: 'AboutCtrl'
            .when '/myUpcomings',
                templateUrl: 'views/myUpcomings.html'
                controller: 'MyUpcomingsCtrl'
                controllerAs: 'MyUpcomingsCtrl'
            .when '/newUpcoming',
                templateUrl: 'views/newUpcoming.html'
                controller: 'NewUpcomingCtrl'
                controllerAs: 'NewUpcomingCtrl'
            .when '/upcoming/:shortUrl/:name',
                templateUrl: 'views/singleUpcoming.html'
                controller: 'SingleUpcomingCtrl'
            .when '/faq',
                templateUrl: 'views/faq.html'
                controller: 'FaqCtrl'
            .otherwise
                redirectTo: '/'

        $locationProvider.html5Mode true
            .hashPrefix '!'

angular.module 'frontendApp'
    .run ($FB) ->
        $FB.init '727286834007338'

module.factory 'myInterceptor', ['$location', 'localStorageService', 'BASEURL',
    ($location, localStorage, BASEURL) ->
        return request: (config) ->
            if config.url[0..4] == '/api/'
                config.url = BASEURL + config.url
                token = localStorage.get 'token'
                username = localStorage.get 'username'

                if token and username
                    config.headers.Authorization = 'JWT token="'+ token+'"'
            return config
]

module.config ['$httpProvider', ($httpProvider) ->
    $httpProvider.interceptors.push 'myInterceptor'
]
