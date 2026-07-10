"""AI Student Performance Prediction System"""

__version__ = "1.0.0"
__author__ = "AI Education Team"
__description__ = "AI-powered student performance prediction and personalized learning system"

from .data_preprocessing import DataPreprocessor
from .model_training import ModelTrainer
from .prediction_engine import PredictionEngine
from .personalized_learning import PersonalizedLearning

__all__ = [
    "DataPreprocessor",
    "ModelTrainer",
    "PredictionEngine",
    "PersonalizedLearning",
]
