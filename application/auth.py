# from flask_login import login_user, login_required, logout_user,current_user
import functools
from flask_httpauth import HTTPTokenAuth
from flask import request, flash, current_app as app, make_response
from flask.json import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from .models import User
from . import db
import datetime
from application import socket
import jwt

auth = HTTPTokenAuth(scheme='Bearer')

@auth.verify_token
def verify_token(token):
    data = jwt.decode(token, app.config['SECRET_KEY'], algorithms='HS256')
    try:
        current_user = User.query.get(data['user_id'])
        print(current_user)
        return current_user
    except Exception as e:
        print(e)
        return

# middleware to check authentication for web socket    
def socket_token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        
        if not 'token' in args[0].keys():
            print('emitting unAuthorized event')
            socket.emit('userUnauthorized')
            return
        try:
            token = args[0]['token']
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms='HS256')
            current_user = User.query.get(data['user_id'])
            # check if current_user should be able to make the socket emit event
            return f(current_user, *args, **kwargs)
        except Exception as e:
            print(f'socket token required failing with this - {e}') 
            socket.emit('userUnauthorized')
            return None
    return decorated

# middleware to check authentication for http requests
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        print(f)
        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(' ')[1]
        else:
            return jsonify({'message':'Token is missing'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'],algorithms='HS256')
            currentUser = User.query.get(data['user_id'])
        except Exception as e:
            print(f'socket token required failing with this - {e}')            
            return jsonify({'message':'Token is invalid'}), 401
        
        return f(currentUser, *args, **kwargs)
    return decorated

@app.route('/user')
@token_required
def get_user(user):
    return make_response({'email':user.email, 'name':user.name}, 200)

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
    token = jwt.encode({'user_id':user.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=2)},app.config['SECRET_KEY'])
    return make_response({'message':'logged in successfully!', 'token':token}, 200)


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
    token = jwt.encode({'user_id':new_user.id, 'exp':datetime.datetime.utcnow()+datetime.timedelta(hours=2)},app.config['SECRET_KEY'])
    # code to validate and add user to database goes here
    return make_response({'message':'User registered', 'token':token}, 201)
