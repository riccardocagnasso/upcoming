'use strict'

###*
 # @ngdoc function
 # @name frontendApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the frontendApp
###

class MainController
    constructor: ($scope, $rootScope) ->
        console.log('main init')
        this.$scope = $scope
        this.$rootScope = $rootScope

        unbind = this.$rootScope.$on 'login', ->
            console.log 'login!'

        $scope.$on('$destroy', unbind)


angular.module('frontendApp')
    .controller 'MainCtrl', ['$scope', '$rootScope', MainController]
