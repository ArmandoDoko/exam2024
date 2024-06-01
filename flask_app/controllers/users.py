from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.user import User
from flask_app.models.painting import Painting
from flask_bcrypt import Bcrypt        
bcrypt = Bcrypt(app)

@app.route('/')
def controller():
    if 'user_id' not in session:
        return redirect ('/logout')
    return redirect('/dashboard')

# @app.route('/register')
# def registerpage():
#     if 'user_id' in session:
#         return redirect('/')
#     return render_template('register.html')

@app.route('/login')
def loginPage():
    if 'user_id' in session:
        return redirect ('/')
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def loginUser():
    if 'user_id' in session:
        return redirect ('/')
    user = User.get_user_by_email(request.form)
    if not user: 
        flash('This user doesnt exist! Check your email', 'emailLogin')
        return redirect(request.referrer)
    if not bcrypt.check_password_hash(user['password'], request.form['password']):
        flash('Invalid password!', 'passwordLogin')
        return redirect(request.referrer)
    session['user_id']=user['id']
    return redirect('/')

@app.route('/register', methods = ['POST'])
def registerUser():
    if 'user_id' in session:
        return redirect ('/')
    if not User.validate_user(request.form):
        return redirect (request.referrer)
    user= User.get_user_by_email(request.form)
    if user:
        flash('This user already exists! Try another email.', 'emailRegister')
        return redirect(request.referrer)
    data={
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': bcrypt.generate_password_hash(request.form['password'])
    }
    user_id=User.create(data)
    session['user_id']=user_id
    return redirect('/')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/')
    paintings = Painting.getAllPaintings()
    data={
        'id': session['user_id']
    }
    loggedUser=User.get_user_by_id(data)
    usersWhoPainted=Painting.get_painters(data)
    return render_template('dashboard.html',paintings=paintings, loggedUser=loggedUser, usersWhoPainted=usersWhoPainted)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')