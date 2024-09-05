/* eslint-disable @typescript-eslint/no-var-requires */
import path from 'path'
import HtmlWebpackPlugin from 'html-webpack-plugin'
import CopyWebpackPlugin from 'copy-webpack-plugin'
import MiniCssExtractPlugin from 'mini-css-extract-plugin'
import CompressionPlugin from 'compression-webpack-plugin'
import CssMinimizerPlugin from 'css-minimizer-webpack-plugin'
import { CleanWebpackPlugin } from 'clean-webpack-plugin'
import ESLintPlugin from 'eslint-webpack-plugin'
import Dotenv from 'dotenv-webpack'
import { BundleAnalyzerPlugin } from 'webpack-bundle-analyzer'
import webpack, { Configuration, WebpackPluginInstance } from 'webpack'

// Importing types for webpack-dev-server
import 'webpack-dev-server'

interface Env {
  analyze?: boolean
}

export default (env: Env, argv: { mode: string }): Configuration => {
  const isProduction = argv.mode === 'production'
  const isAnalyze = Boolean(env?.analyze)

  const config: Configuration = {
    resolve: {
      extensions: ['.tsx', '.ts', '.jsx', '.js', '.cjs']
    },
    entry: ['./src/index.tsx'],
    module: {
      rules: [
        {
          test: /\.tsx?$/,
          exclude: /node_modules/,
          use: ['babel-loader']
        },
        {
          test: /\.(s[ac]ss|css)$/,
          use: [
            MiniCssExtractPlugin.loader,
            {
              loader: 'css-loader',
              options: { sourceMap: !isProduction }
            },
            {
              loader: 'sass-loader',
              options: { sourceMap: !isProduction }
            }
          ]
        },
        {
          test: /\.(png|svg|jpg|gif)$/,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: isProduction ? 'static/media/[name].[contenthash:6].[ext]' : '[path][name].[ext]'
              }
            }
          ]
        },
        {
          test: /\.(eot|ttf|woff|woff2)$/,
          use: [
            {
              loader: 'file-loader',
              options: {
                name: isProduction ? 'static/fonts/[name].[ext]' : '[path][name].[ext]'
              }
            }
          ]
        },
        {
          test: /\.html$/,
          use: 'html-loader'
        }
      ]
    },
    output: {
      filename: 'static/js/main.[contenthash:6].js',
      path: path.resolve(__dirname, 'dist'),
      publicPath: '/'
    },
    // Correctly typed devServer configuration
    devServer: {
      hot: true,
      port: 3000,
      historyApiFallback: true,
      static: {
        directory: path.resolve(__dirname, 'public'),
        serveIndex: true,
        watch: true
      }
    },
    devtool: isProduction ? false : 'source-map',
    plugins: [
      new MiniCssExtractPlugin({
        filename: isProduction ? 'static/css/[name].[contenthash:6].css' : '[name].css'
      }),
      new Dotenv(),
      new CopyWebpackPlugin({
        patterns: [
          {
            from: 'public',
            to: '.',
            filter: (name) => !name.endsWith('index.html')
          }
        ]
      }),
      new HtmlWebpackPlugin({
        template: path.resolve(__dirname, 'public', 'index.html'),
        filename: 'index.html'
      }),
      new ESLintPlugin({
        extensions: ['.tsx', '.ts', '.js', '.jsx']
      })
    ] as WebpackPluginInstance[]
  }

  if (isProduction) {
    config.plugins?.push(
      new webpack.ProgressPlugin(),
      new CompressionPlugin({
        test: /\.(css|js)$/,
        algorithm: 'brotliCompress'
      }),
      new CleanWebpackPlugin()
    )

    if (isAnalyze) {
      config.plugins?.push(new BundleAnalyzerPlugin())
    }

    config.optimization = {
      minimizer: ['...', new CssMinimizerPlugin()]
    }
  }

  return config
}
