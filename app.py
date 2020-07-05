import os
from flask import Flask, request, abort, jsonify
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
            'message': 'Welcome on Casting Agency Project'
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

    @app.route('/movies')
    @requires_auth('get:movies')
    def retrieve_movies(jwt):

        movies = Movie.query.all()
        formated_movies = [movie.format() for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            'success': True,
            'movies': formated_movies
        })

    '''
    DELETE Method
    '''
    @app.route('/actors/<int:id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):

        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        try:
            actor.delete()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):

        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        try:
            movie.delete()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except Exception:
            abort(422)

    '''
    POST Method
    '''

    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(jwt):

        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            actor = Actor(name=new_name, age=new_age, gender=new_gender)
            actor.insert()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except Exception:
            abort(422)

    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(jwt):

        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            movie = Movie(title=new_title, release_date=new_release_date)
            movie.insert()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except Exception:
            abort(422)

    '''
    PATCH Method
    '''

    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def update_actor(jwt, id):

        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        if actor is None:
            abort(404)

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)

        try:
            if new_name is not None:
                actor.name = new_name
            if new_age is not None:
                actor.age = new_age
            if new_gender is not None:
                actor.gender = new_gender

            actor.update()

            return jsonify({
                'success': True,
                'actor': actor.format()
            })

        except Exception:
            abort(422)

    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def update_movie(jwt, id):

        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        if movie is None:
            abort(404)

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)

        try:
            if new_title is not None:
                movie.title = new_title
            if new_release_date is not None:
                movie.release_date = new_release_date

            movie.update()

            return jsonify({
                'success': True,
                'movie': movie.format()
            })

        except Exception:
            abort(422)

    '''
    Error Handling
    '''

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

    @app.errorhandler(403)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "forbidden"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(500)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 500,
            "message": "internal server error"
        }), 500

    @app.errorhandler(AuthError)
    def authentification_failed(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run()
