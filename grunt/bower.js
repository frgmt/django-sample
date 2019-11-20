module.exports = {
    development: {
        options:{
            targetDir: '<%= settings.getVendorDestDir() %>',
            install: true,
            verbose: true,
            cleanTargetDir: true,
            cleanBowerDir: false,
            layout: function (type, component) {
                if (type === 'css') {
                    return 'css';
                } else if (type === 'css/images') {
                    return 'css/images';
                } else if (type === 'img') {
                    return 'img';
                } else if (type === 'fonts') {
                    return 'fonts';
                } else if (type === 'locales') {
                    return 'locales';
                } else {
                    return 'js';
                }
            }
        }
    },
    production: {
        options:{
            targetDir: '<%= settings.getVendorDestDir() %>',
            install: true,
            verbose: true,          
            cleanTargetDir: true,
            cleanBowerDir: false,
            bowerOptions: {            
                production: true
            },
            layout: function (type, component) {
                if (type === 'css') {
                    return 'css';
                } else if (type === 'css/images') {
                    return 'css/images';
                } else if (type === 'img') {
                    return 'img';
                } else if (type === 'fonts') {
                    return 'fonts';
                } else if (type === 'locales') {
                    return 'locales';
                } else {
                    return 'js';
                }
            }
        }
    }
};

