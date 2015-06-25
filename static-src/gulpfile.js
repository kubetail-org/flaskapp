var gulp = require('gulp'),
    del = require('del'),
    sass = require('gulp-sass'),
    autoprefixer = require('gulp-autoprefixer'),
    concat = require('gulp-concat'),
    cssmin = require('gulp-cssmin'),
    path = require('path'),
    rev = require('gulp-rev');


var dirName = '../flaskapp/static';


/**
 * Clean static directory
 */
gulp.task('clean', function(callback) {
  del([dirName], {force: true}, callback);
});


/**
 * Compile sass and minify css
 */
gulp.task('css', function() {
  return gulp.src('src/sass/global.scss')
    .pipe(sass())
    .pipe(autoprefixer({
      browsers: ['last 2 versions'],
      cascade: false
    }))
    .pipe(concat('style.min.css'))
    .pipe(cssmin())
    .pipe(gulp.dest(dirName));
});


/**
 * Add revision hashes to static files
 */
gulp.task('rev', ['css'], function() {
  var base = path.join(process.cwd(), dirName);

  var sources = [
    dirName + '/**/*.css',
    dirName + '/**/*.js',
    dirName + '/**/*.ico',
    dirName + '/**/*.png',
    dirName + '/**/*.eot',
    dirName + '/**/*.svg',
    dirName + '/**/*.ttf',
    dirName + '/**/*.woff',
    '!' + dirName + '/email/**'
  ];

  return gulp.src(sources, {base: base})
    .pipe(rev())
    .pipe(gulp.dest(dirName + '/cache'))
    .pipe(rev.manifest())
    .pipe(gulp.dest(dirName));
});


/**
 * Public tasks
 */
gulp.task('build', ['clean'], function() {
  gulp.start('css', 'rev');
});
