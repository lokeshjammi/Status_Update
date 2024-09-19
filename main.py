import os

import requests
from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired

app = Flask(__name__)
Bootstrap5(app)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
base_file = os.path.dirname(__file__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(base_file, "instance/today_update.db")

db = SQLAlchemy(app)


#==============Database Tables================


class Todays(db.Model):
    id = db.Column(type_=db.Integer, name="id", primary_key=True, autoincrement=True)
    name = db.Column(type_=db.String, name="name", unique=True)
    email = db.Column(type_=db.String, name="email_id", unique=True)
    story_id = db.Column(type_=db.String, name="story_id")
    sprint_id = db.Column(type_=db.Integer, name="sprint_id")
    qa_task_id = db.Column(type_=db.String, name="qa_task_id")
    bugs_todo = db.Column(type_=db.String, name="bugs_todo")
    bugs_progress = db.Column(type_=db.String, name="bugs_progress")
    bugs_done = db.Column(type_=db.String, name="bugs_done")
    bugs_verified = db.Column(type_=db.String, name="bugs_verified")


class Users(db.Model):
    user_id = db.Column(type_=db.Integer, name="user_id", primary_key=True, autoincrement=True)
    user_name = db.Column(type_=db.String, name="user_name", unique=True)
    user_email = db.Column(type_=db.String, name="user_email_id", unique=True)


#==============Database Tables================

with app.app_context():
    db.create_all()


class AddWorkingTickets(FlaskForm):
    qa_name = StringField(label="QA_Name", validators=[DataRequired()])
    qa_email = EmailField(label="QA_Email", validators=[DataRequired()])
    sprint_id = IntegerField(label="Sprint_ID", validators=[DataRequired()])
    story_id = StringField(label="Story_ID", validators=[DataRequired()])
    qa_task_id = StringField(label="QA_Task_ID", validators=[DataRequired()])
    qa_bugs_todo = StringField(label="Todo_Bug_ID", validators=[DataRequired()])
    qa_bugs_progress = StringField(label="InProgress_Bug_ID", validators=[DataRequired()])
    qa_bugs_done = StringField(label="Done_Bug_ID", validators=[DataRequired()])
    qa_bugs_verified = StringField(label="Verified_Bug_ID", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


class AddUsers(FlaskForm):
    new_qa_name = StringField(label="Name", validators=[DataRequired()])
    new_qa_email = EmailField(label="Email", validators=[DataRequired()])
    submit = SubmitField(label="Submit")


@app.route("/")
def homepage():
    db.session.rollback()
    return render_template('index.html')


@app.route("/add_user", methods=['POST', 'GET'])
def add_users():
    db.session.rollback()
    add_new_user = AddUsers()
    try:
        if add_new_user.validate_on_submit():
            query = db.session.query(Users).count()
            print(query)
            new_user = Users(user_id=query + 1, user_name=request.form.get('new_qa_name'),
                             user_email=request.form.get('new_qa_email'))
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for(endpoint='homepage'))
    except Exception as e:
        print(e)
    return render_template('add_user.html', add_new_user=add_new_user)


@app.route("/add_ticket", methods=['POST', 'GET'])
def add_work_tickets():
    add_working_tickets = AddWorkingTickets()
    if add_working_tickets.validate_on_submit():
        query = db.session.query(Todays).count()
        new_status = Todays(id=query + 1, name=request.form.get('qa_name'), email=request.form.get('qa_email'),
                            sprint_id=request.form.get('qa_sprint_id'),
                            story_id=request.form.get('qa_story_id'), )
        db.session.add(new_status)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('add_tickets.html', add=add_working_tickets)


@app.route("/view_users", methods=['POST', 'GET'])
def view_registered_users():
    users_data = db.session.query(Users).all()
    print(users_data)
    return render_template('view_users.html', users_data=users_data)


@app.route("/update")
def update_work_tickets():
    return render_template('update.html')


@app.route("/delete")
def delete_work_tickets():
    return render_template('delete.html')


if __name__ == '__main__':
    app.run(debug=True)
