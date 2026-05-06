import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime

# 1. إعدادات الصفحة
st.set_page_config(page_title="Marine Engine Intelligence", layout="wide")

# 2. الواجهة الرئيسية
st.title("🚢 Marine Engine Diagnostic & Predictive System")
st.subheader("Real-time Performance Monitoring & Fault Prediction")
st.markdown("---")

# 3. القائمة الجانبية (Sidebar)
st.sidebar.header("🕹️ System Controls")

with st.sidebar.expander("Operational Parameters", expanded=True):
    rpm = st.slider("Engine Speed (RPM)", 0, 3500, 1500)
    load = st.slider("Engine Load (%)", 0, 100, 70)

with st.sidebar.expander("Sensor Data", expanded=True):
    temp = st.slider("Coolant Temp (°C)", 20, 130, 85)
    vibration = st.slider("Vibration (mm/s)", 0.0, 25.0, 4.5)

# 4. المحرك البرمجي (Calculations)
power = (rpm * load * 0.105) / 10 if rpm > 0 else 0
torque = (power * 9550) / rpm if rpm > 500 else 0
fuel_consumption = (rpm * load) / 6000 
hourly_cost = fuel_consumption * 1.5 

oil_degradation = (temp * 0.3) + (vibration * 1.5) + (rpm * 0.005)
oil_life = max(0, min(100, 100 - (oil_degradation - 15)))

# 5. نظام الأمان والإنذار
if temp > 110 or vibration > 20:
    alarm_status = "🚨 CRITICAL: SHUTDOWN REQUIRED"
    alarm_color = "red"
elif temp > 95 or vibration > 15:
    alarm_status = "⚠️ WARNING: Abnormal Conditions"
    alarm_color = "orange"
else:
    alarm_status = "✅ NORMAL: System Optimal"
    alarm_color = "green"

# 6. عرض النتائج (Metrics) - هنا شلنا التنسيق اللي كان عامل مشكلة
col1, col2, col3, col4 = st.columns(4)
col1.metric("Output Power", f"{power:.1f} kW")
col2.metric("Est. Torque", f"{torque:.1f} Nm")
col3.metric("Oil Life", f"{oil_life:.1f}%")
col4.metric("Hourly Cost", f"${hourly_cost:.2f}")

# تنبيه الحالة بلون واضح
st.markdown(f"### Current Status: :{alarm_color}[{alarm_status}]")
st.markdown("---")

# 7. الرسوم البيانية التفاعلية
row2_left, row2_right = st.columns(2)

with row2_left:
    st.write("### 🌡️ Thermal & Mechanical Gauges")
    fig_gauge = go.Figure()
    fig_gauge.add_trace(go.Indicator(
        mode = "gauge+number", value = temp,
        domain = {'x': [0, 0.45], 'y': [0, 1]},
        title = {'text': "Temp (°C)"},
        gauge = {'axis': {'range': [20, 130]},
                 'steps': [{'range': [20, 90], 'color': "lightgray"}, {'range': [90, 110], 'color': "orange"}, {'range': [110, 130], 'color': "red"}]}))
    fig_gauge.add_trace(go.Indicator(
        mode = "gauge+number", value = vibration,
        domain = {'x': [0.55, 1], 'y': [0, 1]},
        title = {'text': "Vibration"},
        gauge = {'axis': {'range': [0, 25]},
                 'steps': [{'range': [0, 12], 'color': "lightgray"}, {'range': [12, 18], 'color': "orange"}, {'range': [18, 25], 'color': "red"}]}))
    st.plotly_chart(fig_gauge, use_container_width=True)

with row2_right:
    st.write("### 📊 Specific Fuel Consumption (Efficiency)")
    x_range = np.linspace(500, 3500, 100)
    y_curve = 240 - (x_range * 0.04) + (x_range**2 * 0.000008) 
    current_sfc = 240 - (rpm * 0.04) + (rpm**2 * 0.000008)
    
    fig_sfc = go.Figure()
    fig_sfc.add_trace(go.Scatter(x=x_range, y=y_curve, name="Efficiency Curve", line=dict(color='blue', width=3)))
    fig_sfc.add_trace(go.Scatter(x=[rpm], y=[current_sfc], mode='markers+text', name="Current Point",
                                 text=["Operating Point"], textposition="top center",
                                 marker=dict(color='red', size=15, symbol='diamond')))
    fig_sfc.update_layout(xaxis_title="RPM", yaxis_title="SFC (g/kWh)", height=400)
    st.plotly_chart(fig_sfc, use_container_width=True)

# 8. سجل البيانات
st.markdown("### 📋 System Operations Log")
log_data = pd.DataFrame({
    "Time": [datetime.now().strftime("%H:%M:%S")],
    "RPM": [rpm],
    "Load (%)": [load],
    "Status": [alarm_status]
})
st.table(log_data)