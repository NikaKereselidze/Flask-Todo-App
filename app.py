from flask import Flask, render_template, redirect, session, url_for, request
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todo.db'

db = SQLAlchemy(app)
admin = Admin(app)

@app.route('/')
def home():
	todos = Todo.query.all()
	return render_template('index.html', todos=todos)

@app.route('/add', methods=['POST', 'GET'])
def add():
	if request.method == 'POST':
		todo = request.form.get('todo')
		created_todo = Todo(todo=todo)
		db.session.add(created_todo)
		db.session.commit()
		return redirect(url_for('home'))

@app.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
	if request.method == 'POST':
		update_todo = Todo.query.get(id)
		update_todo.todo = request.form.get('todo_update')
		db.session.commit()
		return redirect(url_for('home'))

@app.route('/delete/<int:id>', methods=['POST', 'GET'])
def delete(id):
	delete_todo = Todo.query.get(id)
	db.session.delete(delete_todo)
	db.session.commit()
	return redirect(url_for('home'))

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	todo = db.Column(db.String(100000), nullable=False)

admin.add_view(ModelView(Todo, db.session))

if __name__ == '__main__':
	app.run(debug=True)