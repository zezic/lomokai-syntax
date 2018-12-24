clutThemes = require('./clut-themes.json')
monokaiThemes = require('./monokai-themes.json')

settings =
  config:
    scheme:
      type: 'string'
      default: 'Classic'
      enum: [
      ]

settings.config.scheme.enum.push clutThemes...
settings.config.scheme.enum.push monokaiThemes...
settings.config.scheme.enum.sort()

module.exports = settings
