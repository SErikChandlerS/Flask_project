import json

from flask import Flask, request, make_response, jsonify
from flask_mysqldb import MySQL
import yaml
import ast

IP = '0.0.0.0'
PORT = 3001
app = Flask(__name__)

app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'newuser'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'goalify'
mysql = MySQL(app)

naming_dict_goals = {
    'id': 'id',
    'label': 'label',
    'description': 'description',
    'summary': 'summary',
    'done': 'done',
    'user_id': 'user_id'
}

naming_dict_goals_rev = {val: key for key, val in naming_dict_goals.items()}

naming_dict_milestones = {
    'milestone_id': 'id',
    'goal_id': 'goal_id',
    'title': 'name',
    'complete_status': 'state',
}

naming_dict_milestones_rev = {val: key for key, val in naming_dict_milestones.items()}


def show_table(table_name):
    """
    a helper function to show a table given its name.
    :param table_name:
    :return: None.
    """
    with app.app_context():
        cur = mysql.connection.cursor()
        cur.execute(f'''SELECT goal_id FROM {table_name};''')
        res = cur.fetchall()
        print(res)
        cur.close()


@app.route('/get-goals', methods=['POST'])
def get_goals():
    """
    a method used to fetch all goals for some user.
    :return: a list of goals.
    """
    if request.method == 'POST':
        user_id = ast.literal_eval(request.data.decode())['user_id']
        command = f'''SELECT * FROM goals WHERE user_id = "{user_id}"'''
        cur = mysql.connection.cursor()
        try:
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response("Server Error", 500)
        rows = cur.fetchall()
        list = []
        for row in rows:
            list.append({'id': row[0],
                         'user_id': row[1],
                         'label': row[2],
                         'summary': row[3],
                         'done': row[4],
                         'description': row[5]})
        dict = {'list': list}

        return make_response(jsonify(dict), 200)


@app.route('/add-goal', methods=['POST'])
def add_goal():
    """
    a method to create a new goal for some user.
    :return: the new goal id or error code.
    """
    if request.method == 'POST':
        print(request.data.decode())
        goal_details = ast.literal_eval(request.data.decode())
        goal_id = goal_details[naming_dict_goals['id']]
        label = goal_details[naming_dict_goals['label']]
        summary = goal_details[naming_dict_goals['summary']]
        description = goal_details[naming_dict_goals['description']]
        done = goal_details[naming_dict_goals['done']]
        user_id = goal_details[naming_dict_goals['user_id']]
        cur = mysql.connection.cursor()
        # command = '''UPDATE goals SET publish_status = ?, created_on = ?, title = ?, description = ?,
        # complete_status = ?, deadline = ?, date_finished = ? WHERE goal_id = ?;'''
        command = f'''INSERT INTO goals(goal_id, user_id, label, summary, done, description) VALUES ("{goal_id}", "{user_id}", "{label}", 
                "{summary}", "{done}", "{description}");'''
        # command = '''INSERT INTO goals(user_id, publish_status, created_on, title, description, complete_status, deadline,
        #                                date_finished) VALUES (?, ?, ?, ?, ?, ?, ?, ?);'''

        try:
            print(command)
            cur.execute(command)
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            return make_response(e, 500)
        return make_response(jsonify({'id': goal_id}), 200)


@app.route('/add-milestone', methods=['POST'])
def add_milestone():
    """
    a method responsible for adding a new milestone to some goal.
    :return: the new milestone id or error code.
    """
    if request.method == 'POST':
        print(ast.literal_eval(request.data.decode()))
        milestone_details = ast.literal_eval(request.data.decode())
        goal_id = milestone_details[naming_dict_milestones['id']]
        title = milestone_details[naming_dict_milestones['title']]
        complete_status = milestone_details[naming_dict_milestones['complete_status']]
        cur = mysql.connection.cursor()
        # command = '''INSERT INTO milestones(goal_id, title, complete_status)
        #     VALUES (?, ?, ?);'''
        command = f'''INSERT INTO milestones(goal_id, title, complete_status) 
             VALUES ("{goal_id}", "{title}", "{complete_status}");'''
        try:
            # cur.execute(command, [goal_id, title, complete_status])
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response("Server Error", 500)
        id = cur.lastrowid
        cur.close()
        return make_response(jsonify({'id': id}), 200)


@app.route('/remove-goal', methods=['POST'])
def remove_goal():
    """
    a method responsible for removing a goal and its milestones.
    :return: response http code.
    """
    if request.method == 'POST':
        print(ast.literal_eval(request.data.decode()))
        goal_details = ast.literal_eval(request.data.decode())
        goal_id = goal_details['id']
        cur = mysql.connection.cursor()
        # command = '''DELETE FROM goals where goal_id = ?'''
        try:
            command = f'''DELETE FROM goals where goal_id = {goal_id};'''
            cur.execute(command)
            mysql.connection.commit()
        except Exception as e:
            mysql.connection.rollback()
            print(e)
            return make_response(goal_id, 500)
        cur.close()
        return make_response("OK", 200)


@app.route('/remove-milestone', methods=['POST'])
def remove_milestone():
    """
    a method responsible for removing a milestone in some goal.
    :return: response http code.
    """
    if request.method == 'POST':
        print(ast.literal_eval(request.data.decode()))
        milestone_details = ast.literal_eval(request.data.decode())
        print(milestone_details)
        milestone_id = milestone_details['id']
        cur = mysql.connection.cursor()
        # command = '''DELETE FROM milestones where milestone_id = ?'''
        command = f'''DELETE FROM milestones where milestone_id = "{milestone_id}"'''
        try:
            # cur.execute(command, [milestone_id])
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response("Server Error", 500)
        cur.close()
        return make_response("OK", 200)


@app.route('/edit-goal', methods=['POST'])
def edit_goal():
    """
    a method responsible for editing a goal.
    :return: response http code.
    """
    if request.method == 'POST':
        goal_details = ast.literal_eval(request.data.decode())
        goal_id = goal_details[naming_dict_goals['id']]
        label = goal_details[naming_dict_goals['label']]
        summary = goal_details[naming_dict_goals['summary']]
        description = goal_details[naming_dict_goals['description']]
        cur = mysql.connection.cursor()
        # command = '''UPDATE goals SET publish_status = ?, created_on = ?, title = ?, description = ?,
        # complete_status = ?, deadline = ?, date_finished = ? WHERE goal_id = ?;'''
        command = f'''UPDATE goals SET goal_id = "{goal_id}", label = "{label}", description = "{description}", 
                summary = "{summary}";'''
        try:
            # cur.execute(command, [publish_status, created_on, title, description, complete_status, deadline, date_finished, goal_id])
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response("Server Error", 500)
        cur.close()
        return make_response("OK", 200)


@app.route('/edit-milestone', methods=['POST'])
def edit_milestone():
    """
    a method responsible for editing a milestone.
    :return: response http code.
    """
    if request.method == 'POST':
        print(ast.literal_eval(request.data.decode()))
        milestone_details = ast.literal_eval(request.data.decode())
        milestone_id = milestone_details[naming_dict_milestones['milestone_id']]
        goal_id = milestone_details[naming_dict_milestones['goal_id']]
        title = milestone_details[naming_dict_milestones['title']]
        complete_status = milestone_details[naming_dict_milestones['complete_status']]
        cur = mysql.connection.cursor()
        # command = '''UPDATE milestones SET title = ?, complete_status = ? WHERE milestone_id = ?;'''
        command = f'''UPDATE milestones SET title = "{title}", complete_status = "{complete_status}" WHERE milestone_id = "{milestone_id}";'''
        try:
            # cur.execute(command, [title, complete_status, milestone_id])
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response("Server Error", 500)
        cur.close()
        return make_response("OK", 200)


@app.route('/discover', methods=['POST'])
def discover():
    """
    a method responsible for finding the last public goals.
    :return: the last public goals
    """
    if request.method == 'POST':
        num_rows = ast.literal_eval(request.data.decode()).get('num_rows', 5)
        # command = '''SELECT * FROM goals LIMIT ?'''
        command = f'''SELECT * FROM goals LIMIT "{num_rows}"'''
        cur = mysql.connection.cursor()
        try:
            # cur.execute(command, [num_rows])
            cur.execute(command)
            mysql.connection.commit()
        except:
            mysql.connection.rollback()
            return make_response(400)
        res = cur.fetchall()
        cur.close()
        return make_response(jsonify(res), 200)


def init_db():
    """
    the main method for initializing the database.
    :return: None
    """
    with app.app_context():
        cur = mysql.connection.cursor()
        command = '''CREATE TABLE IF NOT EXISTS `goals` (
                          `goal_id` varchar(255) PRIMARY KEY,
                          `user_id` varchar(64),
                          `label` varchar(255),
                          `summary` varchar(1024),
                          `done` varchar(64),
                          `description` varchar(1024));'''
        cur.execute(command)
        mysql.connection.commit()

        cur.close()
    show_table("goals")


if __name__ == '__main__':
    init_db()
    app.run(host=IP, debug=True)
