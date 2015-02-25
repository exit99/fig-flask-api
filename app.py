import json
import os
import jinja2
from flask import Flask

from config import BaseConfig, DevConfig, ProdConfig


def create_app():
    config = os.getenv('CONFIG', 'Dev')
    app_name = BaseConfig.PROJECT

    app = Flask(app_name)
    configure_app(app, config=config)
    configure_jinja2(app)
    register_blueprints(app)

    return app


def configure_app(app, config=None):
    configs = {
        'dev': DevConfig,
        'prod': ProdConfig,
        'base': BaseConfig,
    }
    app.config.from_object(configs[config])


def configure_jinja2(app):
    _js_escapes = {
        '\\': '\\u005C',
        '\'': '\\u0027',
        '"': '\\u0022',
        '>': '\\u003E',
        '<': '\\u003C',
        '&': '\\u0026',
        '=': '\\u003D',
        '-': '\\u002D',
        ';': '\\u003B',
        u'\u2028': '\\u2028',
        u'\u2029': '\\u2029'
    }
    # Escape every ASCII character with a value less than 32.
    _js_escapes.update(('%c' % z, '\\u%04X' % z) for z in xrange(32))

    @app.template_filter
    def escapejs(value):
        retval = []
        for letter in value:
            if letter in _js_escapes:
                retval.append(_js_escapes[letter])
            else:
                retval.append(letter)

        return jinja2.Markup("".join(retval))

    @app.template_test('False')
    def false(value):
        return value is False

    @app.template_test('True')
    def true(value):
        return value is True

    @app.template_filter('json')
    def to_json(value):
        return jinja2.Markup(json.dumps(value))


def register_blueprints(app):
    from api.views import api
    app.register_blueprint(api)


if __name__ == '__main__':
    app = create_app()
    host = os.environ.get('HOST', '127.0.0.1')
    port = int(os.environ.get('PORT', 5000))
    app.run(host=host, port=port, debug=app.config["DEBUG"])
