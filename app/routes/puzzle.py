from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user
from app import db
from app.models import Puzzle

puzzle_bp = Blueprint('puzzle', __name__)

@puzzle_bp.route('/puzzles')
def list_puzzles():
    if current_user.is_authenticated:
        return render_template('list.html', puzzles=db.session.query(Puzzle).all())
    
    return redirect(url_for('auth.login'))