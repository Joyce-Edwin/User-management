from flask import Flask, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from config import app, jwt
from schema import user_schema, users_schema, wall_schema, walls_schema
from config import db,ma
from models import User, Wall
from datetime import datetime


@app.route('/login', methods=['POST'])
def login_required():
    username = request.json.get('username')
    password = request.json.get('password')
    try:
        # Validate username and password
        if username != 'admin' or password != 'admin':
            raise Exception('Invalid username or password')

        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 401


@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    username = data.get('username')
    email_id = data.get('email_id')
    address = data.get('address')

    if not username or not email_id:
        return jsonify({'message': 'Forbidden'}), 403

    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({'message': 'Username already exists'}), 400

    new_user = User(username=username, email_id=email_id, address=address)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'User created successfully'}), 201


@app.route('/users/<username>', methods=['DELETE'])
def delete_user(username):
    user = User.query.filter_by(username=username).first()

    if user is None:
        return jsonify({'message': 'User not found'}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200


@app.route('/users', methods=['GET'])
def view_users():
    # # Check if the request is from an admin
    # current_user = get_jwt_identity()
    # if current_user != 'admin':
    #     return jsonify({'message': 'Unauthorized'}), 401

    al_users = User.query.all()
    all_users = users_schema.dump(al_users)
    return users_schema.jsonify(all_users)


@app.route('/wall', methods=['POST'])
def create_wall():
    # Determine user wall or admin wall based on request data
    admin = request.json.get('admin')
    if admin:
        return create_admin_wall()
    else:
        return create_user_wall_post()


def create_user_wall_post():
    user_id = request.json.get('user_id')
    title = request.json.get('title')
    description = request.json.get('description')

    if not user_id or not title or not description:
        return jsonify({'message': 'username or title or description is required'}), 400
    user = User.query.filter_by(id=User.id).first()  # Fetch existing user
    if not user:
        return jsonify({'message': 'User not found'}), 404

    wall_post = Wall(user=user, title=title, description=description)  # Associate wall post with user
    db.session.add(wall_post)
    db.session.commit()
    return jsonify({'message': 'User wall created successfully'}), 201


def create_admin_wall():
    admin = request.json.get('admin')
    title = request.json.get('title')
    description = request.json.get('description')

    if not admin or not title or not description:
        return jsonify({'message': 'Content is required'}), 400

    wall_post = Wall(admin=admin, title=title, description=description)
    db.session.add(wall_post)
    db.session.commit()
    return jsonify({'message': 'Admin wall created successfully'}), 201


@app.route('/wall/<int:id>', methods=['DELETE'])
def delete_wall(id):
    wall = Wall.query.get(id)
    if not wall:
        return jsonify({'error': 'Wall not found'}), 404

    db.session.delete(wall)
    db.session.commit()
    return jsonify({'message': 'Wall deleted successfully'}), 200


@app.route('/posts', methods=['GET'])
def view_posts():
    all_wall_posts = Wall.query.all()
    serialized_posts = [wall.serialize() for wall in all_wall_posts]
    return jsonify({'posts': serialized_posts})


with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True, port=5050)
# {
# "username":"admin",
# "title":"python",
# "description":"python is a high level dynamic language"
# }
