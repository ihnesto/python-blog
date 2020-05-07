from flask import Flask, render_template, redirect, make_response, request, session
# from flask_wtf import FlaskForm
# from wtforms import StringField, ValidationError
# from wtforms.validators import Email, DataRequired, EqualTo
from flask_login import LoginManager, UserMixin


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfdsgbkoeufdhiuoroyxmunfyriwjzmeyzo'

login_manager = LoginManager(app)

class User(db.Model,  UserMixin) :
    username = db.Column(db.String)
    passwd = db.Column(db.String)
    email = db.....

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login')
def index() :
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        passwd = form.passwd.data
        email = form.email.data
        #user = User(username = username, email = email)
        user = User.query.filter_by(username = username, email = email, passwd = passwd)
       
        if user :
            login_user(user)
           
        if user.is_authenticated == True :
            doRemove
        else :
            print('No login')
    session['stage'] = ['Lenovo a4', 'Lenovo a5' ]
    res = make_response(render_template('index.html'))
    # res.set_cookie("userID", value="u123456", max_age = 60)
    # res.set_cookie("passwd", value="krjfglgoitopeldkf", max_age = 60 * 60 * 24 * 4)
    return res

@app.route('/remove-article')
def about() :
    user = session.get('user')
    if user == '' :
        return
    a = Article.query.filter_by(id= articleid).first()
    if a.userId == user :
        doRemove

    session['greet'] =  'greetings'
    # userid = request.cookies.get('userID')
    # passwd = request.cookies.get('passwd')

    return f"<h1>{stage}</h1>"


    
# class RegisterForm(FlaskForm) :
#     username = StringField('USERNAME', validators=[ DataRequired() ])
#     email = StringField('EMAIL', validators=[ Email() ])
#     password1 = StringField('PASSWORD', validators=[ DataRequired() ])
#     password2 = StringField('PASSWORD AGAIN', validators=[ DataRequired(), EqualTo('password1') ])

#     def validate_password2(self, field) :
#         if len(field.data) < 8 or len(field.data) > 13 :
#             raise ValidationError('My validator Password must be from 8 to 13 characters')

   


# @app.route('/register', methods=[ 'GET', 'POST' ])
# def register() :
#     reg = RegisterForm()

#     if reg.validate_on_submit():
#         # reg.username.data
#         # reg.email.data
#         # db.session.add(User)




#         return redirect('/success')

#     return render_template('register.html', regform = reg)

if __name__ == '__main__' :
    app.run(debug=True)
