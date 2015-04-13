describe 'Directives:', ->

  beforeEach ->
    # initialize our angular app
    module 'app'

  describe 'Action directive', ->

    $rootScope = null
    $compile = null

    beforeEach inject((_$rootScope_, _$compile_) ->
      $rootScope = _$rootScope_.$new()
      $compile = _$compile_
    )

    it 'should show the correct message', ->

      # TODO: directives should not depend on root scope
      #       hack it in until we clean that up
      $rootScope.flow = getJSONFixture('favorites.json')
      scope = $rootScope.$new()
      scope.$root = $rootScope

      # pick our first action to build some html for
      scope.action = $rootScope.flow.action_sets[0].actions[0]

      # our action translation hasn't been inspected yet
      expect(scope.action._missingTranslation).toBeUndefined()

      # create an element for our directive and compile it
      ele = angular.element("<div action='action'>[[action.msg]]</div>")
      $compile(ele)(scope)
      scope.$digest()

      # now our translation has been inspected, confirm its not missing
      expect(scope.action._missingTranslation).toBe(false)
      expect(ele.html()).toBe('What is your favorite color?')
