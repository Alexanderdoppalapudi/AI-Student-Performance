"""Data preprocessing module for student data"""

import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import logging

logger = logging.getLogger(__name__)

class DataPreprocessor:
    """Handles data preprocessing and cleaning"""
    
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoders = {}
        self.feature_names = None
    
    def load_data(self, file_path):
        """Load data from CSV file"""
        try:
            data = pd.read_csv(file_path)
            logger.info(f"Data loaded from {file_path}. Shape: {data.shape}")
            return data
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            raise
    
    def handle_missing_values(self, data, strategy='mean'):
        """Handle missing values in the dataset"""
        missing_count = data.isnull().sum().sum()
        logger.info(f"Missing values found: {missing_count}")
        
        if strategy == 'mean':
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].mean())
        elif strategy == 'median':
            numeric_columns = data.select_dtypes(include=[np.number]).columns
            data[numeric_columns] = data[numeric_columns].fillna(data[numeric_columns].median())
        elif strategy == 'drop':
            data = data.dropna()
        
        logger.info(f"Missing values handled using {strategy} strategy")
        return data
    
    def remove_outliers(self, data, method='iqr', threshold=1.5):
        """Remove outliers from the dataset"""
        numeric_columns = data.select_dtypes(include=[np.number]).columns
        
        if method == 'iqr':
            Q1 = data[numeric_columns].quantile(0.25)
            Q3 = data[numeric_columns].quantile(0.75)
            IQR = Q3 - Q1
            
            mask = ~((data[numeric_columns] < (Q1 - threshold * IQR)) |
                     (data[numeric_columns] > (Q3 + threshold * IQR))).any(axis=1)
            data = data[mask]
        
        logger.info(f"Outliers removed. New shape: {data.shape}")
        return data
    
    def encode_categorical(self, data, categorical_columns=None):
        """Encode categorical variables"""
        if categorical_columns is None:
            categorical_columns = data.select_dtypes(include=['object']).columns
        
        for col in categorical_columns:
            if col in data.columns:
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col].astype(str))
                self.label_encoders[col] = le
        
        logger.info(f"Categorical variables encoded: {list(categorical_columns)}")
        return data
    
    def feature_scaling(self, data, columns=None):
        """Scale numerical features"""
        if columns is None:
            columns = data.select_dtypes(include=[np.number]).columns
        
        data[columns] = self.scaler.fit_transform(data[columns])
        logger.info(f"Features scaled: {list(columns)}")
        return data
    
    def create_features(self, data):
        """Create derived features"""
        # Example feature engineering
        if 'study_hours' in data.columns and 'sleep_hours' in data.columns:
            data['study_sleep_ratio'] = data['study_hours'] / (data['sleep_hours'] + 1)
        
        if 'past_gpa' in data.columns and 'current_gpa' in data.columns:
            data['gpa_improvement'] = data['current_gpa'] - data['past_gpa']
        
        if 'assignment_score' in data.columns and 'exam_score' in data.columns:
            data['average_score'] = (data['assignment_score'] + data['exam_score']) / 2
        
        logger.info("Features created")
        return data
    
    def split_data(self, X, y, test_size=0.2, validation_size=0.1, random_state=42):
        """Split data into train, validation, and test sets"""
        # First split: train+validation and test
        X_temp, X_test, y_temp, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Second split: train and validation
        val_split = validation_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(
            X_temp, y_temp, test_size=val_split, random_state=random_state
        )
        
        logger.info(f"Data split - Train: {X_train.shape[0]}, "
                   f"Validation: {X_val.shape[0]}, Test: {X_test.shape[0]}")
        
        return X_train, X_val, X_test, y_train, y_val, y_test
    
    def preprocess_pipeline(self, data, target_column='final_grade'):
        """Complete preprocessing pipeline"""
        logger.info("Starting preprocessing pipeline")
        
        # Handle missing values
        data = self.handle_missing_values(data)
        
        # Remove outliers
        data = self.remove_outliers(data)
        
        # Encode categorical variables
        data = self.encode_categorical(data)
        
        # Create features
        data = self.create_features(data)
        
        # Separate features and target
        if target_column in data.columns:
            y = data[target_column]
            X = data.drop(columns=[target_column])
        else:
            X = data
            y = None
        
        # Store feature names
        self.feature_names = X.columns.tolist()
        
        # Scale features
        X = self.feature_scaling(X)
        
        logger.info("Preprocessing pipeline completed")
        
        return X, y
