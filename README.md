# Weather Data ETL Pipeline and Exploratory Data Analysis

## Project Overview

This project implements a complete ETL (Extract, Transform, Load) pipeline for historical weather data from Lahore, Pakistan.

Weather data is extracted from the Open-Meteo Historical Weather API, validated using Pydantic, transformed and cleaned using Pandas, and loaded into a CSV file.

Exploratory Data Analysis (EDA) is then performed using Pandas and Matplotlib. An interactive Streamlit dashboard is provided for visualizing the results.

## Data Source

**Source:** Open-Meteo Historical Weather API  
**Location:** Lahore, Pakistan

## ETL Pipeline

### Extract

Python Requests is used to retrieve historical weather data from the Open-Meteo API.

### Transform

Pydantic and Pandas are used for:

- Data validation
- Data type conversion
- Missing-value handling
- Duplicate removal
- Date conversion
- Feature creation

### Load

The cleaned dataset is stored in:

`weather_lahore.csv`

## Exploratory Data Analysis

The analysis includes:

- Dataset structure
- Missing values
- Duplicate records
- Summary statistics
- Average temperature
- Hottest day
- Coldest day
- Precipitation analysis
- Wind speed analysis
- Temperature and wind correlation

## Visualizations

The project includes:

1. Temperature trend line chart
2. Precipitation bar chart
3. Temperature histogram
4. Wind speed histogram
5. Temperature vs wind speed scatter plot

## Technologies

- Python
- Pandas
- Requests
- Pydantic
- Matplotlib
- Streamlit
- Open-Meteo API
- CSV
- GitHub

## Run ETL

```bash
python etl.py
```

## Run EDA

```bash
python eda.py
```

## Run Dashboard

```bash
streamlit run app.py
```

## Project Team

**Algorithm Architects**