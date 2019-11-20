module.exports = {
    css: {
        expand : true,
        cwd    : '<%= settings.getCssDir() %>',
        src    : ['**/*.css'],
        dest   : '<%= settings.getCssDir() %>',
        ext    : '<%= settings.cssExt %>'
    }
};

