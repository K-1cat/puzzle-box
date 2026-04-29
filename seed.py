import os

from app import create_app, db
from app.models import User, Puzzle, TextPuzzle, ImagePuzzle, PuzzleType


def seed_database():
    app = create_app()

    with app.app_context():
        # Ensure tables exist
        db.create_all()

        # Remove existing uploaded files for image puzzles
        upload_folder = os.path.join(app.root_path, 'static', 'uploads')
        for image in db.session.query(ImagePuzzle).all():
            if image.image_filename:
                image_path = os.path.join(upload_folder, image.image_filename)
                if os.path.exists(image_path):
                    os.remove(image_path)
                    print(f'Removed uploaded image: {image.image_filename}')

        # Remove existing puzzle data only
        db.session.query(ImagePuzzle).delete()
        db.session.query(TextPuzzle).delete()
        db.session.query(Puzzle).delete()
        db.session.commit()

        # Ensure admin user exists
        admin_user = User.query.filter_by(username='admin').first()
        if not admin_user:
            admin_user = User(username='admin')
            admin_user.set_password('1234')
            db.session.add(admin_user)
            db.session.commit()
            print('Admin user created successfully.')
            print('Username: admin')
            print('Password: 1234')
        else:
            print('Admin user already exists.')

        # Create a single text puzzle
        text_puzzle = Puzzle(title='Sample Text Puzzle', puzzle_type=PuzzleType.TEXT, answer='answer', author_id=admin_user.id)
        db.session.add(text_puzzle)
        db.session.flush()

        puzzle_content = TextPuzzle(puzzle_id=text_puzzle.id, content='This is the first example text puzzle. Solve it!')
        db.session.add(puzzle_content)
        db.session.commit()

        print('Text puzzle created successfully.')
        print('Puzzle ID:', text_puzzle.id)


if __name__ == '__main__':
    seed_database()
