import requests
import pandas as pd
from pydantic import BaseModel, ValidationError
from typing import Optional

# --------------------------------------------------
# PROJECT SETTINGS
# --------------------------------------------------

CITY = "Lahore"
LATITUDE = 31.5204
LONGITUDE = 74.3587

START_DATE = "2025-10-01"
END_DATE = "2026-09-30"

API_URL = "https://archive-api.open-meteo.com/v1/archive"


# --------------------------------------------------
# PYDANTIC VALIDATION MODEL
# --------------------------------------------------

class WeatherRecord(BaseModel):
    date: str
    temperature_max_c: Optional[float] = None
    temperature_min_c: Optional[float] = None
    temperature_mean_c: Optional[float] = None
    precipitation_mm: Optional[float] = None
    wind_speed_max_kmh: Optional[float] = None
    weather_code: Optional[int] = None


# --------------------------------------------------
# EXTRACT
# --------------------------------------------------

def extract_data():

    print("\n========== EXTRACT ==========")
    print("Connecting to Open-Meteo API...")

    parameters = {
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "start_date": START_DATE,
        "end_date": END_DATE,

        "daily": [
            "weather_code",
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max"
        ],

        "timezone": "Asia/Karachi"
    }

    try:
        response = requests.get(
            API_URL,
            params=parameters,
            timeout=30
        )

        response.raise_for_status()

        data = response.json()

        print("Data extracted successfully!")
        return data

    except requests.exceptions.RequestException as error:

        print("API ERROR:")
        print(error)

        return None


# --------------------------------------------------
# TRANSFORM
# --------------------------------------------------

def transform_data(data):

    print("\n========== TRANSFORM ==========")

    if data is None:
        return None

    daily = data.get("daily")

    if daily is None:
        print("No daily weather data found.")
        return None

    df = pd.DataFrame({

        "date":
            daily["time"],

        "temperature_max_c":
            daily["temperature_2m_max"],

        "temperature_min_c":
            daily["temperature_2m_min"],

        "temperature_mean_c":
            daily["temperature_2m_mean"],

        "precipitation_mm":
            daily["precipitation_sum"],

        "wind_speed_max_kmh":
            daily["wind_speed_10m_max"],

        "weather_code":
            daily["weather_code"]
    })

    # Convert date column
    df["date"] = pd.to_datetime(df["date"])

    # Remove duplicate dates
    duplicates_before = df.duplicated(
        subset=["date"]
    ).sum()

    df = df.drop_duplicates(
        subset=["date"]
    )

    # Sort records
    df = df.sort_values("date")

    # Numerical columns
    numeric_columns = [
        "temperature_max_c",
        "temperature_min_c",
        "temperature_mean_c",
        "precipitation_mm",
        "wind_speed_max_kmh",
        "weather_code"
    ]

    for column in numeric_columns:

        df[column] = pd.to_numeric(
            df[column],
            errors="coerce"
        )

    # Additional useful columns
    df["temperature_range_c"] = (
        df["temperature_max_c"]
        - df["temperature_min_c"]
    )

    df["month"] = df["date"].dt.month_name()

    df["month_number"] = df["date"].dt.month

    print("Data transformed successfully!")
    print("Duplicates removed:", duplicates_before)

    return df


# --------------------------------------------------
# VALIDATE
# --------------------------------------------------

def validate_data(df):

    print("\n========== VALIDATE ==========")

    valid = 0
    invalid = 0

    for _, row in df.iterrows():

        try:

            WeatherRecord(
                date=row["date"].strftime("%Y-%m-%d"),

                temperature_max_c=(
                    None if pd.isna(row["temperature_max_c"])
                    else float(row["temperature_max_c"])
                ),

                temperature_min_c=(
                    None if pd.isna(row["temperature_min_c"])
                    else float(row["temperature_min_c"])
                ),

                temperature_mean_c=(
                    None if pd.isna(row["temperature_mean_c"])
                    else float(row["temperature_mean_c"])
                ),

                precipitation_mm=(
                    None if pd.isna(row["precipitation_mm"])
                    else float(row["precipitation_mm"])
                ),

                wind_speed_max_kmh=(
                    None if pd.isna(row["wind_speed_max_kmh"])
                    else float(row["wind_speed_max_kmh"])
                ),

                weather_code=(
                    None if pd.isna(row["weather_code"])
                    else int(row["weather_code"])
                )
            )

            valid += 1

        except ValidationError:
            invalid += 1

    print("Valid records:", valid)
    print("Invalid records:", invalid)


# --------------------------------------------------
# DATA CLEANING
# --------------------------------------------------

def clean_data(df):

    print("\n========== CLEAN ==========")

    print(
        "Missing values before cleaning:"
    )

    print(df.isnull().sum())

    # Interpolate numerical missing values
    numeric_columns = [
        "temperature_max_c",
        "temperature_min_c",
        "temperature_mean_c",
        "precipitation_mm",
        "wind_speed_max_kmh"
    ]

    df[numeric_columns] = (
        df[numeric_columns]
        .interpolate(limit_direction="both")
    )

    # Weather code can use nearest available value
    df["weather_code"] = (
        df["weather_code"]
        .ffill()
        .bfill()
    )

    print(
        "\nMissing values after cleaning:"
    )

    print(df.isnull().sum())

    return df


# --------------------------------------------------
# LOAD
# --------------------------------------------------

def load_data(df):

    print("\n========== LOAD ==========")

    filename = "weather_lahore.csv"

    df.to_csv(
        filename,
        index=False
    )

    print(
        f"Data successfully saved to {filename}"
    )


# --------------------------------------------------
# DATA QUALITY REPORT
# --------------------------------------------------

def quality_report(df):

    print("\n========== DATA QUALITY ==========")

    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print(
        "Duplicate rows:",
        df.duplicated().sum()
    )

    print("\nMissing values:")

    print(
        df.isnull().sum()
    )


# --------------------------------------------------
# MAIN
# --------------------------------------------------

def main():

    print("=" * 55)
    print("LAHORE WEATHER ETL PIPELINE")
    print("=" * 55)

    print(
        f"Location: {CITY}"
    )

    print(
        f"Period: {START_DATE} to {END_DATE}"
    )

    # Extract
    data = extract_data()

    if data is None:
        return

    # Transform
    df = transform_data(data)

    if df is None:
        return

    # Validate
    validate_data(df)

    # Clean
    df = clean_data(df)

    # Quality report
    quality_report(df)

    # Load
    load_data(df)

    print("\n" + "=" * 55)
    print("ETL PIPELINE COMPLETED SUCCESSFULLY")
    print("=" * 55)


if __name__ == "__main__":
    main()