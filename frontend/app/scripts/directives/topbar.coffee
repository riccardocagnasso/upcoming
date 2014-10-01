'use strict'

class TopBarController
    loginData: {}
    username: null

    constructor: ($http, localStorage, $rootScope) ->
        this.$http = $http
        this.$rootScope = $rootScope
        this.localStorage = localStorage
        this.username = this.localStorage.get 'username'

    login: ->
        controller = this
        (this.$http.post '/api/login',
            controller.loginData).success (data) ->
                if data.success
                    controller.username = controller.loginData.username
                    controller.localStorage.set 'token', data
                    controller.localStorage.set 'username', controller.loginData.username
                    controller.loginData = {}

                    controller.$rootScope.$broadcast 'login'

    logout: ->
        this.localStorage.remove 'token'
        this.localStorage.remove 'username'
        this.username = null

        this.$rootScope.$broadcast 'logout'

angular.module('frontendApp')
    .directive 'topBar', ->
        restrict: 'E'
        templateUrl: 'views/topbar.html'
        controllerAs: 'topBarCtrl'
        transclude: true
        controller: [ '$http', 'localStorageService',
                     '$rootScope', TopBarController ]
