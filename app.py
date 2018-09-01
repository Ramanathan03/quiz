import os
from flask import Flask, render_template,flash, redirect, url_for, session, logging, request
import json
import random

app = Flask(__name__)
app.secret_key = 'some_secret'

with open("data/quiz.json","r") as info:
    data = json.load(info)

#create an login form 
@app.route('/',methods=['GET','POST'] )
def login():
    if request.method == "POST":
        with open("data/reg-detail.txt","r") as fp:  
            valid_users = fp.read().splitlines()
            print(valid_users)
            session['username'] = request.form['username']
            password = request.form['password']
            if session['username'] + ':' + password in valid_users:
                return redirect(url_for("quiz"))
            else:
                return redirect('/register')
                
    return render_template('index.html',
    page_title="Go over |Home")
        


# quiz 
@app.route('/quiz', methods=['GET','POST'])
def quiz():
    session['counter'] = 0# If it's a GET request we start the counter at 0
    session['score'] = 0
    session['turns'] = 0
    if request.method == "POST":
        session['counter'] = int(request.form["current_question_number"])
        session['score'] = int(request.form["current_score"])
        session['turns'] = int(request.form["current_turn"])
        # Overwrite the counter if this is a post request
        print(data[session['counter']]["answer"], request.form["Answer"])
        session['end'] = False
        if session['counter'] == 11 or  session['end']:
            return redirect('/gameover')
        else:
             if data[session['counter']]["answer"].upper() == (request.form["Answer"]).upper():
                 flash('Right!')
                 session['counter'] += 1 
                 session['score'] += 1
                 session['turns'] = 0
                 print(session['turns'])
             elif data[session['counter']]["answer"].upper() != (request.form["Answer"]).upper():
                 session['turns'] += 1
                 flash('Wrong!')
                 print(session['turns'])
             if session['turns'] > 1:
                     flash('last question answer is ' + (data[session['counter']]["answer"]))
                     session['turns'] = 0
                     session['counter'] += 1
    return render_template('quiz.html', 
    data=data,
    i=session['counter'], 
    s=session['score'],
    t = session['turns'],
    page_title="Quiz")

def add_score_on_leaderboard(username, score):
    with open('data/scores.txt', 'a+') as scores:
        high_score = get_score()
        if not (username, score) in  high_score:
         scores.write('{}:{}\n'.format(str(username), str(score)))        

def get_score():
    with open('data/scores.txt', 'r') as top_scores:
        high_score=[]
        for line in top_scores.readlines():
            high_score.append(line)
        sorted_top_players = []
        for player in high_score:
            tupe = (player.split(':')[0].strip(), int(player.split(':')[1].strip()))
            sorted_top_players.append(tupe)

        return sorted(sorted_top_players, key=lambda x: x[1])[::-1][:3]

@app.route('/gameover')
def gameover():
    session['username']
    session['end'] = True
    high_score = get_score()
    add_score_on_leaderboard(session['username'], session['score'])
    return render_template('GG.html',
    page_title="GAME OVER |quiz",
    s=session['score'],
    i=session['counter'], 
    u=session['username'], 
    end=session['end'], 
    high_score=high_score)

#create an register form 
@app.route('/register', methods=['GET','POST'])
def register():
     if request.method =="POST":
                 with open("data/reg-detail.txt","a") as register_Detail:
                     register_Detail.writelines(request.form["username"]+ ":")
                     register_Detail.writelines(request.form["Password"]+ "\n")
                     return redirect('/quiz')
     return render_template('register.html',page_title="Register")


    
app.run(host=os.getenv('IP'),
        port=int(os.getenv('PORT')),
        debug=True)
