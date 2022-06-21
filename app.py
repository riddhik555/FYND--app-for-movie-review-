from flask import Flask,flash, request,redirect,render_template, url_for , session ,g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.functions import func
from datetime import datetime , date
from dateutil.parser import parse
import os
# import pandas as pd 
# import sqlalchemy
# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker, relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///movie.db'
app.secret_key=os.urandom(24)
db = SQLAlchemy(app)


class Movie(db.Model):
    __tablename__ = 'Movie'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(50),nullable=False)
    director = db.Column(db.String(50),nullable=False)
    imdb=db.Column(db.Float)
    popularity=db.Column(db.Float)
    genre=db.Column(db.String(100))
    image = db.Column(db.Text, unique=True)
    cast = db.Column(db.Text)
    age_restriction = db.Column(db.Integer)
    release_date = db.Column(db.Date, index=True)
    description = db.Column(db.Text)

    def __init__(self,name, director, imdb, popularity, genre, image ,cast, age_restriction, release_date, description):
        self.name=name
        self.director=director
        self.imdb=imdb
        self.popularity=popularity
        self.genre=genre
        self.image=image
        self.cast=cast
        self.age_restriction=age_restriction
        self.release_date=release_date
        self.description=description
        
    def __repr__(self):
        return '<Movie %r>' %self.id

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(50),nullable=False, unique=False)
    password = db.Column(db.String(255), nullable=False, server_default='')
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    email = db.Column(db.String(225))

    def __init__(self,username,password,firstname, lastname , email):
        self.username=username
        self.password=password
        self.firstname=firstname
        self.lastname=lastname
        self.email=email

    def __repr__(self):
        return '<Users %r>' %self.username   

@app.route('/login', methods=["POST", "GET"])
def login():
    error=None
    if request.method == 'POST':
        session.pop('user' , None)
        username=request.form['username']
        password=request.form['password']
        user= Users.query.filter(username==Users.username, password==Users.password).first()
        if user:
            session['user']=username
            if username=='admin':
                return redirect(url_for('adminhome') )
            else:
                return redirect(url_for('home')  )
        else :
            error="Invalid User"
            return render_template('login.html' , error = error)
    else:
        return render_template('login.html')

@app.route('/register', methods=["POST", "GET"])
def register():
    if request.method =='GET':
        return render_template('register.html')
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        new_user=Users(username, password ,firstname, lastname, email)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/')
    
@app.route('/dropsession')
def dropsession():
    session.pop('user' , None)
    return render_template('login.html')

@app.before_request
def before_request():
    try:
        g.user=None
        if 'user' in session:
            g.user=session['user']
    except (TypeError):
        pass
            
    
    

@app.route('/', methods=["GET"]) 
def index():
        return render_template('login.html')

@app.route('/adminhome', methods=["GET"]) 
def adminhome():
    if g.user:
        movies=Movie.query.all()
        return render_template('index.html', movies=movies , show_hidden=True , user=session['user'])
    else:
        return redirect(url_for('index'))

@app.route('/home', methods=["GET"]) 
def home():
    if g.user:
        movies=Movie.query.all()
        return render_template('index.html', movies=movies ,user=session['user'], show_hidden=False)
    else:
        return redirect(url_for('index'))


@app.route('/<id>')
def single_review(id):
    movie=Movie.query.get(id)
    try:
        if session['user']=='admin':
            show_hidden=True
        else:
            show_hidden=False
        return render_template('single.html', movie=movie , user=session['user'], show_hidden=show_hidden)
    except:
         error="EERROORR"

@app.route('/new', methods=['GET', 'POST'])
def new_review():
    error=None
    if g.user:
        if request.method == 'GET':
            return render_template('form.html', user=session['user'], new=True)
        if request.method == 'POST':
            name = request.form['name']
            director = request.form['director']
            imdb = request.form['imdb']
            popularity = request.form['popularity']
            genre = request.form['genre']
            image = request.form['image']
            cast = request.form['cast']
            age = request.form['age']
            release_date = request.form['date']
            if len(release_date)!=0:
                date = parse(release_date)
            else:
                date=None
            description = request.form['description']
            new_review=Movie(name, director, imdb, popularity, genre, image, cast, age, date , description)
            try:
                db.session.add(new_review)
                db.session.commit()
                return redirect('/adminhome')
            except:
                error = "Database Error"
    else:
        return redirect(url_for('index'))

@app.route('/edit/<id>', methods=['GET', 'POST'])
def edit_review(id):
    if g.user:
        review = Movie.query.get(id)
        if request.method == 'GET':
            return render_template(
                'form.html',
                user=session['user'],
                new=False,
                id=review.id,
                name=review.name,
                director=review.director,
                imdb=review.imdb,
                popularity=review.popularity,
                genre=review.genre,
                image=review.image,
                cast= review.cast,
                age = review.age_restriction,
                date = review.release_date,
                description = review.description

            )
        if request.method == 'POST':
            review.id=id
            review.name = request.form['name']
            review.director = request.form['director']
            review.imdb = request.form['imdb']
            review.popularity = request.form['popularity']
            review.genre = request.form['genre']
            review.image = request.form['image']
            review.cast = request.form['cast']
            review.age_restriction = request.form['age']
            review.release_date = parse(request.form['date'])
            
            review.description = request.form['description']
            db.session.commit()
            return redirect('/adminhome')
            
    else:
        return redirect(url_for('index'))

@app.route('/delete/<id>', methods=['POST', 'GET'])
def delete_review(id):
    if g.user:
        error=None
        review=Movie.query.get(id)
        try:
            db.session.delete(review)
            db.session.commit()
            return redirect("/adminhome")
        except:
            error= "Database Error"
    else:
        return redirect(url_for('index'))

if __name__ == "__main__":
    app.run(debug=True)