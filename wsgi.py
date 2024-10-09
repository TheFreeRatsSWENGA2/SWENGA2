import click, pytest, sys
from flask import Flask
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import User
from App.main import create_app
# from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )
# from App.controllers import ( create_course, create_staff, assign_staff, view_course_staff )
#test for commit
from App.controllers import *


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()
    print('database intialized')

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

create_cli = AppGroup('create', help='create commands')

@app.cli.command('create_course')
def create_course_command():
    """Create a new course."""
    create_course()

@app.cli.command('create_staff')
def create_staff_command():
    """Create new staff member."""
    create_staff()

@app.cli.command('assign_staff')
def assign_staff_command():
    """Assign staff to courses."""
    assign_staff()

@app.cli.command('view_course_staff')
def view_course_staff_command():
    """View all the staff for a specific course."""
    view_course_staff()

@app.cli.command('list_courses')
def list_courses_command():
    """List all courses in the database."""
    list_course() 

@app.cli.command('list_staff')
def list_staff_command():
    """Lists all staff members in the database."""
    list_staff() 

