import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
import time
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Marine Engine Digital Twin", layout="wide")

# 2. العنوان الرئيسي
st.title("⚓ Marine Engine Digital Twin & Predictive Analytics")
st.markdown("---")

# 3. القائمة الجانبية والإعدادات
st.sidebar.header("⚙️ Engine Configuration")
engine_type = st.sidebar.selectbox(
    "Select Engine Category",
    ["Low-Speed 2-Stroke Diesel", "Medium-Speed 4-Stroke Diesel", "High-Speed Gasoline Outboard"]
)

# وضع المحاكاة التلقائية (الـ AI Simulator)
auto_sim = st.sidebar.toggle("🚀 Start Real-time Simulation")

# تعريف حدود التشغيل بناءً على نوع المحرك (Logic Database)
limits = {
    "Low-Speed 2-Stroke Diesel": {"max_rpm": 500, "safe_temp": 85, "crit_vibe": 15, "co2_fact": 2.6},
    "Medium-Speed 4-Stroke Diesel": {"max_rpm": 2500, "safe_temp": 100, "crit_vibe": 18, "co2_fact": 3.1},
    "High-Speed Gasoline Outboard": {"max_rpm": 6000, "safe_temp": 110, "crit_vibe": 22, "co2_fact": 2.3}
}
spec = limits[engine_type]

# معالجة المدخلات
if auto_sim:
    t = time.time()
    rpm = int(spec["max_rpm"] * (0.5 + 0.3 * np.sin(t/5)))
    load = int(50 + 40 * np.sin(t/7))
    temp = int(spec["safe_temp"] * (0.8 + 0.1 * np.cos(t/10)))
    vibration = 5.0 + 2.0 * np.sin(t/3)
else:
    rpm = st.sidebar.slider("Engine Speed (RPM)", 0, spec["max_rpm"], int(spec["max_rpm"]*0.7))
    load = st.sidebar.slider("Engine Load (%)", 0, 100, 75)
    temp = st.sidebar.slider("Coolant Temp (°C)", 20, 140, 85)
    vibration = st.sidebar.slider("Vibration (mm/s)", 0.0, 30.0, 4.5)

# 4. محرك الحسابات الذكي (AI & Engineering Math)
power = (rpm * load * 0.12) / 10 if rpm > 0 else 0
fuel_rate = (rpm * load) / 5500 
co2_emissions = fuel_rate * spec["co2_fact"]
# معادلة توقع عمر الزيت بناءً على الإجهاد الحراري والميكانيكي
oil_health = max(0, min(100, 100 - ((temp * 0.25) + (vibration * 1.5) - 10)))

# 5. عرض المؤشرات الرقمية (KPIs)
m1, m2, m3, m4 = st.columns(4)
m1.metric("Output Power", f"{power:.1f} kW")
m2.metric("Oil Health Score", f"{oil_health:.1f}%")
m3.metric("Fuel Rate", f"{fuel_rate:.2f} L/h")
m4.metric("CO2 Emissions", f"{co2_emissions:.2f} kg/h")

# 6. نظام التنبيهات الذكي
if vibration > spec["crit_vibe"]:
    st.error(f"🛑 CRITICAL VIBRATION: Possible Resonance detected at {rpm} RPM!")
elif temp > spec["safe_temp"]:
    st.warning("⚠️ THERMAL ALERT: Cooling efficiency below threshold.")
else:
    st.success(f"✅ SYSTEM STABLE: {engine_type} operating normally.")

st.markdown("---")

# 7. الرسوم البيانية التفاعلية
col_a, col_b = st.columns(2)

with col_a:
    st.subheader("📟 Live Sensor Data")
    fig = go.Figure()
    fig.add_trace(go.Indicator(
        mode = "gauge+number", value = temp, title = {'text': "Temp (°C)"},
        domain = {'x': [0, 0.45], 'y': [0, 1]},
        gauge = {'axis': {'range': [20, 140]}, 'steps': [{'range': [20, spec["safe_temp"]], 'color': "green"}, {'range': [spec["safe_temp"], 140], 'color': "red"}]}))
    fig.add_trace(go.Indicator(
        mode = "gauge+number", value = vibration, title = {'text': "Vibration (mm/s)"},
        domain = {'x': [0.55, 1], 'y': [0, 1]},
        gauge = {'axis': {'range': [0, 30]}, 'steps': [{'range': [0, spec["crit_vibe"]], 'color': "blue"}, {'range': [spec["crit_vibe"], 30], 'color': "orange"}]}))
    st.plotly_chart(fig, use_container_width=True)

with col_b:
    st.subheader("📊 Performance & Efficiency Map")
    x_range = np.linspace(0, spec["max_rpm"], 100)
    # معادلة كفاءة الوقود النوعية (BSFC)
    y_curve = 250 - (x_range * 0.05) + (x_range**2 * 0.00001)
    curr_y = 250 - (rpm * 0.05) + (rpm**2 * 0.00001)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=x_range, y=y_curve, name="Efficiency Curve", line=dict(color='yellow', width=3)))
    fig2.add_trace(go.Scatter(x=[rpm], y=[curr_y], mode='markers', name="Operating Point", marker=dict(color='red', size=15, symbol='x')))
    fig2.update_layout(xaxis_title="RPM", yaxis_title="SFC (g/kWh)")
    st.plotly_chart(fig2, use_container_width=True)

# 8. تحديث تلقائي للمحاكاة
if auto_sim:
    time.sleep(0.1)
    st.rerun()