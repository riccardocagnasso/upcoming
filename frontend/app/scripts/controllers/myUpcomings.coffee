'use strict'

###*
 # @ngdoc function
 # @name frontendApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the frontendApp
###
class MyUpcomingsCtrl
    upcomings: []
    constructor: ($http, $rootScope, $scope) ->
        controller = this
        this.$http = $http
        this.$scope = $scope
        this.$rootScope = $rootScope

        unbind = this.$rootScope.$on 'upcoming.associate', ->
            controller.loadUpcomings()
        this.$scope.$on '$destroy', unbind

        unbind = this.$rootScope.$on 'upcoming.disassociate', ->
            controller.loadUpcomings()
        this.$scope.$on '$destroy', unbind

        this.loadUpcomings()

    loadUpcomings: ->
        controller = this

        this.$http.get '/api/myUpcomings'
            .success (data) ->
                controller.upcomings = data.upcomings


angular.module('frontendApp')
    .controller 'MyUpcomingsCtrl', ['$http', '$rootScope',
                                    '$scope', MyUpcomingsCtrl]