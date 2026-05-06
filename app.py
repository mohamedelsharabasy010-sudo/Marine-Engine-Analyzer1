import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# 1. إعدادات الصفحة (Design Config)
st.set_page_config(page_title="Marine Engine Intelligence", layout="wide")

# تخصيص المظهر بـ CSS بسيط
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    </style>
    """, unsafe_allow_html=True)

# 2. الواجهة الرئيسية
st.title("🚢 Marine Engine Diagnostic & Predictive System")
st.subheader("Real-time Performance Monitoring & Fault Prediction")
st.markdown("---")

# 3. القائمة الجانبية (Sidebar) - مقسمة لمجموعات
st.sidebar.header("🕹️ System Controls")

with st.sidebar.expander("Operational Parameters", expanded=True):
    rpm = st.slider("Engine Speed (RPM)", 0, 3500, 1500)
    load = st.slider("Engine Load (%)", 0, 100, 70)

with st.sidebar.expander("Sensor Data", expanded=True):
    temp = st.slider("Coolant Temp (°C)", 20, 130, 85)
    vibration = st.slider("Vibration (mm/s)", 0.0, 25.0, 4.5)

# 4. المحرك البرمجي (Calculation Engine)
# معادلات هندسية للمحاكاة (Simulation Formulas)
power = (rpm * load * 0.105) / 10 if rpm > 0 else 0
torque = (power * 9550) / rpm if rpm > 500 else 0
fuel_consumption = (rpm * load) / 6000 # لتر/ساعة تقريباً
hourly_cost = fuel_consumption * 1.5 # فرضاً السعر 1.5 دولار للتر

# معادلة توقع عمر الزيت (Predictive Logic)
# بتقل مع زيادة الحرارة والاهتزاز
oil_degradation = (temp * 0.3) + (vibration * 1.5) + (rpm * 0.005)
oil_life = max(0, min(100, 100 - (oil_degradation - 15)))

# 5. نظام الأمان والإنذار (Safety Interlocks)
if temp > 110 or vibration > 20:
    alarm_status = "🚨 CRITICAL: SHUTDOWN REQUIRED"
    alarm_color = "#ff4b4b" # أحمر
elif temp > 95 or vibration > 15:
    alarm_status = "⚠️ WARNING: Abnormal Conditions"
    alarm_color = "#ffa500" # برتقالي
else:
    alarm_status = "✅ NORMAL: System Optimal"
    alarm_color = "#28a745" # أخضر

# 6. عرض النتائج (Dashboard Metrics)
col1, col2, col3, col4 = st.columns(4)
with col1: st.metric("Output Power", f"{power:.1f} kW")
with col2: st.metric("Est. Torque", f"{torque:.1f} Nm")
with col3: st.metric("Oil Life", f"{oil_life:.1f}%")
with col4: st.metric("Hourly Cost", f"${hourly_cost:.2f}")

st.markdown(f"""
    <div style="background-color:{alarm_color}; padding:15px; border-radius:10px; text-align:center;">
        <h2 style="color:white; margin:0;">{alarm_status}</h2>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# 7. الرسوم البيانية التفاعلية
row2_left, row2_right = st.columns(2)

with row2_left:
    st.write("### 🌡️ Thermal & Mechanical Gauges")
    fig_gauge = go.Figure()
    # عداد الحرارة
    fig_gauge.add_trace(go.Indicator(
        mode = "gauge+number", value = temp,
        domain = {'x': [0, 0.45], 'y': [0, 1]},
        title = {'text': "Temp (°C)"},
        gauge = {'axis': {'range': [20, 130]},
                 'steps': [{'range': [20, 90], 'color': "lightgray"}, {'range': [90, 110], 'color': "orange"}, {'range': [110, 130], 'color': "red"}]}))
    # عداد الاهتزاز
    fig_gauge.add_trace(go.Indicator(
        mode = "gauge+number", value = vibration,
        domain = {'x': [0.55, 1], 'y': [0, 1]},
        title = {'text': "Vibration"},
        gauge = {'axis': {'range': [0, 25]},
                 'steps': [{'range': [0, 12], 'color': "lightgray"}, {'range': [12, 18], 'color': "orange"}, {'range': [18, 25], 'color': "red"}]}))
    st.plotly_chart(fig_gauge, use_container_width=True)

with row2_right:
    st.write("### 📊 Specific Fuel Consumption (Efficiency)")
    # رسم منحنى SFC
    x_range = np.linspace(500, 3500, 100)
    y_curve = 240 - (x_range * 0.04) + (x_range**2 * 0.000008) # منحنى هندسي نموذجي
    
    current_sfc = 240 - (rpm * 0.04) + (rpm**2 * 0.000008)
    
    fig_sfc = go.Figure()
    fig_sfc.add_trace(go.Scatter(x=x_range, y=y_curve, name="Efficiency Curve", line=dict(color='blue', width=3)))
    fig_sfc.add_trace(go.Scatter(x=[rpm], y=[current_sfc], mode='markers+text', name="Current Point",
                                 text=["Operating Point"], textposition="top center",
                                 marker=dict(color='red', size=15, symbol='diamond')))
    fig_sfc.update_layout(xaxis_title="RPM", yaxis_title="SFC (g/kWh)", height=400)
    st.plotly_chart(fig_sfc, use_container_width=True)

# 8. سجل البيانات (Event Logging)
st.markdown("### 📋 System Operations Log")
log_data = pd.DataFrame({
    "Time": [datetime.now().strftime("%H:%M:%S")],
    "RPM": [rpm],
    "Load (%)": [load],
    "Status": [alarm_status.split(':')[-1]]
})
st.table(log_data)

st.success("System is running stable on Streamlit Cloud. All interlocks active.")