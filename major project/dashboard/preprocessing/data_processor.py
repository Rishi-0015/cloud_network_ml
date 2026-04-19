import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split

class DataProcessor:
    def __init__(self):
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
    def load_data(self, filepath='cloud_network_ml/sample_data.csv'):
        df = pd.read_csv(filepath)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    
    def clean_data(self, df):
        # Remove duplicates
        df = df.drop_duplicates()
        
        # Handle missing values using ffill and bfill (newer pandas syntax)
        df = df.ffill()
        df = df.bfill()
        
        # Remove outliers using IQR
        numeric_cols = ['cpu_usage_percent', 'memory_usage_percent', 'bandwidth_mbps', 'packet_loss_percent', 'latency_ms']
        for col in numeric_cols:
            if col in df.columns:
                Q1 = df[col].quantile(0.25)
                Q3 = df[col].quantile(0.75)
                IQR = Q3 - Q1
                lower_bound = Q1 - 3 * IQR
                upper_bound = Q3 + 3 * IQR
                df[col] = df[col].clip(lower_bound, upper_bound)
        
        return df
    
    def extract_features(self, df):
        # Time-based features
        df['hour'] = df['timestamp'].dt.hour
        df['day_of_week'] = df['timestamp'].dt.dayofweek
        df['is_weekend'] = df['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
        
        # Rolling statistics
        df['cpu_rolling_mean'] = df['cpu_usage_percent'].rolling(window=5, min_periods=1).mean()
        df['memory_rolling_mean'] = df['memory_usage_percent'].rolling(window=5, min_periods=1).mean()
        df['bandwidth_rolling_mean'] = df['bandwidth_mbps'].rolling(window=5, min_periods=1).mean()
        
        # Fill any NaN values from rolling
        df = df.fillna(0)
        
        # Device encoding
        df['device_encoded'] = self.label_encoder.fit_transform(df['device_id'])
        
        return df
    
    def prepare_features(self, df):
        feature_cols = ['cpu_usage_percent', 'memory_usage_percent', 'bandwidth_mbps', 
                       'packet_loss_percent', 'latency_ms', 'hour', 'day_of_week', 
                       'is_weekend', 'cpu_rolling_mean', 'memory_rolling_mean', 
                       'bandwidth_rolling_mean', 'device_encoded']
        
        X = df[feature_cols]
        y = df['is_anomaly']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        return X_scaled, y, feature_cols
    
    def split_data(self, X, y, test_size=0.2, val_size=0.1):
        X_temp, X_test, y_temp, y_test = train_test_split(X, y, test_size=test_size, random_state=42, stratify=y)
        val_size_adjusted = val_size / (1 - test_size)
        X_train, X_val, y_train, y_val = train_test_split(X_temp, y_temp, test_size=val_size_adjusted, random_state=42, stratify=y_temp)
        
        return X_train, X_val, X_test, y_train, y_val, y_test

if __name__ == '__main__':
    processor = DataProcessor()
    df = processor.load_data()
    df = processor.clean_data(df)
    df = processor.extract_features(df)
    X, y, features = processor.prepare_features(df)
    X_train, X_val, X_test, y_train, y_val, y_test = processor.split_data(X, y)
    
    print(f"Training set: {X_train.shape}")
    print(f"Validation set: {X_val.shape}")
    print(f"Test set: {X_test.shape}")
    print(f"Features: {features}")
