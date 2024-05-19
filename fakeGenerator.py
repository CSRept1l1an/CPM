import random
import sqlite3
from datetime import datetime, timedelta


def categorize_network_data(net_data):
    category = "low"

    bandwidth_utilization_thresholds = {"medium": 50, "high": 70, "critical": 90}
    latency_thresholds = {"medium": 40, "high": 60, "critical": 80}
    packet_loss_thresholds = {"medium": 2, "high": 3, "critical": 4}
    network_errors_thresholds = {"medium": 3, "high": 6, "critical": 8}
    network_availability_thresholds = {"medium": 98, "high": 97, "critical": 95}

    if net_data["Bandwidth Utilization"] > bandwidth_utilization_thresholds["critical"]:
        category = "critical"
    elif net_data["Bandwidth Utilization"] > bandwidth_utilization_thresholds["high"]:
        category = "high"
    elif net_data["Bandwidth Utilization"] > bandwidth_utilization_thresholds["medium"]:
        category = "medium"

    if net_data["Latency"] > latency_thresholds["critical"]:
        category = "critical"
    elif net_data["Latency"] > latency_thresholds["high"]:
        category = "high"
    elif net_data["Latency"] > latency_thresholds["medium"]:
        category = "medium"

    if net_data["Packet Loss"] > packet_loss_thresholds["critical"]:
        category = "critical"
    elif net_data["Packet Loss"] > packet_loss_thresholds["high"]:
        category = "high"
    elif net_data["Packet Loss"] > packet_loss_thresholds["medium"]:
        category = "medium"

    if net_data["Network Errors"] > network_errors_thresholds["critical"]:
        category = "critical"
    elif net_data["Network Errors"] > network_errors_thresholds["high"]:
        category = "high"
    elif net_data["Network Errors"] > network_errors_thresholds["medium"]:
        category = "medium"

    if net_data["Network Availability/Uptime"] < network_availability_thresholds["critical"]:
        category = "critical"
    elif net_data["Network Availability/Uptime"] < network_availability_thresholds["high"]:
        category = "high"
    elif net_data["Network Availability/Uptime"] < network_availability_thresholds["medium"]:
        category = "medium"

    return category


def generate_network_data():
    net_data = {
        "Bandwidth Utilization": random.uniform(0, 100),
        "Latency": random.uniform(0, 100),
        "Packet Loss": random.uniform(0, 5),
        "Network Errors": random.randint(0, 10),
        "Network Availability/Uptime": random.uniform(95, 100)
    }
    category = categorize_network_data(net_data)
    net_data["Category"] = category
    return net_data


def categorize_it_node_data(it_data):
    category = "low"

    cpu_utilization_thresholds = {"medium": 50, "high": 70, "critical": 90}
    memory_utilization_thresholds = {"medium": 50, "high": 70, "critical": 90}
    disk_io_thresholds = {"medium": 50, "high": 70, "critical": 90}
    disk_usage_thresholds = {"medium": 50, "high": 70, "critical": 90}
    system_uptime_thresholds = {"medium": 98, "high": 97, "critical": 95}

    if it_data["CPU Utilization"] > cpu_utilization_thresholds["critical"]:
        category = "critical"
    elif it_data["CPU Utilization"] > cpu_utilization_thresholds["high"]:
        category = "high"
    elif it_data["CPU Utilization"] > cpu_utilization_thresholds["medium"]:
        category = "medium"

    if it_data["Memory Utilization"] > memory_utilization_thresholds["critical"]:
        category = "critical"
    elif it_data["Memory Utilization"] > memory_utilization_thresholds["high"]:
        category = "high"
    elif it_data["Memory Utilization"] > memory_utilization_thresholds["medium"]:
        category = "medium"

    if it_data["Disk I/O"] > disk_io_thresholds["critical"]:
        category = "critical"
    elif it_data["Disk I/O"] > disk_io_thresholds["high"]:
        category = "high"
    elif it_data["Disk I/O"] > disk_io_thresholds["medium"]:
        category = "medium"

    if it_data["Disk Usage"] > disk_usage_thresholds["critical"]:
        category = "critical"
    elif it_data["Disk Usage"] > disk_usage_thresholds["high"]:
        category = "high"
    elif it_data["Disk Usage"] > disk_usage_thresholds["medium"]:
        category = "medium"

    if it_data["System Uptime"] < system_uptime_thresholds["critical"]:
        category = "critical"
    elif it_data["System Uptime"] < system_uptime_thresholds["high"]:
        category = "high"
    elif it_data["System Uptime"] < system_uptime_thresholds["medium"]:
        category = "medium"

    return category


def generate_it_node_data():
    it_data = {
        "CPU Utilization": random.uniform(0, 100),
        "Memory Utilization": random.uniform(0, 100),
        "Disk I/O": random.uniform(0, 100),
        "Disk Usage": random.uniform(0, 100),
        "System Uptime": random.uniform(95, 100)
    }
    category = categorize_it_node_data(it_data)
    it_data['Category'] = category

    return it_data


def categorize_application_data(app_data):
    category = "low"

    response_time_thresholds = {"medium": 200, "high": 300, "critical": 400}
    error_rate_thresholds = {"medium": 2, "high": 3, "critical": 4}
    throughput_thresholds = {"medium": 500, "high": 750, "critical": 900}
    cpu_usage_thresholds = {"medium": 50, "high": 70, "critical": 90}
    memory_usage_thresholds = {"medium": 50, "high": 70, "critical": 90}
    query_execution_time_thresholds = {"medium": 50, "high": 70, "critical": 90}
    db_throughput_thresholds = {"medium": 500, "high": 750, "critical": 900}

    if app_data["Response Time"] > response_time_thresholds["critical"]:
        category = "critical"
    elif app_data["Response Time"] > response_time_thresholds["high"]:
        category = "high"
    elif app_data["Response Time"] > response_time_thresholds["medium"]:
        category = "medium"

    if app_data["Error Rate"] > error_rate_thresholds["critical"]:
        category = "critical"
    elif app_data["Error Rate"] > error_rate_thresholds["high"]:
        category = "high"
    elif app_data["Error Rate"] > error_rate_thresholds["medium"]:
        category = "medium"

    if app_data["Throughput"] > throughput_thresholds["critical"]:
        category = "critical"
    elif app_data["Throughput"] > throughput_thresholds["high"]:
        category = "high"
    elif app_data["Throughput"] > throughput_thresholds["medium"]:
        category = "medium"

    if app_data["Resource Usage (CPU)"] > cpu_usage_thresholds["critical"]:
        category = "critical"
    elif app_data["Resource Usage (CPU)"] > cpu_usage_thresholds["high"]:
        category = "high"
    elif app_data["Resource Usage (CPU)"] > cpu_usage_thresholds["medium"]:
        category = "medium"

    if app_data["Resource Usage (Memory)"] > memory_usage_thresholds["critical"]:
        category = "critical"
    elif app_data["Resource Usage (Memory)"] > memory_usage_thresholds["high"]:
        category = "high"
    elif app_data["Resource Usage (Memory)"] > memory_usage_thresholds["medium"]:
        category = "medium"

    if app_data["Database Performance (Query Execution Time)"] > query_execution_time_thresholds["critical"]:
        category = "critical"
    elif app_data["Database Performance (Query Execution Time)"] > query_execution_time_thresholds["high"]:
        category = "high"
    elif app_data["Database Performance (Query Execution Time)"] > query_execution_time_thresholds["medium"]:
        category = "medium"

    if app_data["Database Performance (Throughput)"] > db_throughput_thresholds["critical"]:
        category = "critical"
    elif app_data["Database Performance (Throughput)"] > db_throughput_thresholds["high"]:
        category = "high"
    elif app_data["Database Performance (Throughput)"] > db_throughput_thresholds["medium"]:
        category = "medium"

    return category


def generate_application_data():
    app_data = {
        "Response Time": random.uniform(0, 500),
        "Error Rate": random.uniform(0, 5),
        "Throughput": random.uniform(100, 1000),
        "Resource Usage (CPU)": random.uniform(0, 100),
        "Resource Usage (Memory)": random.uniform(0, 100),
        "Database Performance (Query Execution Time)": random.uniform(0, 100),
        "Database Performance (Throughput)": random.uniform(100, 1000)
    }
    category = categorize_application_data(app_data)
    app_data["Category"] = category
    return app_data


conn = sqlite3.connect('management.db')
cur = conn.cursor()

num_entries = 100
total_entries = 0

print("Sample of generated data:")
for _ in range(num_entries):
    total_entries += 1

    timestamp = datetime.now() - timedelta(minutes=random.randint(0, 1440))

    network_data = generate_network_data()
    print("Entry", total_entries)
    print("Timestamp:", timestamp)
    print("Network Data:")
    for attr, value in network_data.items():
        print(f"{attr}: {value}")
    print()

    it_node_data = generate_it_node_data()
    print("Entry", total_entries)
    print("Timestamp:", timestamp)
    print("IT Node Data:")
    for attr, value in it_node_data.items():
        print(f"{attr}: {value}")
    print()

    application_data = generate_application_data()
    print("Entry", total_entries)
    print("Timestamp:", timestamp)
    print("Application Data:")
    for attr, value in application_data.items():
        print(f"{attr}: {value}")
    print()

    category_id = random.randint(1, 4)

    cur.execute('''
            INSERT INTO Network_KPIs (timestamp, bandwidth_utilization, latency, packet_loss, network_errors, 
            network_availability, Category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
              timestamp,
              network_data['Bandwidth Utilization'],
              network_data['Latency'],
              network_data['Packet Loss'],
              network_data['Network Errors'],
              network_data['Network Availability/Uptime'],
              network_data['Category']))

    cur.execute('''
            INSERT INTO IT_Node_KPIs (timestamp, cpu_utilization, memory_utilization, disk_io, disk_usage, 
            system_uptime, Category)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
              timestamp,
              it_node_data['CPU Utilization'],
              it_node_data['Memory Utilization'],
              it_node_data['Disk I/O'],
              it_node_data['Disk Usage'],
              it_node_data['System Uptime'],
              it_node_data['Category']))

    cur.execute('''
            INSERT INTO Application_KPIs (timestamp, response_time, error_rate, throughput, cpu_usage, memory_usage, 
            query_execution_time, db_throughput, Category)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
        timestamp,
        application_data['Response Time'],
        application_data['Error Rate'],
        application_data['Throughput'],
        application_data['Resource Usage (CPU)'],
        application_data['Resource Usage (Memory)'],
        application_data['Database Performance (Query Execution Time)'],
        application_data['Database Performance (Throughput)'],
        application_data['Category']))

conn.commit()

print("Total entries generated:", total_entries)
