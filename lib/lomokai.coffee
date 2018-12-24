fs = require 'fs'
path = require 'path'
{CompositeDisposable} = require 'atom'

class Lomokai

  config: require('./lomokai-settings').config

  activate: ->
    @disposables = new CompositeDisposable
    @packageName = require('../package.json').name
    @disposables.add atom.config.observe "#{@packageName}.scheme", => @enableConfigTheme()
    @disposables.add atom.commands.add 'atom-workspace', "#{@packageName}:select-theme", @createSelectListView

  deactivate: ->
    @disposables.dispose()

  enableConfigTheme: ->
    scheme = atom.config.get "#{@packageName}.scheme"
    @enableTheme scheme

  enableTheme: (scheme) ->
    # No need to enable the theme if it is already active.
    return if @isActiveTheme scheme unless @isPreviewConfirmed
    try
      # Write the requested theme to the `syntax-variables` file.
      fs.writeFileSync @getSyntaxVariablesPath(), @getSyntaxVariablesContent(scheme)
      activePackages = atom.packages.getActivePackages()
      if activePackages.length is 0 or @isPreview
        # Reload own stylesheets to apply the requested theme.
        atom.packages.getLoadedPackage("#{@packageName}").reloadStylesheets()
      else
        # Reload the stylesheets of all packages to apply the requested theme.
        activePackage.reloadStylesheets() for activePackage in activePackages
      @activeScheme = scheme
    catch
      # If unsuccessfull enable the default theme.
      @enableDefaultTheme()

  isActiveTheme: (scheme) ->
    scheme is @activeScheme

  getSyntaxVariablesPath: ->
    path.join __dirname, "..", "styles", "syntax-variables.less"

  getSyntaxVariablesContent: (scheme) ->
    """
    @lomokai-scheme: '#{@getNormalizedName scheme}';

    @import 'schemes/@{lomokai-scheme}';
    @import 'syntax-variables-rest';

    """

  getNormalizedName: (name) ->
    "#{name}"
      .replace (/ /g), '-'
      .toLowerCase()

  enableDefaultTheme: ->
    scheme = atom.config.getDefault "#{@packageName}.scheme"
    @setThemeConfig scheme

  setThemeConfig: (scheme) ->
    atom.config.set "#{@packageName}.scheme", scheme

  createSelectListView: =>
    LomokaiSelectListView = require './lomokai-select-list-view'
    lomokaiSelectListView = new LomokaiSelectListView @
    lomokaiSelectListView.attach()

  isConfigTheme: (scheme) ->
    configScheme = atom.config.get "#{@packageName}.scheme"
    scheme is configScheme

module.exports = new Lomokai
