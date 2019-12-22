require('dotenv').config()
const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: { 
        sosci:'./src/sosci/index.js',
        videouploader: './src/videouploader/index.js'
      },
  plugins: [
   new CleanWebpackPlugin({cleanOnceBeforeBuildPatterns: ['video']}),
   new HtmlWebpackPlugin({
    inject: false,
    filename: '../../../livestream/templates/livestream/room.html',
    template: 'src/sosci/room.ejs',
    chunks: ['sosci']
  }),new HtmlWebpackPlugin({
    inject: false,
    filename: '../../../catalogue/templates/catalogue/course_module_form.html',
    template: 'src/videouploader/course_module_form.ejs',
    chunks: ['videouploader']
  })],
  mode: 'development',
  output: {
    filename: 'video/[name].[contenthash].js',
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