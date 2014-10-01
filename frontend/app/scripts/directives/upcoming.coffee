'use strict'

angular.module 'frontendApp'
    .filter 'countdown', ->
        (input) ->
            (countdown input , null,
                countdown.YEARS | countdown.MONTHS | countdown.DAYS).toString()

class UpcomingController
    deleteButtons: {}

    constructor: ($http, $scope, $rootScope) ->
        controller = this
        this.$http = $http
        this.$scope = $scope
        this.$rootScope = $rootScope

        this.$scope.$on '$destroy', ->
            for k,v of controller.deleteButtons
                controller.deleteButtons[k] = false

    associate: (id) ->
        controller = this

        this.$http.post '/api/associate', {'id': id}
            .success (data) ->
                controller.$rootScope.$broadcast 'upcoming.associate'

    disassociate: (id) ->
        controller = this

        this.$http.post '/api/disassociate', {'id': id}
            .success ->
                controller.$rootScope.$broadcast 'upcoming.disassociate'
                controller.deleteButtons[id] = false

    minusButton: ($event, id) ->
        this.deleteButtons[id] = (not ($ $event.currentTarget).hasClass 'active')

angular.module 'frontendApp' 
    .directive 'upcoming', ->
        restrict: 'E'
        templateUrl: 'views/upcoming.html'
        controllerAs: 'upcomingCtrl'
        transclude: true
        controller: [ '$http', '$scope', '$rootScope', UpcomingController ]
