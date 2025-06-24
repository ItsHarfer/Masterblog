import json
import uuid

from flask import Flask, redirect, url_for
from flask import render_template, request
app = Flask(__name__)


@app.route('/')
def index():
    with open('data/posts.json', 'r') as f:
        blog_posts = json.load(f)

    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        post_id = str(uuid.uuid4())
        author = request.form['author']
        title = request.form['title']
        content = request.form['content']
        post = {
            'id': post_id,
            'author': author,
            'title': title,
            'content': content
        }

        with open('data/posts.json', 'r') as f:
            try:
                blog_posts = json.load(f)
            except json.JSONDecodeError:
                blog_posts = []

        blog_posts.append(post)

        with open('data/posts.json', 'w') as f:
            json.dump(blog_posts, f, indent=2)

        return redirect(url_for('index'))

    return render_template('add.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)