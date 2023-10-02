from flask import render_template, redirect, request, session, flash, url_for
from flask_app import app
from flask_app.models.invention import Invention

@app.route('/new_invention')
def add_invention():
    return render_template('add_invention.html')

@app.route('/create_invention', methods=['POST'])
def create_invention():
    if not Invention.valid(request.form):
        return redirect('/new_invention')
    data = {
        "name": request.form['name'],
        "description": request.form['description'],
        "patent_approved" : request.form['patent_approved'],
        "inventor_id": session['user_id']
    }
    print("Session user_id:", session['user_id'])
    Invention.create_invention(data)

    return redirect('/homepage')

@app.route('/read_one_invention/<int:id>')
def show(id):
    data = {
        'id': id
    }
    return render_template('view_invention.html',first_name=session['first_name'], invention=Invention.get_one_with_user(data))

@app.route('/edit_invention/<int:id>')
def edit_invention(id):
    data = {
        'id': id
    }
    return render_template('edit_invention.html', invention=Invention.get_one_with_user(data))

@app.route('/update_invention', methods=['POST'])
def update_invention():
    invention_id = request.form.get('id')
    if not invention_id:
        flash('Recipe ID is missing')
        return redirect('/homepage')

    data = {
        'id': invention_id,
        'name': request.form['name'],
        'description': request.form['description'],
        "patent_approved" : request.form['patent_approved'],
        'inventor_id': session.get('user_id')
    }

    if not Invention.valid(data):
        return redirect(url_for('edit_invention', id=invention_id))

    Invention.update(data)
    flash('Invention updated successfully')
    return redirect('/homepage')

@app.route('/delete/<int:invention_id>')
def delete_invention(invention_id):
    Invention.delete_invention({'id':invention_id})
    return redirect('/homepage')