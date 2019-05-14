const mix = require('laravel-mix');

/*
 |--------------------------------------------------------------------------
 | Mix Asset Management
 |--------------------------------------------------------------------------
 |
 | Mix provides a clean, fluent API for defining some Webpack build steps
 | for your Laravel application. By default, we are compiling the Sass
 | file for the application as well as bundling up all the JS files.
 |
 */

 mix
    /* CSS */
    .sass('resources/assets/sass/main.scss', 'public/css/oneui.css')
    .sass('resources/assets/sass/oneui/themes/amethyst.scss', 'public/css/themes/')
    .sass('resources/assets/sass/oneui/themes/city.scss', 'public/css/themes/')
    .sass('resources/assets/sass/oneui/themes/flat.scss', 'public/css/themes/')
    .sass('resources/assets/sass/oneui/themes/modern.scss', 'public/css/themes/')
    .sass('resources/assets/sass/oneui/themes/smooth.scss', 'public/css/themes/')

    /* JS */
    .js('resources/assets/js/laravel/app.js', 'public/js/laravel.app.js')
    .js('resources/assets/js/oneui/app.js', 'public/js/oneui.app.js')

    /* Tools */
    .browserSync('localhost:8000')
    .disableNotifications()

    /* Options */
    .options({
        processCssUrls: false
    });
