import os
from flask import Flask, request, abort, jsonify, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth

def create_app(test_config=None):

    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def get_greeting():
        return jsonify({
            'message': 'Hello'
        })

    @app.route('/actors')
    @requires_auth('get:actors')
    def retrieve_actors(jwt):

        actors = Actor.query.all()
        formated_actors = [actor.format() for actor in actors]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'actors': formated_actors
        })

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
