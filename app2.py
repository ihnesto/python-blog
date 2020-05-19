from flask import Flask, render_template, request, redirect, flash, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, EqualTo
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import timedelta
from flask_login import LoginManager, UserMixin, login_user, current_user, logout_user, login_required
from flask_bcrypt import Bcrypt


# blog.py
# app.py
# models.py
# forms.py
# config.py
# routes.py


# Будущий проект - ecommerce
# 1) Витрина
# 2) Аккаунт
# 3) Корзина
# 4) Оформление
# 5) Админ-зона









app = Flask(__name__)

app.config['SECRET_KEY'] = '3254365h6k5g6kh7k5kjlhr5h4ouirhhh324'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
#'mysql+pymysql://root:1234@localhost/blog'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER'] =  'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True 
app.config['MAIL_USERNAME'] = 'abc'
app.config['MAIL_PASSWORD'] = 'abcpasswd'


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(40), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self):
        return f"User('{self.username}' - '{self.email}')"


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(2048), nullable=False)
    content = db.Column(db.Text, nullable=False)
    dateCreation = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, default=1)

    def __repr__(self):
        return f"Article('{self.title}' - '{self.dateCreation}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=6)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('This username is exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('This email is exists')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

posts = [
    {
        'author': 'Ivan Petrov',
        'title': 'Samsung Phones',
        'content': 'A post about Samusng...',
        'dateCreation': '01/05/2020'
    },
    {
        'author': 'Steve Jackson',
        'title': 'Intel processors',
        'content': 'A post about Intel processors',
        'dateCreation': '02/05/2020'
    }
]

# 404, 500, 403
@app.errorhandler(404)
def e404():
    # return redirect('/')
    return '<h1>Страница не найдена - blog</h1>', 404


@app.route("/")
def home():
    print(session)
    return render_template('home.html', posts=posts)

# ЧПУ
# mysitee.com/ phone / samsung / a28
# mysitee.com/phone/lenovo/b28
# mysitee.com/ phone / htc / a28



@app.route("/phone/<brand>/<model>")
def about(brand, model):
    return f'BRAND={brand}, MODEL={model}'
    #print(session)
    #return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    print(session)
    if current_user.is_authenticated:
        return redirect('/')
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account was created', 'success')
        return redirect('/login')
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    print(session)
    if current_user.is_authenticated:
        return redirect('/')
    form = LoginForm()
    # article = Article.query.first()
    # form.email.data = article.title
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data, duration = timedelta(days=5))
            next_page = request.args.get('next')
            if next_page :
                return redirect(next_page)
            else :
                return redirect('/')
            
        else:
            flash('Login Unsuccessful. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
@login_required
def logout():
    print(session)
    logout_user()
    return redirect('/')


@app.route("/profile")
@login_required
def account():
    return render_template('profile.html', title='Profile')

if __name__ == '__main__':
    app.run(debug=True)
