from flask import Blueprint, render_template
from flask_login import login_required, current_user
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.html')

# Temporary admin route to see all users
@main_bp.route('/admin/users')
@login_required
def admin_users():
    if not current_user.username == "admin":
        return "Access denied", 403
    
    users = User.query.all()
    return render_template('admin_users.html', users=users)