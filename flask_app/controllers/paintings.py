from flask_app import app
from flask import render_template, redirect, session, request, flash
from flask_app.models.painting import Painting
from flask_app.models.user import User

@app.route('/add/painting')
def addPainting():
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    loggedUser = User.get_user_by_id(data)
    return render_template('addPainting.html', loggedUser=loggedUser)

@app.route('/create/painting', methods = ['POST'])
def createPainting():
    if 'user_id' not in session:
        return redirect('/')
    if not Painting.validate_painting(request.form):
        return redirect(request.referrer)
    data={
        'title': request.form['title'],
        'description': request.form['description'],
        'price': request.form['price'],
        'quantity': request.form['quantity'],
        'user_id': session['user_id'],
    }
    Painting.create(data)
    return redirect('/')

@app.route('/view/painting/<int:id>')
def viewPainting(id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'painting_id': id,
        'id': session['user_id']
    }
    painting = Painting.get_painting_by_id(data)
    loggedUser = User.get_user_by_id(data)
    usersWhoPainted=Painting.get_painters(data)
    return render_template('painting.html', painting=painting, loggedUser=loggedUser, usersWhoPainted=usersWhoPainted)

@app.route('/delete/painting/<int:id>')
def deletePainting(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'painting_id':id,
        'id':session['user_id']
    }
    painting=Painting.get_painting_by_id(data)
    if not painting:
        return redirect('/')
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']==painting['user_id']:
        Painting.delete_all_painted(data)
        Painting.delete_Painting(data)
    return redirect('/')

@app.route('/edit/painting/<int:id>')
def editPainting(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'painting_id':id,
        'id':session['user_id']
    }
    painting=Painting.get_painting_by_id(data)
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']==painting['user_id']:
        return render_template('edit.html', painting=painting, loggedUser=loggedUser)
    return redirect('/')

@app.route('/update/painting/<int:id>', methods=['POST'])
def updatePainting(id):
    if 'user_id' not in session:
        return redirect('/')
    data={
        'painting_id':id,
        'id':session['user_id'],    
    }
    painting=Painting.get_painting_by_id(data)
    if not painting:
        return redirect('/')
    
    loggedUser=User.get_user_by_id(data)
    if loggedUser['id']!=painting['user_id']:
        return redirect('/')
    updateData={
        'title':request.form['title'],
        'description':request.form['description'],
        'price':request.form['price'],
        'quantity':request.form['quantity'],
        'id':id
    }
    if not Painting.validate_painting(updateData):
        return redirect(request.referrer)
    Painting.update_painting(updateData)
     
    return redirect('/')
    
@app.route('/painted/<int:id>')
def addPainted(id):
    if 'user_id' not in session:
        return redirect('/')
    data ={
        'painting_id':id,
        'id': session['user_id']
    }
    print(f"Data for addPainted: {data}")
    usersWhoPainted=Painting.get_painted(data)
    print(f"Painted by {id}: {usersWhoPainted}")
    if session['user_id'] not in usersWhoPainted:
        try:
            Painting.addPainted(data)
        except Exception as e:
            print(f"Error who Painted: {e}")
        return redirect(request.referrer)
    return redirect(request.referrer)

