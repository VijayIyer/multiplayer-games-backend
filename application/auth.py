# from flask_login import login_user, login_required, logout_user,current_user
import functools
from flask_httpauth import HTTPTokenAuth
from flask import request, flash, current_app as app, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

auth = HTTPTokenAuth(scheme='Bearer')
tokens = {
    "secret-token-1": "john",
    "secret-token-2": "susan"
}

@auth.verify_token
def verify_token(token):
    if token in tokens:
        return tokens[token]

def authenticated_only(f):
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        # print(current_user.email)
        if not current_user.is_authenticated:
            # print(f'{current_user} - unauthorized')
            return make_response({'message':'unauthenticated'}, 401)
        else:
            return f(*args, **kwargs)
    return wrapped

@app.route('/login')
def login_get():
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if user.is_authenticated:
        return make_response({'loggedIn':True}, 200)
    return make_response({'loggedIn':False}, 200)

@app.route('/signup')
def signup_get():
    email = request.args.get('email')
    password = request.args.get('password')
    user = User.query.filter_by(email=email).first()
    if user:
        return make_response({'registered':True}, 200)
    return make_response({'registered':False}, 200)

@app.route('/login', methods=['POST'])
def login_post():
    # login code goes here
    email = request.json.get('email')
    password = request.json.get('password')
    remember = True if request.json.get('remember') else False
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        #flash('Please check your login details and try again.')
        return make_response({'message':'Incorrect email or password'}, 401) # if the user doesn't exist or password is wrong, reload the page
    logged_in = login_user(user, remember=remember)
    if logged_in:
        # print('user logged in')
        return make_response({'message':'logged in successfully'}, 200)
    return make_response({'message':'log in failed'}, 401)


@app.route('/signup', methods=['POST'])
def signup_post():
    body = request.json
    email = body['email']
    name = body['name']
    password = body['password']
    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, return 409 unauthorized because user already exists
        return make_response({'message':'Email address already exists'}, 409)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    print('added new user to Users table')
    # code to validate and add user to database goes here
    return make_response({'message':'User registered'}, 201)

@app.route('/logout')
# @login_required
def logout():
    try:
        logout_user()
        return make_response({'message':'logged out successfully!'}, 201)
    except Exception as e:
        return make_response({'message':f'logout failed with exception : {e}'}, 404)