
from flask import render_template,redirect,request,session,flash
import re
from flask_bcrypt import Bcrypt
from flask_app import app

from flask_app.models.register import User
from flask_app.models.magazine import Magazine

bcrypt = Bcrypt(app)




@app.route('/')
def index():
    return render_template("index.html")

@app.route('/register',methods=['POST'])
def register():
    is_valid = User.validate_user(request.form)
    if not is_valid:
        return redirect("/")

    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password":  bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    if not id:
        flash("Email already taken.","register")
        return redirect('/')
    session['user_id'] = id
    session['first_name']= request.form['first_name']
    return redirect('/user')



    
@app.route("/login",methods=['POST'])
def login():
    data = {
        "email": request.form['email']
    }
    user = User.get_by_email(data)
    if not user:
        flash("Invalid Email/Password","login")
        return redirect("/")
    
    if not bcrypt.check_password_hash(user.password,request.form['password']):
        flash("Invalid Email/Password","login")
        return redirect("/")

    session['user_id'] = user.id
    return redirect('/user')
    
@app.route("/user")
def user():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        "id": session['user_id']
    }
    user = User.get_one(data)
    
    users = User.get_all()

    return render_template("dashboard.html",users=users,user=user,magazines=Magazine.get_everybodys())


@app.route('/user/update/<int:id>', methods=['POSt'])
def update_me(id):
    is_valid_user = User.validate_update_user(request.form)
    if not is_valid_user:
        return redirect('/edit/<int:id>')

    data = {
        'first_name': request.form['first_name'],
        'last_name' : request.form['last_name'],
        'email' : request.form['email']
        
    }
    data= {
        **request.form,
        "id":id
    }

    users=User.update_user(data)
    return redirect("/user")



@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

    