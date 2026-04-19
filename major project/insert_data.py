import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

class DataInserter:
    def __init__(self):
        self.devices = ['router_01', 'switch_02', 'server_03', 'firewall_04', 'load_balancer_05']
        
    def insert_single_record(self, device_id, cpu, memory, bandwidth, packet_loss, latency):
        """Insert a single network record"""
        data = {
            'timestamp': datetime.now(),
            'device_id': device_id,
            'cpu_usage_percent': cpu,
            'memory_usage_percent': memory,
            'bandwidth_mbps': bandwidth,
            'packet_loss_percent': packet_loss,
            'latency_ms': latency,
            'is_anomaly': 1 if (cpu > 85 or memory > 85 or packet_loss > 5 or latency > 100) else 0,
            'fault_type': self._determine_fault_type(cpu, memory, packet_loss, latency)
        }
        
        # Append to existing CSV
        df_new = pd.DataFrame([data])
        csv_path = 'cloud_network_ml/sample_data.csv'
        
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_path, index=False)
            print(f"✓ Inserted record for {device_id}")
        else:
            df_new.to_csv(csv_path, index=False)
            print(f"✓ Created new file with record for {device_id}")
        
        return data
    
    def _determine_fault_type(self, cpu, memory, packet_loss, latency):
        if cpu > 85:
            return 'high_cpu'
        elif memory > 85:
            return 'high_memory'
        elif packet_loss > 5:
            return 'network_congestion'
        elif latency > 100:
            return 'hardware_fault'
        else:
            return 'normal'
    
    def insert_bulk_records(self, num_records=100):
        """Insert multiple random records"""
        records = []
        for i in range(num_records):
            device = random.choice(self.devices)
            cpu = np.random.normal(45, 15)
            memory = np.random.normal(55, 20)
            bandwidth = np.random.normal(500, 150)
            packet_loss = np.random.exponential(0.5)
            latency = np.random.normal(20, 8)
            
            # Randomly inject anomalies (10%)
            if random.random() < 0.1:
                fault = random.choice(['high_cpu', 'high_memory', 'network_congestion', 'hardware_fault'])
                if fault == 'high_cpu':
                    cpu = random.uniform(85, 100)
                elif fault == 'high_memory':
                    memory = random.uniform(85, 98)
                elif fault == 'network_congestion':
                    packet_loss = random.uniform(5, 15)
                elif fault == 'hardware_fault':
                    latency = random.uniform(150, 300)
            
            record = {
                'timestamp': datetime.now() - timedelta(minutes=i),
                'device_id': device,
                'cpu_usage_percent': min(100, max(0, cpu)),
                'memory_usage_percent': min(100, max(0, memory)),
                'bandwidth_mbps': max(0, bandwidth),
                'packet_loss_percent': max(0, min(20, packet_loss)),
                'latency_ms': max(0, min(500, latency)),
                'is_anomaly': 1 if (cpu > 85 or memory > 85 or packet_loss > 5 or latency > 100) else 0,
                'fault_type': self._determine_fault_type(cpu, memory, packet_loss, latency)
            }
            records.append(record)
        
        df_new = pd.DataFrame(records)
        csv_path = 'cloud_network_ml/sample_data.csv'
        
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_path, index=False)
        else:
            df_new.to_csv(csv_path, index=False)
        
        print(f"✓ Inserted {num_records} records")
        anomaly_count = df_new['is_anomaly'].sum()
        print(f"  - Anomalies: {anomaly_count} ({anomaly_count/num_records*100:.1f}%)")
        return df_new
    
    def insert_from_csv(self, csv_file_path):
        """Insert data from an external CSV file"""
        if not os.path.exists(csv_file_path):
            print(f"✗ File not found: {csv_file_path}")
            return None
        
        df_new = pd.read_csv(csv_file_path)
        
        # Ensure required columns exist
        required_columns = ['device_id', 'cpu_usage_percent', 'memory_usage_percent', 
                           'bandwidth_mbps', 'packet_loss_percent', 'latency_ms']
        
        for col in required_columns:
            if col not in df_new.columns:
                print(f"✗ Missing column: {col}")
                return None
        
        # Add timestamp if not present
        if 'timestamp' not in df_new.columns:
            df_new['timestamp'] = datetime.now()
        
        # Calculate anomaly flag if not present
        if 'is_anomaly' not in df_new.columns:
            df_new['is_anomaly'] = df_new.apply(
                lambda row: 1 if (row['cpu_usage_percent'] > 85 or 
                                  row['memory_usage_percent'] > 85 or 
                                  row['packet_loss_percent'] > 5 or 
                                  row['latency_ms'] > 100) else 0, axis=1
            )
        
        csv_path = 'cloud_network_ml/sample_data.csv'
        if os.path.exists(csv_path):
            df_existing = pd.read_csv(csv_path)
            df_combined = pd.concat([df_existing, df_new], ignore_index=True)
            df_combined.to_csv(csv_path, index=False)
        else:
            df_new.to_csv(csv_path, index=False)
        
        print(f"✓ Inserted {len(df_new)} records from {csv_file_path}")
        return df_new

# Interactive menu
if __name__ == '__main__':
    inserter = DataInserter()
    
    print("="*50)
    print("DATA INSERTION TOOL")
    print("="*50)
    print("1. Insert single record")
    print("2. Insert 100 random records")
    print("3. Insert custom number of random records")
    print("4. Insert from CSV file")
    print("5. Exit")
    
    while True:
        choice = input("\nEnter your choice (1-5): ")
        
        if choice == '1':
            print("\n--- Insert Single Record ---")
            device = input("Device ID (router_01/switch_02/server_03/firewall_04/load_balancer_05): ")
            cpu = float(input("CPU Usage (0-100): "))
            memory = float(input("Memory Usage (0-100): "))
            bandwidth = float(input("Bandwidth Mbps: "))
            packet_loss = float(input("Packet Loss %: "))
            latency = float(input("Latency ms: "))
            
            inserter.insert_single_record(device, cpu, memory, bandwidth, packet_loss, latency)
            
        elif choice == '2':
            print("\n--- Inserting 100 random records ---")
            inserter.insert_bulk_records(100)
            
        elif choice == '3':
            num = int(input("Enter number of records to insert: "))
            print(f"\n--- Inserting {num} random records ---")
            inserter.insert_bulk_records(num)
            
        elif choice == '4':
            filepath = input("Enter CSV file path: ")
            inserter.insert_from_csv(filepath)
            
        elif choice == '5':
            print("Exiting...")
            break
        
        # Ask to retrain models
        retrain = input("\nDo you want to retrain models with new data? (y/n): ")
        if retrain.lower() == 'y':
            print("\nRetraining models...")
            os.system('python models/train_models.py')
        
        print("\n" + "-"*50)
