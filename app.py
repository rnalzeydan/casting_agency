import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS



def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  CORS(app)

  return app

APP = create_app()

@APP.route('/')
def index():
    return jsonify({
            'message': 'Hello'
        })



if __name__ == '__main__':
    APP.run()
