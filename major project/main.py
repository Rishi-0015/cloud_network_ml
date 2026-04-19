#!/usr/bin/env python
"""
Cloud Network ML - Main Entry Point
Network Fault Detection and Anomaly Prediction System
"""

import sys
import os
import subprocess
import webbrowser
import time

def print_banner():
    print("="*60)
    print("     CLOUD NETWORK ML - FAULT DETECTION SYSTEM")
    print("="*60)
    print("   - Anomaly Detection using Isolation Forest")
    print("   - Fault Prediction using Random Forest")
    print("   - Real-time Monitoring Dashboard")
    print("="*60)

def check_requirements():
    print("\n[1/4] Checking requirements...")
    try:
        import flask, pandas, numpy, sklearn
        print("✓ All requirements are installed")
        return True
    except ImportError as e:
        print(f"✗ Missing requirement: {e}")
        print("\nPlease install requirements using:")
        print("pip install -r requirements.txt")
        return False

def generate_data():
    print("\n[2/4] Generating sample network data...")
    try:
        from cloud_network_ml.collector import DataCollector
        collector = DataCollector()
        df = collector.generate_sample_data()
        print(f"✓ Generated {len(df)} samples with {df['is_anomaly'].sum()} anomalies")
        return True
    except Exception as e:
        print(f"✗ Error generating data: {e}")
        return False

def train_models():
    print("\n[3/4] Training ML models...")
    try:
        from models.train_models import train_all_models
        train_all_models()
        print("✓ Models trained successfully")
        return True
    except Exception as e:
        print(f"✗ Error training models: {e}")
        return False

def launch_dashboard():
    print("\n[4/4] Launching dashboard...")
    print("\n" + "="*60)
    print("Starting Flask Dashboard...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press CTRL+C to stop the server")
    print("="*60 + "\n")
    
    # Open browser after 2 seconds
    time.sleep(2)
    webbrowser.open("http://localhost:5000")
    
    # Run the dashboard
    try:
        from dashboard.app import socketio, app
        socketio.run(app, debug=False, port=5000, allow_unsafe_werkzeug=True)
    except KeyboardInterrupt:
        print("\n\nShutting down server...")
    except Exception as e:
        print(f"Error launching dashboard: {e}")

def main():
    print_banner()
    
    # Check if we should train first
    if len(sys.argv) > 1 and sys.argv[1] == '--train':
        if check_requirements():
            if generate_data():
                train_models()
        return
    
    # Normal startup
    if not os.path.exists('models/anomaly_detector.pkl'):
        print("\n⚠ Models not found! Running setup...\n")
        if check_requirements():
            if generate_data():
                if train_models():
                    launch_dashboard()
    else:
        launch_dashboard()

if __name__ == '__main__':
    main()
