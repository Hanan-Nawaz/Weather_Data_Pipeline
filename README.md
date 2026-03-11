# 🌦️ Weather Data Pipeline

A fully automated end-to-end ETL pipeline for ingesting, transforming, and storing weather data — orchestrated with Apache Airflow.

---

## Project Structure

```
Weather-Data-Pipeline/
├── README.md
├── data/                          # Raw and processed data storage
├── notebooks/                     # Exploratory analysis & prototyping
├── scripts/
│   ├── extract.py                 # Fetch weather data from API
│   ├── transform.py               # Clean and normalize data
│   └── load.py                    # Load into target data store
├── dags/
│   └── weather_pipeline_dag.py    # Airflow DAG definition
├── requirements.txt               # Python dependencies
└── config/
    └── config.yaml                # Environment & pipeline configuration
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/your-username/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure the pipeline

Edit `config/config.yaml` with your API credentials and database settings:

```yaml
api:
  key: YOUR_API_KEY
  endpoint: https://api.weather.example.com

database:
  host: localhost
  port: 5432
  name: weather_db
```

### 4. Run scripts manually

```bash
python scripts/extract.py
python scripts/transform.py
python scripts/load.py
```

### 5. Deploy with Airflow

```bash
# Copy DAG to your Airflow DAGs folder
cp dags/weather_pipeline_dag.py $AIRFLOW_HOME/dags/

# Start Airflow
airflow scheduler &
airflow webserver
```

---

## Pipeline Overview

```
  [ Weather API ]
       │
       ▼
  extract.py        ← Pulls raw weather data (temperature, humidity, wind, etc.)
       │
       ▼
  transform.py      ← Cleans nulls, normalizes units, adds timestamps
       │
       ▼
  load.py           ← Writes to database / data warehouse
       │
       ▼
  [ Data Store ]
```

The Airflow DAG (`weather_pipeline_dag.py`) orchestrates these steps on a scheduled interval with error handling and retries.

---

## Tech Stack

| Layer         | Tool / Library             |
|---------------|----------------------------|
| Orchestration | Apache Airflow             |
| Language      | Python 3.9+                |
| HTTP Client   | `requests`                 |
| Data Handling | `pandas`                   |
| Storage       | PostgreSQL / CSV           |
| Config        | PyYAML                     |

---

## Configuration Reference

| Key                  | Description                        | Default     |
|----------------------|------------------------------------|-------------|
| `api.key`            | Weather API authentication key     | —           |
| `api.endpoint`       | Base URL of the weather API        | —           |
| `database.host`      | Database host address              | `localhost` |
| `database.port`      | Database port                      | `5432`      |
| `database.name`      | Target database name               | `weather_db`|
| `pipeline.schedule`  | Airflow cron schedule expression   | `@hourly`   |

---

## Notebooks

The `notebooks/` directory contains Jupyter notebooks for:

- Exploratory data analysis (EDA) of raw weather feeds
- Validating transform logic before scripting
- Visualizing historical trends post-load

---

## Running Tests

```bash
pytest tests/
```

---

## Requirements

- Python 3.9+
- Apache Airflow 2.x
- PostgreSQL (or update `load.py` for your target store)
- Valid API key from your weather data provider

---

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit your changes: `git commit -m 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Open a Pull Request

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
