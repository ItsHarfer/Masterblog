import json
import uuid

from flask import Flask, redirect, url_for
from flask import render_template, request

app = Flask(__name__)


def fetch_post_by_id(post_id):
    with open("data/posts.json", "r") as f:
        blog_posts = json.load(f)
        if post_id in blog_posts:
            return blog_posts[post_id]
        else:
            return None


def get_posts():
    with open("data/posts.json", "r") as f:
        try:
            blog_posts = json.load(f)
        except json.JSONDecodeError:
            blog_posts = {}
    return blog_posts


@app.route("/")
def index():
    with open("data/posts.json", "r") as f:
        blog_posts = json.load(f)

    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        post_id = str(uuid.uuid4())
        author = request.form["author"]
        title = request.form["title"]
        content = request.form["content"]
        post = {"author": author, "title": title, "content": content, "likes": 0}

        blog_posts = get_posts()
        blog_posts[post_id] = post

        with open("data/posts.json", "w") as f:
            json.dump(blog_posts, f, indent=2)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<post_id>", methods=["POST"])
def delete(post_id):
    # Get all posts
    blog_posts = get_posts()
    if post_id in blog_posts:
        del blog_posts[post_id]

    with open("data/posts.json", "w") as f:
        json.dump(blog_posts, f, indent=4)

    # Redirect back to the home page
    return redirect(url_for("index"))


@app.route("/update/<post_id>", methods=["GET", "POST"])
def update(post_id):

    post = fetch_post_by_id(post_id)
    blog_posts = get_posts()

    if post_id not in blog_posts:
        return "Post not found", 404

    if request.method == "POST":
        # Update the post in the JSON file
        updated_post = {
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"],
        }
        blog_posts[post_id] = updated_post

        with open("data/posts.json", "w") as f:
            json.dump(blog_posts, f, indent=4)

        # Redirect back to index
        return redirect(url_for("index"))

    # Else, it's a GET request
    # So display the update.html page
    return render_template("update.html", post=post, post_id=post_id)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
