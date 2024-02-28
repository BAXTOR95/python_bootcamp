from flask import Flask, render_template
from post import Post

app = Flask(__name__)


@app.route('/')
def home():
    posts = Post.all_posts()
    return render_template("index.html", posts=posts)


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = Post.all_posts()
    for post in posts:
        if post.id == post_id:
            return render_template("post.html", post=post)
    return render_template("post.html", post=None)


if __name__ == "__main__":
    app.run(debug=True)
