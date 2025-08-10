import uuid
from flask import Flask, render_template, request, redirect, url_for, session, abort, jsonify
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from jinja2 import Environment
from collections import defaultdict
import time

app = Flask(__name__)
app.secret_key = 'a-very-complex-and-secure-secret-key-for-hard-mode'

csrf = CSRFProtect(app)

RATE_LIMIT = 5  # 
RATE_LIMIT_WINDOW = 10  
request_counts = defaultdict(list)

@app.before_request
def rate_limit_check():
    if request.endpoint and 'api' in request.endpoint:
        ip = request.remote_addr
        now = time.time()
        
        request_counts[ip] = [t for t in request_counts[ip] if now - t < RATE_LIMIT_WINDOW]
        
        if len(request_counts[ip]) >= RATE_LIMIT:
            return jsonify({"error": "Too Many Requests, please try again later."}), 429
        
        request_counts[ip].append(now)

USERS = {
    "e7a8c1d2-a3b4-4c5d-8e9f-0a1b2c3d4e5f": {'username': 'admin', 'password': 'password123', 'role': 'admin', 'name': 'Dr. Evelyn Reed'},
    "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d": {'username': 'manager', 'password': 'password123', 'role': 'manager', 'name': 'John Carter'},
    "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5a": {'username': 'employee', 'password': 'password123', 'role': 'employee', 'name': 'Alice Wong'}
}

PROJECTS = {
    "proj-a1a1-b2b2-c3c3": {'name': 'Project Chimera', 'description': 'Analisis data genetik rahasia untuk pengembangan serum baru.', 'owner_uuid': "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", 'assigned_users': ["e7a8c1d2-a3b4-4c5d-8e9f-0a1b2c3d4e5f", "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", "a1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5a"]},
    "proj-d4d4-e5e5-f6f6": {'name': 'Project Phoenix', 'description': 'Pengembangan sistem pertahanan siber generasi berikutnya. Sangat Rahasia.', 'owner_uuid': "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d", 'assigned_users': ["e7a8c1d2-a3b4-4c5d-8e9f-0a1b2c3d4e5f", "f1b2c3d4-e5f6-4a7b-8c9d-0e1f2a3b4c5d"]},
    "proj-g7g7-h8h8-i9i9": {'name': 'Project Hydra', 'description': 'Infrastruktur cloud internal untuk data korporat paling sensitif. Hanya untuk Admin.', 'owner_uuid': "e7a8c1d2-a3b4-4c5d-8e9f-0a1b2c3d4e5f", 'assigned_users': ["e7a8c1d2-a3b4-4c5d-8e9f-0a1b2c3d4e5f"]}
}

TASKS = {
    "task-001": {"project_id": "proj-a1a1-b2b2-c3c3", "title": "Analisis Sampel Genom Awal", "completed": True},
    "task-002": {"project_id": "proj-a1a1-b2b2-c3c3", "title": "Validasi Hasil Analisis dengan Tim Bio-Informatika", "completed": False},
    "task-003": {"project_id": "proj-d4d4-e5e5-f6f6", "title": "Setup Honeypot Firewall Rules", "completed": True},
    "task-004": {"project_id": "proj-d4d4-e5e5-f6f6", "title": "Lakukan Uji Penetrasi pada Server Staging", "completed": False},
}

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ReportForm(FlaskForm):
    title = StringField('Report Title', default='Laporan Status Proyek', validators=[DataRequired()])
    submit = SubmitField('Generate Report')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():  
        username = form.username.data
        password = form.password.data
        for user_id, user_data in USERS.items():
            if user_data['username'] == username and user_data['password'] == password:
                session['user_id'] = user_id
                session['user_role'] = user_data['role']
                session['user_name'] = user_data['name']
                return redirect(url_for('dashboard'))
        return render_template('login.html', form=form, error='Username atau password salah')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session: return redirect(url_for('login'))
    user_id = session['user_id']
    accessible_projects = {pid: pdata for pid, pdata in PROJECTS.items() if user_id in pdata['assigned_users']}
    return render_template('dashboard.html', projects=accessible_projects, USERS=USERS)

@app.route('/proyek/<proyek_uuid>')
def detail_proyek(proyek_uuid):
    if 'user_id' not in session: return redirect(url_for('login'))
    project = PROJECTS.get(proyek_uuid)
    if not project: abort(404)
    return render_template('proyek.html', project=project, project_uuid=proyek_uuid)

@app.route('/proyek/<proyek_uuid>/report', methods=['GET', 'POST'])
def generate_report(proyek_uuid):
    if 'user_id' not in session: return redirect(url_for('login'))
    project = PROJECTS.get(proyek_uuid)
    if not project: abort(404)
    
    form = ReportForm()
    if form.validate_on_submit():
        report_title = form.title.data
        template_string = f"<div class='container'><h1>{report_title}</h1><p>Ini adalah laporan yang dihasilkan untuk proyek: <strong>{project['name']}</strong>.</p></div>"
        rendered_html = Environment().from_string(template_string).render()
        return rendered_html
    return render_template('report_generator.html', project=project, form=form)

@app.route('/profil/<user_uuid>')
def detail_profil(user_uuid):
    if 'user_id' not in session: return redirect(url_for('login'))
    user = USERS.get(user_uuid)
    if not user: abort(404)
    return render_template('profil.html', user=user, user_uuid=user_uuid)

@app.route('/admin')
def panel_admin():
    if 'user_id' not in session: return redirect(url_for('login'))
    if session.get('user_role') != 'admin': abort(403)
    return render_template('admin.html', users=USERS)

@app.route('/api/proyek/<proyek_uuid>/tasks', endpoint='api_get_tasks')
def get_tasks(proyek_uuid):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    if proyek_uuid not in PROJECTS: return jsonify({"error": "Project not found"}), 404
    
    project_tasks = [task for task in TASKS.values() if task['project_id'] == proyek_uuid]
    leaked_user_uuids = PROJECTS[proyek_uuid]['assigned_users']
    
    return jsonify({"tasks": project_tasks, "leaked_assigned_user_uuids": leaked_user_uuids})

@app.route('/api/proyek/<proyek_uuid>/ganti_pemilik', methods=['POST'], endpoint='api_change_owner')
@csrf.exempt  
def change_owner(proyek_uuid):
    if 'user_id' not in session: return jsonify({"error": "Unauthorized"}), 401
    
    project = PROJECTS.get(proyek_uuid)
    if not project: return jsonify({"error": "Project not found"}), 404

    if project['owner_uuid'] != session['user_id']:
        return jsonify({"error": "Forbidden: Only the project owner can change ownership"}), 403

    new_owner_uuid = request.json.get('new_owner_uuid')
    if not new_owner_uuid or new_owner_uuid not in USERS:
        return jsonify({"error": "Invalid new owner UUID"}), 400

    project['owner_uuid'] = new_owner_uuid
    project['assigned_users'].append(new_owner_uuid)
    project['assigned_users'] = list(set(project['assigned_users'])) 
    
    return jsonify({"success": f"Project owner successfully changed to {USERS[new_owner_uuid]['name']}"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)