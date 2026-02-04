import hashlib
import time
import numpy as np
import pandas as pd

def generate_visitor_id(user_agent, referrer, salt="privacy_salt_2026"):
    """
    Generate a privacy-focused visitor ID without storing IP.
    Uses hash of user-agent, referrer, and a daily salt.
    """
    # Create a time bucket (daily) to make the ID rotate
    day_bucket = time.strftime("%Y-%m-%d")
    raw_str = f"{user_agent}{referrer}{day_bucket}{salt}"
    return hashlib.sha256(raw_str.encode()).hexdigest()[:16]

def calculate_bounce_rate(single_page_sessions, total_sessions):
    """
    Formula: (Single Page Sessions / Total Sessions) * 100%
    """
    if total_sessions == 0:
        return 0.0
    return (single_page_sessions / total_sessions) * 100

def calculate_avg_session_time(total_duration, total_sessions):
    """
    Formula: Sum(session duration) / Total Sessions
    """
    if total_sessions == 0:
        return 0.0
    return total_duration / total_sessions

def detect_spike_drop(current_views, avg_daily_views):
    """
    Spike Detection: views > (avg daily * 1.5)
    Drop Detection: views < (avg daily * 0.5)
    """
    if avg_daily_views == 0:
        return None
    
    if current_views > (avg_daily_views * 1.5):
        return "Spike"
    elif current_views < (avg_daily_views * 0.5):
        return "Drop"
    return None

def get_dummy_metrics():
    """
    Generate realistic dummy data for the dashboard.
    """
    dates = pd.date_range(end=pd.Timestamp.now(), periods=30)
    visitors = np.random.randint(400, 600, size=30)
    page_views = visitors * np.random.uniform(1.2, 2.5, size=30)
    page_views = page_views.astype(int)
    
    # Add a spike for testing
    page_views[-1] = int(np.mean(page_views) * 1.8)
    
    df = pd.DataFrame({
        'Date': dates,
        'Visitors': visitors,
        'PageViews': page_views
    })
    
    summary = {
        'total_visitors': int(df['Visitors'].sum()),
        'avg_bounce_rate': 45.0, # Dummy constant
        'avg_session_time': 120, # seconds
        'spike_status': detect_spike_drop(page_views[-1], df['PageViews'].mean())
    }
    
    return df, summary
