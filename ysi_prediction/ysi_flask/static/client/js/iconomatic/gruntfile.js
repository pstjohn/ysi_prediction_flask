module.exports = function(grunt) {

    // Project configuration.
    grunt.initConfig({
        pkg: grunt.file.readJSON('package.json'),

        uglify: {
            options: {
                banner: '/*! \n' +
                        '*  Project: <%= pkg.name %> \n' +
                        '*  Version: <%= pkg.version %> \n' +
                        '*  Description: <%= pkg.description %> \n' +
                        '*  Author: <%= pkg.author %> \n' +
                        '*  Build Date: <%= grunt.template.today("yyyy-mm-dd") %> \n' +
                        '*/ \n '
              , compress: false
              , sourceMap: true
              , preserveComments: 'some' // preserves if it has an bang ! eg /*!
              , mangle: {
                    except: ['N', 'R', 'E', 'L'] // leave these variable names alone ;-)
                }
            },
            dist: {
                src:  'jquery.iconomatic.js',
                dest: 'jquery.iconomatic.min.js'
            }
        }
    });

    grunt.loadNpmTasks('grunt-contrib-uglify');

    // Default task(s).
    grunt.registerTask('default', [ 'uglify']);

};
