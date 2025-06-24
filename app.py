import json
import uuid

from flask import Flask, redirect, url_for
from flask import render_template, request

app = Flask(__name__)


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
        post = {post_id: {"author": author, "title": title, "content": content}}

        with open("data/posts.json", "r") as f:
            try:
                blog_posts = json.load(f)
            except json.JSONDecodeError:
                blog_posts = []

        blog_posts.append(post)

        with open("data/posts.json", "w") as f:
            json.dump(blog_posts, f, indent=2)

        return redirect(url_for("index"))

    return render_template("add.html")


@app.route("/delete/<post_id>", methods=["POST"])
def delete(post_id):
    # Find the blog post with the given id and remove it from the list
    with open("data/posts.json", "r") as f:
        blog_posts = json.load(f)
        if post_id in blog_posts:
            del blog_posts[post_id]
            with open("data/posts.json", "w") as f:
                json.dump(blog_posts, f, indent=4)

        # Redirect back to the home page
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
