# 🌩️ Cloud Network ML - Intelligent Fault Detection & Auto-Healing System

An AI-powered network monitoring system that detects anomalies in real-time and automatically heals network faults using Machine Learning.

## 🚀 Features

- **Real-time Network Monitoring** - Live dashboard with auto-refresh
- **Anomaly Detection** - Isolation Forest ML model (98% accuracy)
- **Fault Prediction** - Random Forest classifier for fault type prediction
- **Auto-Healing System** - Automatically fixes detected anomalies
- **Interactive Dashboard** - Web-based interface with Plotly charts
- **Data Insertion** - Add network data manually or via CSV
- **Alert System** - Real-time threshold-based alerts

## 🛠️ Tech Stack

| Technology | Purpose |
|------------|---------|
| Python 3.10+ | Core programming language |
| Flask | Web dashboard framework |
| Pandas | Data processing |
| Scikit-learn | ML models (Isolation Forest, Random Forest) |
| Plotly | Interactive charts |
| NumPy | Numerical computations |

## 📁 Project Structure
major-project/
├── alerts/
│ └── alert_system.py # Alert generation module
├── cloud_network_ml/
│ ├── collector.py # Data collection
│ └── sample_data.csv # Network dataset
├── dashboard/
│ ├── preprocessing/
│ │ └── data_processor.py # Data cleaning & features
│ ├── static/
│ │ └── style.css # Dashboard styling
│ ├── templates/
│ │ └── index.html # Dashboard UI
│ ├── app.py # Main dashboard
│ └── app_simple.py # Simplified dashboard
├── models/
│ ├── anomaly_detector.py # Isolation Forest model
│ ├── fault_predictor.py # Random Forest model
│ ├── train_models.py # Training script
│ └── *.pkl # Saved models
├── insert_data.py # Data insertion tool
├── main.py # Main entry point
└── requirements.txt # Dependencies

text

## 📦 Installation

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the repository
```bash
git clone https://github.com/yourusername/cloud-network-ml.git
cd cloud-network-ml
Step 2: Install dependencies
bash
pip install -r requirements.txt
Step 3: Generate data and train models
bash
python main.py --train
Step 4: Launch the dashboard
bash
python dashboard/app_simple.py
Step 5: Open your browser
Navigate to http://localhost:5000

🎮 How to Use
Dashboard Controls
Button	Function
Insert Data	Add normal network metrics
Insert Anomaly	Add anomalous data to test healing
Toggle Auto-Heal	Enable/disable automatic healing
Auto Refresh	Update dashboard every 5 seconds
Clear Alerts	Reset alert history
Inserting Data
Via Web Dashboard:

Fill in the form with network metrics

Click "Insert Data"

System detects anomalies automatically

Via Command Line:

bash
python insert_data.py
Choose from:

Single record insertion

Bulk random records

CSV file import

Auto-Healing Actions
Anomaly Type	Threshold	Healing Action
High CPU	>85%	Throttle CPU by 40%
High Memory	>85%	Clear memory cache
Packet Loss	>5%	Re-route network
High Latency	>100ms	Switch to backup server
📊 Model Performance
text
Anomaly Detection (Isolation Forest):
- Accuracy: 97.95%
- Precision: 78%
- Recall: 80%

Fault Prediction (Random Forest):
- Accuracy: 95.20%
🔧 Configuration
Alert Thresholds
Edit alerts/alert_system.py:

python
self.thresholds = {
    'cpu_usage_percent': 85,
    'memory_usage_percent': 85,
    'packet_loss_percent': 5,
    'latency_ms': 100
}
Auto-Healing Rules
Edit dashboard/app_simple.py - auto_heal() function

📝 API Endpoints
Endpoint	Method	Description
/	GET	Dashboard UI
/api/dashboard	GET	Get dashboard data
/api/insert_data	POST	Insert network data
/api/toggle_auto_heal	POST	Toggle auto-healing
/api/get_healing_log	GET	Get healing history
/api/clear_alerts	POST	Clear all alerts
🧪 Testing
Test with Anomaly Data
bash
# Insert a high CPU anomaly
python insert_data.py
# Choose option 1, enter: router_01, 95, 50, 600, 1, 20
Test Auto-Healing
Open dashboard

Click "Insert Anomaly (Test Healing)"

Watch healing log for actions

📈 Sample Data Format
CSV format for bulk import:

csv
device_id,cpu_usage_percent,memory_usage_percent,bandwidth_mbps,packet_loss_percent,latency_ms
router_01,45,55,500,0.5,20
switch_02,92,60,700,2,35
server_03,98,90,800,8,200
🤝 Contributing
Fork the repository

Create feature branch (git checkout -b feature/amazing)

Commit changes (git commit -m 'Add amazing feature')

Push to branch (git push origin feature/amazing)

Open Pull Request

📝 License
MIT License - See LICENSE file for details

👨‍💻 Author
Your Name - [Your GitHub Profile]

🙏 Acknowledgments
Scikit-learn for ML algorithms

Flask for web framework

Plotly for visualizations

⚠️ Troubleshooting
Common Issues
Issue: ModuleNotFoundError: No module named 'pkg_resources'
Solution:

bash
pip install --upgrade setuptools wheel
Issue: Permission denied writing CSV
Solution:

bash
Remove-Item cloud_network_ml/sample_data.csv -Force
Issue: Dashboard not updating
Solution: Click "Auto Refresh" button or refresh browser

🎯 Future Enhancements
LSTM-based time series prediction

Multi-cloud support (AWS, Azure, GCP)

Email/SMS alert notifications

Historical data analytics

REST API for external integrations

Docker containerization

📧 Contact
For questions or support, please open an issue on GitHub.

Made with ❤️ for Network Fault Detection

text

---

**Step 2:** Also create a .gitignore file

Type this command:
```powershell
@"
# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
*.so
*.egg
*.egg-info/
dist/
build/

# Virtual Environment
venv/
env/
ENV/
env.bak/
venv.bak/

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
*.pkl
*.csv
*.log
alerts/alerts_log.json

# OS
.DS_Store
Thumbs.db

# Database
*.db
*.sqlite

# Environment variables
.env
.venv
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
