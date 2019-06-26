from flask.ext.assets import Environment, Bundle


BUNDLE_JS = (
    'js/lib/jquery.min.js',
    'js/lib/jquery.chained.remote.min.js',
    'js/lib/ajax_memory_cache.js',
    'js/lib/jquery.formalize.min.js',
    'js/lib/jquery.powertip.min.js',
    'js/main.js',
)

BUNDLE_CSS = (
    'css/jquery.powertip.css',
    'css/formalize.css',
    'css/font-awesome.min.css',
    'css/art17-ui.css',
    'css/header-styles.css',
    'css/art12.css',
)


js = Bundle(*BUNDLE_JS, filters='jsmin', output='gen/static.js')
css = Bundle(*BUNDLE_CSS, filters='cssmin', output='gen/static.css')
assets_env = Environment()
assets_env.register('js', js)
assets_env.register('css', css)
