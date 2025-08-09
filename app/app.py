from flask import Flask, render_template, request, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ini-adalah-kunci-rahasia-yang-sangat-aman'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    role = db.Column(db.String(50), default='user') # 

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    owner = db.relationship('User', backref=db.backref('notes', lazy=True))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.password == password: 
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Username atau password salah.')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    user_notes = Note.query.filter_by(owner_id=current_user.id).all()
    return render_template('dashboard.html', notes=user_notes)

@app.route('/note/<int:note_id>')
@login_required
def view_note(note_id):
    note = Note.query.get(note_id)
    if not note:
        abort(404)
    return render_template('note.html', note=note)

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def profile_edit():
    if request.method == 'POST':
        for key, value in request.form.items():
            if hasattr(current_user, key) and key not in ['id']:
                setattr(current_user, key, value)
        db.session.commit()
        flash('Profil berhasil diperbarui!')
        return redirect(url_for('profile_edit'))
    return render_template('profile_edit.html')

@app.route('/admin')
@login_required
def admin_panel():
    if current_user.role != 'admin':
        abort(403) 
    all_users = User.query.all()
    return render_template('admin.html', users=all_users)

@app.before_request
def create_tables():
    if not hasattr(app, 'is_db_initialized'):
        with app.app_context():
            db.create_all()
            if not User.query.first():
                db.session.add(User(username='admin', password='admin_password', role='admin'))
                db.session.add(User(username='alice', password='password123', role='user'))
                db.session.add(User(username='bob', password='password123', role='user'))
                db.session.commit()
                db.session.add(Note(content="Ini adalah catatan rahasia milik Alice.", owner_id=2))
                db.session.add(Note(content="Ini adalah catatan super rahasia milik Bob.", owner_id=3))
                db.session.commit()
        app.is_db_initialized = True

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)