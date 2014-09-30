'use strict'

###*
 # @ngdoc function
 # @name frontendApp.controller:MainCtrl
 # @description
 # # MainCtrl
 # Controller of the frontendApp
###
class MyUpcomingsCtrl
    constructor: ($http, $scope) ->
        this.upcomings = []
        this.deleteButtons = {}

        this.$http = $http
        this.$scope = $scope

        this.loadUpcomings()

    loadUpcomings: ->
        controller = this

        this.$http.get 'http://localhost:6543/api/myUpcomings'
            .success (data) ->
                controller.upcomings = data.upcomings

    minusButton: ($event, id) ->
        this.deleteButtons[id] = (not ($ $event.currentTarget).hasClass 'active') 
        console.log this.deleteButtons

    disassociate: (id) ->
        controller = this

        this.$http.post 'http://localhost:6543/api/disassociate', {'id': id}
            .success ->
                controller.deleteButtons = {}
                controller.loadUpcomings()


angular.module('frontendApp')
    .controller 'MyUpcomingsCtrl', ['$http', '$scope', MyUpcomingsCtrl]