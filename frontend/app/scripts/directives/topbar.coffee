'use strict'

class TopBarController
    loginData: {}
    username: null

    constructor: ($http, localStorage, $rootScope, $scope) ->
        controller = this

        this.$http = $http
        this.$rootScope = $rootScope
        this.localStorage = localStorage
        this.username = this.localStorage.get 'username'
        this.$scope = $scope

        this.$scope.$on 'event:google-plus-signin-success', (event, authResult) ->
            controller.loginGoogle authResult

        this.$scope.$on 'event:google-plus-signin-failure', (event, authResult) ->
            console.log 'loginFailure'

        #this.renderSignInButton()

    login: ->
        controller = this
        (this.$http.post '/api/login',
            controller.loginData).success (data) ->
                if data.success
                    controller.username = controller.loginData.username
                    controller.localStorage.set 'token', data.token
                    controller.localStorage.set 'username', controller.loginData.username
                    controller.loginData = {}

                    controller.$rootScope.$broadcast 'login'

    loginGoogle: (authResult) ->
        controller = this

        this.$http.post '/api/loginGoogle', authResult
            .success (data) ->
                if data.success
                    controller.username = data.username
                    controller.localStorage.set 'token', data.token
                    controller.localStorage.set 'username', data.username
                    controller.loginData = {}

                    controller.$rootScope.$broadcast 'login'

    logout: ->
        this.localStorage.remove 'token'
        this.localStorage.remove 'username'
        gapi.auth.signOut();

        this.username = null
        this.$rootScope.$broadcast 'logout'

    renderSignInButton: ->
        gapi.signin.render 'signInButton',
            callback: this.getLoginGoogle this
            clientid: '281630648196-oss9bk6fffvlq85139bql607ra05d839.apps.googleusercontent.com'
            requestvisibleactions: 'http://schemas.google.com/AddActivity'
            scope: 'https://www.googleapis.com/auth/plus.login https://www.googleapis.com/auth/userinfo.email'
            cookiepolicy: 'single_host_origin'

angular.module('frontendApp')
    .directive 'topBar', ->
        restrict: 'E'
        templateUrl: 'views/topbar.html'
        controllerAs: 'topBarCtrl'
        transclude: true
        controller: [ '$http', 'localStorageService',
                     '$rootScope', '$scope', TopBarController ]
