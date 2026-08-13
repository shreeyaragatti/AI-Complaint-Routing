import re
import math
import datetime
from collections import Counter
from database import Database

class TextPreprocessor:
    @staticmethod
    def normalize(text):
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', ' ', text)
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    @staticmethod
    def tokenize(text):
        return re.findall(r'\w+', text.lower())
    
    @staticmethod
    def remove_stopwords(tokens):
        stopwords = {'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                     'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
                     'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
                     'on', 'with', 'at', 'by', 'from', 'as', 'into', 'through', 'during',
                     'before', 'after', 'above', 'below', 'between', 'out', 'off', 'over',
                     'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when',
                     'where', 'why', 'how', 'all', 'each', 'every', 'both', 'few', 'more',
                     'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own',
                     'same', 'so', 'than', 'too', 'very', 'just', 'because', 'but', 'and',
                     'or', 'if', 'while', 'about', 'up', 'it', 'its', 'this', 'that', 'these',
                     'those', 'i', 'me', 'my', 'we', 'our', 'you', 'your', 'he', 'she', 'they',
                     'them', 'his', 'her', 'their', 'what', 'which', 'who', 'whom'}
        return [t for t in tokens if t not in stopwords and len(t) > 2]
    
    @staticmethod
    def extract_features(text):
        tokens = TextPreprocessor.tokenize(text)
        clean_tokens = TextPreprocessor.remove_stopwords(tokens)
        
        word_count = len(text.split())
        char_count = len(text)
        has_numbers = 1 if re.search(r'\d', text) else 0
        
        location_indicators = ['near', 'at', 'in front of', 'behind', 'beside', 'opposite',
                               'road', 'street', 'area', 'locality', 'sector', 'colony',
                               'near', 'beside', 'opposite', 'behind', 'in front of']
        has_location = 1 if any(ind in text.lower() for ind in location_indicators) else 0
        
        time_indicators = ['since', 'morning', 'evening', 'night', 'yesterday', 'today',
                           'hours', 'days', 'ago', 'now', 'since morning', 'since yesterday']
        has_time = 1 if any(ind in text.lower() for ind in time_indicators) else 0
        
        urgency_words = ['urgent', 'immediate', 'emergency', 'critical', 'asap', 'right now']
        urgency_count = sum(1 for w in urgency_words if w in text.lower())
        
        return {
            'word_count': word_count,
            'char_count': char_count,
            'has_numbers': has_numbers,
            'has_location': has_location,
            'has_time': has_time,
            'urgency_word_count': urgency_count,
            'tokens': clean_tokens
        }

class CategoryModel:
    def __init__(self):
        self.category_keywords = {
            'Water Supply': ['water', 'pipe', 'leakage', 'leak', 'flooding', 'supply', 'tap', 
                             'drainage', 'sewer', 'rain', 'drain', 'boring', 'tubewell', 'tank'],
            'Electricity': ['power', 'electricity', 'light', 'outage', 'transformer', 'wire', 
                            'cable', 'voltage', 'bulb', 'electric', 'current', 'meter', 'board'],
            'Roads & Transport': ['road', 'pothole', 'traffic', 'transport', 'bus', 'street', 
                                  'signal', 'bridge', 'accident', 'vehicle', 'car', 'bike', 'highway'],
            'Sanitation': ['garbage', 'waste', 'sanitation', 'cleanliness', 'dirty', 'trash', 
                           'refuse', 'dustbin', 'sewage', 'toilet', 'drain', 'sweeper'],
            'Healthcare': ['hospital', 'medicine', 'doctor', 'health', 'ambulance', 'clinic', 
                           'disease', 'patient', 'nurse', 'medical', 'treatment'],
            'Education': ['school', 'college', 'teacher', 'education', 'student', 'classroom', 
                          'exam', 'university', 'learning', 'principal', 'lecture'],
            'Public Safety': ['crime', 'theft', 'assault', 'fire', 'police', 'dangerous', 
                              'safety', 'emergency', 'accident', 'violence', 'robbery', 'snatching'],
            'Environment': ['pollution', 'air', 'noise', 'tree', 'green', 'forest', 'smoke', 
                            'chemical', 'environment', 'wildlife', 'dust', 'smog'],
            'Housing': ['house', 'building', 'rent', 'apartment', 'housing', 'property', 
                        'landlord', 'construction', 'collapse', 'flat', 'society'],
            'Public Transport': ['bus', 'train', 'metro', 'railway', 'station', 'ticket', 
                                 'commute', 'public transport', 'airport', 'rickshaw', 'taxi']
        }
    
    def predict(self, text, features):
        text_lower = text.lower()
        scores = {}
        
        for category, keywords in self.category_keywords.items():
            score = 0
            for kw in keywords:
                if kw in text_lower:
                    score += 2
                    if text_lower.count(kw) > 1:
                        score += 1
                    if any(pre in text_lower for pre in ['major ', 'severe ', 'serious ', 'broken ', 'no ']):
                        score += 0.5
            scores[category] = score
        
        if features['urgency_word_count'] > 0:
            for cat in scores:
                scores[cat] += features['urgency_word_count'] * 0.5
        
        if not scores or max(scores.values()) == 0:
            return 'General Complaint', 0.0
        
        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 4, 1.0)
        
        if confidence < 0.25:
            return 'General Complaint', confidence
        
        return best, confidence

class SeverityModel:
    def __init__(self):
        self.severity_keywords = {
            'CRITICAL': ['emergency', 'life threatening', 'death', 'fire', 'explosion', 'flood', 
                         'collapse', 'critical', 'urgent', 'immediate danger', 'major accident',
                         'gas leak', 'building collapse', ' electrocution'],
            'HIGH': ['major', 'serious', 'severe', 'dangerous', 'urgent', 'hazard', 'broken', 
                     'leaking', 'flooding', 'severe damage', 'major leakage', 'school', 'hospital',
                     'children', 'danger', 'threat'],
            'MEDIUM': ['moderate', 'damage', 'problem', 'issue', 'broken', 'not working', 
                       'inconvenient', 'medium', 'poor', 'faulty'],
            'LOW': ['minor', 'small', 'cosmetic', 'slight', 'low', 'minor issue', 'small problem',
                    'slow', 'delay']
        }
        
        self.category_severity_boost = {
            'Water Supply': ['leak', 'flood', 'pipe', 'contamination'],
            'Electricity': ['power', 'outage', 'fire', 'spark', 'shock'],
            'Roads & Transport': ['accident', 'pothole', 'major', 'dangerous', 'blocked'],
            'Sanitation': ['garbage', 'drainage', 'sewage', 'overflow', 'stench'],
            'Healthcare': ['emergency', 'ambulance', 'death', 'critical', 'shortage'],
            'Public Safety': ['crime', 'fire', 'theft', 'assault', 'dangerous', 'suspicious']
        }
    
    def predict(self, text, category, features):
        text_lower = text.lower()
        scores = {}
        
        for severity, keywords in self.severity_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[severity] = score
        
        if category in self.category_severity_boost:
            for kw in self.category_severity_boost[category]:
                if kw in text_lower:
                    scores['HIGH'] = scores.get('HIGH', 0) + 1
        
        if features['urgency_word_count'] > 0:
            scores['HIGH'] = scores.get('HIGH', 0) + features['urgency_word_count']
        
        if features['has_time']:
            scores['MEDIUM'] = scores.get('MEDIUM', 0) + 1
        
        if not scores or max(scores.values()) == 0:
            return 'MEDIUM', 0.0
        
        best = max(scores, key=scores.get)
        confidence = min(scores[best] / 3, 1.0)
        return best, confidence

class EmotionAnalysis:
    def __init__(self):
        self.emotion_keywords = {
            'Angry': ['angry', 'furious', 'outraged', 'mad', 'frustrated', 'irritated', 
                      'annoyed', 'upset', 'livid', 'rage', 'worst', 'terrible', 'horrible',
                      'unacceptable', 'ridiculous', 'disgusted'],
            'Frustrated': ['frustrated', 'disappointed', 'unsatisfied', 'helpless', 'ignored',
                           'neglected', 'tired', 'fed up', 'sick of', 'enough'],
            'Anxious': ['worried', 'anxious', 'concerned', 'scared', 'afraid', 'fear', 
                        'danger', 'unsafe', 'risk', 'threat', 'panic', 'emergency'],
            'Urgent': ['urgent', 'immediate', 'asap', 'right now', 'critical', 'emergency',
                       'quickly', 'fast', 'immediately', 'instant'],
            'Neutral': ['please', 'request', 'kindly', 'suggest', 'inform', 'notify']
        }
    
    def analyze(self, text, severity):
        text_lower = text.lower()
        scores = {}
        
        for emotion, keywords in self.emotion_keywords.items():
            score = sum(1 for kw in keywords if kw in text_lower)
            scores[emotion] = score
        
        if severity == 'CRITICAL':
            scores['Anxious'] = scores.get('Anxious', 0) + 2
            scores['Urgent'] = scores.get('Urgent', 0) + 2
        elif severity == 'HIGH':
            scores['Urgent'] = scores.get('Urgent', 0) + 1
        
        if not scores or max(scores.values()) == 0:
            return 'Neutral'
        
        return max(scores, key=scores.get)

class SimilarityDetection:
    def __init__(self, db):
        self.db = db
    
    def jaccard_similarity(self, set1, set2):
        if not set1 or not set2:
            return 0.0
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def tfidf_similarity(self, text1, text2):
        tokens1 = Counter(TextPreprocessor.tokenize(text1))
        tokens2 = Counter(TextPreprocessor.tokenize(text2))
        
        all_terms = set(tokens1.keys()) | set(tokens2.keys())
        if not all_terms:
            return 0.0
        
        dot_product = sum(tokens1.get(t, 0) * tokens2.get(t, 0) for t in all_terms)
        mag1 = math.sqrt(sum(v**2 for v in tokens1.values()))
        mag2 = math.sqrt(sum(v**2 for v in tokens2.values()))
        
        if mag1 == 0 or mag2 == 0:
            return 0.0
        return dot_product / (mag1 * mag2)
    
    def find_similar(self, text, category, threshold=0.3):
        conn = self.db.get_connection()
        all_complaints = conn.execute('''
            SELECT id, text, category FROM complaints 
            WHERE category = ? ORDER BY created_at DESC
        ''', (category,)).fetchall()
        conn.close()
        
        text_tokens = set(TextPreprocessor.remove_stopwords(TextPreprocessor.tokenize(text)))
        
        similar_ids = []
        for complaint in all_complaints:
            other_tokens = set(TextPreprocessor.remove_stopwords(TextPreprocessor.tokenize(complaint['text'])))
            
            jaccard = self.jaccard_similarity(text_tokens, other_tokens)
            tfidf = self.tfidf_similarity(text, complaint['text'])
            
            combined_sim = (jaccard * 0.4) + (tfidf * 0.6)
            
            if combined_sim >= threshold:
                similar_ids.append(complaint['id'])
        
        return len(similar_ids), similar_ids

class LocationAnalysis:
    def __init__(self):
        self.location_indicators = ['near', 'at', 'in front of', 'behind', 'beside', 'opposite',
                                     'road', 'street', 'area', 'locality', 'sector', 'colony',
                                     'block', 'phase', 'village', 'town', 'city', 'district']
        self.priority_locations = ['school', 'hospital', 'market', 'mall', 'station', 'bridge',
                                   'crossing', 'junction', 'highway', 'residential', 'commercial']
    
    def analyze(self, text, location_input):
        text_lower = text.lower()
        analysis = []
        
        found_locations = []
        for ind in self.location_indicators:
            if ind in text_lower:
                found_locations.append(ind)
        
        if location_input and location_input.strip():
            analysis.append(f"User specified location: {location_input}")
        
        if found_locations:
            analysis.append(f"Location indicators found: {', '.join(set(found_locations))}")
        
        priority_score = 0
        for pl in self.priority_locations:
            if pl in text_lower:
                priority_score += 1
                analysis.append(f"Priority location detected: {pl}")
        
        if priority_score >= 2:
            analysis.append("Multiple priority locations - high visibility area")
        elif priority_score == 1:
            analysis.append("Single priority location - moderate visibility")
        
        if not analysis:
            analysis.append("No specific location details provided")
        
        return "; ".join(analysis), priority_score

class HistoricalDataAnalysis:
    def __init__(self, db):
        self.db = db
    
    def analyze(self, category, severity):
        conn = self.db.get_connection()
        
        total_in_cat = conn.execute('''
            SELECT COUNT(*) as c FROM complaints WHERE category = ?
        ''', (category,)).fetchone()['c']
        
        total_severe = conn.execute('''
            SELECT COUNT(*) as c FROM complaints WHERE category = ? AND severity = ?
        ''', (category, severity)).fetchone()['c']
        
        recent_cat = conn.execute('''
            SELECT COUNT(*) as c FROM complaints 
            WHERE category = ? AND created_at > datetime('now', '-7 days')
        ''', (category,)).fetchone()['c']
        
        avg_priority_cat = conn.execute('''
            SELECT AVG(priority_score) as avg FROM complaints WHERE category = ?
        ''', (category,)).fetchone()['avg']
        
        conn.close()
        
        insights = []
        
        if total_in_cat > 10:
            insights.append(f"High complaint volume in {category} ({total_in_cat} total)")
        elif total_in_cat > 5:
            insights.append(f"Moderate complaint volume in {category} ({total_in_cat} total)")
        else:
            insights.append(f"Low complaint volume in {category} ({total_in_cat} total)")
        
        if total_severe > 3:
            insights.append(f"Recurring {severity} severity issues in {category}")
        
        if recent_cat > 3:
            insights.append(f"Spike in {category} complaints this week ({recent_cat})")
        
        if avg_priority_cat and avg_priority_cat > 75:
            insights.append(f"Category has high average priority ({avg_priority_cat:.1f})")
        
        return "; ".join(insights) if insights else "No significant historical patterns detected"

class PriorityEngine:
    def __init__(self):
        self.weights = {
            'severity': 25,
            'emotion': 10,
            'similarity': 10,
            'location': 10,
            'historical': 10,
            'time': 10,
            'text_quality': 5,
            'base': 20
        }
    
    def calculate(self, severity, severity_conf, emotion, similar_count, 
                  location_priority, historical_insights, features):
        score = self.weights['base']
        
        severity_scores = {'CRITICAL': 25, 'HIGH': 18, 'MEDIUM': 10, 'LOW': 5}
        score += severity_scores.get(severity, 10) * (self.weights['severity'] / 25)
        
        emotion_scores = {'Angry': 10, 'Anxious': 8, 'Frustrated': 7, 'Urgent': 9, 'Neutral': 3}
        score += emotion_scores.get(emotion, 3) * (self.weights['emotion'] / 10)
        
        sim_score = min(similar_count * 3, 10)
        score += sim_score * (self.weights['similarity'] / 10)
        
        loc_score = min(location_priority * 3, 10)
        score += loc_score * (self.weights['location'] / 10)
        
        if 'Spike' in historical_insights or 'High complaint volume' in historical_insights:
            score += 10 * (self.weights['historical'] / 10)
        elif 'Moderate' in historical_insights:
            score += 5 * (self.weights['historical'] / 10)
        
        if features['has_time']:
            score += 10 * (self.weights['time'] / 10)
        
        if features['urgency_word_count'] > 0:
            score += min(features['urgency_word_count'] * 3, 10)
        
        if features['word_count'] > 50:
            score += 5 * (self.weights['text_quality'] / 5)
        
        score = max(0, min(100, score))
        return round(score, 1)

class SmartAssignment:
    def __init__(self):
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
        
        self.officers = {
            'Water Supply': ['Eng. Ramesh Kumar', 'Eng. Priya Sharma', 'Supervisor Amit Singh'],
            'Electricity': ['Elect. Sunil Verma', 'Eng. Meera Joshi', 'Asst. Raj Patel'],
            'Roads & Transport': ['Executive Vikram Singh', 'Eng. Neha Gupta', 'Supervisor Deepak R'],
            'Sanitation': ['Health Officer Anita D', 'Supervisor Mohan L', 'Inspector Ritu K'],
            'Healthcare': ['Dr. Sanjay Rao', 'Med. Officer Kavita S', 'Nodal Pradeep M'],
            'Education': ['Deputy Director Arjun M', 'Inspector Shalini T', 'Coordinator Ravi K'],
            'Public Safety': ['ACP Rajeshwari', 'Inspector Sameer K', 'Officer Nisha P'],
            'Environment': ['Env. Officer Tarun G', 'Scientist Meenal J', 'Inspector Vikas D'],
            'Housing': ['Town Planner Sonia R', 'Eng. Alok B', 'Officer Priyanka S'],
            'Public Transport': ['Transport Commr. Rakesh T', 'Manager Anil V', 'Officer Divya M']
        }
        
        self.sla_hours = {
            'CRITICAL': (1, 4),
            'HIGH': (2, 8),
            'MEDIUM': (4, 24),
            'LOW': (8, 48)
        }
    
    def assign_officer(self, category, priority_score, severity):
        import random
        officers = self.officers.get(category, ['General Officer'])
        
        if severity == 'CRITICAL' or priority_score >= 85:
            return officers[0]
        elif severity == 'HIGH' or priority_score >= 70:
            return officers[1] if len(officers) > 1 else officers[0]
        else:
            return officers[2] if len(officers) > 2 else officers[-1]
    
    def assign(self, category, severity, priority_score):
        department = self.departments.get(category, 'General Administration')
        officer = self.assign_officer(category, priority_score, severity)
        
        min_hours, max_hours = self.sla_hours.get(severity, (4, 24))
        if priority_score >= 90:
            min_hours = max(1, min_hours - 1)
        elif priority_score <= 40:
            max_hours = min(48, max_hours + 6)
        
        predicted_sla = f"{min_hours}-{max_hours} hours"
        
        urgency_map = {
            'CRITICAL': 'Immediate',
            'HIGH': 'Within 24 hours',
            'MEDIUM': 'Within 48 hours',
            'LOW': 'Within a week'
        }
        urgency = urgency_map.get(severity, 'Within 48 hours')
        
        return department, officer, urgency, predicted_sla

class ComplaintAI:
    def __init__(self, db):
        self.db = db
        self.preprocessor = TextPreprocessor()
        self.category_model = CategoryModel()
        self.severity_model = SeverityModel()
        self.emotion_analyzer = EmotionAnalysis()
        self.similarity_detector = SimilarityDetection(db)
        self.location_analyzer = LocationAnalysis()
        self.historical_analyzer = HistoricalDataAnalysis(db)
        self.priority_engine = PriorityEngine()
        self.smart_assignment = SmartAssignment()
        self._trained = False
    
    def train_classifier(self):
        self._trained = True
    
    def process_complaint(self, text, complainant_name='', contact='', location=''):
        preprocessed_text = self.preprocessor.normalize(text)
        features = self.preprocessor.extract_features(text)
        
        category, cat_conf = self.category_model.predict(text, features)
        severity, sev_conf = self.severity_model.predict(text, category, features)
        emotion = self.emotion_analyzer.analyze(text, severity)
        
        similar_count, similar_ids = self.similarity_detector.find_similar(text, category)
        
        location_analysis, location_priority = self.location_analyzer.analyze(text, location)
        historical_insights = self.historical_analyzer.analyze(category, severity)
        
        priority_score = self.priority_engine.calculate(
            severity, sev_conf, emotion, similar_count,
            location_priority, historical_insights, features
        )
        
        department, officer, urgency, predicted_sla = self.smart_assignment.assign(
            category, severity, priority_score
        )
        
        complaint_id = self.db.insert_complaint(
            text, preprocessed_text, category, severity, emotion, priority_score,
            department, officer, urgency, similar_count, predicted_sla,
            location_analysis, historical_insights, complainant_name, contact, location
        )
        
        return {
            'success': True,
            'complaint_id': complaint_id,
            'preprocessed_text': preprocessed_text,
            'category': category,
            'category_confidence': round(cat_conf, 2),
            'severity': severity,
            'severity_confidence': round(sev_conf, 2),
            'emotion': emotion,
            'priority_score': priority_score,
            'department': department,
            'officer': officer,
            'urgency': urgency,
            'similar_cases': similar_count,
            'similar_ids': similar_ids[:5],
            'predicted_sla': predicted_sla,
            'location_analysis': location_analysis,
            'historical_data': historical_insights,
            'status': 'Pending',
            'timestamp': datetime.datetime.now().isoformat()
        }
