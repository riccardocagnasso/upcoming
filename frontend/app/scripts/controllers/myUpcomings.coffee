'use strict'

###*
 # @ngdoc function
 # @name frontendApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the frontendApp
###
class MyUpcomingsCtrl
    this.upcomings = []

    constructor: ($http, $scope) ->
        this.$http = $http
        this.$scope = $scope

        this.loadUpcomings()

    loadUpcomings: ->
        controller = this

        this.$http.get 'http://localhost:6543/api/upcomings'
            .success (data) ->
                controller.upcomings = data.upcomings

angular.module('frontendApp')
    .controller 'MyUpcomingsCtrl', ['$http', '$scope', MyUpcomingsCtrl]