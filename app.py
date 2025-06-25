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

app = Flask(__name__)


# Helpers
def load_posts() -> dict[str, dict]:
    """
    Loads posts from a JSON file into a dictionary. The function attempts to read data
    from the "data/posts.json" file and parse its content as JSON. In case of errors
    such as file not found, invalid JSON format, or file access issues, the function
    logs the error and returns an empty dictionary.

    :return: A dictionary containing the content of the posts.json file. Returns an
        empty dictionary if an error occurs during the file read or parsing process.
    :rtype: dict[str, dict]
    """
    try:
        with open("data/posts.json", "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError, PermissionError, OSError) as e:
        logging.error(f"Error loading posts: {e}")
        return {}


def save_posts(posts: dict[str, dict]) -> None:
    """
    Saves a collection of posts to a JSON file. This function takes a dictionary where the
    keys are strings representing post identifiers, and the values are dictionaries
    containing post data. It validates the provided data, ensuring it adheres to the expected
    structure, and logs an error message if the data is invalid. If valid, the posts are
    serialized into a JSON file named "data/posts.json". Proper error handling is implemented
    to manage file-related issues during this operation.

    :param posts: A dictionary where keys are strings representing post identifiers, and
        values are dictionaries containing the post details.
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


def validate_post_form_data() -> tuple[str, str, str] | tuple[None, None, None]:
    """
    Validates and retrieves the `author`, `title`, and `content` from the post form data.
    If any of the required fields are missing or their values are empty after stripping
    whitespace, the function returns a tuple containing `None` values. Otherwise, it
    returns the processed values retrieved from the request.

    :return: A tuple containing the validated `author`, `title`, and `content` strings
        from the form data, or a tuple containing `None` values if validation fails.
    :rtype: tuple[str, str, str] | tuple[None, None, None]
    """
    author = request.form.get("author", "Anonymous").strip()
    title = request.form.get("title", "Untitled").strip()
    content = request.form.get("content", "").strip()

    if not author or not title or not content:
        return None, None, None

    return author, title, content


def fetch_post_by_id(post_id: str) -> dict | None:
    """
    Retrieve a single blog post by ID.

    :param post_id: The ID of the post to retrieve.
    :return: The post dictionary or None if not found.
    """
    blog_posts = load_posts()
    return blog_posts.get(post_id)


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
def add():
    """
    Handles the addition of a new blog post by processing form data from a POST
    request or rendering the form for a GET request.

    For a POST request, this function validates the input form data, generates a
    unique ID for the new blog post, and updates the blog post storage. If successful,
    the user is redirected to the index page.

    For a GET request, it renders the page containing the form for adding a new blog
    post.

    :return: A response object based on the HTTP method. In the case of a GET request,
             it renders a template for the "add" page. For a POST request, it redirects
             to the index page.
    """
    if request.method == "POST":
        post_id = str(uuid.uuid4())
        author, title, content = validate_post_form_data()
        post = {"author": author, "title": title, "content": content, "likes": 0}

        blog_posts = load_posts()
        blog_posts[post_id] = post
        save_posts(blog_posts)

        return redirect(url_for("index"))

    # Else GET request
    return render_template("add.html")


@app.route("/delete/<post_id>", methods=["GET"])
def delete(post_id: str):
    """
    Handles the deletion of a blog post via a GET request. The function checks if the provided
    post ID exists, deletes the post if present, saves the updated list of posts, and redirects
    to the index page. If the post ID is not provided, it returns an appropriate error response.

    :param post_id: The unique identifier of the post to be deleted.
    :type post_id: str
    :return: A `Response` object indicating the result of the operation. This can either be
        a redirect to the index page or an error response if the post ID is not provided.
    """
    if post_id is None:
        return "Post ID not provided", 400

    blog_posts = load_posts()
    if post_id in blog_posts:
        del blog_posts[post_id]
        save_posts(blog_posts)

    return redirect(url_for("index"))


@app.route("/update/<post_id>", methods=["GET", "POST"])
def update(post_id: str):
    """
    Handles updating an existing blog post. Allows rendering an update form for GET requests
    and updating the blog post for POST requests. Each blog post is identified by its unique ID.

    :param post_id: The unique identifier of the blog post to be updated.
    :type post_id: str
    :return: A rendered template for GET requests or a redirect to the index page for
        successful POST requests. If post_id is invalid, returns an appropriate error
        message and HTTP status code.
    """
    if post_id is None:
        return "Post ID not provided", 400

    blog_posts = load_posts()
    post = fetch_post_by_id(post_id)
    if post is None:
        return "Post not found", 404

    if request.method == "POST":
        author, title, content = validate_post_form_data()

        updated_post = {
            "author": author,
            "title": title,
            "content": content,
            "likes": post.get("likes", 0),
        }

        blog_posts[post_id] = updated_post
        save_posts(blog_posts)

        return redirect(url_for("index"))

    # Else is a GET request
    return render_template("update.html", post=post, post_id=post_id)


@app.route("/like/<post_id>", methods=["POST"])
def like(post_id: str):
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
    app.run(host="0.0.0.0", port=5000, debug=True)
