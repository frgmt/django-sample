module.exports = {
    production: {
        expand : true,
        cwd    : '<%= settings.getJsDir() %>',
        src    : ['**/*.js'],
        dest   : '<%= settings.getJsDir() %>',
        ext    : '<%= settings.jsExt %>'
    },
    vendor_pc: {
        files: {
            '<%= settings.getConcatVendorPcFile() %>': ['<%= settings.getConcatVendorPcFile() %>']
        }
    },
    vendor_sp: {
        files: {
            '<%= settings.getConcatVendorSpFile() %>': ['<%= settings.getConcatVendorSpFile() %>']
        }
    }
};

