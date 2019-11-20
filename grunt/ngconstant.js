module.exports = {
    // Options for all targets
    options: {
        space: '  ',
        wrap: '"use strict";\n\n {%= __ngModule %}',
        name: 'sample.constants.settings',
        dest: '<%= settings.getJsDir() %>/constants/settings.js'
    },
    // Environment targets
    development: {
        constants: {
            ENV: {
                NAME: 'development',
                API_ENDPOINT: '//api.sample.local',
                HTML_ENDPOINT: 'https://sample.local:8000'
            }
        }
    },
    development_http: {
        constants: {
            ENV: {
                NAME: 'development',
                API_ENDPOINT: '//api.sample.local:8000',
                HTML_ENDPOINT: 'http://sample.local:8000'
            }
        }
    },
    staging: {
        constants: {
            ENV: {
                NAME: 'staging',
                API_ENDPOINT: '//staging-api-u2o82igj.sample.jp',
                HTML_ENDPOINT: 'https://staging.sample.jp'
            }
        }
    },
    production: {
        constants: {
            ENV: {
                NAME: 'production',
                API_ENDPOINT: '//api.sample.jp',
                HTML_ENDPOINT: 'https://sample.jp'
            }
        }
    }
};
