🌩️ Cloud Network ML - Intelligent Fault Detection & Auto-Healing System
An AI-powered network monitoring system that detects anomalies in real-time and automatically heals network faults using Machine Learning.

🚀 Features
Real-time Network Monitoring - Live dashboard with auto-refresh

Anomaly Detection - Isolation Forest ML model (98% accuracy)

Fault Prediction - Random Forest classifier for fault type prediction

Auto-Healing System - Automatically fixes detected anomalies

Interactive Dashboard - Web-based interface with Plotly charts

Data Insertion - Add network data manually or via CSV

Alert System - Real-time threshold-based alerts

🛠️ Tech Stack
Technology	Purpose
Python 3.10+	Core programming language
Flask	Web dashboard framework
Pandas	Data processing
Scikit-learn	ML models
Plotly	Interactive charts
NumPy	Numerical computations
📁 Project Structure
text
major-project/
├── alerts/
│   └── alert_system.py
├── cloud_network_ml/
│   ├── collector.py
│   └── sample_data.csv
├── dashboard/
│   ├── preprocessing/
│   │   └── data_processor.py
│   ├── static/
│   │   └── style.css
│   ├── templates/
│   │   └── index.html
│   └── app_simple.py
├── models/
│   ├── anomaly_detector.py
│   ├── fault_predictor.py
│   ├── train_models.py
│   └── *.pkl
├── insert_data.py
├── main.py
└── requirements.txt
📦 Installation
bash
# Clone repository
git clone https://github.com/yourusername/cloud-network-ml.git
cd cloud-network-ml

# Install dependencies
pip install -r requirements.txt

# Generate data and train models
python main.py --train

# Launch dashboard
python dashboard/app_simple.py
Open browser at http://localhost:5000

🎮 Dashboard Controls
Button	Function
Insert Data	Add normal network metrics
Insert Anomaly	Add anomalous data to test healing
Toggle Auto-Heal	Enable/disable automatic healing
Auto Refresh	Update dashboard every 5 seconds
Clear Alerts	Reset alert history
🤖 Auto-Healing Actions
Anomaly Type	Threshold	Healing Action
High CPU	>85%	Throttle CPU by 40%
High Memory	>85%	Clear memory cache
Packet Loss	>5%	Re-route network
High Latency	>100ms	Switch to backup server
📊 Model Performance
text
Anomaly Detection: 97.95% Accuracy
Fault Prediction: 95.20% Accuracy
📝 API Endpoints
Endpoint	Method	Description
/api/dashboard	GET	Get dashboard data
/api/insert_data	POST	Insert network data
/api/toggle_auto_heal	POST	Toggle auto-healing
/api/get_healing_log	GET	Get healing history
/api/clear_alerts	POST	Clear all alerts
📈 Sample Data CSV
csv
device_id,cpu_usage_percent,memory_usage_percent,bandwidth_mbps,packet_loss_percent,latency_ms
router_01,45,55,500,0.5,20
switch_02,92,60,700,2,35
server_03,98,90,800,8,200
⚠️ Troubleshooting
bash
# Fix setuptools error
pip install --upgrade setuptools wheel

# Fix permission error
Remove-Item cloud_network_ml/sample_data.csv -Force
🎯 Future Enhancements
LSTM-based time series prediction

Multi-cloud support (AWS, Azure, GCP)

Email/SMS alert notifications

Docker containerization

📝 License
MIT License

Made with ❤️ for Network Fault Detection
