import os
from cProfile import label

from flask import Flask, render_template, request, url_for, redirect
from flask_bootstrap import Bootstrap5
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import values
from wtforms import StringField, SubmitField, EmailField, IntegerField
from wtforms.validators import DataRequired, ReadOnly, Disabled

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

class EditWorkingTicket(FlaskForm):
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
    db.session.rollback()
    get_registered_users_names = []
    get_registered_users_email = []
    add_working_tickets = AddWorkingTickets()
    if add_working_tickets.validate_on_submit():
        query = db.session.query(Todays).count()
        qa_name = request.form.get('qa_name')
        qa_email = request.form.get('qa_email')
        qa_sprint_id = request.form.get('sprint_id')
        qa_story_id = request.form.get('story_id')
        qa_task_id = request.form.get('qa_task_id')
        qa_bugs_todo = request.form.get('qa_bugs_todo')
        qa_bugs_progress = request.form.get('qa_bugs_progress')
        qa_bugs_done = request.form.get('qa_bugs_done')
        qa_bugs_verified = request.form.get('qa_bugs_verified')
        new_ticket_add = Todays(id=query+1, name=qa_name, email=qa_email, sprint_id=qa_sprint_id, story_id=qa_story_id, qa_task_id=qa_task_id,
                                bugs_todo=qa_bugs_todo, bugs_progress=qa_bugs_progress, bugs_done=qa_bugs_done, bugs_verified=qa_bugs_verified)
        db.session.add(new_ticket_add)
        db.session.commit()
        return redirect(url_for('homepage'))
    return render_template('add_tickets.html', add=add_working_tickets, get_registered_users_names=get_registered_users_names,
                           get_registered_users_email=get_registered_users_email)


@app.route("/view_users", methods=['POST', 'GET'])
def view_registered_users():
    users_data = db.session.query(Users).all()
    return render_template('view_users.html', users_data=users_data)


@app.route("/update")
def update_work_tickets():
    return render_template('update.html')


@app.route("/delete")
def delete_work_tickets():
    return render_template('delete.html')

@app.route("/view_all_data", methods=['POST', 'GET'])
def view_all_data():
    db.session.rollback()
    view_all_data = db.session.query(Todays).all()
    return render_template('view_all_users_data.html', users_data = view_all_data)

@app.route("/edit_details/<int:selected_data_id>", methods=['POST', 'GET'])
def edit_details(selected_data_id):
    edit_working_ticket = EditWorkingTicket()
    edit_data = db.session.query(Todays).filter_by(id=selected_data_id).first()
    if edit_working_ticket.validate_on_submit():
        edit_data.sprint_id = request.form.get('sprint_id')
        edit_data.story_id = request.form.get('story_id')
        edit_data.qa_task_id = request.form.get('qa_task_id')
        db.session.commit()
        return redirect(url_for('view_all_data'))
    return render_template('edit_details.html', edit_working_ticket=edit_working_ticket, edit_data=edit_data)


if __name__ == '__main__':
    app.run(debug=True)
