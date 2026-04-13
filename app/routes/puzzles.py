from flask import Blueprint, render_template, redirect, url_for, flash, current_app, request
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from app import db
from app.forms import PuzzleCreationForm
from app.models import Puzzle

puzzles_bp = Blueprint('puzzles', __name__)

@puzzles_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    form = PuzzleCreationForm()
    
    if form.validate_on_submit():
        # Handle image upload
        image_file = form.image.data
        if image_file:
            filename = secure_filename(image_file.filename)
            # Add uniqueness to prevent overwriting
            unique_filename = f"user_{current_user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)   # Ensure folder exists
            
            save_path = os.path.join(upload_folder, unique_filename)
            image_file.save(save_path)
            
            # Create puzzle
            puzzle = Puzzle(
                title=form.title.data,
                description=form.description.data,
                image_filename=unique_filename,
                answer=form.answer.data.strip().lower(),
                difficulty=form.difficulty.data,
                user_id=current_user.id
            )
            
            db.session.add(puzzle)
            db.session.commit()
            
            flash('Your puzzle has been created successfully!', 'success')
            return redirect(url_for('puzzles.list_puzzles'))
    
    return render_template('create_puzzle.html', form=form)

# Puzzle Listing Page
@puzzles_bp.route('/list')
def list_puzzles():
    puzzles = Puzzle.query.order_by(Puzzle.created_at.desc()).all()
    return render_template('list_puzzle.html', puzzles=puzzles)

# Puzzle Playing Page
@puzzles_bp.route('/play/<int:puzzle_id>', methods=['GET', 'POST'])
def play(puzzle_id):
    puzzle = Puzzle.query.get_or_404(puzzle_id)
    
    if request.method == 'POST':
        user_answer = request.form.get('answer', '').strip().lower() # case insensitive and whitespace trimmed
        correct_answer = puzzle.answer.strip().lower()
        
        if user_answer == correct_answer:
            flash('🎉 Correct! Well done!', 'success')
            return redirect(url_for('puzzles.list_puzzles'))
        else:
            flash('❌ Wrong answer. Try again!', 'danger')
    
    return render_template('play_puzzle.html', puzzle=puzzle)