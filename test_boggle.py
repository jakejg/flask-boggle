from unittest import TestCase
from app import app, checkfor_duplicate, submitted_words
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):

    def setUp(self):
        """before every test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

    
        

    def test_home(self):
        with self.client:
            response = self.client.get('/')
            html = response.get_data(as_text=True)
            self.assertIn('board', session)
            self.assertEqual(response.status_code, 200)
            self.assertIn('Time left 60 seconds', html)
            self.assertIn('<h1>Boggle</h1>', html)
    
    def test_duplicates(self):
        checkfor_duplicate("test")
        self.assertEqual(len(submitted_words), 3)
        self.assertFalse(checkfor_duplicate("test"))


    def test_check_word_okay(self):
        with self.client:
            with self.client.session_transaction() as session1:
                session1['board'] = [["D","O", "G", "G", "G"],
                                ["D","O", "G", "G", "G"],
                                ["D","O", "G", "G", "G"],
                                ["D","O", "G", "G", "G"],
                                ["D","O", "G", "G", "G"]]
        response = self.client.get('/check?word=dog')
        self.assertEqual("Okay!", response.json['result'])
            
    def test_check_word_not_on_board(self):
        self.client.get('/')
        response = self.client.get('/check?word=cat')
        self.assertEqual("Not on the Board", response.json['result'])
    
    def test_check_post(self):
        with self.client:
            response = self.client.post('/post-score', json = {'score': 12})
            self.assertIn('highscore', session)

