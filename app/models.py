from . import db
from datetime import datetime

class Users(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    firstname = db.Column(db.String)
    lastname = db.Column(db.String)
    email = db.Column(db.String)
    location = db.Column(db.String)
    biography = db.Column(db.String)
    profile = db.Column(db.String)
    joined_on = db.Column(db.DateTime, default=datetime.utcnow)

    ## references from other relations
    posts = db.relationship("Posts", backref="user")
    liked = db.relationship("Likes", backref="user")
    following = db.relationship("Follows", backref="follower", foreign_keys="Follows.follower_id")
    currentuser = db.relationship("Follows", backref="currentuser", foreign_keys="Follows.user_id")


class Posts(db.Model):
    __tablename__ = 'posts'

    id = db.Column(db.Integer, primary_key=True)
    caption = db.Column(db.String)
    photo = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.relationship("Likes", backref="posts")
    
class Likes(db.Model):
    __tablename__ = 'likes'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))

class Follows(db.Model):
    __tablename__ = 'follows'

    id = db.Column(db.Integer, primary_key=True)
    follower_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
