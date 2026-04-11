import os
from flask import Blueprint, current_app, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from app import db
from datetime import datetime
from app.forms import PuzzleCreationForm
from app.models import Puzzle

puzzles_bp = Blueprint('puzzles', __name__)

@puzzles_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PuzzleCreationForm()
    
    if form.validate_on_submit():        
        # Create puzzle in database
        puzzle = Puzzle(
            title=form.title.data,
            description=form.description.data,
            answer=form.answer.data.strip().lower(),
            difficulty=form.difficulty.data,
            user_id=current_user.id
        )
        
        db.session.add(puzzle)
        db.session.commit()
        
        flash('Your puzzle has been created successfully!', 'success')
        return redirect(url_for('main.index'))
    
    return render_template('create_puzzle.html', form=form)