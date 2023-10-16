from flask import Flask, render_template, request, url_for, redirect, flash, send_from_directory
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user

app = Flask(__name__)

app.config['SECRET_KEY'] = 'any-secret-key-you-choose'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

login_manager = LoginManager()
login_manager.init_app(app)


##CREATE TABLE IN DB
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))


#Line below only required once, when creating DB. 

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))


@app.route('/')
def home():
    return render_template("index.html")


@app.route('/register',methods=["POST","GET"])
def register():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        test = User.query.filter_by(email=email).first()
        if test:
            flash("You've already signed up with that email, log in instead.")
            return redirect(url_for('register'))
        user = User(email=email,
                    password=generate_password_hash(request.form["password"],'pbkdf2:sha256', salt_length=8)
                ,name = name)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for("secrets",name=name))
    return render_template("register.html")


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        email    = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        # user = db.session.query(User).filter(User.email==email).first()
        if user == None:
            flash("Login failed. Please check your email")
            return redirect(url_for('login'))

        elif check_password_hash(user.password,password):
            login_user(user)
            return redirect(url_for("secrets",name=user.name))
        else:
            flash("Password incorrect, please try again")
            return redirect(url_for('login'))
    return render_template("login.html")


@app.route('/secrets')
@login_required
def secrets():
    name = request.args.get("name")
    return render_template("secrets.html",name=name)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route('/download')
@login_required
def download():
    filename = 'files/cheat_sheet.pdf'
    return send_from_directory('static',filename)


if __name__ == "__main__":
    app.run(debug=True)
