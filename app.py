"""
app.py

Main application module for the Masterblog Flask project.

This script serves as the entry point for a simple web-based blog system that allows users
to create, read, update, delete, and like blog posts. Blog entries are stored as JSON data
in a local file-based storage (`data/posts.json`), and the user interface is rendered via HTML templates.

Features:
- Route-based blog interaction via Flask: add, edit, delete, and like blog posts
- JSON-backed persistent data storage with structured read/write helpers
- HTML interface using Jinja2 templates
- RESTful endpoint structure for managing blog post lifecycle
- Basic like feature implemented to allow post engagement

Functions:
- `load_posts()` and `save_posts()` manage I/O access to the blog post JSON file
- `fetch_post_by_id()` retrieves a single post by ID
- `index()`, `add()`, `update()`, `delete()`, and `like()` define the application’s main routes

Required modules:
- Flask: Core web framework (routes, request handling, rendering)
- json: File-based structured data persistence
- uuid: Post ID generation

Author: Martin Haferanke
Date: 25.06.2025
"""

import json
import logging
import uuid

from flask import Flask, redirect, url_for
from flask import render_template, request
from requests import Response

app = Flask(__name__)


# Helpers
def load_posts() -> dict[str, dict]:
    """
    Load blog posts from the JSON file.

    :return: A dictionary of post_id to post data.
    """
    try:
        with open("data/posts.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, OSError) as e:
        logging.error(f"Error loading posts: {e}")
        return {}


def save_posts(posts: dict[str, dict]) -> None:
    """
    Save blog posts to the JSON file.

    :param posts: A dictionary of post_id to post data.
    :return: None
    """
    if not isinstance(posts, dict) or not all(
        isinstance(v, dict) for v in posts.values()
    ):
        logging.error("Error: Invalid posts data")
        return

    try:
        with open("data/posts.json", "w") as f:
            json.dump(posts, f, indent=4)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, OSError) as e:
        logging.error(f"Error saving posts: {e}")


# Routes
@app.route("/")
def index():
    """
    Render the homepage displaying all blog posts.

    :return: Rendered HTML page with the list of posts.
    """
    blog_posts = load_posts()
    return render_template("index.html", posts=blog_posts)


@app.route("/add", methods=["GET", "POST"])
def add() -> Response:
    """
    Handle creation of a new blog post.

    GET: Render form to create a new post.
    POST: Save submitted post and redirect to homepage.

    :return: Rendered form or redirect to index.
    """
    if request.method == "POST":
        post_id = str(uuid.uuid4())
        author = request.form.get("author", "Anonymous")
        title = request.form.get("title", "Untitled")
        content = request.form.get("content", "")

        if not author or not title or not content:
            return "Missing form data", 400

        post = {"author": author, "title": title, "content": content, "likes": 0}

        blog_posts = load_posts()
        blog_posts[post_id] = post
        save_posts(blog_posts)

        return redirect(url_for("index"))

    # Else GET request
    return render_template("add.html")


@app.route("/delete/<post_id>", methods=["POST"])
def delete(post_id: str) -> Response:
    """
    Delete a blog post by its unique ID.

    :param post_id: The ID of the post to delete.
    :return: Redirect to the homepage after deletion.
    """
    if post_id is None:
        return "Post ID not provided", 400

    blog_posts = load_posts()
    if post_id in blog_posts:
        del blog_posts[post_id]
        save_posts(blog_posts)

    return redirect(url_for("index"))


@app.route("/update/<post_id>", methods=["GET", "POST"])
def update(post_id: str) -> str | Response:
    """
    Update a blog post by its unique ID.

    GET: Render form pre-filled with post data.
    POST: Save updated post and redirect to homepage.

    :param post_id: The ID of the post to update.
    :return: Rendered form or redirect to index.
    """
    if post_id is None:
        return "Post ID not provided", 400

    blog_posts = load_posts()
    post = blog_posts.get(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        updated_post = {
            "author": request.form["author"],
            "title": request.form["title"],
            "content": request.form["content"],
            "likes": post.get("likes", 0),
        }
        blog_posts[post_id] = updated_post
        save_posts(blog_posts)

        return redirect(url_for("index"))

    # Else is a GET request
    return render_template("update.html", post=post, post_id=post_id)


@app.route("/like/<post_id>", methods=["POST"])
def like(post_id: str) -> Response:
    """
    Increment the like counter for a blog post.

    :param post_id: The ID of the post to like.
    :return: Redirect to the homepage.
    """

    blog_posts = load_posts()

    if post_id not in blog_posts:
        return "Post not found", 404

    blog_posts[post_id]["likes"] = blog_posts[post_id].get("likes", 0) + 1
    save_posts(blog_posts)

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
