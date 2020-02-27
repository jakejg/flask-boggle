from boggle import Boggle
from flask import Flask, request, render_template, redirect, flash, session, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

boggle_game = Boggle()
submitted_words = set()



@app.route('/')
def display_board():
    
    highscore = session.get('highscore', 0)
    
    curr_board = boggle_game.make_board()
    session['board'] = curr_board
    return render_template('base.html', board = curr_board, highscore = highscore)

@app.route("/check")
def check_word():
    """Check if word is valid."""

    word = request.args["word"]
    curr_board = session['board']
   
    if checkfor_duplicate(word):
        message = boggle_game.check_valid_word(curr_board, word)
    else:
        message = "Already found that word"
    
    return jsonify({'result': message})

@app.route('/post-score', methods=["POST"])
def post_score():
    score = request.json['score']
    highscore = session.get('highscore', 0)
    if score > highscore:
        highscore = score
        session['highscore'] = highscore
   
    return jsonify({'score': highscore})

def checkfor_duplicate(word):
    
    if word in submitted_words:
        return False
    else:
        submitted_words.add(word)
        return True