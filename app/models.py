from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from app import db, login_manager


class Goal(db.Model):
    """
    Create an Goal table
    """

    # Ensures table will be named in plural and not in singular
    # as is the name of the model
    __tablename__ = 'goals'

    goal_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.VARCHAR(255))
    publish_status = db.Column(db.VARCHAR(255))
    created_on = db.Column(db.VARCHAR(63))
    title = db.Column(db.VARCHAR(63))
    description = db.Column(db.VARCHAR(63))
    complete_status = db.Column(db.VARCHAR(63))
    deadline = db.Column(db.VARCHAR(63))
    date_finished = db.Column(db.VARCHAR(63))




class Milestone(db.Model):
    """
    Create a Milestone table
    """

    __tablename__ = 'milestones'

    milestone_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    goal_id = db.Column(db.ForeignKey(Goal.goal_id))
    complete_status = db.Column(db.VARCHAR(255))
    title = db.Column(db.VARCHAR(255))
