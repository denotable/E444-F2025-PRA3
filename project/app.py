# project/app.py
from pathlib import Path
from flask import Flask, render_template, request, session, flash, redirect, url_for, abort, jsonify
from project import models
from project.models import db, Post

basedir = Path(__file__).resolve().parent

# Config
DATABASE = "flaskr.db"
SECRET_KEY = "change_me"
USERNAME = "admin"
PASSWORD = "admin"
SQLALCHEMY_DATABASE_URI = f"sqlite:///{basedir / DATABASE}"
SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(__name__)

# Initialize SQLAlchemy with the app
db.init_app(app)

# Create tables once per process (Flask 3.x safe)
with app.app_context():
    db.create_all()

@app.route("/")
def index():
    entries = Post.query.order_by(Post.id.desc()).all()
    return render_template("index.html", entries=entries)

@app.route("/add", methods=["POST"])
def add_entry():
    if not session.get("logged_in"):
        abort(401)
    new_entry = Post(request.form["title"], request.form["text"])
    db.session.add(new_entry)
    db.session.commit()
    flash("New entry was successfully posted")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        if request.form["username"] != USERNAME:
            error = "Invalid username"
        elif request.form["password"] != PASSWORD:
            error = "Invalid password"
        else:
            session["logged_in"] = True
            flash("You were logged in")
            return redirect(url_for("index"))
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    flash("You were logged out")
    return redirect(url_for("index"))

@app.route("/delete/<int:post_id>")
def delete_entry(post_id):
    result = {"status": 0, "message": "Error"}
    try:
        Post.query.filter_by(id=post_id).delete()
        db.session.commit()
        result = {"status": 1, "message": "Post Deleted"}
        flash("The entry was deleted.")
    except Exception as e:
        result = {"status": 0, "message": repr(e)}
    return jsonify(result)

if __name__ == "__main__":
    app.run()

@app.route('/search/', methods=['GET'])
def search():
    query = request.args.get("query")
    entries = db.session.query(models.Post)
    if query:
        return render_template('search.html', entries=entries, query=query)
    return render_template('search.html')


