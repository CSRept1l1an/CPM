
CREATE TABLE IF NOT EXISTS Network_KPIs
(
    id                    INTEGER PRIMARY KEY,
    timestamp             TEXT,
    bandwidth_utilization REAL,
    latency               REAL,
    packet_loss           REAL,
    network_errors        INTEGER,
    network_availability  REAL,
    Category              TEXT
);

CREATE TABLE IF NOT EXISTS IT_Node_KPIs
(
    id                 INTEGER PRIMARY KEY,
    timestamp          TEXT,
    cpu_utilization    REAL,
    memory_utilization REAL,
    disk_io            REAL,
    disk_usage         REAL,
    system_uptime      REAL,
    Category           TEXT
);

CREATE TABLE IF NOT EXISTS Application_KPIs
(
    id                   INTEGER PRIMARY KEY,
    timestamp            TEXT,
    response_time        REAL,
    error_rate           REAL,
    throughput           REAL,
    cpu_usage            REAL,
    memory_usage         REAL,
    query_execution_time REAL,
    db_throughput        REAL,
    Category             TEXT
);

