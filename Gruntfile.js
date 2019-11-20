module.exports = function(grunt) {
    var path = require('path');
    var taskName = grunt.cli.tasks[0];
    var dependencies = ['dependencies'];

    switch(taskName){
        case "staging":
            // break;
        case "deploy":
            break;
        default:
            dependencies.push('devDependencies');
            break;
    }

    require('load-grunt-config')(grunt, {
        data: {
            settings: {
                projectRoot  : path.join(process.cwd(), 'sample'),
                // assets
                getAssetsDir : function(){ return path.join(this.projectRoot, 'assets'); },
                getLessDir   : function(){ return path.join(this.getAssetsDir(), 'css'); },
                getLessSrc   : function(){ return ['**/*.less']; },
                getTypeScriptDir : function(){ return path.join(this.getAssetsDir(),  'js'); },
                getTypeScriptSrc : function(){ return ['**/*.ts']; },
                getImgDir    : function(){ return path.join(this.getAssetsDir(), 'img'); },
                getVendorDir : function(){ return path.join(this.getAssetsDir(), 'vendor'); },
                // static
                getStaticDir : function(){ return path.join(this.projectRoot, 'static'); },
                getCssDir    : function(){ return path.join(this.getStaticDir(), 'css'); },
                cssExt       : '.css',
                getJsDir     : function(){ return path.join(this.getStaticDir(),  'js'); },
                jsExt        : '.js',
                getImgDestDir: function(){ return path.join(this.getStaticDir(), 'img'); },
                getVendorDestDir: function(){ return path.join(this.getStaticDir(), 'vendor'); },
            }
        },
        loadGruntTasks: {
            scope: dependencies
        }
    });
};

