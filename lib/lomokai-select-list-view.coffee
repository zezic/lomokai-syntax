{SelectListView} = require 'atom-space-pen-views'

class LomokaiSelectListView extends SelectListView

  initialize: (@lomokai) ->
    super
    @list.addClass 'mark-active'
    @setItems @getThemes()

  viewForItem: (theme) ->
    element = document.createElement 'li'
    if @lomokai.isConfigTheme theme.scheme
      element.classList.add 'active'
    element.textContent = theme.name
    element

  getFilterKey: ->
    'name'

  selectItemView: (view) ->
    super
    theme = @getSelectedItem()
    @lomokai.isPreview = true
    @lomokai.enableTheme theme.scheme if @attached

  confirmed: (theme) ->
    @confirming = true
    @lomokai.isPreview = false
    @lomokai.isPreviewConfirmed = true
    @lomokai.setThemeConfig theme.scheme
    @cancel()
    @confirming = false

  cancel: ->
    super
    @lomokai.enableConfigTheme() unless @confirming
    @lomokai.isPreview = false
    @lomokai.isPreviewConfirmed = false

  cancelled: ->
    @panel?.destroy()

  attach: ->
    @panel ?= atom.workspace.addModalPanel(item: this)
    @selectItemView @list.find 'li:last'
    @selectItemView @list.find '.active'
    @focusFilterEditor()
    @attached = true

  getThemes: ->
    schemes = atom.config.getSchema("#{@lomokai.packageName}.scheme").enum
    themes = []
    schemes.forEach (scheme) ->
      themes.push scheme: scheme, name: scheme
    themes

module.exports = LomokaiSelectListView
