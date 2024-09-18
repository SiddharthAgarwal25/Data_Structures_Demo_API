from flask import Flask, request, jsonify, abort
from sqlite3 import Connection as SQLite3Connection
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.engine import Engine
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from LinkedList import LinkedList, Node
from HashTables import HashTable, Data
from BinarySearchTrees import BinarySearchTree
import random
from custom_queue import Queue
from stack import Stack
app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///sqlitedb.file" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = 0
# configure sqlite3 to enforce foreign key constraints

@event.listens_for(Engine, "connect")
def _set_sqlite_pragma(dbapi_connection, connection_record):
    if isinstance(dbapi_connection, SQLite3Connection):
        cursor = dbapi_connection.cursor()
        cursor.execute("PRAGMA foreign_keys=ON;")
        cursor.close()


now = datetime.now()

db = SQLAlchemy(app)
#pylint: disable=no-member

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    email = db.Column(db.String(50))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(50))
    posts = db.relationship("BlogPost", cascade="all, delete")

class BlogPost(db.Model):
    __tablename__ = "blog_post"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    body = db.Column(db.String(500))
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

#routes
@app.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()
    new_user = User(
        name = data["name"],
        email = data["email"],
        address = data["address"],
        phone = data["phone"],
    )

    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message" : "User created"}), 200
# We are using insert at the beginning here because query all gives output in ascending order and we will start from inserting the first row to the beginning of the linked list. 


@app.route("/user/descending_id", methods=["GET"])
def get_all_users_descending():
    users = User.query.all()
    all_users_ll = LinkedList()

    for user in users:
        all_users_ll.insert_at_beg(
            {
                'id' : user.id,
                "name" : user.name,
                "email" : user.email,
                "address": user.address,
                "phone" : user.phone
            }
        )
    return jsonify(all_users_ll.to_array()), 200

@app.route("/user/ascending_id", methods=["GET"])
def get_all_users_ascending():
    users = User.query.all()
    user_list = [{
        'id' : user.id,
        "name" : user.name,
        "email" : user.email,
        "address": user.address,
        "phone" : user.phone

    } for user in users]

    return jsonify(user_list), 200

@app.route("/user/<user_id>", methods=["GET"])
def get_one_user(user_id):
    # user = User.query.get(user_id)
    
    # if user is None:
    #     abort(404, description=f"User with ID {user_id} not found")
    
    # user_data = {
    #     'id': user.id,
    #     'name': user.name,
    #     'email': user.email,
    #     'address': user.address,
    #     'phone': user.phone
    # }
    
    # return jsonify(user_data)
    users = User.query.all()
    all_users_ll = LinkedList()

    for user in users:
        all_users_ll.insert_at_beg(
            {
                'id' : user.id,
                "name" : user.name,
                "email" : user.email,
                "address": user.address,
                "phone" : user.phone
            }
        )
    user = all_users_ll.get_one(user_id)
    return jsonify(user), 200

@app.route("/user/<user_id>", methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message" : "User Deleted"}), 200


@app.route('/blog_post/<user_id>', methods=['POST'])
def create_blog_post(user_id):
    data = request.get_json()
    user = User.query.get(user_id)
    if not user:
        return jsonify({'message' : 'user does not exist!'}), 400
    ht = HashTable(10)
    ht.add_key_value("title", data["title"])
    ht.add_key_value("body", data["body"])
    ht.add_key_value("date", now)
    ht.add_key_value("user_id", user_id)

    new_blog_post = BlogPost(
        title=ht.get_value("title"),
        body=ht.get_value("body"),
        date=ht.get_value("date"),
        user_id=ht.get_value("user_id"),
    )

    ht.print_table()
    db.session.add(new_blog_post)
    db.session.commit()
    return jsonify({"message" : "new blog post created"}), 200

@app.route("/user/<user_id>/posts", methods=["GET"])
def get_all_blog_posts_by_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"message": "User not found"}), 404

    blog_posts = BlogPost.query.filter_by(user_id=user_id).all()
    
    if not blog_posts:
        return jsonify({"message": "No blog posts found for this user"}), 404

    posts_list = [{
        'id': post.id,
        'title': post.title,
        'body': post.body,
        'date': post.date
    } for post in blog_posts]

    return jsonify(posts_list), 200

@app.route("/blog_post/<blog_post_id>", methods=["GET"])
def get_one_blog_post(blog_post_id):
    blog_posts = BlogPost.query.all()
    random.shuffle(blog_posts)

    bst = BinarySearchTree()

    for post in blog_posts:
        bst.insert({
            "id" : post.id,
            "title" : post.title,
            "body" : post.body,
            "user_id" : post.user_id,
        })

    post = bst.search(blog_post_id)

    if not post:
        return jsonify({"message": "post not found"})

    return jsonify(post)

@app.route("/blog_post/numeric_body", methods=["GET"])
def get_numeric_post_bodies():
    blog_posts = BlogPost.query.all()

    q = Queue()

    for post in blog_posts:
        q.first_in(post)

    return_list = []

    for _ in range(len(blog_posts)):
        post = q.first_out()
        numeric_body = 0
        for char in post.data.body:
            numeric_body += ord(char)

        post.data.body = numeric_body

        return_list.append(
            {
                "id": post.data.id,
                "title" : post.data.title,
                "body" : post.data.body,
                "user_id" : post.data.user_id,
            }
        )

    return jsonify(return_list)

@app.route("/blog_post/get_last_N/<num>", methods=["GET"])
def get_last_n(num):
    blog_posts = BlogPost.query.all()
    s = Stack()
    
    for post in blog_posts:
        s.push(post)

    output_list = []
    for _ in range(int(num)):
        post = s.pop()
        output_list.append({
                "id": post.data.id,
                "title" : post.data.title,
                "body" : post.data.body,
                "user_id" : post.data.user_id,
            })
    return jsonify(output_list)



if __name__ == "__main__":
    app.run(debug=True)
