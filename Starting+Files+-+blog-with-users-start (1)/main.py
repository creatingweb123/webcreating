from flask import Flask, render_template, redirect, url_for, flash, abort, request
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreatePostForm, RegisterForm, LoginForm, CommentForm
from flask_gravatar import Gravatar
from functools import wraps


app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
ckeditor = CKEditor(app)
Bootstrap(app)

##CONNECT TO DB
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

gravatar = Gravatar(app, size=100, rating='g', default='retro', force_default=False, force_lower=False, use_ssl=False, base_url=None)


## decorator
def admin_only(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.id != 1:
            return abort(403, description="Resource not found")
        return f(*args, **kwargs)        
    return decorated_function

def admin_author(f):
    @wraps(f)
    def wrapped_function(user_id,*args, **kwargs):
        if current_user.id != user_id or current_user.id != 1:
            return abort(403, description="You are not allowed to delete the comment")
        return f(user_id,*args, **kwargs)        
    return wrapped_function

##CONFIGURE TABLES
class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

    posts = relationship("BlogPost", back_populates='author')
    comments = relationship("Comment",back_populates='author')

class BlogPost(db.Model):
    __tablename__ = "blog_posts"
    id = db.Column(db.Integer, primary_key=True)
    
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)

    author_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    author = relationship("User", back_populates="posts")

    comments = relationship("Comment",back_populates="post")

class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    
    author = relationship("User",back_populates='comments')
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    text = db.Column(db.String(1000))
    ########## Child Relationship #########
    post_id = db.Column(db.Integer, db.ForeignKey('blog_posts.id'),nullable=False)
    post = relationship("BlogPost",back_populates="comments")

@app.route('/')
def get_all_posts():
    posts = BlogPost.query.all()
    return render_template("index.html", all_posts=posts,current_user=current_user)


@app.route('/register',methods=["POST","GET"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        email = form.email.data
        test = User.query.filter_by(email=email).first()
        if test:
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for("register"))
        user = User(
            email = email,
            password = generate_password_hash(form.password.data,'pbkdf2:sha256',salt_length=8),
            name = form.name.data
        )
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("get_all_posts"))
    return render_template("register.html",form=form)


@app.route('/login',methods=["POST","GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email    = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user==None:
            flash("Login failed. Please check your email")
            return redirect(url_for('login'))
        elif check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("get_all_posts"))
        else:
            flash("Password incorrect, please try again")
            return redirect(url_for('login'))
            
    return render_template("login.html",form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('get_all_posts'))


@app.route("/post/<int:post_id>",methods=["POST","GET"])
def show_post(post_id):
    form = CommentForm()
    comments = Comment.query.all()
    requested_post = BlogPost.query.get(post_id)
    if form.validate_on_submit():
        if current_user.is_authenticated:
            new_comment = Comment(
                author_id = current_user.id,
                text = form.body.data,
                post_id = post_id
            )
            db.session.add(new_comment)
            db.session.commit()
            return redirect(url_for("show_post",post_id=post_id))
        else:
            flash("You are not authenticated. Login first")
            return redirect(url_for("show_post",post_id = post_id))
    return render_template("post.html", post=requested_post,current_user = current_user,form=form,comments=comments)

@app.route("/delete-comment/<int:user_id>")
@login_required
@admin_author
def delete_comment(user_id):
    comment_id = request.args.get("comment_id")
    comment = db.session.query(Comment).get(int(comment_id))
    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for("show_post",post_id =post_id))

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/new-post",methods=["POST","GET"])
@admin_only
def add_new_post():
    form = CreatePostForm()
    if form.validate_on_submit():
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            date=date.today().strftime("%B %d, %Y"),
            author_id = current_user.id
        )
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("get_all_posts"))
    return render_template("make-post.html", form=form)


@app.route("/edit-post/<int:post_id>",methods=["POST","GET"])
@admin_only
def edit_post(post_id):
    post = BlogPost.query.get(post_id)
    edit_form = CreatePostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )
    if edit_form.validate_on_submit():
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = post.author
        post.body = edit_form.body.data
        db.session.commit()
        return redirect(url_for("show_post", post_id=post.id))

    return render_template("make-post.html", form=edit_form)


@app.route("/delete/<int:post_id>")
@login_required
@admin_author
def delete_post(post_id):
    post_to_delete = BlogPost.query.get(post_id)
    db.session.delete(post_to_delete)
    db.session.commit()
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000,debug=True)
