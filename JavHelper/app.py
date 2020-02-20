# -*- coding:utf-8 -*-
import os
from flask import Flask, render_template, jsonify
from werkzeug.exceptions import HTTPException
from traceback import format_exc, print_exc

from JavHelper.core.ini_file import recreate_ini, DEFAULT_INI
# init setting file
if not os.path.isfile(DEFAULT_INI):
    print('ini file {} doesn\'t exists, recreate one and apply default settings'.format(DEFAULT_INI))
    recreate_ini(DEFAULT_INI)

from JavHelper.cache import cache
from JavHelper.model.jav_manager import JavManagerDB
from JavHelper.views.emby_actress import emby_actress
from JavHelper.views.parse_jav import parse_jav
from JavHelper.views.jav_browser import jav_browser
from JavHelper.views.scan_directory import directory_scan


def create_app():
    # initialize local db
    JavManagerDB()

    # create and configure the app
    app = Flask(__name__, template_folder='templates')
    cache.init_app(app)

    app.register_blueprint(emby_actress)
    app.register_blueprint(parse_jav)
    app.register_blueprint(jav_browser)
    app.register_blueprint(directory_scan)

    app.config['JSON_AS_ASCII'] = False

    # a simple page that says hello
    @app.route('/')
    def hello():
        return render_template('home.html')

    @app.errorhandler(Exception)
    def handle_exception(e):
        # pass through HTTP errors
        if isinstance(e, HTTPException):
            return e

        print_exc()
        # now you're handling non-HTTP exceptions only
        return jsonify({'errors': format_exc()}), 500

    return app
