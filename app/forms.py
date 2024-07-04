from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, FloatField
from wtforms.validators import DataRequired, Length, ValidationError
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    user_type = SelectField('Type of Service', choices=[('hospital', 'Hospital'), ('vendor', 'Vendor'), ('delivery', 'Delivery')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class OrderForm(FlaskForm):
    item = StringField('Item', validators=[DataRequired()])
    amount = FloatField('Amount', validators=[DataRequired()])
    urgency = BooleanField('Urgency')
    submit = SubmitField('Place Order')

