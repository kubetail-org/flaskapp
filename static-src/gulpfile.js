var path = require('path');

var del = require('del'),
    gulp = require('gulp'),
    plugins = require('gulp-load-plugins')(),
    sass = require('gulp-sass')(require('sass'));


var destDir = '../flaskapp/static';




// ============================================================================
// PUBLIC TASKS
// ============================================================================

gulp.task('build', gulp.series(
  clean,
  gulp.parallel(
    buildCss,
    copyVendor
  ),
  buildRev
));




// ============================================================================
// PRIVATE TASKS
// ============================================================================

function clean(done) {
  return del(destDir, {force: true}, done);
}


function buildCss() {
  return gulp.src('src/sass/global.scss')
    .pipe(sass().on('error', sass.logError))
    .pipe(plugins.autoprefixer({
      cascade: false
    }))
    .pipe(plugins.concat('style.css'))
    .pipe(gulp.dest(destDir))
    .pipe(plugins.cssnano({discardComments: {removeAll: true}}))
    .pipe(plugins.rename('style.min.css'))
    .pipe(gulp.dest(destDir));  
}


function copyVendor() {
  return gulp.src('src/vendor/**/*')
    .pipe(gulp.dest(destDir + '/vendor'));
}


function buildRev() {
  var base = path.join(process.cwd(), destDir);

  var sources = [
    destDir + '/**/*.css',
    destDir + '/**/*.js',
    destDir + '/**/*.ico',
    destDir + '/**/*.png',
    destDir + '/**/*.eot',
    destDir + '/**/*.svg',
    destDir + '/**/*.ttf',
    destDir + '/**/*.woff',
    '!' + destDir + '/email/**'
  ];

  return gulp.src(sources, {base: base})
    .pipe(plugins.rev())
    .pipe(gulp.dest(destDir + '/cache'))
    .pipe(plugins.rev.manifest())
    .pipe(gulp.dest(destDir));
}
