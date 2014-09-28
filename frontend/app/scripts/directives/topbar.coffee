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
      controller:
          class TopBarController
              constructor: ->
                  console.log 'foo123'

              foo: ->
                  console.log 'bar'
  }
