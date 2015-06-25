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
        files: updatePaths({
          "/shared/css/global.css": "/shared/css/_global.scss",
          "/shared-email/style.css": "/shared-email/style.scss"
        })
      }
    },
    /****************************
     * Watch recipes
     ****************************/
    watch: {
      sass: {
        files: [pkgPath('**/*.scss')],
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


/***********************
 * Utilities
 ***********************/
function updatePaths(obj) {
  var d = {}, k;
  for (k in obj) d[pkgPath(k)] = pkgPath(obj[k]);
  return d;
}


function pkgPath(relPath) {
  if (!relPath.indexOf('/') == 0) relPath = '/' + relPath;
  return "../../flaskapp/static" + relPath;
}
