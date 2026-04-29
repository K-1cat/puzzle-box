import enum
from flask_login import UserMixin
from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'

    @property
    def is_admin(self):
        return self.id == 1


class PuzzleType(enum.Enum):
    TEXT = 'text'
    IMAGE = 'image'


class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    puzzle_type = db.Column(db.Enum(PuzzleType), nullable=False)
    answer = db.Column(db.String(100), nullable=True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f'<Puzzle {self.title}>'
    
    def is_text_puzzle(self):
        return self.puzzle_type == PuzzleType.TEXT

    def is_image_puzzle(self):
        return self.puzzle_type == PuzzleType.IMAGE
    

class TextPuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<TextPuzzle {self.id}>'


class ImagePuzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    puzzle_id = db.Column(db.Integer, db.ForeignKey('puzzle.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<ImagePuzzle {self.id}>'