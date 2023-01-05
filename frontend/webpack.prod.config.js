var webpack = require('webpack')
var config = require('./webpack.config.js');

config.mode = "production";

config.optimization = {
  minimize: true
}

module.exports = config
