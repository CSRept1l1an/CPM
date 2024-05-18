import random
from datetime import datetime, timedelta


# Function to generate fake data for Network KPIs
def generate_network_data():
    return {
        "Bandwidth Utilization": random.uniform(0, 100),
        "Latency": random.uniform(0, 100),
        "Packet Loss": random.uniform(0, 5),
        "Network Errors": random.randint(0, 10),
        "Network Availability/Uptime": random.uniform(95, 100)
    }


# Function to generate fake data for IT Node KPIs
def generate_it_node_data():
    return {
        "CPU Utilization": random.uniform(0, 100),
        "Memory Utilization": random.uniform(0, 100),
        "Disk I/O": random.uniform(0, 100),
        "Disk Usage": random.uniform(0, 100),
        "System Uptime": random.uniform(95, 100)
    }


# Function to generate fake data for Application KPIs
def generate_application_data():
    return {
        "Response Time": random.uniform(0, 500),
        "Error Rate": random.uniform(0, 5),
        "Throughput": random.uniform(100, 1000),
        "Resource Usage (CPU)": random.uniform(0, 100),
        "Resource Usage (Memory)": random.uniform(0, 100),
        "Database Performance (Query Execution Time)": random.uniform(0, 100),
        "Database Performance (Throughput)": random.uniform(100, 1000)
    }


num_entries = 100
total_entries = 0

print("Sample of generated data:")
for _ in range(num_entries):
    total_entries += 1

    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))  # Random timestamp within the last 24 hours

    network_data = generate_network_data()
    it_node_data = generate_it_node_data()
    application_data = generate_application_data()

    print("Entry", total_entries)
    print("Timestamp:", timestamp)

    print("Network Data:")
    for attr, value in network_data.items():
        print(f"{attr}: {value}")

    print("IT Node Data:")
    for attr, value in it_node_data.items():
        print(f"{attr}: {value}")

    print("Application Data:")
    for attr, value in application_data.items():
        print(f"{attr}: {value}")

    print()

print("Total entries generated:", total_entries)
