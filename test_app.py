import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Actors, Movies

DB_HOST = os.getenv('DB_HOST', 'localhost:5432')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', '123')
DB_NAME = os.getenv('DB_NAME', 'Agency')
database_path = 'postgresql://{}:{}@{}/{}'.format(DB_USER, DB_PASSWORD, DB_HOST, DB_NAME)


new_movie = {
    'title': 'Sonic: The Hedgehog',
    'genre': 'Fantasy',
    'release_date': '2018.01.05'
}

new_actor = {
    'name': 'Jim Carrey',
    'age': '41',
    'role': 'Anime',
    'gender': 'Male'
}


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        self.assistance_token = 'Bearer' + str(os.getenv('assistant'))
        self.director_token = 'Bearer' + str(os.getenv('director'))
        self.producer_token = 'Bearer' + str(os.getenv('producer'))

        self.assistant = {'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdZSGRURUc0N0M1bEtES01zX0JlYSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWVsYmVrLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjkxZDMxOTc5Y2VjYTAwNzVmNGFhMDYiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjAzNjA2NTAwLCJleHAiOjE2MDM2OTI5MDAsImF6cCI6ImowUU55WnpQVzlDVm42NzhWSVZFQnlZR0dlN0RUaE9xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.f5DK7ty5abd_YswjVI2Qalo7QsnVKOdxRZ7PJAieXfGCEDC7wrwMSYW9cZEn36BbOfggHNaGC_4WU-vS5N0IL8IRjDjwLydVk0lm-EL-l-wfwATW9U5KfSrgX9d2Bjc39wFT4uIft1CW_4IjU8g1VulBm71xStzD2rm4Q7fpRtEHGWwrtIidX40o5WqY5mLyrUIEP9ysx4g1AvxDURAz5ZQZVaPUXYjY4ROb4e2CjBYMybhZdS2PccPpXj9kNSDLFeMJyNDNtkvHzBI1xIO6bODbasVg7-lPozjB99XGJ1XVCb09DLK2Mahnoodb8TIzF4BdMQBlcRBRw6BHQQqsqg'}
        self.director = {'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdZSGRURUc0N0M1bEtES01zX0JlYSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWVsYmVrLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1Zjk1MTlhNTVkZGE2NTAwNzdiZTJiNmEiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjAzNjA3MDMzLCJleHAiOjE2MDM2OTM0MzMsImF6cCI6ImowUU55WnpQVzlDVm42NzhWSVZFQnlZR0dlN0RUaE9xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.jU5E8K3xLXwn5pXVTr8tsnnRtdIdcBK80Ue1b4gki2fWdh1Bkk5sfHpQ2SJ3QqaZ2BurDHAuksge0Fxb8gheqg-HugfZf3jZmZvz-2JpVEBBJhw4Xr834kZNfc1p5iLiVnpDXWyuCwHiGdYKTmdhobfvlnSeLfhiC27TbFvXPHlR0kLQeKeV79tQTAo9FwedyvgRQUUqKqQ9Y_lbTZEOQ1VQC_9eauSZjfjyoNYAcKa-BstfnTwfr_U4tq3d9Tsu8wStSkzODpELesAcFtSs7pJXwsNT9xugYGAv0ZX_Aof3Oh48hMivPXFU57uSTqYEicSJ1kWkwUQ2dMlTgTMAMA'}
        self.producer = {'Authorization': 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImdZSGRURUc0N0M1bEtES01zX0JlYSJ9.eyJpc3MiOiJodHRwczovL2NhcHN0b25lLWVsYmVrLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZjkxYjk5YmM1ZjExZDAwNmVkZjY0Y2QiLCJhdWQiOiJjYXN0aW5nIiwiaWF0IjoxNjAzNjA1NzE0LCJleHAiOjE2MDM2OTIxMTQsImF6cCI6ImowUU55WnpQVzlDVm42NzhWSVZFQnlZR0dlN0RUaE9xIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.wSo0sjh1lj4TbbItCV5Z0PhattDft0vgpplndtKQFPBPEtl3EooeDFheLx_MqJLdXNI-U9ueHc_2N7vx1cft_taACrCsPpvRcwR0WQ4_3KvFczDPMAsuGP4n5-Wox5XReSTdOPKqOlM0b3lt456pLkXTtIvZW8bmC3fENirZtCKB7h06-u7LqMJEfnKVhO6-G9La21-Q3PEhsRd18T54DNKBzfB9Le7DyWGDAbHZeRc8Ax3uzZJ5NsIEab9sUwG3wCPhFb_McbCtjclvlsfXcgbvCuKDrYJytNuTn4ryVvBHHu4HC334ur3AHPdfyjUbg5JEaOCKsvoSIkAioOxtoQ'
}
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()


    def tearDown(self):
        pass

    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['len_movies'])

    def test_movies_by_using_id(self):
        res = self.client().get('/movies/2', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_post_movies(self):
        res = self.client().get('/movies', json=new_movie, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Movie is successfully created')

    def test_post_movies_invalid(self):
        new_movie_error = {
            'title': 'Birds of prey',
            'release_date': '2020.07.26'
        }
        res = self.client().post('/movies', json=new_movie_error, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_delete_movie_by_id(self):
        res = self.client().delete('/movies/5', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Movie is successfully deleted')

    def test_invalid_delete_movies(self):
        res = self.client().delete('/movies/me', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search_movie(self):
        search_item = {'searchTerm': 'a'}
        res = self.client().post('/movies/search', json=search_item, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
        self.assertTrue(data['len_movies'])

    def test_search_movie_invalid(self):
        new_search = {'searchTerm': ''}
        res = self.client().post('/movies/search', json=new_search, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_patch_movie(self):
        patch_title = {'title': 'Mr.Smith'}
        res = self.client().patch('/movies/4', json=patch_title, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Movie Successfully updated!')

    def test_patch_movie_invalid(self):
        patch_title = {'err_title': 'Hello'}
        res = self.client().patch('/movies/4', json=patch_title, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['len_actors'])

    def test_actors_by_using_id(self):
        res = self.client().get('/actors/2', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_actors(self):
        res = self.client().get('/actors', json=new_actor, headers=self.director)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actor is successfully created')

    def test_post_actors_invalid(self):
        new_actor_error = {
            'name': 'Jim Carrey',
            'age': '34'
        }
        res = self.client().post('/actors', json=new_actor_error, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

    def test_delete_actor_by_id(self):
        res = self.client().delete('/actors/3', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actors is successfully deleted')

    def test_invalid_delete_actors(self):
        res = self.client().delete('/actors/me', headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    def test_search_actor(self):
        search_item = {'searchTerm': 'a'}
        res = self.client().post('/actors/search', json=search_item, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(data['len_actors'])

    def test_search_actor_invalid(self):
        new_search = {'searchTerm': ''}
        res = self.client().post('/actors/search', json=new_search, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Not Found")

    def test_patch_actor(self):
        patch_title = {'name': 'Mr.Smith'}
        res = self.client().patch('/actors/1', json=patch_title, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['message'], 'The Actor Successfully updated!')

    def test_patch_actor_invalid(self):
        patch_title = {'err_name': 'Hello'}
        res = self.client().patch('/actors/1', json=patch_title, headers=self.producer)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unprocessable Request")

if __name__ == "__main__":
    unittest.main()