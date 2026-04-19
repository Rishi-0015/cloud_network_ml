from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
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

# Global variables
anomaly_detector = None
fault_predictor = None
processor = None
alert_system = None
alert_history = []
auto_heal_enabled = True
healing_log = []

def load_models():
    global anomaly_detector, fault_predictor, processor, alert_system
    
    print("Loading models...")
    
    processor = DataProcessor()
    anomaly_detector = AnomalyDetector()
    fault_predictor = FaultPredictor()
    
    if not anomaly_detector.load_model('models/anomaly_detector.pkl'):
        return False
    
    if not fault_predictor.load_model('models/fault_predictor.pkl'):
        return False
    
    try:
        import joblib
        processor.scaler = joblib.load('models/scaler.pkl')
        processor.label_encoder = joblib.load('models/label_encoder.pkl')
    except:
        pass
    
    alert_system = AlertSystem()
    print("Models loaded successfully!")
    return True

def auto_heal(alert, device_data):
    """Automatically fix anomalies"""
    global healing_log
    
    healing_action = None
    success = False
    
    if alert['type'] == 'high_cpu':
        # Reduce CPU by throttling
        original_value = device_data.get('cpu_usage_percent', 0)
        device_data['cpu_usage_percent'] = max(30, original_value - 40)
        healing_action = f"🔧 Throttled CPU from {original_value:.1f}% to {device_data['cpu_usage_percent']:.1f}%"
        success = True
        
    elif alert['type'] == 'high_memory':
        # Clear memory cache
        original_value = device_data.get('memory_usage_percent', 0)
        device_data['memory_usage_percent'] = max(35, original_value - 35)
        healing_action = f"💾 Cleared memory cache from {original_value:.1f}% to {device_data['memory_usage_percent']:.1f}%"
        success = True
        
    elif alert['type'] == 'packet_loss':
        # Reset network route
        original_value = device_data.get('packet_loss_percent', 0)
        device_data['packet_loss_percent'] = max(0.5, original_value - 4)
        healing_action = f"🌐 Re-routed network - Packet loss reduced from {original_value:.1f}% to {device_data['packet_loss_percent']:.1f}%"
        success = True
        
    elif alert['type'] == 'high_latency':
        # Switch to backup server
        original_value = device_data.get('latency_ms', 0)
        device_data['latency_ms'] = max(15, original_value - 80)
        healing_action = f"⚡ Switched to backup server - Latency reduced from {original_value:.1f}ms to {device_data['latency_ms']:.1f}ms"
        success = True
        
    elif alert['type'] == 'ml_anomaly':
        # Full system reset
        device_data['cpu_usage_percent'] = 35
        device_data['memory_usage_percent'] = 40
        device_data['packet_loss_percent'] = 0.5
        device_data['latency_ms'] = 20
        healing_action = f"🔄 Full system recovery performed on {device_data.get('device_id', 'unknown')}"
        success = True
    
    if success:
        healing_log.append({
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'device': device_data.get('device_id', 'unknown'),
            'alert_type': alert['type'],
            'action': healing_action
        })
        
        # Keep last 20 healing actions
        if len(healing_log) > 20:
            healing_log.pop(0)
    
    return device_data, healing_action, success

def save_to_csv(data):
    """Save inserted data to CSV file"""
    csv_path = 'cloud_network_ml/sample_data.csv'
    
    df_new = pd.DataFrame([data])
    
    if os.path.exists(csv_path):
        df_existing = pd.read_csv(csv_path)
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.to_csv(csv_path, index=False)
    else:
        df_new.to_csv(csv_path, index=False)
    
    return True

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/insert_data', methods=['POST'])
def insert_data():
    global auto_heal_enabled
    
    try:
        data = request.json
        
        # Create record
        record = {
            'timestamp': datetime.now(),
            'device_id': data['device_id'],
            'cpu_usage_percent': float(data['cpu_usage_percent']),
            'memory_usage_percent': float(data['memory_usage_percent']),
            'bandwidth_mbps': float(data['bandwidth_mbps']),
            'packet_loss_percent': float(data['packet_loss_percent']),
            'latency_ms': float(data['latency_ms']),
        }
        
        # Check if anomaly
        is_anomaly = 1 if (record['cpu_usage_percent'] > 85 or 
                           record['memory_usage_percent'] > 85 or 
                           record['packet_loss_percent'] > 5 or 
                           record['latency_ms'] > 100) else 0
        
        # Determine fault type
        if record['cpu_usage_percent'] > 85:
            fault_type = 'high_cpu'
        elif record['memory_usage_percent'] > 85:
            fault_type = 'high_memory'
        elif record['packet_loss_percent'] > 5:
            fault_type = 'packet_loss'
        elif record['latency_ms'] > 100:
            fault_type = 'high_latency'
        else:
            fault_type = 'normal'
        
        record['is_anomaly'] = is_anomaly
        record['fault_type'] = fault_type
        
        # Auto healing
        healing_message = None
        if auto_heal_enabled and is_anomaly == 1:
            alert = {'type': fault_type}
            healed_record, healing_message, healed = auto_heal(alert, record.copy())
            if healed:
                record = healed_record
                record['is_anomaly'] = 0
                record['fault_type'] = 'normal'
        
        # Save to CSV
        save_to_csv(record)
        
        # Check alerts
        alerts = alert_system.check_metrics(record)
        alert_history.extend(alerts)
        
        return jsonify({
            'success': True,
            'message': f'Data inserted for {record["device_id"]}',
            'is_anomaly': is_anomaly,
            'fault_type': fault_type,
            'auto_healed': healing_message is not None,
            'healing_message': healing_message
        })
        
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/api/toggle_auto_heal', methods=['POST'])
def toggle_auto_heal():
    global auto_heal_enabled
    auto_heal_enabled = not auto_heal_enabled
    return jsonify({
        'status': 'success',
        'auto_heal_enabled': auto_heal_enabled
    })

@app.route('/api/get_healing_log', methods=['GET'])
def get_healing_log():
    return jsonify({'healing_log': healing_log})

@app.route('/api/dashboard')
def get_dashboard_data():
    global alert_history
    
    # Generate random data for demo
    data = generate_realtime_data()
    
    # Check alerts
    alerts = alert_system.check_metrics(data)
    alert_history.extend(alerts)
    
    # Keep last 50 alerts
    if len(alert_history) > 50:
        alert_history = alert_history[-50:]
    
    # Calculate statistics
    total_alerts = len(alert_history)
    critical_alerts = sum(1 for a in alert_history if a.get('severity') == 'critical')
    
    if critical_alerts > 0:
        health_status = "Critical"
    elif total_alerts > 5:
        health_status = "Warning"
    else:
        health_status = "Healthy"
    
    # Create chart data
    normal_count = max(0, 10 - min(10, total_alerts))
    anomaly_count = min(10, total_alerts)
    
    anomaly_chart = {
        'data': [{
            'x': ['Normal', 'Anomaly'],
            'y': [normal_count * 10, anomaly_count * 10],
            'type': 'bar',
            'marker': {'color': ['#28a745', '#dc3545']}
        }],
        'layout': {'title': 'Anomaly Detection Status', 'height': 400}
    }
    
    # Fault distribution
    fault_counts = {'normal': 0, 'high_cpu': 0, 'high_memory': 0, 'packet_loss': 0, 'high_latency': 0}
    for alert in alert_history[-10:]:
        alert_type = alert.get('type', 'normal')
        if alert_type in fault_counts:
            fault_counts[alert_type] += 1
        else:
            fault_counts['normal'] += 1
    
    fault_chart = {
        'data': [{
            'labels': list(fault_counts.keys()),
            'values': list(fault_counts.values()),
            'type': 'pie',
            'marker': {'colors': ['#28a745', '#dc3545', '#ffc107', '#17a2b8', '#6f42c1']}
        }],
        'layout': {'title': 'Fault Distribution', 'height': 400}
    }
    
    # Format alerts
    formatted_alerts = []
    for alert in alert_history[-10:]:
        formatted_alerts.append({
            'timestamp': alert.get('timestamp', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
            'severity': alert.get('severity', 'info'),
            'message': alert.get('message', 'No message')
        })
    
    return jsonify({
        'health_status': health_status,
        'alert_count': total_alerts,
        'device_count': 5,
        'anomaly_rate': min(100, total_alerts * 2),
        'anomaly_chart': anomaly_chart,
        'fault_chart': fault_chart,
        'alerts': formatted_alerts,
        'auto_heal_enabled': auto_heal_enabled,
        'healing_count': len(healing_log)
    })

@app.route('/api/clear_alerts', methods=['POST'])
def clear_alerts():
    global alert_history
    alert_history = []
    alert_system.clear_alerts()
    return jsonify({'status': 'success'})

def generate_realtime_data():
    devices = ['router_01', 'switch_02', 'server_03', 'firewall_04', 'load_balancer_05']
    
    data = {
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'device_id': random.choice(devices),
        'cpu_usage_percent': min(100, max(0, np.random.normal(45, 15))),
        'memory_usage_percent': min(100, max(0, np.random.normal(55, 20))),
        'bandwidth_mbps': max(0, np.random.normal(500, 150)),
        'packet_loss_percent': max(0, min(20, np.random.exponential(0.5))),
        'latency_ms': max(0, min(500, np.random.normal(20, 8))),
    }
    
    # Inject anomalies (10% chance)
    if random.random() < 0.1:
        fault_type = random.choice(['high_cpu', 'high_memory', 'packet_loss', 'high_latency'])
        if fault_type == 'high_cpu':
            data['cpu_usage_percent'] = random.uniform(85, 100)
        elif fault_type == 'high_memory':
            data['memory_usage_percent'] = random.uniform(85, 98)
        elif fault_type == 'packet_loss':
            data['packet_loss_percent'] = random.uniform(5, 15)
        elif fault_type == 'high_latency':
            data['latency_ms'] = random.uniform(150, 300)
        data['is_anomaly'] = 1
        data['fault_type'] = fault_type
    else:
        data['is_anomaly'] = 0
        data['fault_type'] = 'normal'
    
    return data

if __name__ == '__main__':
    print("="*50)
    print("Cloud Network ML Dashboard with AUTO-HEALING")
    print("="*50)
    print("Auto-healing will automatically fix anomalies when detected!")
    
    if load_models():
        print("\nStarting Flask server...")
        print("Access the dashboard at: http://localhost:5000")
        app.run(debug=True, port=5000)
    else:
        print("\nPlease train models first by running: python models/train_models.py")
