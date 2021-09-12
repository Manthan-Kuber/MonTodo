from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
# Connect db to flask using SQLAlchemy
# Set username as root and passoword as empty string as there's no password
#syntax: "sqlclient://user:password@hostIP/databasename (create database first then tables wiill be created)"
# app.config['SQLALCHEMY_DATABASE_URI'] = "mysql://root:""@localhost/flask_todo"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Todo(db.Model):
    srno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self) -> str:  # Repr method to display contents of db in terminal
        return f"{self.srno} - {self.title}"


@app.route("/", methods=['GET', 'POST'])
def hello_world():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        # An  instance of Todo class.We passed title and desc of the form as parameters
        flask_todo = Todo(title=title, desc=desc)
        db.session.add(flask_todo)
        db.session.commit()

    showTodos = Todo.query.all()
    return render_template('index.html', showTodos=showTodos)


# @app.route('/show')
# def showMe():
#     showTodos = Todo.query.all()
#     print(showTodos)
#     return '<p>All items from db are here</p>'


@app.route('/delete/<int:srno>')
def deleteMe(srno):
    todo = Todo.query.filter_by(srno=srno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:srno>',methods=['GET','POST'])
def updateMe(srno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(srno=srno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
        
    todo = Todo.query.filter_by(srno=srno).first()
    return render_template('update.html',todo=todo)


if __name__ == "__main__":
    app.run(debug=True)


# Points to Note:
# 1.Do pip install flask after activating virtual env
# 2.Select interpretar as the virtual env created and not the global interpretar
# 3.Keep the server as development server which will enable auto reload for the app.This can be done inside the app.py file itself or in the terminal
