from flask_app import app
from flask import render_template,redirect,request,session,flash

from flask_bcrypt import Bcrypt
from flask_app import app

from flask_app.models.register import User
from flask_app.models.magazine import Magazine

bcrypt = Bcrypt(app)




@app.route('/add')
def page_add():
    return render_template('add.html',users=User.get_all())

@app.route('/page/add', methods=["POST"])
def create_pages():
    is_valid_page = Magazine.validate_page(request.form)
    if not is_valid_page:
        return redirect('/add')

    data = {
        'title': request.form['title'],
        'description' : request.form['description'],
        'user_id': session['user_id']
    }
    
    Magazine.save_page(data)
    return redirect("/user")


@app.route('/edit/<int:id>')
def edit(id):
    
    data ={ 
        **request.form,
        "id":id
    }
    return render_template("update.html",user=User.get_one(data),magazine=Magazine.get_one(data),magazines=Magazine.get_mine(data))


@app.route('/page/update/<int:id>', methods=['POSt'])
def update_page(id):
    data= {
        **request.form,
        "id":id
    }
    magazines=Magazine.update(data)
    return redirect("/user_page")


@app.route('/show/<int:id>')
def show(id):
    data ={ 
        "id":id
    } 
    # magazine=Magazine.get_them(data)
    
    return render_template("theirs.html",user=User.get_one(data),magazines=Magazine.get_mine(data))



@app.route('/destroy/<int:id>')
def destroy_page(id):
    
    data ={

        'id': id
    }
    Magazine.destroy_page(data)
    return redirect("/user")

