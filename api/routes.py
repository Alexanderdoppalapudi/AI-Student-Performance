"""Flask API routes"""

from flask import Blueprint, request, jsonify, render_template
import logging
from ..src.prediction_engine import PredictionEngine
from ..src.personalized_learning import PersonalizedLearning
from ..src.data_preprocessing import DataPreprocessor

logger = logging.getLogger(__name__)

# Create blueprints
main_bp = Blueprint('main', __name__)
api_bp = Blueprint('api', __name__)

# Initialize engines
prediction_engine = PredictionEngine()
learning_engine = PersonalizedLearning()
preprocessor = DataPreprocessor()

@main_bp.route('/')
def index():
    """Home page"""
    return render_template('index.html')

@main_bp.route('/dashboard')
def dashboard():
    """Dashboard page"""
    return render_template('dashboard.html')

@main_bp.route('/predict')
def predict_page():
    """Prediction page"""
    return render_template('predict.html')

@api_bp.route('/predict', methods=['POST'])
def predict():
    """Make a prediction for a student"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Make prediction
        prediction = prediction_engine.predict_single(data)
        
        # Get recommendations
        recommendations = prediction_engine.get_recommendations(prediction)
        
        # Get personalized learning recommendations
        data['performance_level'] = prediction['performance_level']
        learning_recs = learning_engine.get_recommendations(data)
        
        result = {
            'prediction': prediction,
            'recommendations': recommendations,
            'learning_recommendations': learning_recs
        }
        
        logger.info(f"Prediction successful for student {data.get('student_id', 'N/A')}")
        return jsonify(result), 200
    
    except Exception as e:
        logger.error(f"Error in prediction: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/batch-predict', methods=['POST'])
def batch_predict():
    """Make predictions for multiple students"""
    try:
        data = request.get_json()
        
        if not data or 'students' not in data:
            return jsonify({'error': 'No students data provided'}), 400
        
        students = data['students']
        predictions = prediction_engine.predict_batch(students)
        
        logger.info(f"Batch prediction completed for {len(predictions)} students")
        return jsonify({
            'total': len(predictions),
            'predictions': predictions
        }), 200
    
    except Exception as e:
        logger.error(f"Error in batch prediction: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/learning-recommendations', methods=['POST'])
def get_learning_recommendations():
    """Get personalized learning recommendations"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        recommendations = learning_engine.get_recommendations(data)
        
        logger.info(f"Learning recommendations generated")
        return jsonify(recommendations), 200
    
    except Exception as e:
        logger.error(f"Error generating recommendations: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/preprocess', methods=['POST'])
def preprocess_data():
    """Preprocess student data"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No data provided'}), 400
        
        # Convert to DataFrame
        import pandas as pd
        df = pd.DataFrame([data])
        
        # Preprocess
        X, y = preprocessor.preprocess_pipeline(df)
        
        logger.info("Data preprocessing completed")
        return jsonify({
            'preprocessed': X.to_dict(orient='records'),
            'target': y.tolist() if y is not None else None
        }), 200
    
    except Exception as e:
        logger.error(f"Error in preprocessing: {e}")
        return jsonify({'error': str(e)}), 500

@api_bp.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running'
    }), 200

@api_bp.route('/performance-levels', methods=['GET'])
def get_performance_levels():
    """Get performance level definitions"""
    return jsonify({
        'levels': [
            {'level': 'Excellent', 'gpa_range': '3.7 - 4.0', 'description': 'Outstanding performance'},
            {'level': 'Very Good', 'gpa_range': '3.3 - 3.6', 'description': 'Excellent work'},
            {'level': 'Good', 'gpa_range': '3.0 - 3.2', 'description': 'Above average'},
            {'level': 'Satisfactory', 'gpa_range': '2.7 - 2.9', 'description': 'Meets requirements'},
            {'level': 'Needs Improvement', 'gpa_range': '2.0 - 2.6', 'description': 'Below expectations'},
            {'level': 'At Risk', 'gpa_range': '0.0 - 1.9', 'description': 'Critical attention needed'}
        ]
    }), 200

@api_bp.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@api_bp.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {error}")
    return jsonify({'error': 'Internal server error'}), 500
