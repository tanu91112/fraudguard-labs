import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import time
import json

# Import our modules
from fraudguard_app.components.fraud_detector import FraudDetector
from fraudguard_app.blockchain_sim.registry import RiskScoreRegistry, FraudFlagRegistry, AuditTrail
from fraudguard_app.data.data_generator import generate_transaction_stream

# Page config
st.set_page_config(
    page_title="FraudGuard Labs",
    page_icon="🛡️",
    layout="wide"
)

# Custom CSS for cyberpunk/neon theme
st.markdown("""
<style>
    :root {
        --background-color: #0a0e17;
        --card-background: #121826;
        --primary-color: #00f5ff;
        --secondary-color: #ff00e6;
        --accent-color: #00ff9d;
        --text-color: #ffffff;
        --border-radius: 12px;
    }
    
    body {
        background-color: var(--background-color);
        color: var(--text-color);
        font-family: 'Roboto', sans-serif;
    }
    
    .stApp {
        background-color: var(--background-color);
    }
    
    .card {
        background-color: var(--card-background);
        border-radius: var(--border-radius);
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 20px rgba(0, 245, 255, 0.15);
        border: 1px solid rgba(0, 245, 255, 0.3);
    }
    
    .header {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #1a1f33, #0d1117);
        border-radius: var(--border-radius);
        padding: 15px;
        text-align: center;
        box-shadow: 0 4px 15px rgba(0, 245, 255, 0.2);
    }
    
    .neon-button {
        background: linear-gradient(90deg, var(--primary-color), var(--secondary-color));
        color: white;
        border: none;
        padding: 10px 20px;
        border-radius: var(--border-radius);
        font-weight: bold;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    
    .neon-button:hover {
        box-shadow: 0 0 15px var(--primary-color);
        transform: translateY(-2px);
    }
    
    .fraud-alert {
        background: linear-gradient(135deg, rgba(255, 0, 0, 0.2), rgba(255, 0, 230, 0.2));
        border-left: 4px solid var(--secondary-color);
    }
    
    .normal-transaction {
        background: linear-gradient(135deg, rgba(0, 245, 255, 0.1), rgba(0, 255, 157, 0.1));
        border-left: 4px solid var(--primary-color);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'detector' not in st.session_state:
    st.session_state.detector = FraudDetector()
    
if 'risk_registry' not in st.session_state:
    st.session_state.risk_registry = RiskScoreRegistry()
    
if 'fraud_registry' not in st.session_state:
    st.session_state.fraud_registry = FraudFlagRegistry()
    
if 'audit_trail' not in st.session_state:
    st.session_state.audit_trail = AuditTrail()

if 'transaction_data' not in st.session_state:
    st.session_state.transaction_data = []

if 'alerts' not in st.session_state:
    st.session_state.alerts = []

# Title and header
st.markdown("<h1 class='header'>🛡️ FraudGuard Labs - Real-Time Fraud Detection</h1>", unsafe_allow_html=True)
st.markdown("<p style='color: #a0a0a0;'>AI-Powered Fraud Detection with Blockchain Audit Trail Simulation</p>", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("<h2 class='header'>🎛️ Controls</h2>", unsafe_allow_html=True)
    
    # Simulation controls
    st.markdown("### 🚀 Simulation")
    num_transactions = st.slider("Transactions to Process", 1, 50, 10)
    processing_speed = st.select_slider("Processing Speed", options=["Slow", "Medium", "Fast"], value="Medium")
    
    # Model settings
    st.markdown("### 🤖 AI Model")
    sensitivity = st.slider("Fraud Sensitivity", 0.0, 1.0, 0.5)
    
    # Blockchain simulation
    st.markdown("### 🔗 Blockchain")
    enable_blockchain = st.checkbox("Enable Blockchain Simulation", value=True)
    
    # Action buttons
    st.markdown("---")
    if st.button("🔄 Generate Transactions", key="generate"):
        # Generate transactions
        new_transactions = generate_transaction_stream(num_transactions)
        
        # Process each transaction
        for tx in new_transactions:
            # Get fraud prediction
            is_fraud, risk_score = st.session_state.detector.predict(tx)
            
            # Store in registries if enabled
            if enable_blockchain:
                tx_id = tx['transaction_id']
                st.session_state.risk_registry.store_risk(tx_id, risk_score)
                if is_fraud:
                    st.session_state.fraud_registry.flag_fraud(tx_id, "High risk score detected")
                st.session_state.audit_trail.log_audit(tx_id, risk_score, datetime.now())
            
            # Add to transaction data
            tx_record = {
                "timestamp": datetime.now(),
                "transaction_id": tx['transaction_id'],
                "amount": tx['amount'],
                "merchant": tx['merchant'],
                "category": tx['category'],
                "risk_score": risk_score,
                "is_fraud": is_fraud
            }
            st.session_state.transaction_data.append(tx_record)
            
            # Add to alerts if fraudulent
            if is_fraud:
                alert = {
                    "timestamp": datetime.now(),
                    "transaction_id": tx['transaction_id'],
                    "risk_score": risk_score,
                    "reason": "High risk score detected"
                }
                st.session_state.alerts.append(alert)
                
            # Wait based on speed setting
            if processing_speed == "Slow":
                time.sleep(0.5)
            elif processing_speed == "Medium":
                time.sleep(0.2)
            else:  # Fast
                time.sleep(0.05)
        
        st.success(f"Processed {num_transactions} transactions!")
    
    if st.button("🧹 Clear Data", key="clear"):
        st.session_state.transaction_data = []
        st.session_state.alerts = []
        st.session_state.risk_registry.clear()
        st.session_state.fraud_registry.clear()
        st.session_state.audit_trail.clear()
        st.success("Data cleared!")

# Main dashboard
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<div class='metric-card'><h3>Total Transactions</h3><h2>{}</h2></div>".format(len(st.session_state.transaction_data)), unsafe_allow_html=True)

with col2:
    fraud_count = len([tx for tx in st.session_state.transaction_data if tx['is_fraud']])
    st.markdown("<div class='metric-card'><h3>Fraud Detected</h3><h2 style='color: #ff00e6'>{}</h2></div>".format(fraud_count), unsafe_allow_html=True)

with col3:
    if st.session_state.transaction_data:
        avg_risk = np.mean([tx['risk_score'] for tx in st.session_state.transaction_data])
        st.markdown("<div class='metric-card'><h3>Avg Risk Score</h3><h2 style='color: #00f5ff'>{:.2f}</h2></div>".format(avg_risk), unsafe_allow_html=True)
    else:
        st.markdown("<div class='metric-card'><h3>Avg Risk Score</h3><h2 style='color: #00f5ff'>0.00</h2></div>", unsafe_allow_html=True)

# Charts row
chart_col1, chart_col2 = st.columns(2)

with chart_col1:
    st.markdown("<div class='card'><h3 class='header'>📈 Risk Score Distribution</h3>", unsafe_allow_html=True)
    if st.session_state.transaction_data:
        risk_scores = [tx['risk_score'] for tx in st.session_state.transaction_data]
        fig = px.histogram(x=risk_scores, nbins=20, 
                          color_discrete_sequence=['#00f5ff'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available. Generate transactions to see the chart.")
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown("<div class='card'><h3 class='header'>📊 Fraud Trends Over Time</h3>", unsafe_allow_html=True)
    if st.session_state.transaction_data:
        df = pd.DataFrame(st.session_state.transaction_data)
        df['hour'] = pd.to_datetime(df['timestamp']).dt.hour
        hourly_fraud = df[df['is_fraud']].groupby('hour').size().reset_index(name='count')
        
        fig = px.line(hourly_fraud, x='hour', y='count',
                     color_discrete_sequence=['#ff00e6'])
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available. Generate transactions to see the chart.")
    st.markdown("</div>", unsafe_allow_html=True)

# Transaction table and alerts
table_col1, table_col2 = st.columns(2)

with table_col1:
    st.markdown("<div class='card'><h3 class='header'>📋 Recent Transactions</h3>", unsafe_allow_html=True)
    if st.session_state.transaction_data:
        recent_tx = st.session_state.transaction_data[-10:]  # Last 10 transactions
        df_tx = pd.DataFrame(recent_tx)
        df_tx = df_tx[['timestamp', 'transaction_id', 'amount', 'merchant', 'category', 'risk_score', 'is_fraud']]
        df_tx['timestamp'] = df_tx['timestamp'].dt.strftime('%H:%M:%S')
        st.dataframe(df_tx.style.applymap(lambda x: 'background-color: rgba(255, 0, 230, 0.2)' if x == True else '', subset=['is_fraud']), use_container_width=True)
    else:
        st.info("No transactions yet. Generate some transactions to populate this table.")
    st.markdown("</div>", unsafe_allow_html=True)

with table_col2:
    st.markdown("<div class='card'><h3 class='header'>🚨 Fraud Alerts</h3>", unsafe_allow_html=True)
    if st.session_state.alerts:
        for alert in st.session_state.alerts[-5:]:  # Last 5 alerts
            st.markdown(f"""
            <div class='card fraud-alert'>
                <strong>⚠️ FRAUD ALERT</strong><br>
                <strong>Transaction:</strong> {alert['transaction_id']}<br>
                <strong>Risk Score:</strong> {alert['risk_score']:.3f}<br>
                <strong>Reason:</strong> {alert['reason']}<br>
                <strong>Time:</strong> {alert['timestamp'].strftime('%H:%M:%S')}
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("No fraud alerts yet. Generate transactions to see alerts.")
    st.markdown("</div>", unsafe_allow_html=True)

# Blockchain simulation panel
st.markdown("<div class='card'><h3 class='header'>🔗 Blockchain Registry Simulation</h3>", unsafe_allow_html=True)
registry_col1, registry_col2, registry_col3 = st.columns(3)

with registry_col1:
    st.markdown("##### Risk Score Registry")
    if st.session_state.risk_registry.scores:
        st.metric("Stored Scores", len(st.session_state.risk_registry.scores))
        if st.button("View Registry", key="risk_view"):
            st.json(st.session_state.risk_registry.scores)
    else:
        st.info("No scores stored")

with registry_col2:
    st.markdown("##### Fraud Flag Registry")
    if st.session_state.fraud_registry.flags:
        st.metric("Fraud Flags", len(st.session_state.fraud_registry.flags))
        if st.button("View Registry", key="fraud_view"):
            st.json(st.session_state.fraud_registry.flags)
    else:
        st.info("No fraud flags")

with registry_col3:
    st.markdown("##### Audit Trail")
    if st.session_state.audit_trail.logs:
        st.metric("Audit Logs", len(st.session_state.audit_trail.logs))
        if st.button("View Logs", key="audit_view"):
            st.json(st.session_state.audit_trail.logs)
    else:
        st.info("No audit logs")

st.markdown("</div>", unsafe_allow_html=True)

# Footer with attribution
st.markdown("---")
st.markdown("<p style='text-align: center; color: #a0a0a0;'>🛡️ FraudGuard Labs - Developed by Tanu Chandravanshi for QIE Blockchain Hackathon 2025</p>", unsafe_allow_html=True)