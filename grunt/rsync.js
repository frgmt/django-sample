module.exports = {
    ci: {
        options: {
            args      : ["--verbose", "--archive", "--checksum", "--delete"],
            exclude   : ["/js/",       // typescript
                         "/css/",      // less
                         "/vendor/",   // library
                         ".gitkeep"
                        ],
            src :  '<%= settings.getAssetsDir() %>' + '/',
            dest : '<%= settings.getStaticDir() %>'
        }
    },
    production: {
        options: {
            args      : ["--verbose", "--archive", "--checksum", "--delete"],
            exclude   : ["*.ts",       // typescript
                         "*.less",     // less
                         "/vendor/",   // library
                         ".gitkeep"
                        ],
            src :  '<%= settings.getAssetsDir() %>' + '/',
            dest : '<%= settings.getStaticDir() %>'
        }
    }
};
