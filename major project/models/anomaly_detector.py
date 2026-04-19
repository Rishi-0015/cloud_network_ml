import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
import joblib
import os

class AnomalyDetector:
    def __init__(self, contamination=0.05):
        self.model = IsolationForest(contamination=contamination, random_state=42, n_estimators=100)
        self.contamination = contamination
        
    def train(self, X_train, y_train=None):
        print("Training Isolation Forest model...")
        self.model.fit(X_train)
        print("Model training completed!")
        return self
    
    def predict(self, X):
        # Isolation Forest returns -1 for anomalies, 1 for normal
        predictions = self.model.predict(X)
        # Convert to 1 for anomaly, 0 for normal
        return np.where(predictions == -1, 1, 0)
    
    def evaluate(self, X_test, y_test):
        y_pred = self.predict(X_test)
        print("\nAnomaly Detection Results:")
        print(f"Accuracy: {accuracy_score(y_test, y_pred):.4f}")
        print("\nClassification Report:")
        print(classification_report(y_test, y_pred, target_names=['Normal', 'Anomaly']))
        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))
        return y_pred
    
    def save_model(self, filepath='models/anomaly_detector.pkl'):
        joblib.dump(self.model, filepath)
        print(f"Model saved to {filepath}")
    
    def load_model(self, filepath='models/anomaly_detector.pkl'):
        if os.path.exists(filepath):
            self.model = joblib.load(filepath)
            print(f"Model loaded from {filepath}")
            return True
        print(f"Model file {filepath} not found")
        return False
    
    def detect_anomalies_realtime(self, features):
        prediction = self.model.predict([features])[0]
        return 1 if prediction == -1 else 0

if __name__ == '__main__':
    # Test the detector with sample data
    from sklearn.datasets import make_blobs
    
    # Generate sample data
    X_train, _ = make_blobs(n_samples=1000, centers=1, n_features=5, random_state=42)
    X_test, y_test = make_blobs(n_samples=200, centers=1, n_features=5, random_state=42)
    y_test = np.zeros(200)
    # Add some anomalies
    anomalies = np.random.uniform(low=-10, high=10, size=(20, 5))
    X_test[-20:] = anomalies
    y_test[-20:] = 1
    
    detector = AnomalyDetector(contamination=0.1)
    detector.train(X_train)
    detector.evaluate(X_test, y_test)
    detector.save_model()
