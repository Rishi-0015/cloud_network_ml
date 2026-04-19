# 🌩️ Cloud Network ML - Intelligent Fault Detection & Auto-Healing System

An AI-powered network monitoring system that detects anomalies in real-time and automatically heals network faults using Machine Learning.

## 📁 Project Structure
Cloud_Network_ML/
│
├── main.py # Main entry point
├── insert_data.py # Data insertion tool
├── requirements.txt # Python dependencies
│
├── cloud_network_ml/
│ ├── collector.py # Data generation script
│ └── sample_data.csv # Dataset (10000 samples)
│
├── dashboard/
│ ├── app.py # Main Flask dashboard
│ ├── app_simple.py # Simplified dashboard
│ ├── preprocessing/
│ │ └── data_processor.py # Data cleaning & features
│ ├── static/
│ │ └── style.css # Dashboard styling
│ └── templates/
│ └── index.html # Dashboard UI
│
├── models/
│ ├── anomaly_detector.pkl # Isolation Forest model
│ ├── fault_predictor.pkl # Random Forest model
│ ├── scaler.pkl # Feature scaler
│ ├── label_encoder.pkl # Device encoder
│ └── feature_names.pkl # Feature list
│
├── alerts/
│ └── alert_system.py # Alert generation module
│
└── README.md # Project documentation

text

## 🚀 Installation and Setup

### Prerequisites
- Python 3.10 or higher
- pip package manager

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/Cloud-Network-ML.git
cd Cloud-Network-ML
Step 2: Create Virtual Environment
Windows:

bash
python -m venv venv
venv\Scripts\activate
Mac/Linux:

bash
python3 -m venv venv
source venv/bin/activate
Step 3: Install Dependencies
bash
pip install -r requirements.txt
Step 4: Train Models (First Time Only)
bash
python main.py --train
This will:

Generate 10000 synthetic network samples

Train Isolation Forest for anomaly detection (98% accuracy)

Train Random Forest for fault prediction (95% accuracy)

Save models in the models/ folder

Step 5: Run the Dashboard
bash
python dashboard/app_simple.py
Open your browser and go to: http://localhost:5000

📖 How to Use
1. Dashboard
View system health, active alerts, anomaly rate, and real-time charts.

2. Insert Data
Select device ID (router_01, switch_02, server_03, firewall_04, load_balancer_05)

Adjust 6 parameter sliders (CPU, Memory, Bandwidth, Packet Loss, Latency)

Click "Insert Data" to add normal metrics

Click "Insert Anomaly" to test auto-healing

3. Auto-Healing
System automatically detects anomalies based on thresholds:

Anomaly Type	Threshold	Healing Action
High CPU	>85%	Throttle CPU by 40%
High Memory	>85%	Clear memory cache
Packet Loss	>5%	Re-route network
High Latency	>100ms	Switch to backup server
4. Dashboard Controls
Button	Function
Insert Data	Add normal network metrics
Insert Anomaly	Add anomalous data to test healing
Toggle Auto-Heal	Enable/disable automatic healing
Auto Refresh	Update dashboard every 5 seconds
Clear Alerts	Reset alert history
5. Command Line Data Insertion
bash
python insert_data.py
Options:

Option 1: Insert single record

Option 2: Insert 100 random records

Option 3: Insert custom number of records

Option 4: Insert from CSV file

📊 Model Performance
Model	Algorithm	Accuracy
Anomaly Detector	Isolation Forest	97.95%
Fault Predictor	Random Forest	95.20%
📝 API Endpoints
Endpoint	Method	Description
/	GET	Dashboard UI
/api/dashboard	GET	Get dashboard data
/api/insert_data	POST	Insert network data
/api/toggle_auto_heal	POST	Toggle auto-healing
/api/get_healing_log	GET	Get healing history
/api/clear_alerts	POST	Clear all alerts
📈 Sample Data CSV Format
csv
device_id,cpu_usage_percent,memory_usage_percent,bandwidth_mbps,packet_loss_percent,latency_ms
router_01,45,55,500,0.5,20
switch_02,92,60,700,2,35
server_03,98,90,800,8,200
firewall_04,88,70,600,3,150
load_balancer_05,50,45,550,1,25
⚠️ Troubleshooting
Issue	Solution
ModuleNotFoundError: pkg_resources	pip install --upgrade setuptools wheel
Permission denied writing CSV	Remove-Item cloud_network_ml/sample_data.csv -Force
Dashboard not updating	Click "Auto Refresh" button or refresh browser
Models not found	Run python main.py --train first
🎯 Future Enhancements
LSTM-based time series prediction

Multi-cloud support (AWS, Azure, GCP)

Email/SMS alert notifications

Historical data analytics

REST API for external integrations

Docker containerization

👥 Authors
Name	Registration No
Bagadi Karthik	22UECM0020
Nukala Syam Venkata Dhanush	22UECM0187
Supervisor: Dr. S. Durai, Associate Professor, Department of Computer Science and Engineering

📚 References
Kuila, A., & Kumar, D. (2025). Optimizing Biofuel Production with Artificial Intelligence. John Wiley & Sons.

Hassan, M. M., et al. (2025). Enhancing Prediction of Bioenergy Yield using AI-based Identification of Biomass Species. IEEE ICMISI.

Kazmi, A., et al. (2025). Innovations in bioethanol production. Energy Strategy Reviews, 57, 101634.

Mafat, I. H., et al. (2024). Machine learning and artificial intelligence for algal cultivation and biofuel production optimization. Springer.

Saju, L., et al. (2025). Artificial intelligence and machine intelligence for modeling of bioenergy production. Elsevier.

Patidar, S. K., & Raheman, H. (2023). An AI-based approach to improve fuel properties. Biofuels, 14(6), 619-633.

🙏 Acknowledgments
Vel Tech Rangarajan Dr. Sagunthala R&D Institute of Science and Technology

Department of Computer Science and Engineering

Dr. S. Durai for continuous guidance and support

📝 License
MIT License

⭐ Show Your Support
If you find this project useful, please give it a star on GitHub!

Made with ❤️ for Network Fault Detection
