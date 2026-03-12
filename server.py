from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from dotenv import load_dotenv
import os
import sqlite3
from datetime import datetime
import pandas as pd
from io import BytesIO

load_dotenv()

app = Flask(__name__, static_folder='static', template_folder='templates')
app.secret_key = os.getenv('SECRET_KEY')

# Database connection
DB_PATH = 'students.db'

def get_db_connection():
    """Create a database connection"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize database if needed"""
    if not os.path.exists(DB_PATH):
        print("⚠️  Database not found. Please run the migration script first.")
    else:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM personal_info")
        count = cursor.fetchone()[0]
        print(f"✅ Database connected. Total students: {count}")
        conn.close()

# Initialize on startup
init_db()

def format_date(date_value):
    """Helper function to format dates"""
    if date_value == 'N/A' or not date_value or str(date_value).strip() == '':
        return 'N/A'
    
    try:
        date_str = str(date_value).strip()
        
        # Handle different date formats
        if 'T' in date_str or '+' in date_str:
            date_obj = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        elif ' ' in date_str and ':' in date_str:
            date_obj = datetime.strptime(date_str.split(' ')[0], "%Y-%m-%d")
        elif '.' in date_str and len(date_str) == 10:
            date_obj = datetime.strptime(date_str, "%d.%m.%Y")
        else:
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
        
        return date_obj.strftime("%B %d, %Y")
    except Exception as e:
        return str(date_value)

@app.route('/')
def index():
    return render_template('index.html', details=None)

@app.route('/learning')
def learning_page():
    return render_template('learning.html')

@app.route('/learning.html')
def learning_html():
    return render_template('learning.html')

@app.route('/setting')
def setting_page():
    return render_template('setting.html')

@app.route('/setting.html')
def setting_html():
    return render_template('setting.html')

@app.route('/validation')
def validation_page():
    return render_template('validation.html')

@app.route('/validation.html')
def validation_html():
    return render_template('validation.html')

# Admin credentials
ADMIN_EMAIL = 'erpvcodez@gmail.com'
ADMIN_PASSWORD = 'Vcodez@123'

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        print(f"[LOGIN] Received data: {data}")
        
        if not data or 'email' not in data:
            print(f"[LOGIN] Email missing")
            return jsonify({
                "success": False,
                "message": "Email is required"
            }), 400
            
        email = data['email'].strip().lower()
        password = data.get('password', '').strip()
        phone = data.get('phone', '').strip()
        
        print(f"[LOGIN] Admin check: email={email}, password_provided={bool(password)}")
        
        # Check if this is admin login
        if email == ADMIN_EMAIL.lower() and password == ADMIN_PASSWORD:
            print(f"[LOGIN] Admin login successful")
            session['admin'] = True
            session['admin_email'] = email
            return jsonify({"success": True, "redirect": "/admin-dashboard", "type": "admin"})
        
        # If password was provided but email wasn't admin, it's invalid
        if password:
            print(f"[LOGIN] Password provided but not admin email")
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Otherwise, check student credentials (email + phone)
        if not phone:
            print(f"[LOGIN] Phone missing")
            return jsonify({
                "success": False,
                "message": "Email and phone are required"
            }), 400
        
        print(f"[LOGIN] Student login attempt: email={email}, phone={phone}")
        
        # Remove all non-digit characters from phone for flexible matching
        phone_normalized = ''.join(c for c in phone if c.isdigit())
        print(f"[LOGIN] Phone normalized: {phone_normalized}")

        # Query database for student
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get personal info
        cursor.execute('''
            SELECT * FROM personal_info 
            WHERE LOWER(email) = ?
            LIMIT 1
        ''', (email,))
        
        student = cursor.fetchone()
        
        print(f"[LOGIN] Student found: {student is not None}")
        
        if not student:
            conn.close()
            print(f"[LOGIN] Student not found in database")
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Verify phone number matches (normalize both for comparison)
        db_phone_normalized = ''.join(c for c in (student['phone_number'] or '') if c.isdigit())
        print(f"[LOGIN] DB phone normalized: {db_phone_normalized}, Input phone normalized: {phone_normalized}")
        print(f"[LOGIN] Phone match: {db_phone_normalized == phone_normalized}")
        
        if db_phone_normalized != phone_normalized:
            conn.close()
            print(f"[LOGIN] Phone mismatch")
            return jsonify({
                "success": False,
                "message": "Invalid credentials"
            }), 401
        
        # Get attendance data
        cursor.execute('SELECT * FROM attendance WHERE LOWER(email) = ? LIMIT 1', (email,))
        attendance = cursor.fetchone()
        
        # Get performance data
        cursor.execute('SELECT * FROM performance WHERE LOWER(email) = ? LIMIT 1', (email,))
        performance = cursor.fetchone()
        
        conn.close()
        
        # Store user details in session - include all data from all three tables
        session['details'] = {
            'name': student['name'],
            'email': student['email'],
            'phone': student['phone_number'],
            'time': student['session_timings'] or 'N/A',
            'days': student['days'] or 'N/A',
            'domain': student['domain'],
            'college': student['college'] or 'N/A',
            'dept': student['dept'] or 'N/A',
            'trainer': student['trainer'] or 'N/A',
            'mode': student['mode'] or 'N/A',
            'registration_date': format_date(student['registration_date']),
            'start_date': format_date(student['session_start_date']),
            'end_date': format_date(student['session_end_date']),
            'batch': student['batch'] or 'N/A',
            # Attendance data
            'attendance_count': attendance['attendance_count'] if attendance else 'N/A',
            'stipend_eligibility': attendance['stipend_eligibility'] if attendance else 'N/A',
            'stipend_reason': attendance['stipend_reason'] if attendance else 'N/A',
            'per': 0,
            'attendance_percentage': 0,
            # Performance data
            'project_title': performance['project_title'] if performance else 'N/A',
            'assessment1': performance['assessment_1'] if performance else 0,
            'assessment2': performance['assessment_2'] if performance else 0,
            'task': performance['task'] if performance else 0,
            'project_mark': performance['project_marks'] if performance else 0,
            'final_validation': performance['final_validation'] if performance else 0,
            'total_mark': performance['total_marks'] if performance else 0
        }

        return jsonify({"success": True, "redirect": "/details"})

    except Exception as e:
        print(f"Login error: {str(e)}")
        return jsonify({
            "success": False,
            "message": f"An error occurred during login. Please try again."
        }), 500

@app.route('/details')
def details():
    if 'details' not in session:
        return redirect(url_for('index'))
    
    # Get student email from session
    email = session['details']['email']
    
    # Fetch fresh data from database instead of using cached session
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get personal info
    cursor.execute('SELECT * FROM personal_info WHERE LOWER(email) = ? LIMIT 1', (email.lower(),))
    student = cursor.fetchone()
    
    # Get attendance data
    cursor.execute('SELECT * FROM attendance WHERE LOWER(email) = ? LIMIT 1', (email.lower(),))
    attendance = cursor.fetchone()
    
    # Get performance data
    cursor.execute('SELECT * FROM performance WHERE LOWER(email) = ? LIMIT 1', (email.lower(),))
    performance = cursor.fetchone()
    
    conn.close()
    
    if not student:
        return redirect(url_for('index'))
    
    # Calculate attendance percentage
    attendance_percentage = 0
    if attendance and attendance['attendance_count']:
        try:
            attendance_percentage = float(attendance['attendance_count'])
        except (ValueError, TypeError):
            attendance_percentage = 0
    
    # Build fresh details object with latest data from database
    details = {
        'name': student['name'],
        'email': student['email'],
        'phone': student['phone_number'],
        'time': student['session_timings'] or 'N/A',
        'days': student['days'] or 'N/A',
        'domain': student['domain'],
        'college': student['college'] or 'N/A',
        'dept': student['dept'] or 'N/A',
        'trainer': student['trainer'] or 'N/A',
        'mode': student['mode'] or 'N/A',
        'registration_date': format_date(student['registration_date']),
        'start_date': format_date(student['session_start_date']),
        'end_date': format_date(student['session_end_date']),
        'batch': student['batch'] or 'N/A',
        # Attendance data - FRESH FROM DATABASE
        'attendance_count': attendance['attendance_count'] if attendance else 'N/A',
        'stipend_eligibility': attendance['stipend_eligibility'] if attendance else 'N/A',
        'stipend_reason': attendance['stipend_reason'] if attendance else 'N/A',
        'per': attendance_percentage,
        'attendance_percentage': attendance_percentage,
        # Performance data - FRESH FROM DATABASE
        'project_title': performance['project_title'] if performance else 'N/A',
        'assessment1': performance['assessment_1'] if performance else 0,
        'assessment2': performance['assessment_2'] if performance else 0,
        'task': performance['task'] if performance else 0,
        'project_mark': performance['project_marks'] if performance else 0,
        'final_validation': performance['final_validation'] if performance else 0,
        'total_mark': performance['total_marks'] if performance else 0
    }
    
    return render_template('details.html', details=details)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin' not in session or not session.get('admin'):
        return redirect(url_for('index'))
    
    # Fetch all student data from database
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM personal_info ORDER BY name')
    students_raw = cursor.fetchall()
    
    # Calculate statistics
    cursor.execute('SELECT domain, COUNT(*) as count FROM personal_info GROUP BY domain')
    stats_raw = cursor.fetchall()
    conn.close()
    
    # Convert to dictionary for frontend
    all_students = []
    for row in students_raw:
        student_data = {
            'name': row['name'],
            'email': row['email'],
            'phone': row['phone_number'],
            'college': row['college'] or 'N/A',
            'dept': row['dept'] or 'N/A',
            'domain': row['domain'],
            'mode': row['mode'] or 'N/A',
            'trainer': row['trainer'] or 'N/A',
            'batch': row['batch'] or 'N/A',
            'registration_date': format_date(row['registration_date']),
            'start_date': format_date(row['session_start_date']),
            'end_date': format_date(row['session_end_date'])
        }
        all_students.append(student_data)
    
    # Build stats
    stats = {
        'total': len(all_students),
        'ml': 0,
        'ds': 0,
        'da': 0
    }
    
    for stat_row in stats_raw:
        domain = stat_row['domain']
        count = stat_row['count']
        if domain == 'ML':
            stats['ml'] = count
        elif domain == 'DS':
            stats['ds'] = count
        elif domain == 'DA':
            stats['da'] = count
    
    return render_template('admin_dashboard.html', students=all_students, stats=stats)

@app.route('/admin-get-data', methods=['POST'])
def admin_get_data():
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        trainer = data.get('trainer', '').strip() if data.get('trainer') else None
        batch = data.get('batch', '').strip() if data.get('batch') else None
        domain = data.get('domain', '').strip() if data.get('domain') else None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query
        query = 'SELECT * FROM personal_info WHERE 1=1'
        params = []
        
        if trainer:
            query += ' AND LOWER(trainer) = LOWER(?)'
            params.append(trainer)
        
        if batch:
            query += ' AND LOWER(batch) = LOWER(?)'
            params.append(batch)
        
        if domain:
            query += ' AND LOWER(domain) = LOWER(?)'
            params.append(domain)
        
        query += ' ORDER BY name'
        
        cursor.execute(query, params)
        students_raw = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        results = []
        for row in students_raw:
            student_data = {
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone_number'],
                'college': row['college'] or 'N/A',
                'dept': row['dept'] or 'N/A',
                'domain': row['domain'],
                'mode': row['mode'] or 'N/A',
                'trainer': row['trainer'] or 'N/A',
                'batch': row['batch'] or 'N/A',
                'registration_date': format_date(row['registration_date']),
                'start_date': format_date(row['session_start_date']),
                'end_date': format_date(row['session_end_date'])
            }
            results.append(student_data)
        
        return jsonify({"success": True, "data": results, "count": len(results)})
    
    except Exception as e:
        print(f"Admin data fetch error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An error occurred while fetching data"
        }), 500

@app.route('/admin-search', methods=['POST'])
def admin_search():
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        search_term = data.get('search', '').strip().lower()
        stipend = data.get('stipend', '').strip() if data.get('stipend') else None
        batch = data.get('batch', '').strip() if data.get('batch') else None
        domain = data.get('domain', '').strip() if data.get('domain') else None
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Build dynamic query with search and join with attendance table for stipend filter
        query = '''
        SELECT p.* FROM personal_info p
        LEFT JOIN attendance a ON LOWER(p.email) = LOWER(a.email)
        WHERE (LOWER(p.name) LIKE ? OR LOWER(p.email) LIKE ? OR LOWER(p.phone_number) LIKE ?)
        '''
        params = [f'%{search_term}%', f'%{search_term}%', f'%{search_term}%']
        
        if stipend:
            query += ' AND LOWER(a.stipend_eligibility) LIKE LOWER(?)'
            params.append(f'%{stipend}%')
        
        if batch:
            query += ' AND LOWER(p.batch) = LOWER(?)'
            params.append(batch)
        
        if domain:
            query += ' AND LOWER(p.domain) = LOWER(?)'
            params.append(domain)
        
        query += ' ORDER BY p.name'
        
        cursor.execute(query, params)
        students_raw = cursor.fetchall()
        conn.close()
        
        # Convert to list of dictionaries
        results = []
        for row in students_raw:
            student_data = {
                'name': row['name'],
                'email': row['email'],
                'phone': row['phone_number'],
                'college': row['college'] or 'N/A',
                'dept': row['dept'] or 'N/A',
                'domain': row['domain'],
                'mode': row['mode'] or 'N/A',
                'trainer': row['trainer'] or 'N/A',
                'batch': row['batch'] or 'N/A',
                'registration_date': format_date(row['registration_date']),
                'start_date': format_date(row['session_start_date']),
                'end_date': format_date(row['session_end_date'])
            }
            results.append(student_data)
        
        return jsonify({"success": True, "data": results, "count": len(results)})
    
    except Exception as e:
        print(f"Admin search error: {str(e)}")
        return jsonify({
            "success": False,
            "message": "An error occurred while searching"
        }), 500

@app.route('/admin-student-edit')
def admin_student_edit():
    if 'admin' not in session or not session.get('admin'):
        return redirect(url_for('index'))
    
    email = request.args.get('email', '').lower()
    if not email:
        return redirect(url_for('admin_dashboard'))
    
    return render_template('admin_student_edit.html')

@app.route('/api/student/<email>')
def get_student(email):
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Get personal info
        cursor.execute('SELECT * FROM personal_info WHERE LOWER(email) = ?', (email.lower(),))
        student = cursor.fetchone()
        
        if not student:
            conn.close()
            return jsonify({"success": False, "message": "Student not found"}), 404
        
        # Get attendance info
        cursor.execute('SELECT * FROM attendance WHERE LOWER(email) = ?', (email.lower(),))
        attendance = cursor.fetchone()
        
        # Get performance info
        cursor.execute('SELECT * FROM performance WHERE LOWER(email) = ?', (email.lower(),))
        performance = cursor.fetchone()
        
        conn.close()
        
        student_data = {
            # Personal Information
            'id': student['id'],
            'name': student['name'],
            'email': student['email'],
            'phone_number': student['phone_number'],
            'college': student['college'] or '',
            'registration_date': student['registration_date'] or '',
            'dept': student['dept'] or '',
            'domain': student['domain'],
            'mode': student['mode'] or '',
            'session_timings': student['session_timings'] or '',
            'days': student['days'] or '',
            'session_start_date': student['session_start_date'] or '',
            'session_end_date': student['session_end_date'] or '',
            'trainer': student['trainer'] or '',
            'batch': student['batch'] or '',
            # Attendance Information
            'attendance_count': attendance['attendance_count'] if attendance else '',
            'stipend_eligibility': attendance['stipend_eligibility'] if attendance else '',
            'stipend_reason': attendance['stipend_reason'] if attendance else '',
            # Performance Information
            'project_title': performance['project_title'] if performance else '',
            'assessment_1': performance['assessment_1'] if performance else '',
            'assessment_2': performance['assessment_2'] if performance else '',
            'task': performance['task'] if performance else '',
            'project_marks': performance['project_marks'] if performance else '',
            'final_validation': performance['final_validation'] if performance else '',
            'total_marks': performance['total_marks'] if performance else ''
        }
        
        return jsonify({"success": True, "student": student_data})
    
    except Exception as e:
        print(f"Error fetching student: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred"}), 500

@app.route('/api/student/<email>/update', methods=['POST'])
def update_student(email):
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        print(f"[UPDATE] Email: {email}, Data received: {data}")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Update personal info
        cursor.execute('''
            UPDATE personal_info 
            SET phone_number = ?, college = ?, dept = ?, domain = ?,
                mode = ?, session_timings = ?, days = ?, 
                registration_date = ?, session_start_date = ?, session_end_date = ?,
                trainer = ?, batch = ?
            WHERE LOWER(email) = ?
        ''', (
            data.get('phone_number', ''),
            data.get('college', ''),
            data.get('dept', ''),
            data.get('domain', ''),
            data.get('mode', ''),
            data.get('session_timings', ''),
            data.get('days', ''),
            data.get('registration_date', ''),
            data.get('session_start_date', ''),
            data.get('session_end_date', ''),
            data.get('trainer', ''),
            data.get('batch', ''),
            email.lower()
        ))
        print(f"[UPDATE] Personal info rows affected: {cursor.rowcount}")
        
        # Update or insert attendance info
        cursor.execute('''
            INSERT INTO attendance (email, attendance_count, stipend_eligibility, stipend_reason)
            VALUES (?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                attendance_count = excluded.attendance_count,
                stipend_eligibility = excluded.stipend_eligibility,
                stipend_reason = excluded.stipend_reason
        ''', (
            email.lower(),
            data.get('attendance_count', ''),
            data.get('stipend_eligibility', ''),
            data.get('stipend_reason', '')
        ))
        print(f"[UPDATE] Attendance rows affected: {cursor.rowcount}")
        
        # Update or insert performance info
        cursor.execute('''
            INSERT INTO performance (email, project_title, assessment_1, assessment_2, task, project_marks, final_validation, total_marks)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(email) DO UPDATE SET
                project_title = excluded.project_title,
                assessment_1 = excluded.assessment_1,
                assessment_2 = excluded.assessment_2,
                task = excluded.task,
                project_marks = excluded.project_marks,
                final_validation = excluded.final_validation,
                total_marks = excluded.total_marks
        ''', (
            email.lower(),
            data.get('project_title', ''),
            data.get('assessment_1', ''),
            data.get('assessment_2', ''),
            data.get('task', ''),
            data.get('project_marks', ''),
            data.get('final_validation', ''),
            data.get('total_marks', '')
        ))
        print(f"[UPDATE] Performance rows affected: {cursor.rowcount}")
        
        conn.commit()
        conn.close()
        print(f"[UPDATE] ✅ All updates committed successfully for {email}")
        
        return jsonify({"success": True, "message": "Student data updated successfully"})
    
    except Exception as e:
        print(f"[UPDATE] ❌ Error updating student: {str(e)}")
        return jsonify({"success": False, "message": "An error occurred while updating"}), 500

@app.route('/api/add-candidate', methods=['POST'])
def add_candidate():
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['name', 'email', 'phone_number', 'domain']
        for field in required_fields:
            if not data.get(field):
                return jsonify({"success": False, "message": f"Missing required field: {field}"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Check if email already exists
        cursor.execute('SELECT email FROM personal_info WHERE LOWER(email) = ?', (data.get('email', '').lower(),))
        if cursor.fetchone():
            return jsonify({"success": False, "message": "Email already exists in database"}), 400
        
        # Insert into personal_info table
        cursor.execute('''
            INSERT INTO personal_info (
                name, email, phone_number, college, dept, domain, mode,
                session_timings, days, registration_date, session_start_date,
                session_end_date, trainer, batch, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
        ''', (
            data.get('name', ''),
            data.get('email', '').lower(),
            data.get('phone_number', ''),
            data.get('college', ''),
            data.get('dept', ''),
            data.get('domain', ''),
            data.get('mode', ''),
            data.get('session_timings', ''),
            data.get('days', ''),
            data.get('registration_date', ''),
            data.get('session_start_date', ''),
            data.get('session_end_date', ''),
            data.get('trainer', ''),
            data.get('batch', '')
        ))
        print(f"[ADD-CANDIDATE] Personal info inserted for {data.get('email')}")
        
        # Insert into attendance table
        cursor.execute('''
            INSERT INTO attendance (email, attendance_count, stipend_eligibility, stipend_reason)
            VALUES (?, ?, ?, ?)
        ''', (
            data.get('email', '').lower(),
            data.get('attendance_count', ''),
            data.get('stipend_eligibility', ''),
            data.get('stipend_reason', '')
        ))
        print(f"[ADD-CANDIDATE] Attendance info inserted for {data.get('email')}")
        
        # Insert into performance table
        cursor.execute('''
            INSERT INTO performance (
                email, project_title, assessment_1, assessment_2, task,
                project_marks, final_validation, total_marks
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            data.get('email', '').lower(),
            data.get('project_title', ''),
            data.get('assessment_1', ''),
            data.get('assessment_2', ''),
            data.get('task', ''),
            data.get('project_marks', ''),
            data.get('final_validation', ''),
            data.get('total_marks', '')
        ))
        print(f"[ADD-CANDIDATE] Performance info inserted for {data.get('email')}")
        
        conn.commit()
        conn.close()
        
        print(f"[ADD-CANDIDATE] ✅ New candidate added successfully: {data.get('email')}")
        return jsonify({"success": True, "message": "Candidate added successfully"})
    
    except Exception as e:
        print(f"[ADD-CANDIDATE] ❌ Error adding candidate: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/api/bulk-import-validate', methods=['POST'])
def bulk_import_validate():
    """Validate bulk import file and check for duplicates"""
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        if 'file' not in request.files:
            return jsonify({"success": False, "message": "No file provided"}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({"success": False, "message": "No file selected"}), 400
        
        # Read file (CSV or Excel with multi-sheet support)
        try:
            if file.filename.endswith('.xlsx') or file.filename.endswith('.xls'):
                # Read file bytes to avoid file pointer issues
                file_bytes = file.read()
                from io import BytesIO
                file_obj = BytesIO(file_bytes)
                
                # Check if file has multiple sheets
                xls = pd.ExcelFile(file_obj)
                sheet_names = xls.sheet_names
                
                # If it has the standard three sheets, merge them
                if 'PERSONAL INFORMATION' in sheet_names and 'ATTENDANCE' in sheet_names and 'OVERALL PERFORMANCE' in sheet_names:
                    # Reset file pointer
                    file_obj = BytesIO(file_bytes)
                    
                    # Read all three sheets
                    df_personal = pd.read_excel(file_obj, sheet_name='PERSONAL INFORMATION')
                    file_obj = BytesIO(file_bytes)
                    df_attendance = pd.read_excel(file_obj, sheet_name='ATTENDANCE')
                    file_obj = BytesIO(file_bytes)
                    df_performance = pd.read_excel(file_obj, sheet_name='OVERALL PERFORMANCE')
                    
                    print(f"[BULK-IMPORT] Sheets found: Personal={len(df_personal)}, Attendance={len(df_attendance)}, Performance={len(df_performance)}")
                    
                    # Merge on email (case-insensitive)
                    df_personal['Email_lower'] = df_personal['Email'].str.lower().str.strip()
                    df_attendance['Email_lower'] = df_attendance['Email'].str.lower().str.strip()
                    df_performance['Email_lower'] = df_performance['Email'].str.lower().str.strip()
                    
                    # Merge all sheets
                    df = df_personal.merge(df_attendance[['Email_lower', 'ATTENDNACE', 'STIPEND', 'REASON']], 
                                          on='Email_lower', how='left')
                    df = df.merge(df_performance[['Email_lower', 'Project title', 'Assesment 1', 'Assesment 2', 'Task', 'Project marks', 'Final validation', 'Total']], 
                                 on='Email_lower', how='left')
                    
                    # Remove the helper column
                    df = df.drop('Email_lower', axis=1)
                    print(f"[BULK-IMPORT] Merged dataframe shape: {df.shape}, columns: {list(df.columns)}")
                else:
                    # Single sheet or different structure, read first sheet
                    file_obj = BytesIO(file_bytes)
                    df = pd.read_excel(file_obj)
            else:
                df = pd.read_csv(file)
        except Exception as e:
            print(f"[BULK-IMPORT-VALIDATE] File read error: {str(e)}")
            return jsonify({"success": False, "message": f"Error reading file: {str(e)}"}), 400
        
        # Required columns for all three tables (exact names from Excel files)
        required_columns = {
            'Personal Information': ['Name', 'Email', 'Phone Number', 'Domain'],
            'Attendance': ['Email', 'ATTENDNACE', 'STIPEND', 'REASON'],
            'Overall Performance': ['Email', 'Project title', 'Assesment 1', 'Assesment 2', 'Task', 'Project marks', 'Final validation', 'Total']
        }
        
        # Check for required columns (case-insensitive matching)
        missing_columns = {}
        df_columns_lower = {col.lower().strip(): col for col in df.columns}  # Map lowercase to original
        
        for section, columns in required_columns.items():
            missing = [col for col in columns if col.lower() not in df_columns_lower]
            if missing:
                missing_columns[section] = missing
        
        if missing_columns:
            missing_str = '; '.join([f"{k}: {', '.join(v)}" for k, v in missing_columns.items()])
            return jsonify({
                "success": False, 
                "message": f"Missing required columns: {missing_str}"
            }), 400
        
        # Create a mapping of lowercase to original column names
        column_mapping = {col.lower().strip(): col for col in df.columns}
        
        # Convert column names to lowercase for consistency
        df.columns = [col.lower().strip() for col in df.columns]
        
        # Validation checks
        validation_report = {
            "total_rows": len(df),
            "valid_rows": 0,
            "duplicate_emails_in_file": [],
            "duplicate_emails_in_db": [],
            "missing_required_fields": [],
            "errors": []
        }
        
        # Get existing emails from database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT LOWER(email) FROM personal_info')
        existing_emails = {row[0] for row in cursor.fetchall()}
        conn.close()
        
        # Track emails seen in file
        seen_emails = set()
        valid_records = []  # Store only valid records
        
        # Store mapping in session for later use
        session['bulk_import_column_mapping'] = column_mapping
        
        for idx, row in df.iterrows():
            row_num = idx + 2  # Excel row number (1-indexed, +1 for header)
            email = str(row.get('email', '')).strip().lower()
            
            # Check for missing required fields (using lowercase column names)
            missing_fields = []
            if not str(row.get('name', '')).strip():
                missing_fields.append('Name')
            if not email:
                missing_fields.append('Email')
            if not str(row.get('phone number', '')).strip():
                missing_fields.append('Phone Number')
            if not str(row.get('domain', '')).strip():
                missing_fields.append('Domain')
            
            if missing_fields:
                validation_report["missing_required_fields"].append({
                    "row": row_num,
                    "email": email or "N/A",
                    "fields": missing_fields
                })
                continue
            
            # Check for duplicates in file
            if email in seen_emails:
                validation_report["duplicate_emails_in_file"].append({
                    "row": row_num,
                    "email": email
                })
                continue
            
            # Check for duplicates in database
            if email in existing_emails:
                validation_report["duplicate_emails_in_db"].append({
                    "row": row_num,
                    "email": email
                })
                continue
            
            # This record is valid - add to list
            seen_emails.add(email)
            valid_records.append(row.to_dict())
            validation_report["valid_rows"] += 1
        
        # Store only VALID records in session for import
        session['bulk_import_data'] = valid_records
        session['bulk_import_df_columns'] = list(df.columns)
        
        print(f"[BULK-IMPORT-VALIDATE] Valid records to import: {len(valid_records)}")
        
        # Allow import if there are valid rows (duplicates will be skipped)
        can_import = (
            validation_report["valid_rows"] > 0 and
            len(validation_report["missing_required_fields"]) == 0
        )
        
        return jsonify({
            "success": True,
            "can_import": can_import,
            "validation_report": validation_report
        })
    
    except Exception as e:
        print(f"[BULK-IMPORT-VALIDATE] Error: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/api/bulk-import-process', methods=['POST'])
def bulk_import_process():
    """Process and import validated bulk data"""
    if 'admin' not in session or not session.get('admin'):
        return jsonify({"success": False, "message": "Unauthorized"}), 401
    
    try:
        if 'bulk_import_data' not in session:
            return jsonify({"success": False, "message": "No validation data found. Please validate first."}), 400
        
        records = session['bulk_import_data']
        
        if not records:
            return jsonify({"success": False, "message": "No valid records to import"}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        
        imported_count = 0
        errors = []
        
        for record in records:
            try:
                # Map lowercase column names from Excel (exact names from ML Portal.xlsx, DS Portal.xlsx, DA Portal.xlsx)
                email = str(record.get('email', '')).strip().lower()
                
                # Insert into personal_info (mapping Excel columns to DB fields)
                cursor.execute('''
                    INSERT INTO personal_info (
                        name, email, phone_number, college, dept, domain, mode,
                        session_timings, days, registration_date, session_start_date,
                        session_end_date, trainer, batch, created_at
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
                ''', (
                    str(record.get('name', '')).strip(),
                    email,
                    str(record.get('phone number', '')).strip(),
                    str(record.get('college', '')).strip() if record.get('college') else '',
                    str(record.get('dept', '')).strip() if record.get('dept') else '',
                    str(record.get('domain', '')).strip(),
                    str(record.get('mode', '')).strip() if record.get('mode') else '',
                    str(record.get('session timings', '')).strip() if record.get('session timings') else '',
                    str(record.get('days', '')).strip() if record.get('days') else '',
                    str(record.get('registration date', '')).strip() if record.get('registration date') else '',
                    str(record.get('session start date', '')).strip() if record.get('session start date') else '',
                    str(record.get('session end date', '')).strip() if record.get('session end date') else '',
                    str(record.get('trainer', '')).strip() if record.get('trainer') else '',
                    str(record.get('batch', '')).strip() if record.get('batch') else ''
                ))
                
                # Insert into attendance (mapping Excel columns: ATTENDNACE -> attendance_count, STIPEND -> stipend_eligibility, REASON -> stipend_reason)
                cursor.execute('''
                    INSERT INTO attendance (email, attendance_count, stipend_eligibility, stipend_reason)
                    VALUES (?, ?, ?, ?)
                ''', (
                    email,
                    str(record.get('attendnace', '')).strip() if record.get('attendnace') else '',
                    str(record.get('stipend', '')).strip() if record.get('stipend') else '',
                    str(record.get('reason', '')).strip() if record.get('reason') else ''
                ))
                
                # Insert into performance (mapping Excel columns: Assesment 1 & 2, Final validation -> final_validation, Total -> total_marks)
                cursor.execute('''
                    INSERT INTO performance (
                        email, project_title, assessment_1, assessment_2, task,
                        project_marks, final_validation, total_marks
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    email,
                    str(record.get('project title', '')).strip() if record.get('project title') else '',
                    str(record.get('assesment 1', '')).strip() if record.get('assesment 1') else '',
                    str(record.get('assesment 2', '')).strip() if record.get('assesment 2') else '',
                    str(record.get('task', '')).strip() if record.get('task') else '',
                    str(record.get('project marks', '')).strip() if record.get('project marks') else '',
                    str(record.get('final validation', '')).strip() if record.get('final validation') else '',
                    str(record.get('total', '')).strip() if record.get('total') else ''
                ))
                
                imported_count += 1
                print(f"[BULK-IMPORT] Imported: {email}")
            
            except Exception as e:
                errors.append(f"Error importing {record.get('email', 'unknown')}: {str(e)}")
                print(f"[BULK-IMPORT] Error: {str(e)}")
        
        conn.commit()
        conn.close()
        
        # Clear session data
        session.pop('bulk_import_data', None)
        session.pop('bulk_import_df_columns', None)
        session.pop('bulk_import_column_mapping', None)
        
        print(f"[BULK-IMPORT] ✅ Imported {imported_count} records successfully")
        
        return jsonify({
            "success": True,
            "imported_count": imported_count,
            "errors": errors,
            "message": f"✅ Successfully imported {imported_count} new student(s)!"
        })
    
    except Exception as e:
        print(f"[BULK-IMPORT-PROCESS] Error: {str(e)}")
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500

@app.route('/admin-logout')
def admin_logout():
    session.pop('admin', None)
    session.pop('admin_email', None)
    return redirect(url_for('index'))

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
