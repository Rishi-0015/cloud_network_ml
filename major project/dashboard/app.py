from flask import Flask, render_template, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import pandas as pd
import numpy as np
import sys
import os
import random
from datetime import datetime
import threading
import time

# Add paths
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import modules
from dashboard.preprocessing.data_processor import DataProcessor
from models.anomaly_detector import AnomalyDetector
from models.fault_predictor import FaultPredictor
from alerts.alert_system import AlertSystem

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables
anomaly_detector = None
fault_predictor = None
processor = None
alert_system = None
monitoring_active = False
monitoring_thread = None

def load_models():
    global anomaly_detector, fault_predictor, processor, alert_system
    
    print("Loading models...")
    
    # Initialize processor
    processor = DataProcessor()
    
    # Load models
    anomaly_detector = AnomalyDetector()
    fault_predictor = FaultPredictor()
    
    # Try to load existing models
    if not anomaly_detector.load_model('models/anomaly_detector.pkl'):
        print("Models not found. Please run train_models.py first")
        return False
    
    if not fault_predictor.load_model('models/fault_predictor.pkl'):
        print("Fault predictor model not found")
        return False
    
    # Load scaler and label encoder
    try:
        import joblib
        processor.scaler = joblib.load('models/scaler.pkl')
        processor.label_encoder = joblib.load('models/label_encoder.pkl')
    except:
        print("Warning: Could not load preprocessor objects")
    
    # Initialize alert system
    alert_system = AlertSystem()
    
    print("Models loaded successfully!")
    return True

def generate_realtime_data():
    # Generate simulated real-time metrics
    devices = ['router_01', 'switch_02', 'server_03', 'firewall_04', 'load_balancer_05']
    
    data = {
        'timestamp': datetime.now(),
        'device_id': random.choice(devices),
        'cpu_usage_percent': np.random.normal(45, 15),
        'memory_usage_percent': np.random.normal(55, 20),
        'bandwidth_mbps': np.random.normal(500, 150),
        'packet_loss_percent': max(0, np.random.exponential(0.5)),
        'latency_ms': max(0, np.random.normal(20, 8)),
        'is_anomaly': 0,
        'fault_type': 'normal'
    }
    
    # Constrain values
    data['cpu_usage_percent'] = min(100, max(0, data['cpu_usage_percent']))
    data['memory_usage_percent'] = min(100, max(0, data['memory_usage_percent']))
    data['packet_loss_percent'] = min(20, data['packet_loss_percent'])
    data['latency_ms'] = min(500, max(0, data['latency_ms']))
    
    # Occasionally inject anomalies (10% chance)
    if random.random() < 0.1:
        data['is_anomaly'] = 1
        fault_type = random.choice(['high_cpu', 'high_memory', 'network_congestion', 'hardware_fault'])
        data['fault_type'] = fault_type
        
        if fault_type == 'high_cpu':
            data['cpu_usage_percent'] = np.random.uniform(85, 100)
        elif fault_type == 'high_memory':
            data['memory_usage_percent'] = np.random.uniform(85, 98)
        elif fault_type == 'network_congestion':
            data['bandwidth_mbps'] = np.random.uniform(800, 1200)
            data['packet_loss_percent'] = np.random.uniform(5, 15)
        elif fault_type == 'hardware_fault':
            data['latency_ms'] = np.random.uniform(150, 300)
    
    return data

def process_and_predict(data):
    # Prepare features for prediction
    df = pd.DataFrame([data])
    
    # Create a copy to avoid warnings
    df_copy = df.copy()
    
    # Extract time features
    df_copy['hour'] = df_copy['timestamp'].dt.hour
    df_copy['day_of_week'] = df_copy['timestamp'].dt.dayofweek
    df_copy['is_weekend'] = df_copy['day_of_week'].apply(lambda x: 1 if x >= 5 else 0)
    
    # Rolling stats (using current value since only one row)
    df_copy['cpu_rolling_mean'] = df_copy['cpu_usage_percent']
    df_copy['memory_rolling_mean'] = df_copy['memory_usage_percent']
    df_copy['bandwidth_rolling_mean'] = df_copy['bandwidth_mbps']
    
    # Device encoding
    try:
        from sklearn.preprocessing import LabelEncoder
        le = LabelEncoder()
        le.fit(['router_01', 'switch_02', 'server_03', 'firewall_04', 'load_balancer_05'])
        df_copy['device_encoded'] = le.transform([data['device_id']])[0]
    except:
        df_copy['device_encoded'] = 0
    
    feature_cols = ['cpu_usage_percent', 'memory_usage_percent', 'bandwidth_mbps', 
                   'packet_loss_percent', 'latency_ms', 'hour', 'day_of_week', 
                   'is_weekend', 'cpu_rolling_mean', 'memory_rolling_mean', 
                   'bandwidth_rolling_mean', 'device_encoded']
    
    # Fill any missing values
    for col in feature_cols:
        if col not in df_copy.columns:
            df_copy[col] = 0
    
    X = df_copy[feature_cols].values
    
    # Scale features
    try:
        import joblib
        scaler = joblib.load('models/scaler.pkl')
        X = scaler.transform(X)
    except:
        pass
    
    # Predict anomaly
    try:
        is_anomaly = anomaly_detector.predict(X)[0]
        data['is_anomaly'] = int(is_anomaly)
    except:
        pass
    
    # Predict fault type
    if data['is_anomaly'] == 1:
        try:
            fault_pred, confidence = fault_predictor.predict_fault_type(X[0])
            data['fault_type'] = fault_predictor.fault_types[fault_pred] if fault_pred < len(fault_predictor.fault_types) else 'unknown'
        except:
            pass
    else:
        data['fault_type'] = 'normal'
    
    # Check alerts
    alerts = alert_system.check_metrics(data)
    
    return data, alerts

def monitoring_loop():
    global monitoring_active
    while monitoring_active:
        data = generate_realtime_data()
        processed_data, alerts = process_and_predict(data)
        
        # Emit update to all connected clients
        dashboard_data = get_dashboard_data()
        socketio.emit('dashboard_update', dashboard_data)
        
        time.sleep(5)  # Update every 5 seconds

def get_dashboard_data():
    # Get recent alerts
    recent_alerts = alert_system.get_recent_alerts(10)
    
    # Calculate statistics
    total_alerts = alert_system.get_alert_summary()['total']
    critical_alerts = alert_system.get_alert_summary()['critical']
    
    # Determine health status
    if critical_alerts > 0:
        health_status = "Critical"
    elif total_alerts > 5:
        health_status = "Warning"
    else:
        health_status = "Healthy"
    
    # Create anomaly chart data
    anomaly_chart = {
        'data': [{
            'x': ['Normal', 'Anomaly'],
            'y': [max(0, 100 - total_alerts * 2), min(100, total_alerts * 2)],
            'type': 'bar',
            'marker': {'color': ['#28a745', '#dc3545']}
        }],
        'layout': {'title': 'Anomaly Detection Status', 'height': 400}
    }
    
    # Count fault types from alerts
    fault_counts = {'normal': 0, 'high_cpu': 0, 'high_memory': 0, 'network_congestion': 0, 'hardware_fault': 0}
    for alert in recent_alerts:
        alert_type = alert.get('type', 'unknown')
        if alert_type in fault_counts:
            fault_counts[alert_type] += 1
    
    # Create fault distribution chart
    fault_chart = {
        'data': [{
            'labels': list(fault_counts.keys()),
            'values': list(fault_counts.values()),
            'type': 'pie',
            'marker': {'colors': ['#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1']}
        }],
        'layout': {'title': 'Fault Distribution (Last 10 Alerts)', 'height': 400}
    }
    
    # Format alerts for display
    formatted_alerts = []
    for alert in recent_alerts:
        formatted_alerts.append({
            'timestamp': alert['timestamp'],
            'severity': alert['severity'],
            'message': alert['message']
        })
    
    dashboard_data = {
        'health_status': health_status,
        'alert_count': total_alerts,
        'device_count': 5,
        'anomaly_rate': min(100, total_alerts * 2),
        'anomaly_chart': anomaly_chart,
        'fault_chart': fault_chart,
        'alerts': formatted_alerts
    }
    
    return dashboard_data

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dashboard')
def api_dashboard():
    return jsonify(get_dashboard_data())

@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('dashboard_update', get_dashboard_data())

@socketio.on('request_update')
def handle_update():
    emit('dashboard_update', get_dashboard_data())

@socketio.on('start_monitoring')
def start_monitoring():
    global monitoring_active, monitoring_thread
    if not monitoring_active:
        monitoring_active = True
        monitoring_thread = threading.Thread(target=monitoring_loop)
        monitoring_thread.daemon = True
        monitoring_thread.start()
        print("Monitoring started")
    emit('dashboard_update', get_dashboard_data())

@socketio.on('stop_monitoring')
def stop_monitoring():
    global monitoring_active
    monitoring_active = False
    print("Monitoring stopped")

if __name__ == '__main__':
    print("="*50)
    print("Cloud Network ML Dashboard")
    print("="*50)
    
    # Load models
    if load_models():
        print("\nStarting Flask server...")
        print("Access the dashboard at: http://localhost:5000")
        socketio.run(app, debug=False, port=5000, allow_unsafe_werkzeug=True)
    else:
        print("\nPlease train models first by running: python models/train_models.py")
