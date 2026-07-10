"""Prediction engine for student performance"""

import numpy as np
import logging
from .utils import load_model, validate_student_data, get_performance_level, log_prediction

logger = logging.getLogger(__name__)

class PredictionEngine:
    """Handles student performance predictions"""
    
    def __init__(self, model_path='models/gradient_boost_model.pkl'):
        try:
            self.model = load_model(model_path)
        except FileNotFoundError:
            logger.warning(f"Model not found at {model_path}. Using dummy model for testing.")
            self.model = None
        self.feature_names = None
    
    def predict_single(self, student_data, return_proba=True):
        """Make prediction for a single student"""
        try:
            # Validate input
            validate_student_data(student_data)
            
            # Prepare features
            features = self._prepare_features(student_data)
            
            if self.model is None:
                # Dummy prediction for testing
                prediction = 3.5
                confidence = 0.85
            else:
                # Make prediction
                prediction = self.model.predict(features.reshape(1, -1))[0]
                
                if return_proba:
                    try:
                        proba = self.model.predict_proba(features.reshape(1, -1))[0]
                        confidence = float(np.max(proba))
                    except:
                        confidence = None
                else:
                    confidence = None
            
            # Get performance level
            performance_level = get_performance_level(float(prediction))
            
            result = {
                'predicted_gpa': float(prediction),
                'performance_level': performance_level,
                'confidence': confidence,
                'student_id': student_data.get('student_id', 'N/A')
            }
            
            # Log prediction
            log_prediction(
                student_data.get('student_id', 'N/A'),
                student_data,
                prediction,
                confidence
            )
            
            logger.info(f"Prediction made: {result}")
            return result
        
        except Exception as e:
            logger.error(f"Error making prediction: {e}")
            raise
    
    def predict_batch(self, students_data):
        """Make predictions for multiple students"""
        results = []
        for student_data in students_data:
            try:
                result = self.predict_single(student_data)
                results.append(result)
            except Exception as e:
                logger.warning(f"Error predicting for student: {e}")
                results.append({'error': str(e), 'student_id': student_data.get('student_id', 'N/A')})
        
        return results
    
    def _prepare_features(self, student_data):
        """Prepare features for prediction"""
        # Define feature order (must match training data)
        feature_order = [
            'study_hours', 'attendance', 'past_gpa', 'assignment_score',
            'engagement_level', 'sleep_hours', 'extracurricular',
            'internet_speed', 'device_quality'
        ]
        
        features = []
        for feature in feature_order:
            if feature in student_data:
                features.append(float(student_data[feature]))
            else:
                features.append(0.0)  # Default value if feature missing
        
        return np.array(features)
    
    def get_recommendations(self, prediction_result):
        """Get recommendations based on prediction"""
        gpa = prediction_result['predicted_gpa']
        
        recommendations = []
        
        if gpa < 2.0:
            recommendations = [
                "Urgent: Schedule meeting with academic advisor",
                "Consider tutoring in core subjects",
                "Increase study hours by 50%",
                "Review study techniques and materials",
                "Explore peer study groups"
            ]
        elif gpa < 2.7:
            recommendations = [
                "Increase study consistency",
                "Seek help in challenging subjects",
                "Consider study groups",
                "Review time management strategies",
                "Improve attendance if applicable"
            ]
        elif gpa < 3.3:
            recommendations = [
                "Maintain current study habits",
                "Challenge yourself with advanced materials",
                "Consider leadership roles in academic projects",
                "Explore elective courses in areas of interest"
            ]
        else:
            recommendations = [
                "Continue excellent performance",
                "Consider peer tutoring or mentoring",
                "Explore advanced coursework",
                "Consider research opportunities",
                "Maintain work-life balance"
            ]
        
        return recommendations
