
# 📊 Cloud-native Monitoring & Workload Simulation Platform

This project provides a containerized microservice-based system for simulating workloads and monitoring infrastructure using **FastAPI**, **Prometheus**, **Grafana**, and **MySQL**. It includes producer-consumer logic, automated dashboard provisioning, and simulated traffic generation to test system scalability and reliability.

---

## 🧱 Project Structure

```
cc/
├── docker1/                  # Core services and monitoring setup
│   ├── api/                  # FastAPI service (Producer & Consumer)
│   ├── grafana/              # Grafana config & dashboards
│   ├── mysql-init/           # MySQL init scripts
│   ├── Dockerfile.api        # Dockerfile for API service
│   ├── Dockerfile.consumer   # Dockerfile for Consumer service
│   └── requirements.txt      # Python dependencies
├── docker-compose.yml        # Multi-container orchestration
├── prometheus.yml            # Prometheus scraping configuration
├── simulate_workload.py      # Entry point to simulate traffic
├── workload_simulator/       # Simulates HTTP load
└── venv/                     # Python virtual environment (excluded from version control)
```

---

## 🚀 Features

- 🔁 **Producer/Consumer Microservices** with FastAPI.
- 📦 **MySQL** for storing logs/events.
- 📊 **Grafana dashboards** for visual monitoring.
- 📡 **Prometheus** for metrics scraping.
- 🔬 **Workload simulator** for generating synthetic traffic.
- 🐳 Fully containerized with **Docker Compose**.

---

## 🧪 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/jayashreem27/cc.git
cd cc
```

### 2. Run the Full Stack

```bash
docker-compose up --build
```

This will:
- Build the API and consumer containers.
- Start Prometheus and Grafana.
- Initialize MySQL with `init.sql`.
- Load pre-configured Grafana dashboards.

### 3. Access the Services

- **Grafana Dashboard**: [http://localhost:3000](http://localhost:3000)
  - Default login: `admin` / `admin`
- **FastAPI Docs**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **Prometheus UI**: [http://localhost:9090](http://localhost:9090)

---

## 🧪 Simulate Workload

You can simulate HTTP requests to the API for performance testing:

```bash
python simulate_workload.py
```

Or use:

```bash
python workload_simulator/simulate_requests.py
```

These scripts simulate traffic to test how the system handles real-world loads.

---

## ⚙️ Configuration

### Environment

- `docker1/api/` contains all API logic:
  - `producer.py` sends messages
  - `consumer_logs.py` listens to and logs them
- `mysql-init/init.sql` sets up the initial DB schema
- `prometheus.yml` is used to scrape API metrics

---

## 📦 Dependencies

Install Python dependencies (optional if running outside Docker):

```bash
pip install -r docker1/requirements.txt
```

---

## 📈 Dashboard

Grafana loads `prometheus-dashboard.json` automatically and connects to Prometheus.

You can monitor:
- Request throughput
- Error rates
- Latency and performance metrics

---

## 🛠️ Dev Tips

- Use `wait-for-it.sh` to ensure service dependencies are ready before starting.
- Python `venv/` is included for development but ignored in Docker builds.
- Edit `docker-compose.yml` to scale components or expose additional ports.

---

## 📄 License

MIT License — feel free to fork, modify, and improve!

---

## 👩‍💻 Author

Built by [Jayashree M](https://github.com/jayashreem27) — Computer Science & Cybersecurity Enthusiast 🚀
