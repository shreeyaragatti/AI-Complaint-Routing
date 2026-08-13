from flask import Flask, render_template, request, jsonify, session
import sqlite3
import datetime
import os
from ai_engine import ComplaintAI, Database

app = Flask(__name__)
app.secret_key = 'complaint-routing-secret-key-2026'
db = Database()
ai = ComplaintAI(db)

def get_db():
    conn = sqlite3.connect('complaints.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit')
def submit_page():
    return render_template('submit.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/complaint', methods=['POST'])
def submit_complaint():
    data = request.get_json()
    complaint_text = data.get('text', '').strip()
    complainant_name = data.get('name', '').strip()
    contact = data.get('contact', '').strip()
    location = data.get('location', '').strip()
    
    if not complaint_text:
        return jsonify({'success': False, 'error': 'Complaint text is required'}), 400
    
    result = ai.process_complaint(complaint_text, complainant_name, contact, location)
    return jsonify(result)

@app.route('/api/complaints')
def get_complaints():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    complaints = conn.execute('SELECT * FROM complaints ORDER BY created_at DESC').fetchall()
    conn.close()
    return jsonify([dict(c) for c in complaints])

@app.route('/api/complaints/<int:complaint_id>')
def get_complaint(complaint_id):
    conn = get_db()
    conn.row_factory = sqlite3.Row
    complaint = conn.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,)).fetchone()
    conn.close()
    if complaint:
        return jsonify(dict(complaint))
    return jsonify({'error': 'Not found'}), 404

@app.route('/api/analytics')
def get_analytics():
    conn = get_db()
    conn.row_factory = sqlite3.Row
    
    stats = {}
    
    total = conn.execute('SELECT COUNT(*) as c FROM complaints').fetchone()['c']
    stats['total'] = total
    
    stats['by_category'] = [dict(r) for r in conn.execute('''
        SELECT category, COUNT(*) as count FROM complaints 
        WHERE category IS NOT NULL GROUP BY category ORDER BY count DESC
    ''').fetchall()]
    
    stats['by_severity'] = [dict(r) for r in conn.execute('''
        SELECT severity, COUNT(*) as count FROM complaints 
        WHERE severity IS NOT NULL GROUP BY severity ORDER BY count DESC
    ''').fetchall()]
    
    stats['by_status'] = [dict(r) for r in conn.execute('''
        SELECT status, COUNT(*) as count FROM complaints 
        GROUP BY status ORDER BY count DESC
    ''').fetchall()]
    
    stats['by_department'] = [dict(r) for r in conn.execute('''
        SELECT department, COUNT(*) as count FROM complaints 
        WHERE department IS NOT NULL GROUP BY department ORDER BY count DESC
    ''').fetchall()]
    
    stats['by_emotion'] = [dict(r) for r in conn.execute('''
        SELECT emotion, COUNT(*) as count FROM complaints 
        WHERE emotion IS NOT NULL GROUP BY emotion ORDER BY count DESC
    ''').fetchall()]
    
    stats['by_officer'] = [dict(r) for r in conn.execute('''
        SELECT officer, COUNT(*) as count FROM complaints 
        WHERE officer IS NOT NULL GROUP BY officer ORDER BY count DESC
    ''').fetchall()]
    
    avg_priority = conn.execute('SELECT AVG(priority_score) as avg FROM complaints').fetchone()['avg']
    stats['avg_priority'] = round(avg_priority, 1) if avg_priority else 0
    
    stats['recent'] = [dict(r) for r in conn.execute('''
        SELECT id, text, category, severity, emotion, priority_score, department, officer, status, created_at 
        FROM complaints ORDER BY created_at DESC LIMIT 10
    ''').fetchall()]
    
    conn.close()
    return jsonify(stats)

@app.route('/api/complaints/<int:complaint_id>/status', methods=['PUT'])
def update_status(complaint_id):
    data = request.get_json()
    status = data.get('status', '').strip()
    if not status:
        return jsonify({'error': 'Status required'}), 400
    
    conn = get_db()
    conn.execute('UPDATE complaints SET status = ?, updated_at = ? WHERE id = ?',
                 (status, datetime.datetime.now().isoformat(), complaint_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

@app.route('/api/complaints/<int:complaint_id>/resolve', methods=['PUT'])
def resolve_complaint(complaint_id):
    conn = get_db()
    conn.execute('UPDATE complaints SET status = ?, resolved_at = ?, updated_at = ? WHERE id = ?',
                 ('Resolved', datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), complaint_id))
    conn.commit()
    conn.close()
    return jsonify({'success': True})

if __name__ == '__main__':
    db.init_db()
    ai.train_classifier()
    app.run(debug=True, host='0.0.0.0', port=5000)
