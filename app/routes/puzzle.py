from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required
from app import db
from app.models import Puzzle, PuzzleType, TextPuzzle, ImagePuzzle
from werkzeug.utils import secure_filename
import os

puzzle_bp = Blueprint('puzzle', __name__)

@puzzle_bp.route('/puzzles')
def list_puzzles():
    return render_template('list.html', puzzles=db.session.query(Puzzle).all())


@puzzle_bp.route('/puzzles/<int:puzzle_id>', methods=['GET', 'POST'])
def view_puzzle(puzzle_id):
    puzzle = db.session.query(Puzzle).filter_by(id=puzzle_id).first_or_404()

    if request.method == 'POST':
        answer = request.form.get('answer')
        if answer == puzzle.answer:
            flash('Correct answer!', 'success')
        else:
            flash('Incorrect answer.', 'danger')
        return redirect(request.url)
    
    if puzzle.puzzle_type == PuzzleType.TEXT:
        text_puzzle = db.session.query(TextPuzzle).filter_by(puzzle_id=puzzle_id).first()
        return render_template('view.html', puzzle=puzzle, text_puzzle=text_puzzle)
    elif puzzle.puzzle_type == PuzzleType.IMAGE:
        image_puzzle = db.session.query(ImagePuzzle).filter_by(puzzle_id=puzzle_id).first()
        return render_template('view.html', puzzle=puzzle, image_puzzle=image_puzzle)
    else:
        return render_template('view.html', puzzle=None)


@puzzle_bp.route('/puzzles/create')
@login_required
def create_puzzle():
    return render_template('create.html')


@puzzle_bp.route('/puzzles/create/text', methods=['GET', 'POST'])
@login_required
def create_text_puzzle():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        answer = request.form.get('answer')
        
        if not title or not content or not answer:
            flash('Title, content, and answer are required.', 'danger')
            return redirect(request.url)
        
        # Create puzzle
        puzzle = Puzzle(title=title, puzzle_type=PuzzleType.TEXT, answer=answer, author_id=current_user.id)
        db.session.add(puzzle)
        db.session.flush()  # Get puzzle.id
        
        # Create text puzzle
        text_puzzle = TextPuzzle(puzzle_id=puzzle.id, content=content)
        db.session.add(text_puzzle)
        db.session.commit()
        
        flash('Text puzzle created successfully!', 'success')
        return redirect(url_for('puzzle.list_puzzles'))
    
    return render_template('create_text.html')


@puzzle_bp.route('/puzzles/create/image', methods=['GET', 'POST'])
@login_required
def create_image_puzzle():
    if request.method == 'POST':
        title = request.form.get('title')
        image = request.files.get('image')
        answer = request.form.get('answer')
        
        if not title or not image or not answer:
            flash('Title, image, and answer are required.', 'danger')
            return redirect(request.url)
        
        # Secure filename and save
        filename = secure_filename(image.filename)
        image_path = os.path.join('app', 'static', 'uploads', filename)
        image.save(image_path)
        
        # Create puzzle
        puzzle = Puzzle(title=title, puzzle_type=PuzzleType.IMAGE, answer=answer, author_id=current_user.id)
        db.session.add(puzzle)
        db.session.flush()
        
        # Create image puzzle
        image_puzzle = ImagePuzzle(puzzle_id=puzzle.id, image_filename=filename)
        db.session.add(image_puzzle)
        db.session.commit()
        
        flash('Image puzzle created successfully!', 'success')
        return redirect(url_for('puzzle.list_puzzles'))
    
    return render_template('create_image.html')