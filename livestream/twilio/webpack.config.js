const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: { 
        'sosci/static/js/live/sosci':'./src/sosci/index.js',
        'sosci/static/js/video/videouploader': './src/videouploader/index.js'
      },
  plugins: [new CleanWebpackPlugin(cleanOnceBeforeBuildPatterns: ['sosci/static/js/live', 'sosci/static/js/video']),new HtmlWebpackPlugin({
    inject: false,
    filename: '../livestream/templates/livestream/room.html',
    template: 'src/sosci/room.html',
    chunks: ['sosci']
  }),new HtmlWebpackPlugin({
    inject: false,
    filename: '../../catalogue/templates/catalogue/course_module_form.html',
    template: 'src/videouploader/course_module_form.html',
    chunks: ['videouploader']
  })],
  mode: 'development',
  output: {
    filename: '[name].[contenthash].js',
    libraryTarget: 'umd',
    path: path.resolve('../../'),
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