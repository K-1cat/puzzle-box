from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FileField
from flask_wtf.file import FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError, Regexp
from app.models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(),
        Length(min=3, max=20),
        Regexp('^[a-zA-Z0-9_]+$', message='Username can only contain letters, numbers and underscores (_).')
    ])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is already taken. Please choose another.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class PuzzleCreationForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=100)])
    description = TextAreaField('Description (optional)')
    image = FileField('Puzzle Image', validators=[
        FileRequired(message='Please upload an image!'),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Only image files allowed!')
    ])
    answer = StringField('Answer', validators=[DataRequired(), Length(max=100)])
    difficulty = SelectField('Difficulty', choices=[('Easy', 'Easy'), ('Medium', 'Medium'), ('Hard', 'Hard')], validators=[DataRequired()])
    submit = SubmitField('Submit Puzzle')