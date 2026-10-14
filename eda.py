import pandas as pd
import matplotlib.pyplot as plt
import os


# --------------------------------------------------
# LOAD CLEANED DATASET
# --------------------------------------------------

df = pd.read_csv("weather_lahore.csv")

df["date"] = pd.to_datetime(df["date"])


print("=" * 60)
print("LAHORE WEATHER EXPLORATORY DATA ANALYSIS")
print("=" * 60)


# --------------------------------------------------
# DATASET STRUCTURE
# --------------------------------------------------

print("\n1. DATASET SIZE")

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])


print("\n2. FIRST FIVE RECORDS")

print(df.head())


print("\n3. DATA TYPES")

print(df.dtypes)


# --------------------------------------------------
# MISSING VALUES
# --------------------------------------------------

print("\n4. MISSING VALUES")

print(df.isnull().sum())


# --------------------------------------------------
# DUPLICATES
# --------------------------------------------------

print("\n5. DUPLICATE RECORDS")

print(
    df.duplicated().sum()
)


# --------------------------------------------------
# SUMMARY STATISTICS
# --------------------------------------------------

print("\n6. SUMMARY STATISTICS")

print(
    df.describe()
)


# --------------------------------------------------
# WEATHER STATISTICS
# --------------------------------------------------

average_temperature = (
    df["temperature_mean_c"].mean()
)

maximum_temperature = (
    df["temperature_max_c"].max()
)

minimum_temperature = (
    df["temperature_min_c"].min()
)

total_precipitation = (
    df["precipitation_mm"].sum()
)

average_wind = (
    df["wind_speed_max_kmh"].mean()
)


print("\n7. WEATHER STATISTICS")

print(
    "Average temperature:",
    round(average_temperature, 2),
    "°C"
)

print(
    "Maximum temperature:",
    maximum_temperature,
    "°C"
)

print(
    "Minimum temperature:",
    minimum_temperature,
    "°C"
)

print(
    "Total precipitation:",
    round(total_precipitation, 2),
    "mm"
)

print(
    "Average maximum wind speed:",
    round(average_wind, 2),
    "km/h"
)


# --------------------------------------------------
# HOTTEST DAY
# --------------------------------------------------

hottest_index = (
    df["temperature_max_c"].idxmax()
)

hottest_day = df.loc[hottest_index]


print("\n8. HOTTEST DAY")

print(
    "Date:",
    hottest_day["date"].date()
)

print(
    "Temperature:",
    hottest_day["temperature_max_c"],
    "°C"
)


# --------------------------------------------------
# COLDEST DAY
# --------------------------------------------------

coldest_index = (
    df["temperature_min_c"].idxmin()
)

coldest_day = df.loc[coldest_index]


print("\n9. COLDEST DAY")

print(
    "Date:",
    coldest_day["date"].date()
)

print(
    "Temperature:",
    coldest_day["temperature_min_c"],
    "°C"
)


# --------------------------------------------------
# WETTEST DAY
# --------------------------------------------------

wettest_index = (
    df["precipitation_mm"].idxmax()
)

wettest_day = df.loc[wettest_index]


print("\n10. WETTEST DAY")

print(
    "Date:",
    wettest_day["date"].date()
)

print(
    "Precipitation:",
    wettest_day["precipitation_mm"],
    "mm"
)


# --------------------------------------------------
# CORRELATION
# --------------------------------------------------

correlation = (
    df["temperature_mean_c"]
    .corr(df["wind_speed_max_kmh"])
)


print("\n11. TEMPERATURE/WIND CORRELATION")

print(
    round(correlation, 3)
)


# --------------------------------------------------
# CREATE VISUALIZATIONS DIRECTORY
# --------------------------------------------------

os.makedirs(
    "visualizations",
    exist_ok=True
)


# --------------------------------------------------
# GRAPH 1
# TEMPERATURE OVER TIME
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.plot(
    df["date"],
    df["temperature_mean_c"],
    label="Mean Temperature"
)

plt.title(
    "Lahore Mean Temperature Over Time"
)

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")

plt.grid(alpha=0.3)

plt.legend()

plt.tight_layout()

plt.savefig(
    "visualizations/temperature_trend.png"
)

plt.close()


# --------------------------------------------------
# GRAPH 2
# PRECIPITATION
# --------------------------------------------------

plt.figure(figsize=(12, 6))

plt.bar(
    df["date"],
    df["precipitation_mm"]
)

plt.title(
    "Daily Precipitation in Lahore"
)

plt.xlabel("Date")
plt.ylabel("Precipitation (mm)")

plt.tight_layout()

plt.savefig(
    "visualizations/precipitation.png"
)

plt.close()


# --------------------------------------------------
# GRAPH 3
# TEMPERATURE HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.hist(
    df["temperature_mean_c"],
    bins=20,
    edgecolor="black"
)

plt.title(
    "Temperature Distribution"
)

plt.xlabel("Mean Temperature (°C)")
plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "visualizations/temperature_distribution.png"
)

plt.close()


# --------------------------------------------------
# GRAPH 4
# WIND SPEED HISTOGRAM
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.hist(
    df["wind_speed_max_kmh"],
    bins=20,
    edgecolor="black"
)

plt.title(
    "Wind Speed Distribution"
)

plt.xlabel(
    "Maximum Wind Speed (km/h)"
)

plt.ylabel("Frequency")

plt.tight_layout()

plt.savefig(
    "visualizations/wind_distribution.png"
)

plt.close()


# --------------------------------------------------
# GRAPH 5
# TEMPERATURE VS WIND
# --------------------------------------------------

plt.figure(figsize=(9, 6))

plt.scatter(
    df["temperature_mean_c"],
    df["wind_speed_max_kmh"],
    alpha=0.6
)

plt.title(
    "Temperature vs Wind Speed"
)

plt.xlabel(
    "Mean Temperature (°C)"
)

plt.ylabel(
    "Maximum Wind Speed (km/h)"
)

plt.tight_layout()

plt.savefig(
    "visualizations/temperature_vs_wind.png"
)

plt.close()


print(
    "\nAll visualizations saved successfully!"
)

print(
    "\nEDA COMPLETED SUCCESSFULLY!"
)