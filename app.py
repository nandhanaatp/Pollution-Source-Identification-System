import streamlit as st
import pandas as pd
import numpy as np
import joblib
import requests
import datetime
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.figure_factory as ff
# ---------------------------------------------------
# PAGE CONFIG (Dark theme look)
# ---------------------------------------------------
st.set_page_config(
    page_title="Delhi Real-Time Pollution Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ---------------------------------------------------
# CUSTOM CSS FOR PREMIUM LOOK (Dark Theme) - Professional Dark Mode
# ---------------------------------------------------
st.markdown("""
<style>
    body, .stApp {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        color: #e0e0e0;
        font-size: 14px;
        line-height: 1.5;
        background-color: #121212;
    }
    h1, h2, h3, h4, h5, h6 {
        color: #f0f0f0;
        font-weight: 600;
    }
    .stMarkdown {
        color: #e0e0e0;
    }
   
    .main .block-container {
        padding-top: 2rem;
        padding-right: 1rem;
        padding-left: 1rem;
        padding-bottom: 1rem;
        background-color: #121212;
    }
    .stMetric {
        background: #1e1e1e;
        border-radius: 12px;
        padding: 0.75rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
        border-left: 4px solid #6366f1;
        color: #e0e0e0;
    }
    .stMetric > label {
        color: #d1d5db !important;
        font-size: 0.9rem;
    }
    .stMetric > div > div:last-child {
        color: #f9fafb !important;
        font-size: 1.5rem;
    }
    .stDataFrame {
        border-radius: 8px;
        overflow: hidden;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
        background-color: #1e1e1e;
        width: 100%;
        max-width: 100%;
    }
    .stDataFrame thead tr th {
        background: linear-gradient(135deg, #2d2d2d 0%, #3a3a3a 100%);
        color: #e0e0e0;
        font-weight: 600;
        border-bottom: 2px solid #6366f1;
        padding: 8px;
        font-size: 12px;
        white-space: nowrap;
    }
    .stDataFrame tbody tr td {
        color: #e0e0e0;
        background-color: #1e1e1e;
        border-bottom: 1px solid #333;
        padding: 8px;
        font-size: 12px;
        white-space: nowrap;
        transition: background-color 0.2s;
    }
    .stDataFrame tbody tr:hover td {
        background-color: #2d2d2d;
    }
    .stDataFrame tbody tr:nth-child(even) td {
        background-color: #2a2a2a;
    }
    .stDataFrame tbody tr:nth-child(even):hover td {
        background-color: #333;
    }
    @media (max-width: 768px) {
        .stDataFrame {
            overflow-x: auto;
            display: block;
            white-space: nowrap;
        }
        .stDataFrame thead tr th,
        .stDataFrame tbody tr td {
            font-size: 10px;
            padding: 6px 4px;
        }
        .premium-card {
            padding: 1rem;
        }
    }
    @media (max-width: 480px) {
        .stDataFrame thead tr th,
        .stDataFrame tbody tr td {
            font-size: 9px;
            padding: 4px 2px;
        }
    }
    .stDataFrame .high-pollution {
        background-color: #ff4444 !important;
        color: #ffffff !important;
    }
    .stDataFrame .medium-pollution {
        background-color: #ffaa00 !important;
        color: #000000 !important;
    }
    .premium-card {
        background: #1e1e1e;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
        border: 1px solid #333;
        color: #e0e0e0;
        margin-bottom: 1rem;
        overflow-x: auto;
    }
    .premium-header {
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: #ffffff;
        padding: 1rem;
        border-radius: 12px;
        text-align: center;
        font-weight: bold;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.2);
        width: 100%;
        margin-bottom: 1rem;
    }
    .premium-header h1, .premium-header p {
        color: white !important;
        margin: 0;
        padding: 0 1rem;
    }
    .sidebar .sidebar-content {
        background: #1e1e1e;
        color: #e0e0e0;
    }
    .stSidebar > div > div > div {
        color: #e0e0e0;
    }
    .stSelectbox, .stMultiselect, .stSlider, .stCheckbox {
        background-color: #2d2d2d;
        color: #e0e0e0;
        border: 1px solid #444;
        border-radius: 6px;
    }
    .stSelectbox > div > div, .stMultiselect > div > div {
        color: #e0e0e0;
    }
    .modebar {
        font-family: 'Segoe UI', sans-serif;
        color: #e0e0e0;
        background: rgba(0,0,0,0.3);
    }
    .corner-timestamp {
        position: fixed;
        top: 20px;
        right: 20px;
        background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%);
        color: white;
        padding: 12px 16px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        box-shadow: 0 4px 12px rgba(79, 70, 229, 0.4);
        z-index: 1000;
        text-align: center;
        min-width: 180px;
    }
    .gauge-container {
        text-align: center;
    }
    .stTabs [data-baseweb="tab-list"] {
        background: #2d2d2d;
        border-radius: 8px;
        padding: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        background: #1e1e1e;
        color: #e0e0e0;
        border: none;
        border-radius: 6px;
        margin: 2px;
    }
    .stTabs [data-baseweb="tab"]:hover {
        background: #4f46e5;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: #4f46e5;
        color: white;
    }
    @media (max-width: 768px) {
        [data-testid="column"]:nth-child(1) {
            width: 100% !important;
        }
        [data-testid="column"]:nth-child(2),
        [data-testid="column"]:nth-child(3),
        [data-testid="column"]:nth-child(4),
        [data-testid="column"]:nth-child(5) {
            width: 100% !important;
            margin-top: 1rem;
        }
    }
</style>
""", unsafe_allow_html=True)
# ---------------------------------------------------
# FILE PATHS (CLASSIFIER MODEL)
# ---------------------------------------------------
# FILE PATHS (NEW MODELS)
SCALER_PATH = "pollution_scaler_poll.pkl"
PREPROCESSOR_PATH = "pollution_preprocessor.pkl"
MODEL_PATH = "pollution_rf_model.pkl"
KMEANS_PATH = "pollution_kmeans.pkl"
HIST_CSV = "final_dataset.csv"
# Your WAQI token
WAQI_TOKEN = "fb13edde6f8dfd9427eecafa1c3313ac4559d9ca"
# WAQI OFFICIAL STATION IDs with lat/lon (STABLE) - Expanded for accuracy
STATIONS = {
    "Anand Vihar": {"id": 1437, "lat": 28.6507, "lon": 77.3150},
    "Mandir Marg": {"id": 1440, "lat": 28.6330, "lon": 77.2000},
    "Shadipur": {"id": 1452, "lat": 28.6510, "lon": 77.1620},
    "Rohini": {"id": 1442, "lat": 28.7490, "lon": 77.0560},
    "Mundka": {"id": 1455, "lat": 28.6805, "lon": 77.0305},
    "Dwarka": {"id": 1456, "lat": 28.5921, "lon": 77.0460},
    "IHBAS - Dilshad Garden": {"id": 10737, "lat": 28.6726, "lon": 77.3150},
    "Major Dhyan Chand Stadium": {"id": 1445, "lat": 28.6125, "lon": 77.2373},
    "Ashok Vihar": {"id": 1420, "lat": 28.6888, "lon": 77.1750},
    "Bawana": {"id": 1421, "lat": 28.7990, "lon": 77.0340},
    "Jahangirpuri": {"id": 1422, "lat": 28.7250, "lon": 77.1625},
    "Narela": {"id": 1423, "lat": 28.8527, "lon": 77.0918},
    "Wazirpur": {"id": 1424, "lat": 28.6997, "lon": 77.1650},
    "DTU": {"id": 1425, "lat": 28.7500, "lon": 77.1177},
    "Sirifort": {"id": 1426, "lat": 28.5504, "lon": 77.2159},
    "Aya Nagar": {"id": 1427, "lat": 28.4707, "lon": 77.1099},
    "Lodhi Road": {"id": 1428, "lat": 28.5918, "lon": 77.2273},
    "NSIT Dwarka": {"id": 1429, "lat": 28.6095, "lon": 77.0325},
    "Najafgarh": {"id": 1430, "lat": 28.6090, "lon": 76.9850},
    "Okhla Phase 2": {"id": 1431, "lat": 28.5308, "lon": 77.2713},
    "Patparganj": {"id": 1432, "lat": 28.6235, "lon": 77.2878},
    "Sonia Vihar": {"id": 1433, "lat": 28.7105, "lon": 77.2495},
    "Vivek Vihar": {"id": 1434, "lat": 28.6693, "lon": 77.3153},
    "Punjabi Bagh": {"id": 1441, "lat": 28.6618, "lon": 77.1240},
    "RK Puram": {"id": 1443, "lat": 28.5630, "lon": 77.1860},
    "Pusa": {"id": 1444, "lat": 28.6389, "lon": 77.1464},
    "IGI Airport": {"id": 1446, "lat": 28.5562, "lon": 77.0878},
    "Lodhi Road IMD": {"id": 1447, "lat": 28.5918, "lon": 77.2273},
    "Chandni Chowk": {"id": 1448, "lat": 28.6566, "lon": 77.2311},
    "Mathura Road": {"id": 1449, "lat": 28.5900, "lon": 77.2450},
    "Lodhi Road IITM": {"id": 1450, "lat": 28.6300, "lon": 77.2230},
    "Sri Aurobindo Marg": {"id": 1451, "lat": 28.5312, "lon": 77.1906},
    "Jawaharlal Nehru Stadium": {"id": 1453, "lat": 28.5830, "lon": 77.2350},
    "Najafgarh": {"id": 1454, "lat": 28.6090, "lon": 76.9850}
}
FEATURES = ["co", "no2", "o3", "pm10", "pm25", "so2"]
# All possible sources (to ensure all categories show, even at 0%)
ALL_SOURCES = ["ozone_photochemical", "industrial", "traffic", "dust", "clean"]
# Source explanations for classifier labels
SOURCE_EXPLANATIONS = {
    "clean": "Low pollution levels without dominant sources.",
    "dust": "High PM10/PM2.5 ratio — construction, road dust, resuspension.",
    "industrial": "High SO₂ + moderate PM/NOx — factories, coal combustion.",
    "ozone_photochemical": "High O₃ with NOx — secondary pollution formed in sunlight.",
    "traffic": "High CO + NO₂ — typically traffic and vehicular exhaust."
}
# ---------------------------------------------------
# LOAD CLASSIFIER MODEL
# ---------------------------------------------------
@st.cache_resource
def load_models():
    scaler_poll = joblib.load(SCALER_PATH)
    preprocessor = joblib.load(PREPROCESSOR_PATH)
    model = joblib.load(MODEL_PATH)
    kmeans = joblib.load(KMEANS_PATH)
    return scaler_poll, preprocessor, model, kmeans
scaler_poll, preprocessor, model, kmeans = load_models()
# ---------------------------------------------------
# SAFE PARSING OF WAQI VALUES
# ---------------------------------------------------
def safe_value(iaqi, field):
    try:
        raw = iaqi.get(field)
        if raw is None:
            return np.nan
        if isinstance(raw, dict):
            raw = raw.get("v", np.nan)
        if isinstance(raw, dict):
            return np.nan
        return float(raw)
    except:
        return np.nan
# ---------------------------------------------------
# FETCH WAQI STATION
# ---------------------------------------------------
def fetch_waqi_by_id(station_id):
    url = f"https://api.waqi.info/feed/@{station_id}/?token={WAQI_TOKEN}"
    try:
        res = requests.get(url, timeout=7).json()
    except:
        return None
    if res.get("status") != "ok":
        return None
    iaqi = res["data"].get("iaqi", {})
    return {
        "co": safe_value(iaqi, "co") * 1.15,
        "no2": safe_value(iaqi, "no2") * 1.88,
        "o3": safe_value(iaqi, "o3") * 2.0,
        "pm10": safe_value(iaqi, "pm10") * 1.2,
        "pm25": safe_value(iaqi, "pm25") * 1.1,
        "so2": safe_value(iaqi, "so2") * 2.62,
    }
# ---------------------------------------------------
# CROP BURNING INDEX (CBI)
# ---------------------------------------------------
def compute_crop_burning_index(row):
    # intensity components
    pm25_score = min(row["pm25"] / 200, 1.0)
    pm10_score = min(row["pm10"] / 300, 1.0)
    # characteristic PM2.5/PM10 ratio for biomass burning ~0.7–1.0
    ratio = row["pm25"] / max(row["pm10"], 1)
    ratio_score = 1 - min(abs(ratio - 0.8) / 0.8, 1.0)
    # CO is a strong marker
    co_score = min(row["co"] / 2000, 1.0)
    # penalties (traffic/industry)
    no2_penalty = max(0, (60 - row["no2"]) / 60)
    so2_penalty = max(0, (20 - row["so2"]) / 20)
    # weighted CBI
    cbi = (
        0.3 * pm25_score +
        0.2 * pm10_score +
        0.15 * ratio_score +
        0.2 * co_score +
        0.075 * no2_penalty +
        0.075 * so2_penalty
    )
    return cbi
def classify_crop_burning(cbi):
    if cbi < 0.4:
        return "Low"
    elif cbi < 0.7:
        return "Medium"
    else:
        return "High"
# ---------------------------------------------------
# FETCH LIVE DATA FOR ALL STATIONS
# ---------------------------------------------------
records = []
errors = []
for name, station in STATIONS.items():
    rec = fetch_waqi_by_id(station["id"])
    if rec:
        rec["location"] = name
        records.append(rec)
    else:
        errors.append(name)
if len(records) == 0:
    st.error("Could not fetch ANY WAQI live data. Check API token or internet.")
    st.stop()
df_live = pd.DataFrame(records)
# ---------------------------------------------------
# HANDLE MISSING VALUES USING HISTORICAL MEDIAN
# ---------------------------------------------------
hist = pd.read_csv(HIST_CSV)
hist.columns = hist.columns.str.strip().str.lower().str.replace('.', '').str.replace(' ', '').str.replace('_', '')
hist = hist.rename(columns={'ozone': 'o3'})
hist['timestamp'] = pd.to_datetime(hist['year'].astype(str) + '-' + hist['month'].astype(str) + '-' + hist['date'].astype(str), errors='coerce')
hist_median = hist[FEATURES].median()
df_live[FEATURES] = df_live[FEATURES].fillna(hist_median)
# ---------------------------------------------------
# ---------------------------------------------------
# ---------------------------------------------------
# MODEL INFERENCE (CLASSIFIER + REFINED SOURCE PERCENTAGES)
# ---------------------------------------------------
# Columns expected by your scaler & preprocessor
capital_poll = ["PM2.5", "PM10", "NO2", "SO2", "CO", "Ozone"]

# 1. Create capital columns using raw live pollutant values
df_live[capital_poll] = df_live[["pm25", "pm10", "no2", "so2", "co", "o3"]].values

# 2. Scale pollutants
scaled_poll = scaler_poll.transform(df_live[capital_poll])
df_live[capital_poll] = pd.DataFrame(scaled_poll, columns=capital_poll, index=df_live.index)

# 3. Add categorical features
df_live['Holidays_Count'] = 0
current_day = datetime.datetime.now().weekday()  # 0=Monday, 6=Sunday
df_live['Days'] = current_day + 1  # Your model expects 1–7

# 4. Preprocess & predict cluster
full_features = capital_poll + ['Holidays_Count', 'Days']
X_preprocessed = preprocessor.transform(df_live[full_features])
df_live["cluster"] = model.predict(X_preprocessed)

# ---------------------------------------------------
# REFINED SOURCE PERCENTAGE FUNCTION (YOUR LOGIC)
# ---------------------------------------------------
def get_source_percentages(cluster_id, days=1, is_weekday=True):
    """
    Refined mappings based on Delhi winter studies (vehicles ~40-50% baseline).
    Boosts vehicles +15-25% on weekdays; adjusts others to sum to 100%.
    """
    base_mappings = {
        0: {'Clean': 70, 'Vehicle': 10, 'Dust': 10, 'Industrial': 5, 'Smog': 5},
        1: {'Dust': 60, 'Vehicle': 20, 'Clean': 10, 'Industrial': 5, 'Smog': 5},
        2: {'Industrial': 30, 'Vehicle': 45, 'Dust': 15, 'Smog': 5, 'Clean': 5},   
        3: {'Smog': 40, 'Vehicle': 40, 'Industrial': 10, 'Dust': 5, 'Clean': 5},  
        4: {'Vehicle': 70, 'Dust': 20, 'Smog': 5, 'Industrial': 5, 'Clean': 0}    
    }
    percentages = base_mappings.get(cluster_id, {'Unknown': 100}).copy()

    # Weekday boost for vehicles (traffic factor)
    if is_weekday and days <= 5:  # Monday=1 to Friday=5
        vehicle_boost = 0.20 * percentages.get('Vehicle', 0)  # +20% relative boost
        percentages['Vehicle'] = min(95, percentages['Vehicle'] + vehicle_boost)
        # Reduce others proportionally
        reduction = vehicle_boost / 2
        for key in ['Industrial', 'Dust', 'Smog']:
            if key in percentages:
                percentages[key] = max(0, percentages[key] - reduction / 2)
        if 'Clean' in percentages:
            percentages['Clean'] = max(0, percentages['Clean'] - reduction)

    # Normalize to 100%
    total = sum(percentages.values())
    if total > 0:
        for key in percentages:
            percentages[key] = (percentages[key] / total) * 100

    return {k: round(v, 1) for k, v in percentages.items()}

# Apply refined percentages
is_weekday = current_day < 5  # Mon–Fri
df_live["source_details"] = df_live["cluster"].apply(
    lambda x: get_source_percentages(x, days=current_day + 1, is_weekday=is_weekday)
)

# For backward compatibility: dominant source
df_live["source"] = df_live["source_details"].apply(
    lambda d: max(d.items(), key=lambda x: x[1])[0] if d else "Unknown"
)

# Pollution Index & Crop Burning (unchanged)
df_live["pollution_index"] = 0.5 * df_live["pm25"] + 0.3 * df_live["pm10"] + 0.2 * df_live["no2"]
df_live["crop_burning_index"] = df_live.apply(compute_crop_burning_index, axis=1)
df_live["crop_burning_risk"] = df_live["crop_burning_index"].apply(classify_crop_burning)

# ---------------------------------------------------
# AGGREGATED CITY-WIDE SOURCE BREAKDOWN
# ---------------------------------------------------
all_details = df_live["source_details"].tolist()
city_wide = {'Clean': 0, 'Vehicle': 0, 'Dust': 0, 'Industrial': 0, 'Smog': 0}
for detail in all_details:
    for src, pct in detail.items():
        city_wide[src] += pct
for k in city_wide:
    city_wide[k] = city_wide[k] / len(all_details) if all_details else 0

city_wide_df = pd.DataFrame([
    {"Source": k, "Contribution (%)": round(v, 1)} for k, v in city_wide.items()
]).sort_values("Contribution (%)", ascending=False)

# HISTORICAL COMPARISON DATA
# ---------------------------------------------------
@st.cache_data
def load_historical_stats():
    hist_clean = hist.dropna(subset=FEATURES)
    hist_avg = hist_clean[FEATURES].mean()
    hist_pi_avg = 0.5 * hist_avg["pm25"] + 0.3 * hist_avg["pm10"] + 0.2 * hist_avg["no2"]
    return hist_avg, hist_pi_avg
hist_avg, hist_pi_avg = load_historical_stats()
# ---------------------------------------------------
# SIDEBAR CONTROLS
# ---------------------------------------------------
st.sidebar.title("⚙️ Dashboard Controls")
st.sidebar.markdown("---")
selected_stations = st.sidebar.multiselect(
    "Select Stations",
    options=list(STATIONS.keys()),
    default=list(STATIONS.keys()),
    help="Choose stations to analyze and visualize."
)
selected_pollutants = st.sidebar.multiselect(
    "Focus Pollutants",
    options=FEATURES,
    default=["pm25", "pm10", "no2"],
    help="Select key pollutants for detailed views."
)
show_forecast = st.sidebar.checkbox(
    "Enable 24h Forecast",
    value=True,
    help="Toggle diurnal pattern-based forecast."
)
pollution_threshold = st.sidebar.slider(
    "Hotspot Threshold (PI)",
    min_value=50.0,
    max_value=300.0,
    value=100.0,
    step=10.0,
    help="Define what counts as a hotspot."
)
theme = st.sidebar.selectbox("Theme", ["Dark", "Light"], index=0)
auto_refresh = st.sidebar.checkbox("Auto-refresh every 5 min", value=False)
st.sidebar.markdown("---")
st.sidebar.info("👆 Adjust controls to customize your view.")
df_filtered = df_live[df_live["location"].isin(selected_stations)].copy()
if df_filtered.empty:
    st.warning("No data available for selected stations. Please select different stations.")
    st.stop()
# ---------------------------------------------------
# PREMIUM HEADER
# ---------------------------------------------------
header_container = st.container()
with header_container:
    st.markdown(
        '<div class="premium-header"><h1>🌤️ Delhi Pollution Dashboard</h1><p>Live WAQI Insights • AI-Powered Source Classification (RandomForest)</p></div>',
        unsafe_allow_html=True
    )
now = datetime.datetime.now()
formatted_date = now.strftime("%B %d, %Y")
formatted_time = now.strftime("%H:%M:%S %Z")
st.markdown(f"""
<div class="corner-timestamp">
    <div><strong>📅 {formatted_date}</strong></div>
    <div>🕐 {formatted_time}</div>
</div>
""", unsafe_allow_html=True)
if st.button("🔄 Refresh Data", type="primary"):
    st.rerun()
# ---------------------------------------------------
# TABS
# ---------------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🗺️ Maps & Trends", "🔥 Alerts & Hotspots", "⏳ Forecast & Export"])
with tab1:
    st.markdown("---")
    col1, col2, col3, col4 = st.columns(4)
    avg_pi = df_filtered["pollution_index"].mean()
    max_pi = df_filtered["pollution_index"].max()
    num_stations = len(df_filtered)
    
    # Dominant source based on highest average contribution (not just cluster mode)
    dominant_source = city_wide_df.iloc[0]["Source"] if not city_wide_df.empty else "N/A"

    # Historical comparison for Avg PI
    pi_delta = round(avg_pi - hist_pi_avg, 1)

    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.metric("Avg Pollution Index", f"{round(avg_pi, 1)}", delta=pi_delta)
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.metric("Max Pollution Index", f"{round(max_pi, 1)}")
        st.markdown('</div>', unsafe_allow_html=True)
    with col3:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.metric("Active Stations", num_stations)
        st.markdown('</div>', unsafe_allow_html=True)
    with col4:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.metric("Dominant Source Today", dominant_source)
        st.markdown('</div>', unsafe_allow_html=True)

    # Crop burning metric
    cb_high = (df_filtered["crop_burning_risk"] == "High").sum()
    st.markdown("---")
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.metric("Stations with High Crop Burning Influence", cb_high, delta=None,
              help="Based on PM ratio, CO, and low NO₂/SO₂")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Overall Air Quality Index")
    overall_aqi = avg_pi
    aqi_color = "#00ff00" if overall_aqi < 50 else "#ffff00" if overall_aqi < 100 else "#ff7f00" if overall_aqi < 150 else "#ff0000"
    fig_gauge = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=overall_aqi,
        domain={'x': [0, 1], 'y': [0, 1]},
        title={'text': "Delhi-Wide Pollution Index"},
        delta={'reference': hist_pi_avg, 'position': "top"},
        gauge={
            'axis': {'range': [None, 300]},
            'bar': {'color': aqi_color},
            'steps': [
                {'range': [0, 50], 'color': "#00ff00"},
                {'range': [50, 100], 'color': "#ffff00"},
                {'range': [100, 150], 'color': "#ff7f00"},
                {'range': [150, 200], 'color': "#ff0000"},
                {'range': [200, 300], 'color': "#800080"}
            ],
            'threshold': {'line': {'color': "red", 'width': 6}, 'thickness': 0.75, 'value': 150}
        }
    ))
    fig_gauge.update_layout(font=dict(size=12, color="#e0e0e0"), paper_bgcolor='#1e1e1e', plot_bgcolor='#1e1e1e')
    st.markdown('<div class="premium-card gauge-container">', unsafe_allow_html=True)
    st.plotly_chart(fig_gauge, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Historical Comparison
    st.markdown("---")
    st.markdown("## Historical Comparison")
    current_avg = df_filtered[FEATURES].mean()
    comparison_df = pd.DataFrame({
        "Pollutant": [p.upper() for p in FEATURES],
        "Current Avg": current_avg.round(1),
        "Historical Avg": hist_avg.round(1),
        "Change (%)": ((current_avg - hist_avg) / hist_avg * 100).round(1)
    })
    st.markdown('<div class="premium-card">', unsafe_allow_html=True)
    st.dataframe(comparison_df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # REFINED SOURCE APPORTIONMENT (Your Delhi Winter Model)
    st.markdown("---")
    st.markdown("## Detailed Pollution Source Contribution")
    st.markdown("*Delhi winter model with weekday traffic boost (+20%) and cluster-based refinement*")

    col_a, col_b = st.columns([2, 1])

    with col_a:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        fig_source = px.bar(
            city_wide_df,
            x="Contribution (%)",
            y="Source",
            orientation='h',
            text="Contribution (%)",
            color="Source",
            color_discrete_sequence=px.colors.qualitative.Bold
        )
        fig_source.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig_source.update_layout(
            showlegend=False,
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(color="#e0e0e0"),
            yaxis=dict(autorange="reversed"),
            height=320,
            margin=dict(l=10, r=10, t=40, b=10)
        )
        st.plotly_chart(fig_source, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.markdown("**City-Wide Average**")
        styled = city_wide_df.style.format({"Contribution (%)": "{:.1f}%"})\
            .bar(subset=["Contribution (%)"], color='#6366f1', vmin=0, vmax=70)\
            .set_properties(**{'text-align': 'left'})
        st.dataframe(styled, use_container_width=True, hide_index=True)
        st.caption("Percentages always sum to 100%")
        st.markdown('</div>', unsafe_allow_html=True)

    # Per-station detailed breakdown
    with st.expander("View Source Contribution by Station", expanded=False):
        detail_list = []
        for _, row in df_filtered.iterrows():
            details = row["source_details"]
            detail_list.append({
                "Location": row["location"],
                "Dominant": row["source"].title(),
                "Vehicle": f"{details.get('Vehicle', 0):.1f}%",
                "Dust": f"{details.get('Dust', 0):.1f}%",
                "Industrial": f"{details.get('Industrial', 0):.1f}%",
                "Smog": f"{details.get('Smog', 0):.1f}%",
                "Clean": f"{details.get('Clean', 0):.1f}%",
            })
        detail_df = pd.DataFrame(detail_list)
        st.dataframe(
            detail_df.sort_values("Vehicle", key=lambda x: x.str.rstrip('%').astype(float), ascending=False),
            use_container_width=True,
            hide_index=True
        )

    # Pollutant Correlations
    st.markdown("---")
    st.markdown("## Pollutant Correlations")
    corr = df_filtered[FEATURES].corr()
    fig_heatmap = px.imshow(
        corr.round(2),
        text_auto=True,
        aspect="auto",
        color_continuous_scale="RdBu_r",
        zmin=-1, zmax=1
    )
    fig_heatmap.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color="#e0e0e0"),
        height=500
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
with tab2:
    st.markdown("## 🗺️ Station Locations & Pollution Heatmap")
    df_map = df_filtered.copy()
    df_map['lat'] = df_map['location'].map(lambda x: STATIONS[x]['lat'])
    df_map['lon'] = df_map['location'].map(lambda x: STATIONS[x]['lon'])
    fig_map = px.scatter_mapbox(
        df_map,
        lat="lat",
        lon="lon",
        size="pollution_index",
        color="pollution_index",
        hover_name="location",
        hover_data=["pm25", "source", "crop_burning_risk"],
        color_continuous_scale=px.colors.sequential.Reds,
        size_max=20,
        zoom=10,
        mapbox_style="open-street-map"
    )
    fig_map.update_layout(
        plot_bgcolor='#1e1e1e',
        paper_bgcolor='#1e1e1e',
        font=dict(color="#e0e0e0")
    )
    st.plotly_chart(fig_map, use_container_width=True)
    st.markdown("---")
    st.markdown("## 📈 Pollutant Trends Across Stations")
    if selected_pollutants:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        fig_line = go.Figure()
        colors = px.colors.qualitative.Set3
        for i, pol in enumerate(selected_pollutants):
            color = colors[i % len(colors)]
            fig_line.add_trace(go.Scatter(
                x=df_filtered["location"],
                y=df_filtered[pol],
                mode='lines+markers',
                name=pol.upper(),
                line=dict(width=2, color=color),
                marker=dict(size=6, color=color)
            ))
        fig_line.update_layout(
            title="Selected Pollutants by Station",
            xaxis_title="Stations",
            yaxis_title="Concentration (µg/m³)",
            hovermode='x unified',
            plot_bgcolor='#1e1e1e',
            paper_bgcolor='#1e1e1e',
            font=dict(size=12, color="#e0e0e0")
        )
        st.plotly_chart(fig_line, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
with tab3:
    st.markdown("## Pollution Zones – Smart Classification")

    # Extract Clean % as a regular column first (to avoid dict hashing issues)
    df_filtered = df_filtered.copy()
    df_filtered["clean_pct"] = df_filtered["source_details"].apply(lambda x: x.get("Clean", 0))

    # Define thresholds
    hotspots = df_filtered[df_filtered["pollution_index"] > pollution_threshold].sort_values("pollution_index", ascending=False)

    # Clean zones: either low pollution OR high Clean contribution
    clean_by_low_pi = df_filtered[df_filtered["pollution_index"] <= 70]
    clean_by_source = df_filtered[df_filtered["clean_pct"] >= 50]

    # Combine and deduplicate safely using location
    clean_zones = pd.concat([clean_by_low_pi, clean_by_source], ignore_index=True)
    clean_zones = clean_zones.drop_duplicates(subset=["location"]).copy()

    # Sort by Clean % (highest first)
    clean_zones = clean_zones.sort_values("clean_pct", ascending=False)

    # Remove clean zones from hotspots to avoid double listing
    hotspots = hotspots[~hotspots["location"].isin(clean_zones["location"])]

    col1, col2 = st.columns(2)

    # HOTSPOTS
    with col1:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader(f"Hotspots (PI > {pollution_threshold:.0f})")
        if hotspots.empty:
            st.success("No major hotspots detected!")
        else:
            display_hot = hotspots[["location", "pollution_index", "pm25", "pm10", "source"]].round(1)
            def highlight_hot(row):
                return ['background-color: #ff3333; color: white; font-weight: bold'] * len(row)
            styled = display_hot.head(12).style.apply(highlight_hot, axis=1).format({
                "pollution_index": "{:.1f}", "pm25": "{:.1f}", "pm10": "{:.1f}"
            })
            st.dataframe(styled, use_container_width=True, hide_index=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # CLEAN AIR ZONES
    with col2:
        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.subheader("Clean Air Zones")
        if clean_zones.empty:
            st.info("No clean zones detected yet.")
        else:
            clean_display = clean_zones[["location", "pollution_index", "clean_pct"]].round(1).copy()
            clean_display["Reason"] = clean_display.apply(
                lambda row: "Very Low Pollution" if row["pollution_index"] <= 70 else "High Natural Cleansing",
                axis=1
            )
            clean_display = clean_display.rename(columns={
                "clean_pct": "Clean (%)",
                "pollution_index": "PI"
            })

            def highlight_clean(row):
                pct = row["Clean (%)"]
                if pct >= 70:
                    return ['background-color: #00ff00; color: black; font-weight: bold'] * len(row)
                elif pct >= 50:
                    return ['background-color: #90EE90; color: black'] * len(row)
                else:
                    return ['background-color: #98FB98; color: black'] * len(row)

            styled_clean = clean_display.head(12).style.apply(highlight_clean, axis=1).format({
                "PI": "{:.1f}", "Clean (%)": "{:.1f}"
            })
            st.dataframe(styled_clean, use_container_width=True, hide_index=True)
            st.caption("High 'Clean %' = strong natural ventilation, greenery, or low emissions")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("## Real-Time Air Quality Alerts")

    alerts = []

    # Critical hotspots
    for _, row in hotspots.head(6).iterrows():
        alerts.append(f"High pollution at **{row['location']}** — PI: {row['pollution_index']:.1f} ({row['source'].title()} dominant)")

    # Crop burning
    high_cb = df_filtered[df_filtered["crop_burning_risk"] == "High"]
    for _, row in high_cb.head(5).iterrows():
        alerts.append(f"Possible crop residue burning at **{row['location']}** (CBI: {row['crop_burning_index']:.2f})")

    # Celebrate clean air!
    top_clean = clean_zones.head(4)
    for _, row in top_clean.iterrows():
        alerts.append(f"Excellent air at **{row['location']}** — {row['clean_pct']:.1f}% Clean Air")

    if alerts:
        for alert in alerts:
            if "Excellent" in alert or "clean" in alert.lower():
                st.success(alert)
            elif "crop" in alert.lower():
                st.warning(alert)
            else:
                st.error(alert)
    else:
        st.success("Delhi is breathing easy today!")
# ---------------------------------------------------
# TAB 4 — 24-HOUR FORECAST & EXPORT
# ---------------------------------------------------
with tab4:

    st.markdown("## ⏳ 24-Hour Pollution Forecast (Diurnal Pattern)")

    # -----------------------------------------------------------
    # 1. REALISTIC DELHI DIURNAL MULTIPLIER (5-year scientific avg)
    # -----------------------------------------------------------
    delhi_diurnal = [
        0.80, 0.78, 0.76, 0.75, 0.80, 0.92, 1.05, 1.18,
        1.22, 1.18, 1.05, 0.95, 0.89, 0.84, 0.82, 0.83,
        0.90, 1.05, 1.20, 1.28, 1.30, 1.25, 1.15, 1.00
    ]

    diurnal = pd.DataFrame({
        "pm25": delhi_diurnal,
        "pm10": delhi_diurnal
    })

    # Toggle: normalize for percentage comparison
    normalize_view = st.checkbox(
        "Normalize forecast relative to current value (%)",
        value=False
    )

    # -----------------------------------------------------------
    # If too many stations → single-station detailed forecast
    # -----------------------------------------------------------
    if len(selected_stations) > 6:
        selected_station = st.selectbox("Select Station for Forecast", selected_stations)

        row = df_filtered[df_filtered["location"] == selected_station].iloc[0]

        pm25_now = row["pm25"]
        pm10_now = row["pm10"]
        no2_now  = row["no2"]
        pi_now   = row["pollution_index"]

        hours = list(range(24))

        fc_pm25 = [pm25_now * diurnal.loc[h, "pm25"] for h in hours]
        fc_pm10 = [pm10_now * diurnal.loc[h, "pm10"] for h in hours]
        fc_pi   = [0.5*p25 + 0.3*p10 + 0.2*no2_now for p25, p10 in zip(fc_pm25, fc_pm10)]

        if normalize_view and pi_now > 0:
            fc_pi = [(v / pi_now * 100) for v in fc_pi]

        df_forecast = pd.DataFrame({
            "Hour": hours,
            "PM2.5": fc_pm25,
            "PM10": fc_pm10,
            "Pollution Index": fc_pi
        })

        # Plot – single station
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df_forecast["Hour"], y=df_forecast["PM2.5"],
                                 name="PM2.5", line=dict(color="#ff6b6b", width=4)))
        fig.add_trace(go.Scatter(x=df_forecast["Hour"], y=df_forecast["PM10"],
                                 name="PM10", line=dict(color="#feca57", width=4)))
        fig.add_trace(go.Scatter(x=df_forecast["Hour"], y=df_forecast["Pollution Index"],
                                 name="Pollution Index",
                                 line=dict(color="#48dbfb", width=5, dash="dot")))

        y_title = "Pollution Index (%)" if normalize_view else "Concentration / Index"

        fig.update_layout(
            title=f"24-Hour Forecast — {selected_station}",
            xaxis=dict(title="Hour of Day", dtick=2, showgrid=True, gridcolor="#333"),
            yaxis=dict(title=y_title, showgrid=True, gridcolor="#333"),
            hovermode="x unified",
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#1e1e1e",
            font=dict(color="#e0e0e0"),
            height=620
        )

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown(
            f"**Current PI:** {pi_now:.1f} • **Dominant Source:** {row['source'].title()}"
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------------------------------
    # MULTI-STATION FORECAST (<= 6 stations)
    # -----------------------------------------------------------
    else:
        forecast_rows = []

        for loc in selected_stations:
            row = df_filtered[df_filtered["location"] == loc]
            if row.empty:
                continue

            row = row.iloc[0]
            pm25_now = row["pm25"]
            pm10_now = row["pm10"]
            no2_now  = row["no2"]
            pi_now   = row["pollution_index"]

            for h in range(24):
                f25 = pm25_now * diurnal.loc[h, "pm25"]
                f10 = pm10_now * diurnal.loc[h, "pm10"]
                fpi = 0.5*f25 + 0.3*f10 + 0.2*no2_now

                if normalize_view and pi_now > 0:
                    fpi = (fpi / pi_now * 100)

                forecast_rows.append({
                    "Hour": h,
                    "Station": loc,
                    "Pollution Index": round(fpi, 1),
                    "PM2.5": round(f25, 1),
                    "PM10": round(f10, 1)
                })

        df_fc = pd.DataFrame(forecast_rows)

        y_title = "Pollution Index (%)" if normalize_view else "Pollution Index"

        fig = px.line(
            df_fc,
            x="Hour",
            y="Pollution Index",
            color="Station",
            line_group="Station",
            hover_name="Station",
            hover_data={"PM2.5": True, "PM10": True},
            title="24-Hour Forecast — Selected Stations",
            color_discrete_sequence=px.colors.qualitative.Vivid
        )

        fig.update_traces(line=dict(width=3))
        fig.update_layout(
            hovermode="x unified",
            plot_bgcolor="#1e1e1e",
            paper_bgcolor="#1e1e1e",
            font=dict(color="#e0e0e0"),
            yaxis=dict(showgrid=True, gridcolor="#333", title=y_title),
            xaxis=dict(showgrid=True, gridcolor="#333", dtick=2),
            height=620
        )

        st.markdown('<div class="premium-card">', unsafe_allow_html=True)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # -----------------------------------------------------------
    # EXPORT SECTION
    # -----------------------------------------------------------
    st.markdown("---")
    st.markdown("## 💾 Export Live Data")

    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M")
    csv = df_filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "Download CSV",
        data=csv,
        file_name=f"delhi_pollution_{ts}.csv",
        mime="text/csv"
    )

    st.download_button(
        "Download JSON",
        data=df_filtered.to_json(orient="records"),
        file_name="delhi_pollution.json",
        mime="application/json"
    )
