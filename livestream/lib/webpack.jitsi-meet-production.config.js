require('dotenv').config()
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: { 
        conference:'./src/jitsimeet/index.js'
      },
  externals: {
    jquery: 'jQuery'
  },      
  plugins: [
   new CleanWebpackPlugin({cleanOnceBeforeBuildPatterns: ['live']}),
   new HtmlWebpackPlugin({
    inject: false,
    filename: '../../../livestream/templates/livestream/jitsi_meet_room.html',
    template: 'src/jitsimeet/jitsi_meet_room.ejs'
  })],
  mode: 'production',
  output: {
    filename: 'live/[name].[contenthash].js',
    libraryTarget: 'umd',
    path: path.resolve('../../sosci/static/js'),
    publicPath: "js"
  },  
module: {
  rules: [
    {
      test: /\.m?js$/,
      exclude: /(node_modules|bower_components)/,
      use: {
        loader: 'babel-loader',
        options: {
          presets: ['@babel/preset-env']
        }
      }
    }
  ]
}  
};