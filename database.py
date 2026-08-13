import sqlite3
import datetime
import os

DB_PATH = 'complaints.db'

EXPECTED_COLUMNS = [
    ('preprocessed_text', 'TEXT'),
    ('category', 'TEXT'),
    ('severity', 'TEXT'),
    ('emotion', 'TEXT'),
    ('priority_score', 'REAL'),
    ('department', 'TEXT'),
    ('officer', 'TEXT'),
    ('urgency', 'TEXT'),
    ('similar_cases', 'INTEGER DEFAULT 0'),
    ('predicted_sla', 'TEXT'),
    ('location_analysis', 'TEXT'),
    ('historical_data', 'TEXT'),
    ('status', "TEXT DEFAULT 'Pending'"),
    ('complainant_name', 'TEXT'),
    ('contact', 'TEXT'),
    ('location', 'TEXT'),
    ('created_at', "TEXT DEFAULT CURRENT_TIMESTAMP"),
    ('updated_at', 'TEXT'),
    ('resolved_at', 'TEXT'),
]


class Database:
    def init_db(self):
        conn = sqlite3.connect(DB_PATH)
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS complaints (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                text TEXT NOT NULL,
                preprocessed_text TEXT,
                category TEXT,
                severity TEXT,
                emotion TEXT,
                priority_score REAL,
                department TEXT,
                officer TEXT,
                urgency TEXT,
                similar_cases INTEGER DEFAULT 0,
                predicted_sla TEXT,
                location_analysis TEXT,
                historical_data TEXT,
                status TEXT DEFAULT 'Pending',
                complainant_name TEXT,
                contact TEXT,
                location TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT,
                resolved_at TEXT
            )
        ''')
        conn.commit()

        existing = {row[1] for row in conn.execute('PRAGMA table_info(complaints)').fetchall()}
        for col_name, col_type in EXPECTED_COLUMNS:
            if col_name not in existing:
                conn.execute(f'ALTER TABLE complaints ADD COLUMN {col_name} {col_type}')
        conn.commit()
        conn.close()
    
    def get_connection(self):
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    
    def insert_complaint(self, text, preprocessed_text, category, severity, emotion, priority_score, 
                        department, officer, urgency, similar_cases, predicted_sla, 
                        location_analysis, historical_data, complainant_name, contact, location):
        conn = self.get_connection()
        cursor = conn.execute('''
            INSERT INTO complaints (text, preprocessed_text, category, severity, emotion, priority_score, 
                                   department, officer, urgency, similar_cases, predicted_sla, 
                                   location_analysis, historical_data, complainant_name, contact, location)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (text, preprocessed_text, category, severity, emotion, priority_score, 
              department, officer, urgency, similar_cases, predicted_sla, 
              location_analysis, historical_data, complainant_name, contact, location))
        complaint_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return complaint_id
    
    def get_all_complaints(self):
        conn = self.get_connection()
        complaints = conn.execute('SELECT * FROM complaints ORDER BY created_at DESC').fetchall()
        conn.close()
        return [dict(c) for c in complaints]
    
    def get_complaint(self, complaint_id):
        conn = self.get_connection()
        complaint = conn.execute('SELECT * FROM complaints WHERE id = ?', (complaint_id,)).fetchone()
        conn.close()
        return dict(complaint) if complaint else None
    
    def update_status(self, complaint_id, status):
        conn = self.get_connection()
        conn.execute('UPDATE complaints SET status = ?, updated_at = ? WHERE id = ?',
                     (status, datetime.datetime.now().isoformat(), complaint_id))
        conn.commit()
        conn.close()
    
    def resolve_complaint(self, complaint_id):
        conn = self.get_connection()
        conn.execute('UPDATE complaints SET status = ?, resolved_at = ?, updated_at = ? WHERE id = ?',
                     ('Resolved', datetime.datetime.now().isoformat(), datetime.datetime.now().isoformat(), complaint_id))
        conn.commit()
        conn.close()
    
    def get_analytics(self):
        conn = self.get_connection()
        
        total = conn.execute('SELECT COUNT(*) as c FROM complaints').fetchone()['c']
        
        by_category = [dict(r) for r in conn.execute('''
            SELECT category, COUNT(*) as count FROM complaints 
            WHERE category IS NOT NULL GROUP BY category ORDER BY count DESC
        ''').fetchall()]
        
        by_severity = [dict(r) for r in conn.execute('''
            SELECT severity, COUNT(*) as count FROM complaints 
            WHERE severity IS NOT NULL GROUP BY severity ORDER BY count DESC
        ''').fetchall()]
        
        by_status = [dict(r) for r in conn.execute('''
            SELECT status, COUNT(*) as count FROM complaints GROUP BY status ORDER BY count DESC
        ''').fetchall()]
        
        by_department = [dict(r) for r in conn.execute('''
            SELECT department, COUNT(*) as count FROM complaints 
            WHERE department IS NOT NULL GROUP BY department ORDER BY count DESC
        ''').fetchall()]
        
        by_emotion = [dict(r) for r in conn.execute('''
            SELECT emotion, COUNT(*) as count FROM complaints 
            WHERE emotion IS NOT NULL GROUP BY emotion ORDER BY count DESC
        ''').fetchall()]
        
        by_officer = [dict(r) for r in conn.execute('''
            SELECT officer, COUNT(*) as count FROM complaints 
            WHERE officer IS NOT NULL GROUP BY officer ORDER BY count DESC
        ''').fetchall()]
        
        avg_priority = conn.execute('SELECT AVG(priority_score) as avg FROM complaints').fetchone()['avg']
        
        recent = [dict(r) for r in conn.execute('''
            SELECT id, text, category, severity, emotion, priority_score, department, officer, status, created_at 
            FROM complaints ORDER BY created_at DESC LIMIT 10
        ''').fetchall()]
        
        conn.close()
        
        return {
            'total': total,
            'by_category': by_category,
            'by_severity': by_severity,
            'by_status': by_status,
            'by_department': by_department,
            'by_emotion': by_emotion,
            'by_officer': by_officer,
            'avg_priority': round(avg_priority, 1) if avg_priority else 0,
            'recent': recent
        }
