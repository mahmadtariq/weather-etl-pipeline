import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Lahore Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title(
    "🌤️ Lahore Weather ETL & EDA Dashboard"
)

st.write(
    """
    This dashboard presents exploratory data analysis
    of historical weather data for Lahore, Pakistan.
    The data was extracted from the Open-Meteo API,
    validated using Pydantic, transformed using Pandas,
    and stored in CSV format.
    """
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():

    data = pd.read_csv(
        "weather_lahore.csv"
    )

    data["date"] = pd.to_datetime(
        data["date"]
    )

    return data


df = load_data()


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "Dashboard Filters"
)

minimum_date = df["date"].min().date()
maximum_date = df["date"].max().date()

date_range = st.sidebar.date_input(
    "Select date range",
    value=(minimum_date, maximum_date),
    min_value=minimum_date,
    max_value=maximum_date
)


if len(date_range) == 2:

    start_date = pd.Timestamp(
        date_range[0]
    )

    end_date = pd.Timestamp(
        date_range[1]
    )

    filtered_df = df[
        (df["date"] >= start_date)
        &
        (df["date"] <= end_date)
    ]

else:

    filtered_df = df.copy()


# --------------------------------------------------
# KEY METRICS
# --------------------------------------------------

st.header(
    "📊 Weather Summary"
)

average_temperature = (
    filtered_df["temperature_mean_c"].mean()
)

highest_temperature = (
    filtered_df["temperature_max_c"].max()
)

lowest_temperature = (
    filtered_df["temperature_min_c"].min()
)

total_precipitation = (
    filtered_df["precipitation_mm"].sum()
)

average_wind = (
    filtered_df["wind_speed_max_kmh"].mean()
)


column1, column2, column3 = st.columns(3)

column1.metric(
    "Average Temperature",
    f"{average_temperature:.1f} °C"
)

column2.metric(
    "Highest Temperature",
    f"{highest_temperature:.1f} °C"
)

column3.metric(
    "Lowest Temperature",
    f"{lowest_temperature:.1f} °C"
)


column4, column5 = st.columns(2)

column4.metric(
    "Total Precipitation",
    f"{total_precipitation:.1f} mm"
)

column5.metric(
    "Average Max Wind",
    f"{average_wind:.1f} km/h"
)


# --------------------------------------------------
# TEMPERATURE TREND
# --------------------------------------------------

st.header(
    "🌡️ Temperature Trend"
)

fig1, ax1 = plt.subplots(
    figsize=(12, 5)
)

ax1.plot(
    filtered_df["date"],
    filtered_df["temperature_max_c"],
    label="Maximum"
)

ax1.plot(
    filtered_df["date"],
    filtered_df["temperature_mean_c"],
    label="Mean"
)

ax1.plot(
    filtered_df["date"],
    filtered_df["temperature_min_c"],
    label="Minimum"
)

ax1.set_xlabel("Date")
ax1.set_ylabel("Temperature (°C)")

ax1.legend()

ax1.grid(alpha=0.3)

st.pyplot(fig1)

plt.close(fig1)


# --------------------------------------------------
# PRECIPITATION
# --------------------------------------------------

st.header(
    "🌧️ Daily Precipitation"
)

fig2, ax2 = plt.subplots(
    figsize=(12, 5)
)

ax2.bar(
    filtered_df["date"],
    filtered_df["precipitation_mm"]
)

ax2.set_xlabel("Date")

ax2.set_ylabel(
    "Precipitation (mm)"
)

st.pyplot(fig2)

plt.close(fig2)


# --------------------------------------------------
# TEMPERATURE DISTRIBUTION
# --------------------------------------------------

st.header(
    "📊 Temperature Distribution"
)

fig3, ax3 = plt.subplots(
    figsize=(9, 5)
)

ax3.hist(
    filtered_df["temperature_mean_c"],
    bins=20,
    edgecolor="black"
)

ax3.set_xlabel(
    "Mean Temperature (°C)"
)

ax3.set_ylabel(
    "Frequency"
)

st.pyplot(fig3)

plt.close(fig3)


# --------------------------------------------------
# WIND DISTRIBUTION
# --------------------------------------------------

st.header(
    "💨 Wind Speed Distribution"
)

fig4, ax4 = plt.subplots(
    figsize=(9, 5)
)

ax4.hist(
    filtered_df["wind_speed_max_kmh"],
    bins=20,
    edgecolor="black"
)

ax4.set_xlabel(
    "Maximum Wind Speed (km/h)"
)

ax4.set_ylabel(
    "Frequency"
)

st.pyplot(fig4)

plt.close(fig4)


# --------------------------------------------------
# SCATTER PLOT
# --------------------------------------------------

st.header(
    "🔗 Temperature vs Wind Speed"
)

fig5, ax5 = plt.subplots(
    figsize=(9, 5)
)

ax5.scatter(
    filtered_df["temperature_mean_c"],
    filtered_df["wind_speed_max_kmh"],
    alpha=0.6
)

ax5.set_xlabel(
    "Mean Temperature (°C)"
)

ax5.set_ylabel(
    "Maximum Wind Speed (km/h)"
)

st.pyplot(fig5)

plt.close(fig5)


# --------------------------------------------------
# CORRELATION
# --------------------------------------------------

correlation = (
    filtered_df["temperature_mean_c"]
    .corr(
        filtered_df["wind_speed_max_kmh"]
    )
)

st.subheader(
    "Temperature-Wind Correlation"
)

st.write(
    f"Correlation coefficient: **{correlation:.3f}**"
)


# --------------------------------------------------
# HOTTEST AND COLDEST DAYS
# --------------------------------------------------

st.header(
    "🔥 Extreme Weather Days"
)


hottest_day = filtered_df.loc[
    filtered_df["temperature_max_c"].idxmax()
]

coldest_day = filtered_df.loc[
    filtered_df["temperature_min_c"].idxmin()
]


left, right = st.columns(2)


with left:

    st.subheader(
        "🔥 Hottest Day"
    )

    st.write(
        "Date:",
        hottest_day["date"].date()
    )

    st.write(
        "Temperature:",
        f'{hottest_day["temperature_max_c"]:.1f} °C'
    )


with right:

    st.subheader(
        "❄️ Coldest Day"
    )

    st.write(
        "Date:",
        coldest_day["date"].date()
    )

    st.write(
        "Temperature:",
        f'{coldest_day["temperature_min_c"]:.1f} °C'
    )


# --------------------------------------------------
# DATA QUALITY
# --------------------------------------------------

st.header(
    "✅ Data Quality"
)

quality1, quality2, quality3 = st.columns(3)

quality1.metric(
    "Records",
    len(filtered_df)
)

quality2.metric(
    "Missing Values",
    int(filtered_df.isnull().sum().sum())
)

quality3.metric(
    "Duplicate Rows",
    int(filtered_df.duplicated().sum())
)


# --------------------------------------------------
# SUMMARY STATISTICS
# --------------------------------------------------

st.header(
    "📈 Summary Statistics"
)

st.dataframe(
    filtered_df.describe()
)


# --------------------------------------------------
# DATASET
# --------------------------------------------------

st.header(
    "📋 Cleaned Weather Dataset"
)

st.dataframe(
    filtered_df,
    use_container_width=True
)


# --------------------------------------------------
# DOWNLOAD
# --------------------------------------------------

csv = filtered_df.to_csv(
    index=False
).encode("utf-8")


st.download_button(
    label="Download Filtered CSV",
    data=csv,
    file_name="lahore_weather_filtered.csv",
    mime="text/csv"
)


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Data Source: Open-Meteo Historical Weather API"
)