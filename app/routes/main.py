from flask import Blueprint, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.models import User

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    return render_template('index.jinja')

# Temporary admin route to see all users
@main_bp.route('/admin/users')
@login_required
def admin_users():
    # Only allow access if user_id == 1 (admin)
    if current_user.id != 1:
        flash("Access denied. Admin only.", "danger")
        return redirect(url_for('main.index'))
    
    users = User.query.order_by(User.id).all()
    return render_template('admin_users.jinja', users=users)