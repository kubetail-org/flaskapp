module.exports = function(grunt) {
  grunt.initConfig({
    /****************************
     * Compile SASS files
     ****************************/
    sass: {
      target1: {
        options: {
          style: "compressed"
        },
        files: {
          "webapp/static/shared/css/global.css": "webapp/static/shared/css" +
            "/_global.scss",
          "webapp/static/shared-email/style.css": "webapp/static" +
            "/shared-email/style.scss",
        }
      }
    },
    /****************************
     * Watch recipes
     ****************************/
    watch: {
      sass: {
        files: ['**/*.scss'],
        tasks: ['sass']
      }
    }
  });

  grunt.loadNpmTasks('grunt-contrib-sass');
  grunt.loadNpmTasks('grunt-contrib-watch');

  grunt.registerTask('default', ['build']);
  grunt.registerTask('build', [
    'sass'
  ]);
}
