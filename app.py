import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



def create_app(test_config=None):

    app = Flask(__name__)
    #setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        greeting = "Hello"
        return greeting


    return app

app = create_app()

if __name__ == '__main__':
    app.run()