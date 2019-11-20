module.exports = {
    staging: {
        options: {
            sourceMap: true
        },
        expand : true,
        cwd    : '<%= settings.getLessDir() %>',
        src    : '<%= settings.getLessSrc() %>',
        dest   : '<%= settings.getCssDir() %>',
        ext    : '<%= settings.cssExt %>'
    },
    production: {
        options: {
            compress: true
        },
        expand : true,
        cwd    : '<%= settings.getLessDir() %>',
        src    : '<%= settings.getLessSrc() %>',
        dest   : '<%= settings.getCssDir() %>',
        ext    : '<%= settings.cssExt %>'
    }
};
