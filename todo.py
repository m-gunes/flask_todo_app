from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import os
from datetime import datetime
# from sqlalchemy.sql import func

DB_HOST = os.getenv('PSQL_URL')
DB_NAME = os.getenv('PSQL_DB')
DB_USER = os.getenv('PSQL_USER')
DB_PASS = os.getenv('PSQL_PASS')

DB_URL = 'postgresql+psycopg2://{user}:{pw}@{url}/{db}'.format(
   user=DB_USER, pw=DB_PASS, url=DB_HOST, db=DB_NAME
   )

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)



class Todo(db.Model):
   id = db.Column(db.Integer, primary_key=True)
   title = db.Column(db.String(100), nullable=False) # (nullable=False) == (NOT NULL)
   complete = db.Column(db.Boolean, default=False, nullable=False)
   created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.now())
   # created_at = db.Column(db.DateTime(timezone=True), default=func.now())
   # created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=datetime.utcnow)

# db.drop_all()
db.create_all() # method to create the tables and database



@app.route('/')
def index():
   todos = Todo.query.all()
   return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST'])
def addTodo():
   title = request.form.get('title')
   newTodo = Todo(title=title)
   db.session.add(newTodo)
   db.session.commit()
   return redirect(url_for('index'))
   
@app.route('/complete/<string:id>')
def updateTodo(id):
   todo = Todo.query.filter_by(id=id).first()
   todo.complete = not todo.complete
   db.session.commit()
   return redirect(url_for('index'))

@app.route('/delete/<string:id>')
def deleteTodo(id):
   todo = Todo.query.filter_by(id=id).first()
   db.session.delete(todo)
   db.session.commit()
   return redirect(url_for('index'))
