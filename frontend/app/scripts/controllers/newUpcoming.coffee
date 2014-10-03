'use strict'

class NewUpcomingCtrl
    this.upcomings = []
    this.newUpcoming = {}

    constructor: ($http, $rootScope, $scope) ->
        controller = this
        this.$http = $http
        this.$scope = $scope
        this.$rootScope = $rootScope

        unbind = this.$rootScope.$on 'upcoming.associate', ->
            controller.searchUpcomings()
        this.$scope.$on('$destroy', unbind)
        unbind = this.$rootScope.$on 'upcoming.disassociate', ->
            controller.searchUpcomings()
        this.$scope.$on('$destroy', unbind)

        ($ '.input-group.date').datepicker
            format: "yyyy-mm-dd"

        $ '.tagsinput'
            .tagsinput()

    nameChange: ->
        this.searchUpcomings()

    searchUpcomings: ->
        controller = this

        this.$http.post '/api/searchUpcomings', {searchquery: this.newUpcoming.name}
            .success (data) ->
                controller.upcomings = data.upcomings

    createUpcoming: ->
        controller = this

        console.log newForm.$valid

        this.$http.post '/api/createUpcoming', this.newUpcoming
            .success (data) ->
                controller.searchUpcomings()
                controller.newUpcoming = {}


angular.module('frontendApp')
    .controller 'NewUpcomingCtrl', ['$http', '$rootScope',
                                    '$scope', NewUpcomingCtrl]
