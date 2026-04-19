import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os

class FaultPredictor:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
        self.fault_types = ['normal', 'high_cpu', 'high_memory', 'network_congestion', 'hardware_fault']
        
    def train(self, X_train, y_train):
        print("Training Random Forest model for fault prediction...")
        self.model.fit(X_train, y_train)
        print("Model training completed!")
        return self
    
    def predict(self, X):
        return self.model.predict(X)
    
    def predict_proba(self, X):
        return self.model.predict_proba(X)
    
    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        print("\nFault Prediction Results:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=self.fault_types))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        return y_pred
    
    def save_model(self, filepath='models/fault_predictor.pkl'):
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='models/fault_predictor.pkl'):
        if os.path.exists(filepath):
            self.model = joblib.load(filepath)
            print(f"Model loaded from {filepath}")
            return True
        print(f"Model file {filepath} not found")
        return False
    
    def predict_fault_type(self, features):
        prediction = self.model.predict([features])[0]
        probabilities = self.model.predict_proba([features])[0]
        confidence = max(probabilities) * 100
        return prediction, confidence

if __name__ == '__main__':
    # Test with sample data
    from sklearn.datasets import make_classification
    
    X_train, y_train = make_classification(n_samples=1000, n_features=10, n_classes=5, 
                                           n_informative=8, random_state=42)
    X_test, y_test = make_classification(n_samples=200, n_features=10, n_classes=5,
                                        n_informative=8, random_state=42)
    
    predictor = FaultPredictor()
    predictor.train(X_train, y_train)
    predictor.evaluate(X_test, y_test)
    predictor.save_model()
