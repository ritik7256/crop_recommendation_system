# import streamlit as st
# import pandas as pd
# import numpy as np
# import pickle
# import requests
# import plotly.express as px

# # -----------------------------
# # PAGE CONFIG
# # -----------------------------
# st.set_page_config(
#     page_title="AI Crop Recommendation System",
#     page_icon="🌱",
#     layout="wide"
# )

# # -----------------------------
# # LOAD MODEL
# # -----------------------------
# model = pickle.load(open("model.pkl", "rb"))

# # -----------------------------
# # CUSTOM CSS
# # -----------------------------
# st.markdown("""
# <style>
# .main {
#     background-color: #f4fff4;
# }

# .stButton>button {
#     background-color: green;
#     color: white;
#     border-radius: 10px;
#     height: 3em;
#     width: 100%;
#     font-size: 18px;
# }

# .big-font {
#     font-size: 50px !important;
#     font-weight: bold;
#     color: green;
# }

# .card {
#     padding: 20px;
#     border-radius: 15px;
#     background: white;
#     box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
# }
# </style>
# """, unsafe_allow_html=True)

# # -----------------------------
# # TITLE
# # -----------------------------
# st.markdown(
#     '<p class="big-font">🌱 Smart Crop Recommendation System</p>',
#     unsafe_allow_html=True
# )

# st.write("AI-powered agriculture assistant using Machine Learning")

# # -----------------------------
# # SIDEBAR
# # -----------------------------
# st.sidebar.header("Enter Soil Details")

# N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)
# P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)
# K = st.sidebar.slider("Potassium (K)", 0, 205, 50)
# ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 6.5)

# city = st.sidebar.text_input("Enter City", "Lucknow")

# # -----------------------------
# # WEATHER API
# # -----------------------------
# API_KEY = "8d8fb13863134dc18fd213011262205"

# url = f"http://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}"

# response = requests.get(url)

# data = response.json()

# temperature = data["current"]["temp_c"]
# humidity = data["current"]["humidity"]

# # Simulated rainfall
# rainfall = 80

# # -----------------------------
# # WEATHER DISPLAY
# # -----------------------------
# col1, col2, col3 = st.columns(3)

# with col1:
#     st.metric("🌡 Temperature", f"{temperature} °C")

# with col2:
#     st.metric("💧 Humidity", f"{humidity}%")

# with col3:
#     st.metric("🌧 Rainfall", f"{rainfall} mm")

# # -----------------------------
# # CHART
# # -----------------------------
# soil_data = pd.DataFrame({
#     "Nutrient": ["Nitrogen", "Phosphorus", "Potassium"],
#     "Value": [N, P, K]
# })

# fig = px.bar(
#     soil_data,
#     x="Nutrient",
#     y="Value",
#     title="Soil Nutrient Analysis"
# )

# st.plotly_chart(fig, use_container_width=True)

# # -----------------------------
# # PREDICTION
# # -----------------------------
# if st.button("Recommend Crop"):

#     features = np.array([[N, P, K,
#                           temperature,
#                           humidity,
#                           ph,
#                           rainfall]])

#     prediction = model.predict(features)

#     probabilities = model.predict_proba(features)

#     top3 = np.argsort(probabilities[0])[-3:][::-1]

#     crops = model.classes_

#     st.success(f"✅ Best Crop: {prediction[0].upper()}")

#     st.subheader("Top Recommendations")

#     for i in top3:
#         st.write(
#             f"🌱 {crops[i]} — {probabilities[0][i]*100:.2f}%"
#         )

#     st.subheader("Smart Farming Insight")

#     if humidity > 70:
#         st.info("High humidity detected. Suitable for rice cultivation.")

#     if ph < 5:
#         st.warning("Soil is acidic. Consider adding lime.")

#     if temperature > 35:
#         st.error("High temperature may affect sensitive crops.")


import streamlit as st
import pandas as pd
import numpy as np
import pickle
import requests
import plotly.express as px

from datetime import datetime, timedelta

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Smart Crop Recommendation",
    page_icon="🌱",
    layout="wide"
)

# =========================================================
# LOAD MODEL
# =========================================================

model = pickle.load(open("model.pkl", "rb"))

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

.main {
    background-color: #f4fff4;
}

.title {
    font-size: 50px;
    color: #2E8B57;
    font-weight: bold;
}

.subtitle {
    font-size: 20px;
    color: gray;
}

.stButton>button {
    background-color: #2E8B57;
    color: white;
    font-size: 20px;
    border-radius: 12px;
    height: 60px;
    width: 100%;
    border: none;
}

.stButton>button:hover {
    background-color: #1f6b45;
    color: white;
}

.metric-card {
    padding: 20px;
    border-radius: 15px;
    background: white;
    box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# CROP INFORMATION
# =========================================================

crop_info = {

    "rice": {
        "hindi": "चावल",
        "fertilizer": "Urea + DAP",
        "profit": "₹65,000 - ₹90,000 per acre"
    },

    "maize": {
        "hindi": "मक्का",
        "fertilizer": "NPK 20-20-20",
        "profit": "₹40,000 - ₹60,000 per acre"
    },

    "cotton": {
        "hindi": "कपास",
        "fertilizer": "Potash Rich Fertilizer",
        "profit": "₹70,000 - ₹1,20,000 per acre"
    },

    "wheat": {
        "hindi": "गेहूं",
        "fertilizer": "Urea",
        "profit": "₹50,000 - ₹80,000 per acre"
    },

    "coffee": {
        "hindi": "कॉफी",
        "fertilizer": "Organic Compost",
        "profit": "₹1,00,000+ per acre"
    },

    "mungbean": {
        "hindi": "मूंग",
        "fertilizer": "Bio Fertilizer",
        "profit": "₹35,000 - ₹60,000 per acre"
    },

    "lentil": {
        "hindi": "मसूर",
        "fertilizer": "DAP",
        "profit": "₹40,000 - ₹70,000 per acre"
    },

    "pomegranate": {
        "hindi": "अनार",
        "fertilizer": "Organic Manure",
        "profit": "₹1,50,000+ per acre"
    }
}

# =========================================================
# WEATHER API
# =========================================================

API_KEY = "8d8fb13863134dc18fd213011262205"

# =========================================================
# WEATHER FUNCTION
# =========================================================

def get_weather_data(location):

    temperatures = []
    humidities = []
    rainfalls = []

    weather_history = []

    # Last 30 Days Historical Data
    for i in range(1, 31):

        date = datetime.now() - timedelta(days=i)

        formatted_date = date.strftime("%Y-%m-%d")

        url = (
            f"http://api.weatherapi.com/v1/history.json?"
            f"key={API_KEY}&q={location}&dt={formatted_date}"
        )

        try:

            response = requests.get(url)

            data = response.json()

            # Invalid location handling
            if "forecast" not in data:
                continue

            day = data["forecast"]["forecastday"][0]["day"]

            temp = day.get("avgtemp_c", 0)
            humidity = day.get("avghumidity", 0)
            rainfall = day.get("totalprecip_mm", 0)

            temperatures.append(temp)
            humidities.append(humidity)
            rainfalls.append(rainfall)

            weather_history.append({
                "Date": formatted_date,
                "Temperature": temp,
                "Humidity": humidity,
                "Rainfall": rainfall
            })

        except:
            continue

    # Safety check
    if len(temperatures) == 0:
        return 0, 0, 0, pd.DataFrame()

    avg_temp = sum(temperatures) / len(temperatures)
    avg_humidity = sum(humidities) / len(humidities)

    # Average rainfall
    avg_rainfall = sum(rainfalls) / len(rainfalls)

    weather_df = pd.DataFrame(weather_history)

    return avg_temp, avg_humidity, avg_rainfall, weather_df

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<p class="title">🌱 AI Smart Crop Recommendation System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">AI-powered agricultural advisory system using Machine Learning</p>',
    unsafe_allow_html=True
)

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🌾 Enter Soil Details")

district = st.sidebar.text_input("District / City", "Lucknow")

state = st.sidebar.text_input("State", "Uttar Pradesh")

N = st.sidebar.slider("Nitrogen (N)", 0, 140, 50)

P = st.sidebar.slider("Phosphorus (P)", 0, 145, 50)

K = st.sidebar.slider("Potassium (K)", 0, 205, 50)

ph = st.sidebar.slider("Soil pH", 0.0, 14.0, 6.5)

location = f"{district}, {state}"

# =========================================================
# FETCH WEATHER
# =========================================================

with st.spinner("Fetching historical weather data..."):

    temperature, humidity, rainfall, weather_df = get_weather_data(location)

# =========================================================
# WEATHER METRICS
# =========================================================

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🌡 Avg Temperature", f"{temperature:.2f} °C")

with col2:
    st.metric("💧 Avg Humidity", f"{humidity:.2f}%")

with col3:
    st.metric("🌧 Avg Rainfall", f"{rainfall:.2f} mm")

# =========================================================
# WEATHER CHART
# =========================================================

st.subheader("🌦 Weather Trend Analysis (Last 30 Days)")

if not weather_df.empty:

    fig_weather = px.line(
        weather_df,
        x="Date",
        y=["Temperature", "Humidity", "Rainfall"],
        markers=True,
        title="Historical Weather Analysis"
    )

    st.plotly_chart(fig_weather, use_container_width=True)

# =========================================================
# SOIL ANALYSIS CHART
# =========================================================

st.subheader("🧪 Soil Nutrient Analysis")

soil_data = pd.DataFrame({
    "Nutrient": ["Nitrogen", "Phosphorus", "Potassium"],
    "Value": [N, P, K]
})

fig = px.bar(
    soil_data,
    x="Nutrient",
    y="Value",
    color="Nutrient",
    text="Value",
    title="Soil Nutrient Levels"
)

st.plotly_chart(fig, use_container_width=True)

# =========================================================
# PREDICTION BUTTON
# =========================================================

if st.button("🌱 Recommend Crop"):

    features = np.array([[
        N,
        P,
        K,
        temperature,
        humidity,
        ph,
        rainfall
    ]])

    prediction = model.predict(features)

    probabilities = model.predict_proba(features)

    top3 = np.argsort(probabilities[0])[-3:][::-1]

    crops = model.classes_

    st.success(
        f"✅ Best Crop Recommendation: {prediction[0].upper()}"
    )

    # =====================================================
    # TOP 3 RECOMMENDATIONS
    # =====================================================

    st.subheader("🏆 Top 3 Crop Recommendations")

    for i in top3:

        crop = crops[i]

        confidence = probabilities[0][i] * 100

        info = crop_info.get(crop, {})

        hindi_name = info.get("hindi", "N/A")

        fertilizer = info.get("fertilizer", "N/A")

        profit = info.get("profit", "N/A")

        st.markdown(f"""
        ---
        ## 🌱 {crop.upper()} ({hindi_name})

        ✅ Confidence Score:
        **{confidence:.2f}%**

        🧪 Recommended Fertilizer:
        **{fertilizer}**

        💰 Estimated Profit:
        **{profit}**
        """)

    # =====================================================
    # SMART INSIGHTS
    # =====================================================

    st.subheader("📊 Smart Farming Insights")

    if rainfall > 5:
        st.success(
            "Good rainfall conditions detected for farming."
        )

    if humidity > 70:
        st.info(
            "High humidity detected. Suitable for rice cultivation."
        )

    if ph < 5:
        st.warning(
            "Soil is acidic. Consider adding lime."
        )

    if ph > 8:
        st.warning(
            "Soil is alkaline. Use organic compost."
        )

    if temperature > 35:
        st.error(
            "High temperature may affect sensitive crops."
        )

    if N < 40:
        st.warning(
            "Nitrogen level is low. Use nitrogen-rich fertilizers."
        )

    if P < 40:
        st.warning(
            "Phosphorus is low. Root growth may be affected."
        )

    if K < 40:
        st.warning(
            "Potassium is low. Crop quality may reduce."
        )

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    "🌾 Developed using Machine Learning, Streamlit, Weather API & Data Analytics"
)