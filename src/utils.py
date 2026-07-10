"""Utility functions for the AI Student Performance System"""

import os
import json
import logging
from datetime import datetime
import numpy as np
from pathlib import Path

logger = logging.getLogger(__name__)

def setup_logging(log_file='logs/app.log'):
    """Setup logging configuration"""
    Path('logs').mkdir(exist_ok=True)
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )

def create_directories():
    """Create required directories if they don't exist"""
    directories = ['data/raw', 'data/processed', 'models', 'logs', 'api/static', 'api/templates']
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def save_model(model, model_path):
    """Save model to disk"""
    import joblib
    Path(model_path).parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, model_path)
    logger.info(f"Model saved to {model_path}")

def load_model(model_path):
    """Load model from disk"""
    import joblib
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model not found at {model_path}")
    model = joblib.load(model_path)
    logger.info(f"Model loaded from {model_path}")
    return model

def normalize_features(data, mean=None, std=None):
    """Normalize features using Z-score normalization"""
    if mean is None:
        mean = np.mean(data, axis=0)
    if std is None:
        std = np.std(data, axis=0)
    
    normalized_data = (data - mean) / (std + 1e-8)
    return normalized_data, mean, std

def calculate_metrics(y_true, y_pred, y_pred_proba=None):
    """Calculate evaluation metrics"""
    from sklearn.metrics import (
        accuracy_score, precision_score, recall_score, f1_score,
        confusion_matrix, classification_report, roc_auc_score
    )
    
    metrics = {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='weighted', zero_division=0),
        'recall': recall_score(y_true, y_pred, average='weighted', zero_division=0),
        'f1': f1_score(y_true, y_pred, average='weighted', zero_division=0),
        'confusion_matrix': confusion_matrix(y_true, y_pred).tolist(),
        'classification_report': classification_report(y_true, y_pred)
    }
    
    if y_pred_proba is not None:
        try:
            metrics['auc_roc'] = roc_auc_score(y_true, y_pred_proba, multi_class='ovr')
        except:
            pass
    
    return metrics

def get_model_path(model_name):
    """Get the path to a model file"""
    return f"models/{model_name}.pkl"

def get_data_path(data_name):
    """Get the path to a data file"""
    return f"data/processed/{data_name}.csv"

def log_prediction(student_id, features, prediction, confidence):
    """Log prediction for audit trail"""
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'student_id': student_id,
        'features': str(features),
        'prediction': prediction,
        'confidence': confidence
    }
    logger.info(json.dumps(log_entry))

def validate_student_data(data):
    """Validate student data format"""
    required_fields = [
        'study_hours', 'attendance', 'past_gpa',
        'assignment_score', 'engagement_level'
    ]
    
    for field in required_fields:
        if field not in data:
            raise ValueError(f"Missing required field: {field}")
        
        if not isinstance(data[field], (int, float)):
            raise ValueError(f"Field {field} must be numeric")
    
    # Validate ranges
    if not (0 <= data['study_hours'] <= 168):
        raise ValueError("Study hours must be between 0 and 168")
    
    if not (0 <= data['attendance'] <= 100):
        raise ValueError("Attendance must be between 0 and 100")
    
    if not (0 <= data['past_gpa'] <= 4.0):
        raise ValueError("Past GPA must be between 0 and 4.0")
    
    if not (0 <= data['assignment_score'] <= 100):
        raise ValueError("Assignment score must be between 0 and 100")
    
    if not (1 <= data['engagement_level'] <= 5):
        raise ValueError("Engagement level must be between 1 and 5")
    
    return True

def get_performance_level(gpa):
    """Get performance level from GPA"""
    if gpa >= 3.7:
        return "Excellent"
    elif gpa >= 3.3:
        return "Very Good"
    elif gpa >= 3.0:
        return "Good"
    elif gpa >= 2.7:
        return "Satisfactory"
    elif gpa >= 2.0:
        return "Needs Improvement"
    else:
        return "At Risk"
