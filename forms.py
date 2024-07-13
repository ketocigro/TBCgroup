from flask_wtf import FlaskForm
from wtforms import StringField,  SelectField,  SubmitField, IntegerField, PasswordField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError, NumberRange, Length, InputRequired
from models import Guitar, Bass, Keyboard, Microphone, Accessory, Comment, User, Card, Basket

class AddItemForm(FlaskForm):
    category = SelectField('Category', choices=[('guitar', 'Guitar'), ('bass', 'Bass'), ('keyboard', 'Keyboard'), ('microphone', 'Microphone'), ('accessory', 'Accessory')], validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    price = IntegerField('Price', validators=[DataRequired(), NumberRange(min=0)])
    img = StringField('Image URL', validators=[DataRequired()])
    id = IntegerField('ID')
    submit = SubmitField('Add Item')



class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])

    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class CommentForm(FlaskForm):
    comment = TextAreaField('Comment', validators=[DataRequired()])
    submit = SubmitField('Submit Comment')

class CardForm(FlaskForm):
    account_number = StringField('Account Number', validators=[DataRequired(), Length(min= 20, max=20, message='Account number must be between 1 and 20 characters') ])
    address = TextAreaField('Address', validators=[DataRequired(), Length(max=200)])
    phone_number = StringField('Phone Number', validators=[DataRequired(), Length(max=20)])
    submit = SubmitField('Submit')

class BasketForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[InputRequired(), NumberRange(min=1)])