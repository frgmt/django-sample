module.exports = {
  options: {
    livereload: true
  },
  template: {
    files: ['sample/templates/**/*.html'],
    tasks: ['exec:reload']
  },
  less: {
    files: ['sample/assets/css/**/*.less'],
    tasks: ['newer:less:staging']
  },
  typescript: {
    files: ['sample/assets/js/**/*.ts'],
    tasks: ['newer:typescript:staging']
  },
  rsync: {
    files: ['sample/assets/img/**/*',
            'sample/assets/partials/**/*.html',
            'sample/assets/locale/*.json',
            'sample/assets/admin/**/*'
           ],
    tasks: ['rsync:ci']
  },
  exec: {
    files: ['**/*.py', '!sample/sample/__init__.py', '!sample/sample/wsgi*.py'],
    tasks: ['exec:reload']
  }
};

