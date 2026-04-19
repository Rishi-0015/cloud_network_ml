import pandas as pd
import numpy as np
from datetime import datetime
import json
import os

class AlertSystem:
    def __init__(self):
        self.alerts = []
        self.thresholds = {
            'cpu_usage_percent': 85,
            'memory_usage_percent': 85,
            'packet_loss_percent': 5,
            'latency_ms': 100
        }
        
    def check_metrics(self, metrics_dict):
        alerts_generated = []
        
        # Check CPU usage
        if metrics_dict.get('cpu_usage_percent', 0) > self.thresholds['cpu_usage_percent']:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'critical',
                'type': 'high_cpu',
                'message': f"High CPU usage: {metrics_dict['cpu_usage_percent']:.1f}% on {metrics_dict.get('device_id', 'unknown')}",
                'value': metrics_dict['cpu_usage_percent']
            }
            alerts_generated.append(alert)
            
        # Check Memory usage
        if metrics_dict.get('memory_usage_percent', 0) > self.thresholds['memory_usage_percent']:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'critical',
                'type': 'high_memory',
                'message': f"High Memory usage: {metrics_dict['memory_usage_percent']:.1f}% on {metrics_dict.get('device_id', 'unknown')}",
                'value': metrics_dict['memory_usage_percent']
            }
            alerts_generated.append(alert)
            
        # Check Packet Loss
        if metrics_dict.get('packet_loss_percent', 0) > self.thresholds['packet_loss_percent']:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'warning',
                'type': 'packet_loss',
                'message': f"High Packet Loss: {metrics_dict['packet_loss_percent']:.1f}% on {metrics_dict.get('device_id', 'unknown')}",
                'value': metrics_dict['packet_loss_percent']
            }
            alerts_generated.append(alert)
            
        # Check Latency
        if metrics_dict.get('latency_ms', 0) > self.thresholds['latency_ms']:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'warning',
                'type': 'high_latency',
                'message': f"High Latency: {metrics_dict['latency_ms']:.1f}ms on {metrics_dict.get('device_id', 'unknown')}",
                'value': metrics_dict['latency_ms']
            }
            alerts_generated.append(alert)
            
        # Add anomaly alert if detected by ML
        if metrics_dict.get('is_anomaly', 0) == 1:
            alert = {
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'severity': 'critical',
                'type': 'ml_anomaly',
                'message': f"ML Model detected anomaly on {metrics_dict.get('device_id', 'unknown')} - Fault Type: {metrics_dict.get('fault_type', 'unknown')}",
                'value': 1
            }
            alerts_generated.append(alert)
            
        # Add to alerts list (keep last 100)
        self.alerts.extend(alerts_generated)
        if len(self.alerts) > 100:
            self.alerts = self.alerts[-100:]
            
        return alerts_generated
    
    def get_recent_alerts(self, count=10):
        return self.alerts[-count:]
    
    def clear_alerts(self):
        self.alerts = []
        
    def get_alert_summary(self):
        if not self.alerts:
            return {'critical': 0, 'warning': 0, 'total': 0}
            
        critical_count = sum(1 for a in self.alerts if a['severity'] == 'critical')
        warning_count = sum(1 for a in self.alerts if a['severity'] == 'warning')
        
        return {
            'critical': critical_count,
            'warning': warning_count,
            'total': len(self.alerts)
        }
    
    def save_alerts(self, filepath='alerts/alerts_log.json'):
        os.makedirs('alerts', exist_ok=True)
        with open(filepath, 'w') as f:
            json.dump(self.alerts, f, indent=2)
        print(f"Alerts saved to {filepath}")
    
    def load_alerts(self, filepath='alerts/alerts_log.json'):
        if os.path.exists(filepath):
            with open(filepath, 'r') as f:
                self.alerts = json.load(f)
            print(f"Loaded {len(self.alerts)} alerts from {filepath}")

if __name__ == '__main__':
    alert_system = AlertSystem()
    
    # Test with sample metrics
    test_metrics = {
        'device_id': 'router_01',
        'cpu_usage_percent': 92,
        'memory_usage_percent': 88,
        'packet_loss_percent': 6,
        'latency_ms': 150,
        'is_anomaly': 1,
        'fault_type': 'high_cpu'
    }
    
    alerts = alert_system.check_metrics(test_metrics)
    for alert in alerts:
        print(f"[{alert['severity'].upper()}] {alert['message']}")
    
    print(f"\nAlert Summary: {alert_system.get_alert_summary()}")
