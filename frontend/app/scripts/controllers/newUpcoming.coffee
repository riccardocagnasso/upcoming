'use strict'

class NewUpcomingCtrl
    this.upcomings = []
    this.newUpcoming = {}

    constructor: ($http, $scope) ->
        this.$http = $http
        this.$scope = $scope

    nameChange: ->
        this.searchUpcomings()

    searchUpcomings: ->
        controller = this

        this.$http.get 'http://localhost:6543/api/searchUpcomings'
            .success (data) ->
                console.log data.upcomings
                controller.upcomings = data.upcomings

    associate: (id) ->
        console.log(id)


angular.module('frontendApp')
    .controller 'NewUpcomingCtrl', ['$http', '$scope', NewUpcomingCtrl]