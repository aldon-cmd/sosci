const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
var HtmlWebpackPlugin = require('html-webpack-plugin');

module.exports = {
  entry: { 
        sosci:'./src/sosci/index.js',
        videouploader: './src/videouploader/index.js'
      },
  plugins: [new CleanWebpackPlugin(),new HtmlWebpackPlugin()],
  mode: 'development',
  output: {
    filename: '[name].[contenthash].js',
    //library: 'sosci',
    libraryTarget: 'umd',
    path: path.resolve(__dirname, 'dist'),
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