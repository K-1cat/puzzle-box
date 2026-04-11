# Puzzle Box

**A web platform where anyone can easily create, publish, and solve various puzzles.**

Puzzle Box is a full-stack web application that allows users to create original puzzles (escape-room style, logic puzzles, visual puzzles, etc.), publish them, and let others enjoy solving them.

## ✨ Features (Currently Implemented)
- Clean and responsive web interface
- Modular Flask architecture using Blueprints
- User authentication system (registration & login)
- Database management with SQLAlchemy
- Interactive puzzle solving page

## 🚀 Features (Planned / In Progress)
- File upload system for puzzle images
- Puzzle creation editor (image upload + hotspot / answer settings)
- Puzzle list with search and filtering
- User profile and created puzzles management
- Multiple puzzle types support (visual, logic, word, etc)
- Add social features (likes, comments, rankings)

## 🔧 Tech Stack

**Backend**
- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF

**Frontend**
- HTML5 + Jinja2 Templates
- CSS3
- JavaScript (planned)

**Database**
- SQLite (Development)
- PostgreSQL (Planned for Production)

**Others**
- Pillow (Image processing)
- WTForms
- dotenv

## 📁 Project Structure

```bash
puzzle-box/
├── app/                          # Main Flask application package
│   ├── __init__.py               # Flask app initialization
│   ├── config.py                 # Configuration settings
│   ├── models.py                 # Database models
│   ├── forms.py                  # WTForms definitions
│   ├── routes/                   # Route blueprints
│   │   ├── __init__.py
│   │   ├── auth.py               # Authentication routes
│   │   ├── puzzles.py            # Puzzle list, creation, and play routes
│   │   └── main.py               # Main application routes
│   ├── templates/                # Jinja2 HTML templates
│   │   ├── admin_users.html      # Admin template
│   │   ├── base.html             # Base template
│   │   ├── create_puzzle.html    # Puzzle Creation template
│   │   ├── index.html            # Homepage template
│   │   ├── list_puzzle.html      # Puzzle Listing template
│   │   ├── login.html            # Login template
│   │   ├── play_puzzle.html      # Puzzle Playing template
│   │   └── register.html         # Register template
│   └── static/                   # Static files (CSS, JS, images)
│       └── css/
├── uploads/                      # User-uploaded files
├── instance/                     # SQLite database files
├── .venv/                        # Python virtual environment (gitignored)
├── .env                          # Environment variables (gitignored)
├── .gitignore
├── requirements.txt              # Python dependencies
├── run.py                        # Entry point to run the application
└── README.md
```

## 🏃 How to Run Locally

1. Clone the repository
    ```bash
    git clone https://github.com/K-1cat/puzzle-box.git
    cd puzzle-box
    ```

2. Create and activate a virtual environment
    ```bash
    python -m venv venv
    # Mac / Linux
    source venv/bin/activate
    # Windows
    venv\Scripts\activate
    ```

3. Install dependencies
    ```bash
    pip install -r requirements.txt
    ```

4. Run the application
    ```bash
    python run.py
    ```

5. Open your browser and go to http://127.0.0.1:5000
