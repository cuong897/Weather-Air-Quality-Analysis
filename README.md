# Weather & Air Quality – Group 3.3 (HCMC 2023)

[![Python 3.11](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/downloads/) [![Jupyter](https://img.shields.io/badge/Jupyter-Notebook-orange.svg)](https://jupyter.org/)

End‑to‑end analysis of weather and air quality for Ho Chi Minh City (10.823, 106.6296) in 2023: data loading, QA, temporal aggregation, visualization, and basic forecasting/anomaly detection.

---

## Overview

- Course: Data Processing Programming – Semester 1 (2025–2026), VNU UET
- Group: 3.3 – Ho Chi Minh City, year 2023
- Sources:
	- Meteostat – weather (temperature, precipitation, wind speed/direction, air pressure)
	- Open-Meteo – air quality (PM10, PM2.5, UV Index, others when available)
- Period: 01/01/2023–31/12/2023 (HCMC)
- Resolution: hourly/daily (raw) → daily/weekly/monthly (analysis)

## Features

- Data ingestion from Meteostat and Open-Meteo for a single city and year
- Transparent QA pipeline with rule-based flags and summary statistics
- Daily, weekly, and monthly indicators for weather and air quality
- At least 5 publication-ready visualizations (PDF) for the report
- Baseline PM2.5 forecasting with lag features (linear regression)
- PM2.5 anomaly detection using Z‑score and IQR

## Project structure

```
.
├── raw/          # Raw CSVs (weather_data.csv, air_quality.csv)
├── processed/    # Cleaned data, QA outputs, daily/weekly/monthly tables
├── figures/      # Plots (PDF) used in the report
├── reports/      # QA summaries and LaTeX report
├── src/          # Jupyter notebooks and helper script(s)
├── README.md     # This file
└── requirements.txt
```

Key files:

- Raw data: [raw/weather_data.csv](raw/weather_data.csv), [raw/air_quality.csv](raw/air_quality.csv)
- Main dataset: [processed/merged_daily.csv](processed/merged_daily.csv) (weather + AQ, daily)
- Aggregates: [processed/data_weekly.csv](processed/data_weekly.csv), [processed/data_monthly.csv](processed/data_monthly.csv), [processed/data_monthly_indexed.csv](processed/data_monthly_indexed.csv)
- Indicator dictionary: [processed/indicators_documentation.csv](processed/indicators_documentation.csv) (name, purpose, formula, unit)
- QA outputs: [reports/qa_summary.csv](reports/qa_summary.csv), [reports/qa_weather_daily.csv](reports/qa_weather_daily.csv), [reports/qa_aqi_hourly.csv](reports/qa_aqi_hourly.csv)
- Technical report source: [reports/report.tex](reports/report.tex)
- Notebooks:
	- [src/clean_data.ipynb](src/clean_data.ipynb) – cleaning, QA rules, time alignment, merged_daily.csv
	- [src/resample.ipynb](src/resample.ipynb) – daily/weekly/monthly aggregation and indicators
	- [src/draw.ipynb](src/draw.ipynb) – visualizations saved to figures
	- [src/pm25_forecast.ipynb](src/pm25_forecast.ipynb) – PM2.5 forecasting (linear regression baseline)
	- [src/pm25_anomaly.ipynb](src/pm25_anomaly.ipynb) – PM2.5 anomaly detection (Z‑score, IQR)

## Setup

Prerequisites:

- Python 3.11
- Jupyter Notebook / JupyterLab or VS Code with Jupyter support

Create and activate a virtual environment (example with conda):

```powershell
conda create -n weather-aqi python=3.11
conda activate weather-aqi
pip install -r requirements.txt
```

Launch Jupyter from the project root:

```powershell
jupyter notebook
```

Then open the notebooks in [src](src) using the `weather-aqi` kernel.

## Core pipeline

### 1) QA and cleaning

Notebook: [src/clean_data.ipynb](src/clean_data.ipynb)

- Apply rules such as: precipitation < 0, wind speed < 0, unrealistic air pressure, out-of-range UV Index, simple PM2.5 vs PM10 consistency checks, duplicated/missing timestamps, and time-zone/unit harmonization.
- Prefer **flagging** suspicious values instead of dropping them.
- Outputs: cleaned daily/hourly data in [processed](processed) and QA summaries in [reports](reports), especially [reports/qa_summary.csv](reports/qa_summary.csv).

### 2) Aggregation and indicators

Notebook: [src/resample.ipynb](src/resample.ipynb)

- Compute daily/weekly/monthly statistics after QA, such as:
	- Temperature: mean, median, p95
	- Rainfall: totals and rainy days (≥ 1 mm)
	- Wind: average speed, direction frequency
	- Pressure: mean and standard deviation
	- Air quality: PM2.5/PM10 p95, exceedance days, daily max UV Index
- Save results to [processed/data_weekly.csv](processed/data_weekly.csv), [processed/data_monthly.csv](processed/data_monthly.csv), [processed/data_monthly_indexed.csv](processed/data_monthly_indexed.csv).
- Document every indicator in [processed/indicators_documentation.csv](processed/indicators_documentation.csv).

### 3) Visualizations

Notebook: [src/draw.ipynb](src/draw.ipynb)

- Produce ≥ 5 plots (time series, bar charts, heatmaps, composition charts, dashboards) with clear titles, axes, units, and legends.
- Export figures as PDFs into [figures](figures) for use in the technical report.

## Advanced analysis (optional bonus)

- [src/pm25_forecast.ipynb](src/pm25_forecast.ipynb):
	- Short-term daily PM2.5 forecasting using lag features and linear regression.
	- Evaluate MAE, RMSE, R² against a persistence baseline (today = yesterday).
- [src/pm25_anomaly.ipynb](src/pm25_anomaly.ipynb):
	- Detect daily PM2.5 anomalies via Z‑score and IQR.
	- Output flags and plots highlighting anomalous days.

## How to rerun the project

1. Ensure [raw/weather_data.csv](raw/weather_data.csv) and [raw/air_quality.csv](raw/air_quality.csv) exist (or regenerate via [src/download_data.py](src/download_data.py) if needed).
2. Run [src/clean_data.ipynb](src/clean_data.ipynb) (Run All): write cleaned data and QA CSVs to [processed](processed) and [reports](reports), and create [processed/merged_daily.csv](processed/merged_daily.csv).
3. Run [src/resample.ipynb](src/resample.ipynb): generate weekly/monthly tables and indicator documentation in [processed](processed).
4. Run [src/draw.ipynb](src/draw.ipynb): generate all figures into [figures](figures).
5. (Optional) Run [src/pm25_forecast.ipynb](src/pm25_forecast.ipynb) and [src/pm25_anomaly.ipynb](src/pm25_anomaly.ipynb) for forecasting and anomaly analysis.

Together with the LaTeX report in [reports/report.tex](reports/report.tex) and requirements.txt, this README provides the information needed to reproduce and assess the project according to the course assignment.