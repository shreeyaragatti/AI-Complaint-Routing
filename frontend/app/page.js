'use client';

import { useState, useEffect } from 'react';

function LiveDemo() {
  const [complaint, setComplaint] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastId, setLastId] = useState(null);

  const fetchLatest = async () => {
    try {
      const res = await fetch('/api/complaints');
      if (!res.ok) throw new Error('Failed to fetch');
      const data = await res.json();
      if (data.length > 0) {
        const latest = data[0];
        if (latest.id !== lastId) {
          setLastId(latest.id);
          setComplaint(latest);
        }
      } else if (!complaint) {
        setComplaint(null);
      }
      setError(null);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchLatest();
    const interval = setInterval(fetchLatest, 3000);
    return () => clearInterval(interval);
  }, []);

  if (loading) {
    return (
      <div className="demo-card">
        <div className="empty-state" style={{ gridColumn: '1 / -1' }}>
          <i className="fas fa-spinner fa-spin"></i>
          <p>Loading latest complaint...</p>
        </div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="demo-card">
        <div className="empty-state" style={{ gridColumn: '1 / -1' }}>
          <i className="fas fa-exclamation-circle"></i>
          <p>Unable to load complaints. Make sure the backend is running.</p>
        </div>
      </div>
    );
  }

  if (!complaint) {
    return (
      <div className="demo-card">
        <div className="empty-state" style={{ gridColumn: '1 / -1' }}>
          <i className="fas fa-inbox"></i>
          <p>No complaints submitted yet. Be the first to submit one!</p>
        </div>
      </div>
    );
  }

  const severityClass = complaint.severity === 'CRITICAL' ? 'severity-critical' :
                        complaint.severity === 'HIGH' ? 'severity-high' :
                        complaint.severity === 'MEDIUM' ? 'severity-medium' : 'severity-low';

  const urgencyClass = complaint.urgency === 'Immediate' ? 'urgency-high' :
                       complaint.urgency === 'Within 24 hours' ? 'urgency-medium' : 'urgency-low';

  const emotionClass = complaint.emotion === 'Angry' ? 'emotion-angry' :
                       complaint.emotion === 'Anxious' ? 'emotion-anxious' :
                       complaint.emotion === 'Frustrated' ? 'emotion-frustrated' :
                       complaint.emotion === 'Urgent' ? 'emotion-urgent' : 'emotion-neutral';

  return (
    <div className="demo-card">
      <div className="demo-input">
        <h4>Input Complaint</h4>
        <div className="sample-text">
          &ldquo;{complaint.text}&rdquo;
        </div>
        {complaint.complainant_name && (
          <div style={{ marginTop: '1rem', fontSize: '0.875rem', color: 'var(--text-muted)' }}>
            <i className="fas fa-user" style={{ marginRight: '0.5rem' }}></i>
            {complaint.complainant_name}
            {complaint.location && (
              <>
                <span style={{ margin: '0 0.5rem' }}>|</span>
                <i className="fas fa-map-marker-alt" style={{ marginRight: '0.5rem' }}></i>
                {complaint.location}
              </>
            )}
          </div>
        )}
      </div>
      <div className="demo-arrow">
        <i className="fas fa-arrow-right"></i>
      </div>
      <div className="demo-output">
        <h4>
          AI Pipeline Output
          <span className="live-indicator">
            <span className="live-dot"></span>
            Live
          </span>
        </h4>
        <div className="output-grid">
          <div className="output-item">
            <span className="label">Category</span>
            <span className="value">{complaint.category || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Severity</span>
            <span className={`value ${severityClass}`}>{complaint.severity || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Emotion</span>
            <span className={`value ${emotionClass}`}>{complaint.emotion || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Priority Score</span>
            <span className="value">{complaint.priority_score || 0}/100</span>
          </div>
          <div className="output-item">
            <span className="label">Department</span>
            <span className="value">{complaint.department || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Assigned Officer</span>
            <span className="value">{complaint.officer || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Urgency</span>
            <span className={`value ${urgencyClass}`}>{complaint.urgency || '-'}</span>
          </div>
          <div className="output-item">
            <span className="label">Similar Cases</span>
            <span className="value">{complaint.similar_cases || 0}</span>
          </div>
          <div className="output-item full-width">
            <span className="label">Predicted SLA</span>
            <span className="value">{complaint.predicted_sla || '-'}</span>
          </div>
        </div>
        <div style={{ marginTop: '1rem', fontSize: '0.75rem', color: 'var(--text-muted)', textAlign: 'right' }}>
          Complaint #{complaint.id} &bull; {new Date(complaint.created_at).toLocaleString()}
        </div>
      </div>
    </div>
  );
}

export default function HomePage() {
  return (
    <>
      <header className="hero">
        <div className="hero-content">
          <h1><i className="fas fa-brain"></i> AI-Powered Complaint Routing</h1>
          <p className="subtitle">Advanced pipeline: NLP preprocessing, multi-model classification, emotion analysis, and smart officer assignment</p>
          <div className="hero-buttons">
            <a href="/submit" className="btn btn-primary btn-large">
              <i className="fas fa-paper-plane"></i> Submit a Complaint
            </a>
            <a href="/dashboard" className="btn btn-secondary btn-large">
              <i className="fas fa-tachometer-alt"></i> View Dashboard
            </a>
          </div>
        </div>
      </header>

      <section className="features">
        <div className="container">
          <h2 className="section-title">AI Pipeline Architecture</h2>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-filter"></i>
              </div>
              <h3>Text Preprocessing</h3>
              <p>Normalizes text, removes stopwords, and extracts linguistic features for analysis.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-tags"></i>
              </div>
              <h3>Category Model</h3>
              <p>Classifies complaints into 10+ categories with confidence scoring using keyword analysis.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-exclamation-triangle"></i>
              </div>
              <h3>Severity Model</h3>
              <p>Determines CRITICAL, HIGH, MEDIUM, or LOW severity based on context and category-specific keywords.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-smile"></i>
              </div>
              <h3>Emotion Analysis</h3>
              <p>Detects user emotion (Angry, Frustrated, Anxious, Urgent, Neutral) to prioritize sensitive cases.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-star"></i>
              </div>
              <h3>Priority Engine</h3>
              <p>Weighted scoring combining severity, emotion, similarity, location, and historical data.</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">
                <i className="fas fa-project-diagram"></i>
              </div>
              <h3>Smart Assignment</h3>
              <p>Routes to the right department, assigns specific officer, and predicts SLA with urgency levels.</p>
            </div>
          </div>
        </div>
      </section>

      <section className="demo-section">
        <div className="container">
          <h2 className="section-title">See It In Action</h2>
          <LiveDemo />
        </div>
      </section>
    </>
  );
}
