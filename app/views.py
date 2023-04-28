"""
Flask Documentation:     https://flask.palletsprojects.com/
Jinja2 Documentation:    https://jinja.palletsprojects.com/
Werkzeug Documentation:  https://werkzeug.palletsprojects.com/
This file creates your application.
"""

from app import app
from flask import render_template, request, jsonify, send_file, send_from_directory
import os
from app.models import Posts, Likes, Follows, Users
from werkzeug.utils import secure_filename
from flask_wtf.csrf import generate_csrf
from app import db
from .forms import RegisterForm, LoginForm, PostForm
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from functools import wraps

# ------------decorator function for authorization--------------------- #
def authorize(f):
    @wraps(f)
    def decorated_function(*args, **kws):
            if not 'Authorization' in request.headers:
                return jsonify({
                    "error": "token missing!"
                }), 401
            currentuser = None
            token = request.headers["Authorization"].split(" ")[1]
            try:
                currentuser = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
            except:
                return jsonify({
                    "error": "token missing!"
                }), 401 
            return f(*args, **kws)    
    return decorated_function
## --------------------------------------------------------------------- ##

###
# Routing for your application.
###
@app.route('/api/v1/csrf-token', methods=['GET'])
def get_csrf():
    return jsonify({'csrf_token': generate_csrf()})

@app.route('/')
def index(user):
    return jsonify({"message":"This is the beginning of our API"})

# ------------ register route--------------------- #
@app.route("/api/v1/register", methods=["POST"])
def register():
    form = RegisterForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        location = request.form['location']
        biography = request.form['biography']
        f = form.profile.data
        filename = secure_filename(f.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(img_url)

        user = Users(
            username=username,
            password=generate_password_hash(password, method='pbkdf2:sha256'),
            firstname=firstname,
            lastname=lastname,
            email=email,
            location=location,
            biography=biography,
            profile=filename
        )

        db.session.add(user)
        db.session.commit()
        joined = user.joined_on

        return jsonify({
            "message": "User successfully added",
            "username": str(username),
            "password": str(user.password),
            "firstname": str(firstname),
            "lastname": str(lastname),
            "email": str(email),
            "location": str(location),
            "biography": str(biography),
            "profile_photo": "/api/v1/photo/" + str(filename),
            "joined_on": str(joined)
        })
    else: 
        return jsonify({
            "errors": form_errors(form)
        })
    
# ------------ login route --------------------- #

@app.route("/api/v1/auth/login", methods=["POST"])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        username = request.form['username']
        password = request.form['password']
        user = Users.query.filter_by(username=username).first()
        if(not user):
            return jsonify({
                "error": "User do not exist!"
            })
        if(not(check_password_hash(user.password, password))):
            return jsonify({
                "error": "Invalid credentials!"
            })
        data = {}
        data['id'] = user.id
        data['username'] = user.username
        token = jwt.encode(data, app.config["SECRET_KEY"], algorithm="HS256")
        return jsonify({
            "message": "User successfully logged in",
            "token": token
        })

# ------------ logout route --------------------- #        
        
@app.route("/api/v1/auth/logout", methods=["POST"])
def logout():
    return jsonify({
        "message": "User logged out"
    })

# ------------ for fetching a single user --------------------- #

@app.route("/api/v1/users/<userId>", methods=["GET"])
def get_user(userId):
    if (userId == "currentuser"):
        token = request.headers["Authorization"].split(" ")[1]
        user = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
        print(user)
        userId = user['id']
        # return jsonify({"user": "hello current user"}),200
    user = Users.query.filter_by(id=userId).first()
    if (not user):
        return jsonify({
            "error": "user not found"
        }), 404
    return jsonify({
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "firstname": user.firstname,
            "lastname": user.lastname,
            "email": user.email,
            "location": user.location,
            "biography": user.biography,
            "profile_photo": "/api/v1/photo/" + user.profile,
            "joined_on": user.joined_on
        }), 200

# ------------ posting new user specific posts --------------------- #
@app.route("/api/v1/users/<userId>/posts", methods=["POST"])
@authorize
def create_post(userId):
    form = PostForm()
    id = userId
    user = Users.query.filter_by(id=id).first()
    if(not user):
        return jsonify({
            "message": "user do not exist"
        })
    
    if request.method == "POST" and form.validate_on_submit():
        caption = request.form['caption']
        f = form.photo.data
        filename = secure_filename(f.filename)
        img_url = os.path.join(app.config['UPLOAD_FOLDER'],filename)
        f.save(img_url)

        post = Posts(
            photo=filename,
            caption=caption,
            user=user
        )

        db.session.add(post)
        db.session.commit()

        return jsonify({
            "message": "post created"
        })
    else:
        return "server error"

# ------------ getting user specific posts --------------------- #

@app.route("/api/v1/users/<userId>/posts", methods=["GET"])
@authorize
def get_posts(userId):

    user = Users.query.filter_by(id=userId).first()
    posts = user.posts
    arr = []
    for post in posts:
        obj = {
            "photo": "/api/v1/photo/" + post.photo,
            "caption": post.caption
        }
        arr.append(obj)
    return jsonify({
        "posts": arr
    })

# ------------ all posts --------------------- #

@app.route("/api/v1/posts", methods=["GET"])
def all_posts():
    posts = Posts.query.all()
    arr = []
    for post in posts:
        obj = {
            "id": post.id,
            "user_id": post.user_id,
            "photo": "/api/v1/photo/" + post.photo,
            "caption": post.caption,
            "created_at": post.created_at,
            "likes": len(post.likes)
        }
        arr.append(obj)
    return jsonify({
        "posts": arr
    })

# ------------ following a target user --------------------- #
@app.route("/api/users/<userId>/follow", methods=["POST"])
@authorize
def follow(userId):
    currentuser = Users.query.filter_by(id=userId).first()
    if(not currentuser):
        return jsonify({
            "error": "user does not exist"
        })
    
    data = request.get_json()
    print(data)
    target_id = data['follow_id']
    print(target_id)
    targetuser = Users.query.filter_by(id=target_id).first()

    follow = Follows(follower=targetuser, currentuser=currentuser)
    db.session.add(follow)
    db.session.commit()

    return jsonify({
        "message": "You are now following " + targetuser.username
    })

# ------------ number of followers --------------------- #
@app.route("/api/users/<userId>/follow", methods=["GET"])
@authorize
def followers(userId):
    currentuser = Users.query.filter_by(id=userId).first()

    if(not currentuser):
        return jsonify({
            "error": "user does not exist"
        })
    
    return jsonify({
        "followers": len(currentuser.following)
    })

# ------------ liking a specific post --------------------- #
@app.route("/api/v1/posts/<postId>/like", methods=["POST"])
def like(postId):
    try:
        token = request.headers["Authorization"].split(" ")[1]
        decoded_data = jwt.decode(token, app.config['SECRET_KEY'], algorithms="HS256")
    except:
        return jsonify({
            "error": "token not present!"
        }), 404
    userId = decoded_data['id']
    currentuser = Users.query.filter_by(id=userId).first()
    post = Posts.query.filter_by(id=postId).first()
    like = Likes(posts=post, user=currentuser)
    db.session.add(like)
    db.session.commit()

    return jsonify({
        "message": "You liked the post",
        "likes": len(post.likes)
    })

# ------------ resturning file name specific image --------------------- #
@app.route("/api/v1/photo/<filename>", methods=['GET'])
def get_image(filename):
    return send_from_directory(os.path.join(os.getcwd(), app.config['UPLOAD_FOLDER']), filename)

def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404