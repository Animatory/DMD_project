'use strict'

const { VueLoaderPlugin } = require('vue-loader')

module.exports = {
  mode: 'development',
  entry: [
    './static/js/app.js'
  ],
  output: {
    path: __dirname + '/static/js/',
    filename: 'main.js',
  },
  module: {
    rules: [
      {
        test: /\.vue$/,
        use: 'vue-loader'
      }
    ]
  },
  plugins: [
    new VueLoaderPlugin()
  ]
}