module.exports = {
    staging: {
        options: {
            module: 'amd', //or commonjs
            target: 'es5', //or es3
            sourceMap: true
        },
        expand : true,
        cwd    : '<%= settings.getTypeScriptDir() %>',
        src    : '<%= settings.getTypeScriptSrc() %>',
        dest   : '<%= settings.getJsDir() %>',
        ext    : '<%= settings.jsExt %>'
    },
    production: {
        options: {
            module: 'amd', //or commonjs
            target: 'es5', //or es3
            compress: true
        },
        expand : true,
        cwd    : '<%= settings.getTypeScriptDir() %>',
        src    : '<%= settings.getTypeScriptSrc() %>',
        dest   : '<%= settings.getJsDir() %>',
        ext    : '<%= settings.jsExt %>'
    }
};

