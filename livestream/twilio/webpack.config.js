const path = require('path');

module.exports = {
  entry: './sosci_live/src/index.js',
  mode: 'development',
  output: {
    filename: 'sosci.js',
    //library: 'sosci',
    libraryTarget: 'umd',
    path: path.resolve(__dirname, '../../sosci/static/js'),
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