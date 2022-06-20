import bcrypt
from flask import render_template,redirect,session,request, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.ninja import Ninja
from flask_bcrypt import Bcrypt
bcrypt= Bcrypt(app)

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/home')
    return render_template('login_register.html')

@app.route('/register', methods=['POST'])
def register():
    if not User.validate_register(request.form):
        return redirect('/')
    data ={ 
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id= User.save(data)
    session['user_id']= id
    return redirect ('/home')


@app.route('/login',methods=['POST'])
def login():
    user = User.get_by_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/home')


@app.route('/home')
def pageninjas():
    if 'user_id' not in session:
        return redirect ('/logout')
    data={
        'user_id': session['user_id']
    }
    ninjas = Ninja.get_all()
    return render_template('index.html', user=User.get_by_id(data), all_ninjas=ninjas)


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')