from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.member import Member
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    return render_template("index.html")

@app.route('/create_member', methods=['POST'])
def create_member():
    if not Member.validate_user(request.form):
        return redirect('/')
    data = {
        "fname": request.form["fname"],
        "lname": request.form["lname"],
        "email": request.form["email"],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Member.save(data)
    session['id'] = id
    return redirect('/welcome')

@app.route('/welcome')
def welcome():
    if 'id' not in session:
        return redirect('/logout')
    data ={
        'id': session['id']
    }
    return render_template('welcome.html',member=Member.get_member_id(data))

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/login',methods=['POST'])
def login():
    member = Member.get_member_email(request.form)

    if not member:
        flash("Invalid Email", "Login")
        return redirect('/')
    if not bcrypt.check_password_hash(member.password, request.form['password']):
        flash("Invalid Password", "Login")
        return redirect('/')
    session['id'] = member.id
    return redirect('/welcome')