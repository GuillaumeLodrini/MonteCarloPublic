// Webpack uses this to work with directories
const path = require('path');
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const BundleTracker = require('webpack-bundle-tracker');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');

var __destinationdirname = '../static/bundles/';

var config = {
    entry: {
        main: './style/main.js',

        // These are all the available vendors in the vendors folder. Load what you use only to generate a lightweight file!
        vendors: [
            './vendors/js/jquery.min.js',
            //'./vendors/js/fresco.js',
            //'./vendors/js/remodal.js',
            //'./vendors/js/slick.min.js',
            //'./vendors/js/select2.min.js',
            //'./vendors/css/fresco.css',
            //'./vendors/css/remodal/remodal.css',
            //'./vendors/css/remodal/remodal-default-theme.css',
            //'./vendors/css/slick.css',
            //'./vendors/css/select2.min.css',
        ],

        main_script : './js/main_script.js',
        cms_edit: './js/cms_edit.js'
    },
    output: {
        path: path.resolve(__destinationdirname),
        filename: '[name]-[hash].js'
    },
    externals: {
        jquery: 'jQuery'
    },
    mode: 'development',
    module: {
        rules: [
            {
                test: /\.js$/,
                exclude: /(node_modules)/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-env']
                    }
                }
            },
            {
                // Apply rule for .sass, .scss or .css files
                test: /\.(sa|sc|c)ss$/,

                // Set loaders to transform files.
                // Loaders are applying from right to left(!)
                // The first loader will be applied after others
                use: [
                    {
                        // After all CSS loaders we use plugin to do his work.
                        // It gets all transformed CSS and extracts it into separate
                        // single bundled file
                        loader: MiniCssExtractPlugin.loader
                    },
                    {
                        // This loader resolves url() and @imports inside CSS
                        loader: "css-loader",
                    },
                    {
                        // Then we apply postCSS fixes like autoprefixer and minifying
                        loader: "postcss-loader"
                    },
                    {
                        // First we transform SASS to standard CSS
                        loader: "sass-loader",
                        options: {
                            implementation: require("sass")
                        }
                    }
                ]
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/,
                type: 'asset/resource',
                exclude: /node_modules/
            },
            {
                test: /jquery.+\.js$/,
                use: [{
                    loader: 'expose-loader',
                    options: {
                      exposes: ['$', 'jQuery'],
                    },
                }]
            }
        ]
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: "[name]-[contenthash].css"
        }),
        new BundleTracker({
            filename: "./webpack-stats.json"
        })
    ]
}

module.exports = config
