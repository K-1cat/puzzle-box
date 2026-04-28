from app import create_app, db
from app.models import User

def seed_database():
    app = create_app()
    
    with app.app_context():
        # Delete existing data
        db.session.query(User).delete()
        db.session.commit()

        # Create all tables
        db.create_all()
        
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if admin_user:
            print("Admin user already exists.")
        else:
            # Create admin user
            admin_user = User(username='admin')
            admin_user.set_password('password123')
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("Admin user created successfully.")
            print("Username: admin")
            print("Password: password123")

if __name__ == '__main__':
    seed_database()
