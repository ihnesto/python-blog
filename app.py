from flask import Flask, render_template, redirect
from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError
from wtforms.validators import Email, DataRequired, EqualTo


app = Flask(__name__)
app.config['SECRET_KEY'] = 'dfdsgbkoeufdhiuoroyxmunfyriwjzmeyzo'

@app.route('/')
def index() :
    return render_template('index.html')

class RegisterForm(FlaskForm) :
    username = StringField('USERNAME', validators=[ DataRequired() ])
    email = StringField('EMAIL', validators=[ Email() ])
    password1 = StringField('PASSWORD', validators=[ DataRequired() ])
    password2 = StringField('PASSWORD AGAIN', validators=[ DataRequired(), EqualTo('password1') ])

    def validate_password2(self, field) :
        if len(field.data) < 8 or len(field.data) > 13 :
            raise ValidationError('My validator Password must be from 8 to 13 characters')

   


@app.route('/register', methods=[ 'GET', 'POST' ])
def register() :
    reg = RegisterForm()

    if reg.validate_on_submit():
        # reg.username.data
        # reg.email.data
        # db.session.add(User)




        return redirect('/success')

    return render_template('register.html', regform = reg)

if __name__ == '__main__' :
    app.run(debug=True)
