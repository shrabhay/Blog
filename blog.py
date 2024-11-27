from datetime import datetime
from flask import Flask, abort, render_template, redirect, url_for, flash
from flask_bootstrap import Bootstrap5
from flask_ckeditor import CKEditor
from flask_gravatar import Gravatar
import re
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
import sqlite3
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from forms import AddNewPostForm, RegisterForm, LoginForm, CommentForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)
ckeditor = CKEditor(app)
gravatar = Gravatar(app)


class User(UserMixin):
    def __init__(self, user_id, email, password, name):
        self.id = user_id
        self.email = email
        self.password = password
        self.name = name


login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM user WHERE id = ?', (user_id,))
    user = cur.fetchone()
    cur.close()
    conn.close()
    if user:
        return User(user_id=user[0], email=user[1], password=user[2], name=user[3])
    return None


def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user or current_user.id != 1:
            return abort(403)
        return f(*args, **kwargs)
    return decorated_function


# db = sqlite3.connect('posts.db')
# cursor = db.cursor()
#
# cursor.execute('CREATE TABLE user ('
#                'id INTEGER PRIMARY KEY NOT NULL,'
#                'email VARCHAR(500) UNIQUE NOT NULL,'
#                'password VARCHAR(500) NOT NULL,'
#                'name VARCHAR(500) NOT NULL)')

insert_post_query = """
INSERT INTO blog_post (title, date, body, author, img_url, subtitle)
VALUES (?, ?, ?, ?, ?, ?)
"""

add_user_query = """
INSERT INTO user (email, password, name) VALUES(?, ?, ?)
"""

add_comment_query = """
INSERT INTO blog_comments (user_id, post_id, comment) VALUES(?, ?, ?)
"""


@app.route('/')
def get_all_posts():
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog_post')
    posts = cur.fetchall()
    cur.close()
    conn.close()
    return render_template("index.html", all_posts=posts, current_user=current_user)


@app.route('/post/<int:post_id>', methods=['GET', 'POST'])
def show_post(post_id):
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()
    comment_form = CommentForm()
    cur.execute('SELECT * FROM blog_post WHERE id = ?', (post_id,))
    requested_post = cur.fetchone()

    if comment_form.validate_on_submit():
        if current_user.is_authenticated:
            comment = comment_form.comment.data
            cur.execute(add_comment_query, (current_user.id, post_id, comment))
            conn.commit()
        else:
            flash("You must be logged in to submit a comment, please log in and try again.")
            return redirect(url_for('login'))

    cur.execute('SELECT * FROM blog_comments WHERE post_id = ?', (post_id,))
    comments = cur.fetchall()

    users = []
    for item in comments:
        cur.execute('SELECT name, email FROM user WHERE id = ?', (item[0],))
        user = cur.fetchone()
        cleaned_comment = re.sub(r'<.*?>', '', item[2]).strip()
        users.append((user[0], user[1], cleaned_comment))
        print(users)

    cur.close()
    conn.close()
    return render_template("post.html", post=requested_post, current_user=current_user,
                           form=comment_form, comments=users)


@app.route('/new-post', methods=['GET', 'POST'])
@admin_only
def add_new_post():
    form = AddNewPostForm()
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()

    if form.validate_on_submit():
        title = form.title.data
        subtitle = form.subtitle.data
        author = form.author.data
        img_url = form.img_url.data
        body = form.body.data
        date = datetime.now().strftime('%B %d, %Y')

        cur.execute(insert_post_query, (title, date, body, author, img_url, subtitle))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('get_all_posts'))
    return render_template('make-post.html', form=form, current_user=current_user)


@app.route('/edit-post/<int:post_id>', methods=['GET', 'POST'])
@admin_only
def edit_existing_post(post_id):
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM blog_post WHERE id = ?', (post_id,))
    post_to_be_edited = cur.fetchone()

    edit_post_form = AddNewPostForm(
        title=post_to_be_edited[1],
        subtitle=post_to_be_edited[6],
        author=post_to_be_edited[4],
        img_url=post_to_be_edited[5],
        body=post_to_be_edited[3]
    )

    if edit_post_form.validate_on_submit():
        title = edit_post_form.title.data
        subtitle = edit_post_form.subtitle.data
        author = edit_post_form.author.data
        img_url = edit_post_form.img_url.data
        body = edit_post_form.body.data
        cur.execute('UPDATE blog_post SET title = ? WHERE id = ?', (title, post_id))
        cur.execute('UPDATE blog_post SET subtitle = ? WHERE id = ?', (subtitle, post_id))
        cur.execute('UPDATE blog_post SET author = ? WHERE id = ?', (author, post_id))
        cur.execute('UPDATE blog_post SET img_url = ? WHERE id = ?', (img_url, post_id))
        cur.execute('UPDATE blog_post SET body = ? WHERE id = ?', (body, post_id))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('show_post', post_id=post_id))

    return render_template('make-post.html', form=edit_post_form, is_edit=True,
                           current_user=current_user)


@app.route('/delete/<int:post_id>')
@admin_only
def delete_post(post_id):
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM blog_post WHERE id = ?', (post_id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('get_all_posts'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()

    if form.validate_on_submit():
        cur.execute('SELECT * FROM user WHERE email = ?', (form.email.data,))
        user_data = cur.fetchone()

        if user_data:
            flash('An account with the email already exists, log in instead.')
            return redirect(url_for('login'))
        else:
            password_hash = generate_password_hash(
                password=form.password.data,
                method='pbkdf2:sha256',
                salt_length=8
            )
            cur.execute(add_user_query, (form.email.data, password_hash, form.name.data))
            conn.commit()

            cur.execute('SELECT * FROM user WHERE email = ?', (form.email.data,))
            new_user_data = cur.fetchone()

            user = User(user_id=new_user_data[0], email=new_user_data[1], password=new_user_data[2],
                        name=new_user_data[3])
            login_user(user)

            cur.close()
            conn.close()
            return redirect(url_for('get_all_posts'))
    return render_template('register.html', form=form, current_user=current_user)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    conn = sqlite3.connect('posts.db')
    cur = conn.cursor()

    if form.validate_on_submit():
        cur.execute('SELECT * FROM user WHERE email = ?', (form.email.data,))
        user_data = cur.fetchone()

        if user_data:
            if check_password_hash(pwhash=user_data[2], password=form.password.data):
                user = User(user_id=user_data[0], email=user_data[1], password=user_data[2], name=user_data[3])
                login_user(user)
                return redirect(url_for('get_all_posts'))
            else:
                flash("You have entered an incorrect password, please try again!")
                return redirect(url_for('login'))
        else:
            flash("The entered email does not exist, please try again!")
            return redirect(url_for('login'))
    return render_template('login.html', form=form, current_user=current_user)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/about")
def about():
    return render_template("about.html", current_user=current_user)


@app.route("/contact")
def contact():
    return render_template("contact.html", current_user=current_user)


if __name__ == "__main__":
    app.run(debug=True, port=5003)
