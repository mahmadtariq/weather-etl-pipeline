
import streamlit as st
import pandas as pd
import requests
import plotly.express as px
import plotly.graph_objects as go
from datetime import date, timedelta

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Weather Intelligence Dashboard",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main background */
    .stApp {
        background:
            radial-gradient(circle at 10% 10%, rgba(0, 153, 255, 0.18), transparent 30%),
            radial-gradient(circle at 90% 20%, rgba(120, 80, 255, 0.15), transparent 30%),
            linear-gradient(135deg, #07111f 0%, #0b1728 50%, #101827 100%);
        color: white;
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #081321 0%, #0d1b2e 100%);
        border-right: 1px solid rgba(255,255,255,0.08);
    }

    /* Main title */
    .main-title {
        font-size: 48px;
        font-weight: 800;
        text-align: center;
        margin-top: 5px;
        margin-bottom: 5px;
        background: linear-gradient(90deg, #00d4ff, #7c5cff, #ff4ecd);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        text-align: center;
        color: #a9b7ca;
        font-size: 18px;
        margin-bottom: 25px;
    }

    /* Glass cards */
    .glass-card {
        background: rgba(255,255,255,0.055);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 20px;
        padding: 22px;
        backdrop-filter: blur(12px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.20);
    }

    .weather-card {
        background: linear-gradient(
            135deg,
            rgba(0, 212, 255, 0.16),
            rgba(124, 92, 255, 0.14)
        );
        border: 1px solid rgba(255,255,255,0.13);
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        box-shadow: 0 15px 40px rgba(0,0,0,0.25);
    }

    .metric-value {
        font-size: 34px;
        font-weight: 800;
        color: white;
    }

    .metric-label {
        font-size: 14px;
        color: #a9b7ca;
        text-transform: uppercase;
        letter-spacing: 1px;
    }

    .section-title {
        font-size: 26px;
        font-weight: 700;
        margin-top: 25px;
        margin-bottom: 10px;
    }

    .city-banner {
        text-align: center;
        font-size: 30px;
        font-weight: 700;
        margin: 10px 0 20px 0;
    }

    .status {
        text-align: center;
        color: #8fa6bf;
        font-size: 13px;
        margin-top: 30px;
    }

    /* Buttons */
    .stButton > button {
        width: 100%;
        border-radius: 12px;
        border: 1px solid rgba(255,255,255,0.12);
        background: linear-gradient(90deg, #0077ff, #684cff);
        color: white;
        font-weight: 700;
        transition: 0.25s;
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,119,255,0.35);
    }

    /* Download button */
    .stDownloadButton > button {
        width: 100%;
        border-radius: 12px;
        font-weight: 700;
    }

    /* Hide Streamlit default menu/footer */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def find_city(city):
    """Find city coordinates using Open-Meteo geocoding API."""

    url = "https://geocoding-api.open-meteo.com/v1/search"

    params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code != 200:
        return None

    data = response.json()

    if "results" not in data or not data["results"]:
        return None

    result = data["results"][0]

    return {
        "name": result.get("name", city),
        "country": result.get("country", "Unknown"),
        "latitude": result["latitude"],
        "longitude": result["longitude"],
        "timezone": result.get("timezone", "auto")
    }


@st.cache_data(ttl=3600)
def get_weather(latitude, longitude, start_date, end_date):

    url = "https://archive-api.open-meteo.com/v1/archive"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "start_date": start_date,
        "end_date": end_date,
        "daily": ",".join([
            "temperature_2m_max",
            "temperature_2m_min",
            "temperature_2m_mean",
            "precipitation_sum",
            "wind_speed_10m_max"
        ]),
        "timezone": "auto"
    }

    response = requests.get(url, params=params, timeout=30)

    if response.status_code != 200:
        return None

    data = response.json()

    if "daily" not in data:
        return None

    daily = data["daily"]

    df = pd.DataFrame({
        "Date": daily["time"],
        "Max Temperature (°C)": daily["temperature_2m_max"],
        "Min Temperature (°C)": daily["temperature_2m_min"],
        "Mean Temperature (°C)": daily["temperature_2m_mean"],
        "Precipitation (mm)": daily["precipitation_sum"],
        "Wind Speed (km/h)": daily["wind_speed_10m_max"]
    })

    df["Date"] = pd.to_datetime(df["Date"])

    return df


def weather_emoji(temp, rain, wind):

    if rain > 10:
        return "🌧️", "Rainy"
    elif rain > 2:
        return "🌦️", "Light Rain"
    elif temp >= 35:
        return "🔥", "Very Hot"
    elif temp >= 28:
        return "☀️", "Hot"
    elif temp >= 20:
        return "🌤️", "Pleasant"
    elif temp >= 10:
        return "⛅", "Cool"
    else:
        return "❄️", "Cold"


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🌍 Weather Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Interactive ETL • Historical Weather Analytics • Global City Explorer</div>',
    unsafe_allow_html=True
)


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 🌎 Explore Weather")

    city = st.text_input(
        "🔎 Search for a city",
        value="Lahore",
        placeholder="Example: London"
    )

    st.markdown("---")

    st.markdown("### 📅 Historical Period")

    today = date.today()

    default_start = today - timedelta(days=365)
    default_end = today - timedelta(days=5)

    date_range = st.date_input(
        "Select date range",
        value=(default_start, default_end),
        min_value=date(1940, 1, 1),
        max_value=default_end
    )

    st.markdown("---")

    st.markdown("### ⚙️ Dashboard Controls")

    chart_type = st.selectbox(
        "Temperature chart",
        [
            "Temperature Area",
            "Temperature Lines",
            "Temperature Range"
        ]
    )

    show_points = st.checkbox(
        "Show chart points",
        value=False
    )

    st.markdown("---")

    st.info(
        "💡 Search any city and explore its historical weather data."
    )

    st.caption("Powered by Open-Meteo API")


# ============================================================
# VALIDATE DATE RANGE
# ============================================================

if isinstance(date_range, tuple) and len(date_range) == 2:

    start_date = date_range[0]
    end_date = date_range[1]

else:

    start_date = default_start
    end_date = default_end


# ============================================================
# FIND CITY
# ============================================================

with st.spinner("🌐 Finding your city..."):

    location = find_city(city)


if location is None:

    st.error(
        "❌ City not found. Try another city such as Lahore, Karachi, London, Tokyo or Dubai."
    )

    st.stop()


# ============================================================
# CITY INFORMATION
# ============================================================

st.markdown(
    f"""
    <div class="city-banner">
        📍 {location['name']}, {location['country']}
    </div>
    """,
    unsafe_allow_html=True
)

location_col1, location_col2, location_col3 = st.columns(3)

with location_col1:
    st.caption(f"Latitude: {location['latitude']:.4f}")

with location_col2:
    st.caption(f"Longitude: {location['longitude']:.4f}")

with location_col3:
    st.caption(f"Timezone: {location['timezone']}")


# ============================================================
# GET WEATHER
# ============================================================

with st.spinner("☁️ Downloading historical weather data..."):

    df = get_weather(
        location["latitude"],
        location["longitude"],
        start_date.isoformat(),
        end_date.isoformat()
    )


if df is None or df.empty:

    st.error(
        "⚠️ Weather data could not be retrieved for this period."
    )

    st.stop()


# ============================================================
# DATA CLEANING
# ============================================================

numeric_columns = [
    "Max Temperature (°C)",
    "Min Temperature (°C)",
    "Mean Temperature (°C)",
    "Precipitation (mm)",
    "Wind Speed (km/h)"
]

for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors="coerce")

df = df.dropna(subset=["Mean Temperature (°C)"])

df["Temperature Range (°C)"] = (
    df["Max Temperature (°C)"]
    - df["Min Temperature (°C)"]
)

df["Month"] = df["Date"].dt.strftime("%b")

df["Day"] = df["Date"].dt.day


# ============================================================
# CURRENT / LATEST AVAILABLE SUMMARY
# ============================================================

latest = df.iloc[-1]

latest_temp = latest["Mean Temperature (°C)"]
latest_max = latest["Max Temperature (°C)"]
latest_min = latest["Min Temperature (°C)"]
latest_rain = latest["Precipitation (mm)"]
latest_wind = latest["Wind Speed (km/h)"]

emoji, condition = weather_emoji(
    latest_temp,
    latest_rain,
    latest_wind
)


# ============================================================
# HERO WEATHER CARD
# ============================================================

st.markdown("### ✨ Latest Available Weather")

hero1, hero2, hero3 = st.columns([1.4, 1, 1])

with hero1:

    st.markdown(
        f"""
        <div class="weather-card">
            <div style="font-size:65px;">{emoji}</div>
            <div style="font-size:38px;font-weight:800;">
                {latest_temp:.1f}°C
            </div>
            <div style="font-size:18px;color:#b8c6d9;">
                {condition}
            </div>
            <div style="margin-top:8px;color:#8398b0;">
                {latest['Date'].strftime('%d %B %Y')}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with hero2:

    st.markdown(
        f"""
        <div class="weather-card">
            <div style="font-size:40px;">🌡️</div>
            <div class="metric-value">{latest_max:.1f}°C</div>
            <div class="metric-label">Maximum</div>
            <br>
            <div style="font-size:30px;">{latest_min:.1f}°C</div>
            <div class="metric-label">Minimum</div>
        </div>
        """,
        unsafe_allow_html=True
    )


with hero3:

    st.markdown(
        f"""
        <div class="weather-card">
            <div style="font-size:40px;">💨</div>
            <div class="metric-value">{latest_wind:.1f}</div>
            <div class="metric-label">Wind km/h</div>
            <br>
            <div style="font-size:30px;">{latest_rain:.1f} mm</div>
            <div class="metric-label">Precipitation</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# KPI CARDS
# ============================================================

st.markdown("### 📊 Weather Overview")

k1, k2, k3, k4, k5 = st.columns(5)

avg_temp = df["Mean Temperature (°C)"].mean()
max_temp = df["Max Temperature (°C)"].max()
min_temp = df["Min Temperature (°C)"].min()
total_rain = df["Precipitation (mm)"].sum()
avg_wind = df["Wind Speed (km/h)"].mean()

with k1:
    st.metric("🌡️ Avg Temperature", f"{avg_temp:.1f} °C")

with k2:
    st.metric("🔥 Highest", f"{max_temp:.1f} °C")

with k3:
    st.metric("❄️ Lowest", f"{min_temp:.1f} °C")

with k4:
    st.metric("🌧️ Total Rain", f"{total_rain:.1f} mm")

with k5:
    st.metric("💨 Avg Wind", f"{avg_wind:.1f} km/h")


# ============================================================
# TEMPERATURE CHART
# ============================================================

st.markdown("### 🌡️ Temperature Trends")

if chart_type == "Temperature Area":

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Max Temperature (°C)"],
            name="Maximum",
            mode="lines+markers" if show_points else "lines",
            line=dict(width=2)
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Min Temperature (°C)"],
            name="Minimum",
            mode="lines+markers" if show_points else "lines",
            fill="tonexty",
            line=dict(width=2)
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        hovermode="x unified",
        xaxis_title="Date",
        yaxis_title="Temperature (°C)",
        legend_title="Temperature"
    )

elif chart_type == "Temperature Lines":

    fig = px.line(
        df,
        x="Date",
        y=[
            "Max Temperature (°C)",
            "Mean Temperature (°C)",
            "Min Temperature (°C)"
        ],
        template="plotly_dark",
        markers=show_points
    )

    fig.update_layout(
        height=500,
        hovermode="x unified"
    )

else:

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Max Temperature (°C)"],
            mode="lines",
            name="Maximum"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=df["Date"],
            y=df["Min Temperature (°C)"],
            mode="lines",
            name="Minimum",
            fill="tonexty"
        )
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        hovermode="x unified"
    )

st.plotly_chart(fig, width="stretch")


# ============================================================
# SECOND ROW
# ============================================================

col1, col2 = st.columns(2)


# PRECIPITATION
with col1:

    st.markdown("### 🌧️ Precipitation")

    rain_df = df.copy()

    rain_fig = px.bar(
        rain_df,
        x="Date",
        y="Precipitation (mm)",
        template="plotly_dark",
        hover_data={
            "Precipitation (mm)": ":.2f"
        }
    )

    rain_fig.update_layout(
        height=420,
        xaxis_title="Date",
        yaxis_title="Rainfall (mm)"
    )

    st.plotly_chart(rain_fig, width="stretch")


# WIND
with col2:

    st.markdown("### 💨 Wind Speed")

    wind_fig = px.line(
        df,
        x="Date",
        y="Wind Speed (km/h)",
        template="plotly_dark",
        markers=show_points
    )

    wind_fig.update_layout(
        height=420,
        xaxis_title="Date",
        yaxis_title="Wind Speed (km/h)"
    )

    st.plotly_chart(wind_fig, width="stretch")


# ============================================================
# DISTRIBUTIONS
# ============================================================

st.markdown("### 📈 Weather Distributions")

dist1, dist2 = st.columns(2)

with dist1:

    temp_fig = px.histogram(
        df,
        x="Mean Temperature (°C)",
        nbins=30,
        template="plotly_dark",
        marginal="box"
    )

    temp_fig.update_layout(
        height=400,
        xaxis_title="Mean Temperature (°C)",
        yaxis_title="Number of Days"
    )

    st.plotly_chart(temp_fig, width="stretch")


with dist2:

    wind_hist = px.histogram(
        df,
        x="Wind Speed (km/h)",
        nbins=30,
        template="plotly_dark",
        marginal="box"
    )

    wind_hist.update_layout(
        height=400,
        xaxis_title="Wind Speed (km/h)",
        yaxis_title="Number of Days"
    )

    st.plotly_chart(wind_hist, width="stretch")


# ============================================================
# TEMPERATURE VS WIND
# ============================================================

st.markdown("### 🔬 Temperature vs Wind Relationship")

scatter_fig = px.scatter(
    df,
    x="Mean Temperature (°C)",
    y="Wind Speed (km/h)",
    size="Precipitation (mm)",
    hover_data=["Date", "Max Temperature (°C)", "Min Temperature (°C)"],
    template="plotly_dark"
)

scatter_fig.update_layout(
    height=500
)

st.plotly_chart(scatter_fig, width="stretch")


# ============================================================
# EXTREME DAYS
# ============================================================

st.markdown("### 🏆 Weather Records")

hot_day = df.loc[
    df["Max Temperature (°C)"].idxmax()
]

cold_day = df.loc[
    df["Min Temperature (°C)"].idxmin()
]

rain_day = df.loc[
    df["Precipitation (mm)"].idxmax()
]

record1, record2, record3 = st.columns(3)

with record1:

    st.markdown(
        f"""
        <div class="glass-card">
            <h3>🔥 Hottest Day</h3>
            <h2>{hot_day['Max Temperature (°C)']:.1f}°C</h2>
            <p>{hot_day['Date'].strftime('%d %B %Y')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with record2:

    st.markdown(
        f"""
        <div class="glass-card">
            <h3>❄️ Coldest Day</h3>
            <h2>{cold_day['Min Temperature (°C)']:.1f}°C</h2>
            <p>{cold_day['Date'].strftime('%d %B %Y')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


with record3:

    st.markdown(
        f"""
        <div class="glass-card">
            <h3>🌧️ Wettest Day</h3>
            <h2>{rain_day['Precipitation (mm)']:.1f} mm</h2>
            <p>{rain_day['Date'].strftime('%d %B %Y')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# CORRELATION
# ============================================================

st.markdown("### 🧠 Data Insights")

correlation = df[
    [
        "Mean Temperature (°C)",
        "Wind Speed (km/h)"
    ]
].corr().iloc[0, 1]

insight1, insight2, insight3 = st.columns(3)

with insight1:

    st.metric(
        "Temperature ↔ Wind",
        f"{correlation:.2f}"
    )


with insight2:

    st.metric(
        "Days Analyzed",
        f"{len(df):,}"
    )


with insight3:

    st.metric(
        "Rainy Days",
        f"{(df['Precipitation (mm)'] > 0).sum():,}"
    )


# ============================================================
# MONTHLY ANALYSIS
# ============================================================

st.markdown("### 📅 Monthly Temperature Analysis")

monthly = (
    df.groupby("Month", sort=False)
    .agg(
        Average_Temperature=("Mean Temperature (°C)", "mean"),
        Maximum_Temperature=("Max Temperature (°C)", "max"),
        Rainfall=("Precipitation (mm)", "sum")
    )
    .reset_index()
)

monthly_fig = px.bar(
    monthly,
    x="Month",
    y="Average_Temperature",
    template="plotly_dark",
    hover_data=[
        "Maximum_Temperature",
        "Rainfall"
    ]
)

monthly_fig.update_layout(
    height=420,
    xaxis_title="Month",
    yaxis_title="Average Temperature (°C)"
)

st.plotly_chart(monthly_fig, width="stretch")


# ============================================================
# DATA QUALITY
# ============================================================

with st.expander("🛡️ Data Quality Report"):

    q1, q2, q3 = st.columns(3)

    with q1:
        st.metric(
            "Rows",
            f"{len(df):,}"
        )

    with q2:
        st.metric(
            "Missing Values",
            f"{df.isna().sum().sum():,}"
        )

    with q3:
        st.metric(
            "Duplicate Rows",
            f"{df.duplicated().sum():,}"
        )

    st.write("Column Information")

    st.dataframe(
        df.dtypes.astype(str).to_frame("Data Type"),
        width="stretch"
    )


# ============================================================
# DATASET
# ============================================================

with st.expander("📋 Explore Complete Dataset"):

    st.dataframe(
        df,
        width="stretch",
        height=450
    )


# ============================================================
# SUMMARY STATISTICS
# ============================================================

with st.expander("📊 Statistical Summary"):

    st.dataframe(
        df[numeric_columns].describe().round(2),
        width="stretch"
    )


# ============================================================
# DOWNLOAD
# ============================================================

st.markdown("### 📥 Export Your Data")

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Download Weather Dataset (CSV)",
    data=csv,
    file_name=f"{location['name']}_weather.csv",
    mime="text/csv"
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="status">
        🌍 Weather Intelligence Dashboard &nbsp;•&nbsp;
        Open-Meteo API &nbsp;•&nbsp;
        Python ETL &nbsp;•&nbsp;
        Pandas &nbsp;•&nbsp;
        Plotly &nbsp;•&nbsp;
        Streamlit
        <br><br>
        <b>Algorithm Architect</b>
    </div>
    """,
    unsafe_allow_html=True
)
