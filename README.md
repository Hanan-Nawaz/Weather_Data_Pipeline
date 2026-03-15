# 🌦️ Weather Data Pipeline

A fully automated end-to-end ETL pipeline for ingesting, transforming, and storing weather data, orchestrated with Apache Airflow.

---

## Project Structure

```
Weather-Data-Pipeline/
├── README.md
├── .gitignore
├── LICENSE
├── pyproject.toml
├── uv.lock
├── .python-version                # Contains python version used in project 
├── main.py                        # File containg etl code from scripts 
├── logger/                        # Contains custom logger code 
├── logs/                          # Contains logs generated during exceution 
├── eda/                           # Exploratory analysis & prototyping
├── scripts/
│   ├── extract.py                 # Fetch weather data from API
│   ├── transform.py               # Clean and normalize data
│   └── load.py                    # Load into target data store
├── dags/
│   └── weather_pipeline_dag.py    # Airflow DAG definition
└── config/
    └── config.yaml                # Environment & pipeline configuration
```

---

## Quick Start

### 1. Clone the repository

```bash
git clone https://github.com/Hanan-Nawaz/weather-data-pipeline.git
cd weather-data-pipeline
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Configure the pipeline

Edit `config/config.yaml` with your API credentials and database settings and cities of your choice.


### 4. Run scripts manually

```bash
uv run scripts/extract.py
uv run scripts/transform.py
uv run scripts/load.py
```

### 5. Deploy with Airflow

```bash
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
| Language      | Python 3.12                |
| HTTP Client   | `requests`                 |
| Data Handling | `pandas`                   |
| Storage       | PostgreSQL / CSV           |
| Config        | PyYAML                     |

---

## Running Tests

```bash
pytest tests/
```

- will be added soon.

---

## Requirements

- Python 3.12
- Apache Airflow 2.9.3
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
