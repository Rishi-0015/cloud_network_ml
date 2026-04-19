import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

class DataCollector:
    def __init__(self):
        self.devices = ['router_01', 'switch_02', 'server_03', 'firewall_04', 'load_balancer_05']
        
    def generate_sample_data(self, n_samples=10000):
        data = []
        start_date = datetime.now() - timedelta(days=30)
        
        for i in range(n_samples):
            timestamp = start_date + timedelta(minutes=i*5)
            device = random.choice(self.devices)
            
            # Normal metrics
            cpu_usage = np.random.normal(45, 15)
            memory_usage = np.random.normal(55, 20)
            bandwidth_mbps = np.random.normal(500, 150)
            packet_loss = np.random.exponential(0.5)
            latency_ms = np.random.normal(20, 8)
            
            # Inject anomalies (5% of data)
            is_anomaly = 0
            if random.random() < 0.05:
                is_anomaly = 1
                if random.choice(['cpu', 'memory', 'bandwidth', 'latency']) == 'cpu':
                    cpu_usage = np.random.uniform(85, 100)
                else:
                    memory_usage = np.random.uniform(85, 98)
                    bandwidth_mbps = np.random.uniform(800, 1200)
                    latency_ms = np.random.uniform(150, 300)
                    packet_loss = np.random.uniform(5, 15)
            
            data.append({
                'timestamp': timestamp,
                'device_id': device,
                'cpu_usage_percent': round(cpu_usage, 2),
                'memory_usage_percent': round(memory_usage, 2),
                'bandwidth_mbps': round(bandwidth_mbps, 2),
                'packet_loss_percent': round(packet_loss, 2),
                'latency_ms': round(latency_ms, 2),
                'is_anomaly': is_anomaly,
                'fault_type': 'normal' if is_anomaly == 0 else random.choice(['high_cpu', 'high_memory', 'network_congestion', 'hardware_fault'])
            })
        
        df = pd.DataFrame(data)
        df.to_csv('cloud_network_ml/sample_data.csv', index=False)
        return df

if __name__ == '__main__':
    collector = DataCollector()
    df = collector.generate_sample_data()
    print(f"Generated {len(df)} samples saved to sample_data.csv")
    print(f"Anomalies: {df['is_anomaly'].sum()} ({df['is_anomaly'].mean()*100:.1f}%)")
