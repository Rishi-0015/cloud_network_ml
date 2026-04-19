import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pandas as pd
import numpy as np
from dashboard.preprocessing.data_processor import DataProcessor
from models.anomaly_detector import AnomalyDetector
from models.fault_predictor import FaultPredictor
import joblib
import warnings
warnings.filterwarnings('ignore')

def train_all_models():
    print("="*50)
    print("Starting Model Training Pipeline")
    print("="*50)
    
    # 1. Load and process data
    print("\n1. Loading and processing data...")
    processor = DataProcessor()
    
    # Generate data if not exists
    if not os.path.exists('cloud_network_ml/sample_data.csv'):
        print("Generating sample data...")
        from cloud_network_ml.collector import DataCollector
        collector = DataCollector()
        collector.generate_sample_data()
    
    df = processor.load_data()
    print(f"Loaded {len(df)} samples")
    
    df = processor.clean_data(df)
    print(f"After cleaning: {len(df)} samples")
    
    df = processor.extract_features(df)
    X, y, features = processor.prepare_features(df)
    
    # For fault prediction (multi-class)
    fault_labels = df['fault_type'].map({
        'normal': 0, 'high_cpu': 1, 'high_memory': 2, 
        'network_congestion': 3, 'hardware_fault': 4
    }).fillna(0).values
    
    X_train, X_val, X_test, y_train, y_val, y_test = processor.split_data(X, y)
    _, _, _, fault_train, fault_val, fault_test = processor.split_data(X, fault_labels)
    
    print(f"\nData Split:")
    print(f"Training: {X_train.shape[0]} samples")
    print(f"Validation: {X_val.shape[0]} samples")
    print(f"Test: {X_test.shape[0]} samples")
    
    # 2. Train Anomaly Detector
    print("\n2. Training Anomaly Detector...")
    anomaly_detector = AnomalyDetector(contamination=y_train.mean())
    anomaly_detector.train(X_train)
    anomaly_detector.evaluate(X_test, y_test)
    anomaly_detector.save_model()
    
    # 3. Train Fault Predictor
    print("\n3. Training Fault Predictor...")
    fault_predictor = FaultPredictor()
    fault_predictor.train(X_train, fault_train)
    fault_predictor.evaluate(X_test, fault_test)
    fault_predictor.save_model()
    
    # 4. Save feature names and scaler
    print("\n4. Saving preprocessor objects...")
    joblib.dump(processor.scaler, 'models/scaler.pkl')
    joblib.dump(processor.label_encoder, 'models/label_encoder.pkl')
    joblib.dump(features, 'models/feature_names.pkl')
    
    print("\n" + "="*50)
    print("Model Training Completed Successfully!")
    print("="*50)
    
    return anomaly_detector, fault_predictor, processor

if __name__ == '__main__':
    train_all_models()
