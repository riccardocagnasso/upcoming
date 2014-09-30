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

        this.$http.post 'http://localhost:6543/api/searchUpcomings', {searchquery: this.newUpcoming.name}
            .success (data) ->
                console.log data.upcomings
                controller.upcomings = data.upcomings

    associate: (id) ->
        controller = this

        this.$http.post 'http://localhost:6543/api/associate', {'id': id}
            .success (data) ->
                console.log data
                console.log 'associate'


angular.module('frontendApp')
    .controller 'NewUpcomingCtrl', ['$http', '$scope', NewUpcomingCtrl]