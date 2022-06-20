from flask import render_template, redirect, request, session
from flask_app import app
from flask_app.models.user import User
from flask_app.models.thoughts import thoughts

@app.route('/thoughts')
def thoughts():
    return render_template('thoughts.html')

@app.route('/create/ninja', methods=['POST'])
def create_ninja():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Ninja.validate_ninja(request.form):
        return redirect('/ninjas')
    Ninja.save(request.form)
    return redirect('/')

@app.route('/ninja/<int:id>')
def show_ninja(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'thoughts_id' : id,
        'user_id': session['user_id']
    }
    myNinja = Ninja.get_one(data)
    return render_template('showOneNinja.html', ninja=myNinja,  user=User.get_by_id(data),)

@app.route('/ninja/<int:id>/like', methods=['GET','PUT'])
def like_ninja(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data={
        'thoughts_id': id,
        'user_id': session['user_id'],
        
    }

    Ninja.addLike(data)
    updatedNinja = Ninja.getUsersWhoLiked(data)
    updatedData = {
        'thoughts_id': id,
        'likes': updatedNinja.likes
    }
    Ninja.update(updatedData)
    return render_template('showOneNinja.html', ninja=updatedNinja,  user=User.get_by_id(data))

@app.route('/thoughts/<int:id>/unlike', methods=['GET','PUT'])
def unlike_ninja(id):
    if 'user_id' not in session:
            return redirect('/logout')
    data={
        'thoughts_id': id,
        'user_id': session['user_id'],
    }
    User.unLike(data)
    updatedNinja = Ninja.getUsersWhoLiked(data)
    
    return render_template('showOneNinja.html', ninja=updatedNinja,  user=User.get_by_id(data))
