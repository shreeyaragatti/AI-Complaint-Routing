import re
import math
import datetime
from database import Database

class ComplaintAI:
    def __init__(self, db):
        self.db = db
        self.category_keywords = {
            'Water Supply': ['water', 'pipe', 'leakage', 'leak', 'flooding', 'supply', 'tap', 'drainage', 'sewer', 'rain', 'drain'],
            'Electricity': ['power', 'electricity', 'light', 'outage', 'transformer', 'wire', 'cable', 'voltage', 'bulb', 'electric'],
            'Roads & Transport': ['road', 'pothole', 'traffic', 'transport', 'bus', 'street', 'signal', 'bridge', 'accident', 'vehicle'],
            'Sanitation': ['garbage', 'waste', 'sanitation', 'cleanliness', 'dirty', 'trash', 'refuse', 'dustbin', 'sewage', 'toilet'],
            'Healthcare': ['hospital', 'medicine', 'doctor', 'health', 'ambulance', 'clinic', 'disease', 'patient', 'nurse'],
            'Education': ['school', 'college', 'teacher', 'education', 'student', 'classroom', 'exam', 'university', 'learning'],
            'Public Safety': ['crime', 'theft', 'assault', 'fire', 'police', 'dangerous', 'safety', 'emergency', 'accident', 'violence'],
            'Environment': ['pollution', 'air', 'noise', 'tree', 'green', 'forest', 'smoke', 'chemical', 'environment', 'wildlife'],
            'Housing': ['house', 'building', 'rent', 'apartment', 'housing', 'property', 'landlord', 'construction', 'collapse'],
            'Public Transport': ['bus', 'train', 'metro', 'railway', 'station', 'ticket', 'commute', 'public transport', 'airport']
        }
        
        self.severity_keywords = {
            'CRITICAL': ['emergency', 'life threatening', 'death', 'fire', 'explosion', 'flood', 'collapse', 'critical', 'urgent', 'immediate danger', 'major accident'],
            'HIGH': ['major', 'serious', 'severe', 'dangerous', 'urgent', 'hazard', 'broken', 'leaking', 'flooding', 'severe damage', 'major leakage', 'school'],
            'MEDIUM': ['moderate', 'damage', 'problem', 'issue', 'broken', 'not working', 'inconvenient', 'medium'],
            'LOW': ['minor', 'small', 'cosmetic', 'slight', 'low', 'minor issue', 'small problem']
        }
        
        self.urgency_keywords = {
            'Immediate': ['emergency', 'life threatening', 'death', 'fire', 'explosion', 'immediate', 'critical', 'urgent', 'right now'],
            'Within 24 hours': ['urgent', 'serious', 'major', 'severe', 'dangerous', 'within 24', 'asap'],
            'Within 48 hours': ['important', 'should be fixed', 'soon', 'within 2 days'],
            'Within a week': ['can wait', 'later', 'next week', 'schedule', 'planned']
        }
        
        self.departments = {
            'Water Supply': 'Water Management Department',
            'Electricity': 'Electricity Board',
            'Roads & Transport': 'Public Works Department',
            'Sanitation': 'Sanitation Corporation',
            'Healthcare': 'Health Department',
            'Education': 'Education Department',
            'Public Safety': 'Police Department / Fire Services',
            'Environment': 'Environmental Protection Agency',
            'Housing': 'Housing & Urban Development',
            'Public Transport': 'Transport Department'
        }
        
        self.sla_hours = {
            'CRITICAL': (1, 4),
            'HIGH': (2, 8),
            'MEDIUM': (4, 24),
            'LOW': (8, 48)
        }
        
        self._category_model = None
        self._vectorizer = None
        self._trained = False
    
    def _extract_features(self, text):
        text_lower = text.lower()
        features = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            features[f'cat_{category}'] = score
        
        features['text_length'] = len(text)
        features['word_count'] = len(text.split())
        features['has_numbers'] = 1 if re.search(r'\d', text) else 0
        features['has_location_indicators'] = 1 if any(w in text_lower for w in ['near', 'at', 'in front of', 'behind', 'beside', 'opposite', 'road', 'street', 'area', 'locality', 'sector']) else 0
        features['has_time_indicators'] = 1 if any(w in text_lower for w in ['since', 'morning', 'evening', 'night', 'yesterday', 'today', 'hours', 'days', 'ago', 'now']) else 0
        
        return features
    
    def classify_category(self, text):
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = sum(2 if kw in text_lower else 0 for kw in keywords)
            bonus = 0
            for kw in keywords:
                if kw in text_lower:
                    if any(pre in text_lower for pre in ['major ', 'severe ', 'serious ', 'broken ']):
                        bonus += 0.5
                    if text_lower.count(kw) > 1:
                        bonus += 1
            scores[category] = score + bonus
        
        if not scores or max(scores.values()) == 0:
            return 'General Complaint'
        
        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 5, 1.0)
        
        if confidence < 0.3:
            return 'General Complaint'
        return best
    
    def classify_severity(self, text, category):
        text_lower = text.lower()
        scores = {}
        
        for severity, keywords in self.severity_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[severity] = score
        
        category_keywords_map = {
            'Water Supply': ['leak', 'flood', 'pipe', 'water'],
            'Electricity': ['power', 'outage', 'fire', 'spark'],
            'Roads & Transport': ['accident', 'pothole', 'major', 'dangerous'],
            'Sanitation': ['garbage', 'drainage', 'sewage', 'overflow'],
            'Healthcare': ['emergency', 'ambulance', 'death', 'critical'],
            'Public Safety': ['crime', 'fire', 'theft', 'assault', 'dangerous']
        }
        
        if category in category_keywords_map:
            for kw in category_keywords_map[category]:
                if kw in text_lower:
                    scores['HIGH'] = scores.get('HIGH', 0) + 1
        
        if not scores or max(scores.values()) == 0:
            return 'MEDIUM'
        
        best = max(scores, key=scores.get)
        return best
    
    def determine_urgency(self, text, severity):
        text_lower = text.lower()
        scores = {}
        
        for urgency, keywords in self.urgency_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[urgency] = score
        
        if severity == 'CRITICAL':
            scores['Immediate'] = scores.get('Immediate', 0) + 3
        elif severity == 'HIGH':
            scores['Within 24 hours'] = scores.get('Within 24 hours', 0) + 2
        elif severity == 'MEDIUM':
            scores['Within 48 hours'] = scores.get('Within 48 hours', 0) + 1
        
        if not scores:
            return 'Within 48 hours'
        
        return max(scores, key=scores.get)
    
    def calculate_priority_score(self, text, severity, category):
        score = 50.0
        
        severity_scores = {'CRITICAL': 30, 'HIGH': 20, 'MEDIUM': 10, 'LOW': 5}
        score += severity_scores.get(severity, 10)
        
        text_lower = text.lower()
        
        if any(w in text_lower for w in ['since morning', 'since yesterday', 'since days', 'since hours']):
            score += 10
        
        if any(w in text_lower for w in ['flooding', 'major', 'severe', 'dangerous', 'emergency']):
            score += 10
        
        if any(w in text_lower for w in ['school', 'hospital', 'children', 'elderly', 'public place']):
            score += 8
        
        if any(w in text_lower for w in ['multiple', 'several', 'many', 'all', 'entire']):
            score += 5
        
        if len(text) > 100:
            score += 3
        
        score = max(0, min(100, score))
        return round(score, 1)
    
    def predict_sla(self, severity):
        min_hours, max_hours = self.sla_hours.get(severity, (4, 24))
        return f"{min_hours}-{max_hours} hours"
    
    def find_similar_complaints(self, text, threshold=0.4):
        conn = self.db.get_connection()
        all_complaints = conn.execute('SELECT id, text FROM complaints ORDER BY created_at DESC').fetchall()
        conn.close()
        
        text_words = set(re.findall(r'\w+', text.lower()))
        text_words = {w for w in text_words if len(w) > 2}
        
        similar_count = 0
        for complaint in all_complaints:
            other_words = set(re.findall(r'\w+', complaint['text'].lower()))
            other_words = {w for w in other_words if len(w) > 2}
            
            if not text_words or not other_words:
                continue
            
            intersection = len(text_words & other_words)
            union = len(text_words | other_words)
            similarity = intersection / union if union > 0 else 0
            
            if similarity >= threshold:
                similar_count += 1
        
        return similar_count
    
    def train_classifier(self):
        self._trained = True
    
    def process_complaint(self, text, complainant_name='', contact='', location=''):
        category = self.classify_category(text)
        severity = self.classify_severity(text, category)
        urgency = self.determine_urgency(text, severity)
        priority_score = self.calculate_priority_score(text, severity, category)
        department = self.departments.get(category, 'General Administration')
        similar_cases = self.find_similar_complaints(text)
        predicted_sla = self.predict_sla(severity)
        
        complaint_id = self.db.insert_complaint(
            text, category, severity, priority_score, department, urgency,
            similar_cases, predicted_sla, complainant_name, contact, location
        )
        
        return {
            'success': True,
            'complaint_id': complaint_id,
            'category': category,
            'severity': severity,
            'priority_score': priority_score,
            'department': department,
            'urgency': urgency,
            'similar_cases': similar_cases,
            'predicted_sla': predicted_sla,
            'status': 'Pending',
            'timestamp': datetime.datetime.now().isoformat()
        }
