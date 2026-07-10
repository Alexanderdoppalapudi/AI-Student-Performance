"""Model training module"""

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import Adam
import logging
from .utils import save_model, calculate_metrics

logger = logging.getLogger(__name__)

class ModelTrainer:
    """Handles model training and optimization"""
    
    def __init__(self):
        self.models = {}
        self.histories = {}
        self.best_model = None
        self.best_score = 0
    
    def train_random_forest(self, X_train, y_train, **kwargs):
        """Train Random Forest model"""
        logger.info("Training Random Forest model")
        
        params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'max_depth': kwargs.get('max_depth', 10),
            'min_samples_split': kwargs.get('min_samples_split', 5),
            'min_samples_leaf': kwargs.get('min_samples_leaf', 2),
            'random_state': 42,
            'n_jobs': -1
        }
        
        model = RandomForestClassifier(**params)
        model.fit(X_train, y_train)
        self.models['random_forest'] = model
        
        logger.info("Random Forest model trained successfully")
        return model
    
    def train_gradient_boosting(self, X_train, y_train, **kwargs):
        """Train Gradient Boosting model"""
        logger.info("Training Gradient Boosting model")
        
        params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'learning_rate': kwargs.get('learning_rate', 0.1),
            'max_depth': kwargs.get('max_depth', 5),
            'random_state': 42
        }
        
        model = GradientBoostingClassifier(**params)
        model.fit(X_train, y_train)
        self.models['gradient_boosting'] = model
        
        logger.info("Gradient Boosting model trained successfully")
        return model
    
    def train_xgboost(self, X_train, y_train, **kwargs):
        """Train XGBoost model"""
        logger.info("Training XGBoost model")
        
        # Encode labels if they are strings
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y_train_encoded = le.fit_transform(y_train)
        
        params = {
            'n_estimators': kwargs.get('n_estimators', 100),
            'learning_rate': kwargs.get('learning_rate', 0.1),
            'max_depth': kwargs.get('max_depth', 5),
            'random_state': 42,
            'objective': 'multi:softmax' if len(np.unique(y_train)) > 2 else 'binary:logistic',
            'num_class': len(np.unique(y_train)) if len(np.unique(y_train)) > 2 else None
        }
        
        if params['num_class'] is None:
            params.pop('num_class')
        
        model = XGBClassifier(**params)
        model.fit(X_train, y_train_encoded)
        self.models['xgboost'] = model
        self.label_encoder = le
        
        logger.info("XGBoost model trained successfully")
        return model
    
    def train_neural_network(self, X_train, y_train, **kwargs):
        """Train Neural Network model"""
        logger.info("Training Neural Network model")
        
        # Encode labels
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        y_train_encoded = le.fit_transform(y_train)
        
        # One-hot encode for multi-class
        from tensorflow.keras.utils import to_categorical
        num_classes = len(np.unique(y_train))
        y_train_categorical = to_categorical(y_train_encoded, num_classes)
        
        # Build model
        model = Sequential([
            Dense(128, activation='relu', input_dim=X_train.shape[1]),
            Dropout(0.3),
            Dense(64, activation='relu'),
            Dropout(0.3),
            Dense(32, activation='relu'),
            Dropout(0.2),
            Dense(num_classes, activation='softmax')
        ])
        
        model.compile(
            optimizer=Adam(learning_rate=0.001),
            loss='categorical_crossentropy',
            metrics=['accuracy']
        )
        
        # Train model
        epochs = kwargs.get('epochs', 50)
        batch_size = kwargs.get('batch_size', 32)
        
        history = model.fit(
            X_train, y_train_categorical,
            epochs=epochs,
            batch_size=batch_size,
            validation_split=0.2,
            verbose=0
        )
        
        self.models['neural_network'] = model
        self.histories['neural_network'] = history
        self.label_encoder = le
        
        logger.info("Neural Network model trained successfully")
        return model
    
    def train_all_models(self, X_train, y_train, **kwargs):
        """Train all available models"""
        logger.info("Starting training of all models")
        
        self.train_random_forest(X_train, y_train, **kwargs)
        self.train_gradient_boosting(X_train, y_train, **kwargs)
        self.train_xgboost(X_train, y_train, **kwargs)
        self.train_neural_network(X_train, y_train, **kwargs)
        
        logger.info("All models trained successfully")
    
    def evaluate_models(self, X_test, y_test):
        """Evaluate all trained models"""
        logger.info("Evaluating all models")
        results = {}
        
        for model_name, model in self.models.items():
            logger.info(f"Evaluating {model_name}")
            
            if model_name == 'neural_network':
                from tensorflow.keras.utils import to_categorical
                le = self.label_encoder
                y_test_encoded = le.transform(y_test)
                num_classes = len(np.unique(y_test))
                y_test_categorical = to_categorical(y_test_encoded, num_classes)
                
                y_pred_proba = model.predict(X_test)
                y_pred = np.argmax(y_pred_proba, axis=1)
                y_pred = le.inverse_transform(y_pred)
            else:
                y_pred = model.predict(X_test)
                try:
                    y_pred_proba = model.predict_proba(X_test)
                except:
                    y_pred_proba = None
            
            metrics = calculate_metrics(y_test, y_pred, y_pred_proba)
            results[model_name] = metrics
            
            logger.info(f"{model_name} - Accuracy: {metrics['accuracy']:.4f}")
        
        return results
    
    def save_all_models(self):
        """Save all trained models"""
        for model_name, model in self.models.items():
            if model_name == 'neural_network':
                model.save(f'models/{model_name}_model.h5')
            else:
                save_model(model, f'models/{model_name}_model.pkl')
            logger.info(f"Model {model_name} saved")
