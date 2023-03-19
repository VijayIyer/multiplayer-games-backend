from flask_login import login_user, login_required, logout_user
from flask import request, flash, current_app as app, make_response
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from . import db

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
    print(request.json)
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
        print('user logged in')
        return make_response({'message':'logged in successfully'}, 200)
    return make_response({'message':'log in failed'}, 401)


@app.route('/signup', methods=['POST'])
def signup_post():
    print(request.json)
    body = request.json
    email = body['email']
    name = body['name']
    password = body['password']

    user = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database

    if user: # if a user is found, we want to redirect back to signup page so user can try again
        return make_response({'message':'Email address already exists'}, 401)

    # create a new user with the form data. Hash the password so the plaintext version isn't saved.
    new_user = User(email=email, name=name, password=generate_password_hash(password, method='sha256'))

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()
    # code to validate and add user to database goes here
    return make_response({'message':'User registered'}, 201)

@app.route('/logout')
@login_required
def logout():
    try:
        logout_user()
        return make_response({'message':'logged out successfully!'}, 201)
    except Exception as e:
        return make_response({'message':f'logout failed with exception : {e}'}, 404)