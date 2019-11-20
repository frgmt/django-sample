module.exports = {
    reload: {
        cwd: 'sample/sample',
        command: 'touch __init__.py wsgi_vagrant.py wsgi_localhost.py'
    },
    collectstatic_local: {
        cwd: 'sample',
        command: 'python3 manage.py collectstatic --noinput -i admin --settings=sample.settings.localhost_http'
    },
    clean_static: {
        cwd: 'sample/static',
        command: 'rm -R *'
    }
};
