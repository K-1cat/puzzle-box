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
        image_filename = None
        
        # Handle image upload if provided
        if form.image.data:
            image_file = form.image.data
            filename = secure_filename(image_file.filename)
            unique_filename = f"user_{current_user.id}_{int(datetime.utcnow().timestamp())}_{filename}"
            
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            image_file.save(os.path.join(upload_folder, unique_filename))
            image_filename = unique_filename
        
        # Build config based on puzzle type
        config = {}
        if form.puzzle_type.data == 'image_text':
            config = {
                "type": "image_text",
                "answer": form.answer.data.strip().lower() if form.answer.data else ""
            }
        elif form.puzzle_type.data == 'dragdrop':
            config = {"type": "dragdrop", "items": []}   # Will be filled later with drag & drop data
        elif form.puzzle_type.data == 'letter_grid':
            config = {"type": "letter_grid", "grid": [], "words": []}
        
        puzzle = Puzzle(
            title=form.title.data,
            description=form.description.data,
            puzzle_type=form.puzzle_type.data,
            config=config,
            image_filename=image_filename,
            answer=form.answer.data.strip().lower() if form.puzzle_type.data == 'image_text' else None,
            difficulty=form.difficulty.data,
            user_id=current_user.id
        )
        
        db.session.add(puzzle)
        db.session.commit()
        
        flash('Puzzle created successfully!', 'success')
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