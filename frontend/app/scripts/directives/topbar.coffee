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
      restrict: 'E',
      templateUrl: 'views/topbar.html'
      controllerAs: 'topBarCtrl'
      controller: [ 'localStorageService',
          class TopBarController
              loginData: {}
              constructor: (localStorage) ->
                  this.localStorage = localStorage
                  this.username = this.localStorage.get 'username'

              login: ->
                  controller = this

                  ($.post 'http://localhost:6543/api/login', this.loginData)
                    .success (data) ->
                        controller.localStorage.set 'userToken', data
                        controller.localStorage.set 'username', controller.loginData.username
                        controller.username = controller.loginData.username
                        controller.loginData = {}

                    .fail (data) ->
                        console.log data
                        console.log 'failure'

                logout: ->
                    this.localStorage.remove 'userToken'
                    this.localStorage.remove 'username'
                    this.username = null

        ]
  }
