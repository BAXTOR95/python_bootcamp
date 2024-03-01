from flask import Flask, render_template, url_for
from post import Post
from datetime import datetime

app = Flask(__name__)

# Get the current date and time
current_date = datetime.now()

# Format the current date
formatted_date = current_date.strftime("%B %d, %Y")


@app.route('/')
def index():
    posts = Post.all_posts()

    return render_template(
        "index.html",
        posts=posts,
        header_image_url=url_for('static', filename='assets/img/home-bg.jpg'),
        date=formatted_date,
    )


@app.route('/about')
def about():
    return render_template(
        'about.html',
        header_image_url=url_for('static', filename='assets/img/about-bg.jpg'),
    )


@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        header_image_url=url_for('static', filename='assets/img/contact-bg.jpg'),
    )


@app.route('/post/<int:post_id>')
def post(post_id):
    posts = Post.all_posts()
    for post in posts:
        if post.id == post_id:
            return render_template(
                "post.html",
                post=post,
                header_image_url=url_for(
                    'static', filename=f'assets/img/{post.image}'
                ),
                date=formatted_date,
            )
    return render_template(
        "post.html",
        post=None,
        header_image_url=url_for('static', filename='assets/img/post-bg.jpg'),
        date=formatted_date,
    )


if __name__ == "__main__":
    app.run(debug=True)
