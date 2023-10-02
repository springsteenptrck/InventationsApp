from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.invention import Invention
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/login')

@app.route('/login')
def sign_in():
    return render_template('login_registration.html' )

@app.route('/register', methods=['POST'])
def new_user():
    if not User.valid(request.form):
        return redirect('/login')
    
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password" : pw_hash
    }
    user_id = User.create_user(data)
    session['user_id'] = user_id
    session['first_name'] = request.form['first_name']
    return redirect('/homepage')


@app.route('/login/user', methods=['POST'])
def user_login():
    data = { "email" : request.form["email"] }
    user_in_db = User.get_by_email(data)
    if not user_in_db:
        flash("*Invalid Email/Password", category='login_form_error')
        return redirect("/login")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("*Invalid Email/Password", category='login_form_error')
        return redirect('/login')
    session['user_id'] = user_in_db.id
    session['first_name'] = user_in_db.first_name
    return redirect("/homepage")


@app.route('/homepage')
def home_page():
    if 'user_id' not in session:
        return redirect('/login')
    
    user_id = session['user_id']
    user = User.get_by_id(user_id)
    inventions = Invention.read_all_inventions()

    return render_template('home_page.html', first_name=session['first_name'], user=user, inventions=inventions)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')
