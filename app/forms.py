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
    title = StringField('Puzzle Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description (optional)')
    
    puzzle_type = SelectField('Puzzle Type', choices=[
        ('image_text', 'Image + Text Answer'),
        ('dragdrop', 'Drag & Drop'),
        ('letter_grid', 'Letter Grid / Word Search')
    ], default='image_text')
    
    image = FileField('Background Image (optional for some types)', validators=[
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])
    
    answer = StringField('Correct Answer (for Image/Text type)', validators=[Length(max=100)])
    difficulty = SelectField('Difficulty', choices=[
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard')
    ], default='Medium')
    
    submit = SubmitField('Create Puzzle')