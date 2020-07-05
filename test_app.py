import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movie, Actor

assistant_token = "Bearer {}".format(os.environ.get('ASSISTANT_TOKEN'))
director_token = "Bearer {}".format(os.environ.get('DIRECTOR_TOKEN'))
producer_token = "Bearer {}".format(os.environ.get('PRODUCER_TOKEN'))


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "casting_agency_test"
        self.database_path = "postgresql://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Raghad',
            'age': '22',
            'gender': 'Female'
        }

        self.edit_actor = {
            'name': 'Raghad',
            'age': '24',
            'gender': 'Female'
        }

        self.new_movie = {
            'title': 'Despicable Me',
            'release_date': '2010'
        }

        self.edit_movie = {
            'title': 'Despicable Me',
            'release_date': '2019'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for success behavior
    """

    def test_get_actors(self):
        res = self.client().get(
            '/actors',  headers={'Authorization': assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_movies(self):
        res = self.client().get(
            '/movies',  headers={"Authorization": assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_add_new_actor(self):
        res = self.client().post('/actors', json=self.new_actor,
                                 headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_add_new_movie(self):
        res = self.client().post('/movies', json=self.new_movie,
                                 headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/1',  headers={"Authorization": director_token})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(actor, None)

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/1',  headers={"Authorization": producer_token})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 1).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(movie, None)

    def test_modify_actor(self):
        res = self.client().patch('/actors/12', json=self.edit_actor,
                                  headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])

    def test_modify_movie(self):
        res = self.client().patch('/movies/12', json=self.edit_movie,
                                  headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    '''
    Test for error behavior
    '''

    def test_401_get_actors(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_401_get_movies(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)

    def test_404_delete_actor(self):
        res = self.client().delete(
            '/actors/1000',  headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_404_delete_movie(self):
        res = self.client().delete(
            '/movie/1000',  headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_403_post_actor(self):
        res = self.client().post('/actors',  json=self.new_actor,
                                 headers={"Authorization": assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_403_post_movie(self):
        res = self.client().post('/movies',  json=self.new_movie,
                                 headers={"Authorization": director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_404_patch_actor(self):
        res = self.client().patch('/actor/1000', json=self.edit_actor,
                                  headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')

    def test_404_patch_movie(self):
        res = self.client().patch('/movie/1000',  json=self.edit_movie,
                                  headers={"Authorization": producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'not found')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
