'use strict'

###*
 # @ngdoc function
 # @name frontendApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the frontendApp
###
angular.module('frontendApp')
    .directive 'topBar', -> {
        restrict: 'E'
        templateUrl: 'views/topbar.html'
        controllerAs: 'topBarCtrl'
        transclude: true
        controller: [ '$http', 'localStorageService',
            class TopBarController
                loginData: {}
                username: null

                constructor: ($http, localStorage) ->
                    this.$http = $http
                    this.localStorage = localStorage
                    this.username = this.localStorage.get 'username'

                login: ->
                    controller = this
                    (this.$http.post 'http://localhost:6543/api/login',
                        controller.loginData).success (data) ->
                            if data.success
                                controller.username = controller.loginData.username
                                controller.localStorage.set 'token', data
                                controller.localStorage.set 'username', controller.loginData.username
                                #controller.loginData = {}

                                controller.$http.get 'http://localhost:6543/api/upcomings'

                logout: ->
                    this.localStorage.remove 'token'
                    this.localStorage.remove 'username'
                    this.username = null

            ]
    }
