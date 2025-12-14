# FraudGuard Labs - Real-Time Fraud Detection with Blockchain Simulation

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.29.0-red)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

**FraudGuard Labs** is a hackathon-ready project that demonstrates real-time fraud detection using AI combined with a blockchain-inspired simulation. The system features a sleek, interactive dashboard with cyberpunk/neon aesthetics.

## 🛡️ Project Overview

FraudGuard combines machine learning algorithms with blockchain-inspired data structures to detect and record fraudulent transactions in real-time. The system simulates a complete fraud detection pipeline with:

- **AI Fraud Detection Engine**: Uses Isolation Forest algorithm for anomaly detection
- **Real-time Transaction Processing**: Simulates live transaction streams
- **Blockchain Registry Simulation**: Immutable storage for risk scores and fraud flags
- **Interactive Dashboard**: Real-time visualization with Streamlit

## 🚀 Key Features

### AI Fraud Detection
- Binary classification (fraudulent vs legitimate)
- Risk scoring (0-1 scale)
- Anomaly detection using Isolation Forest
- Feature engineering for transaction patterns

### Blockchain Simulation
- **RiskScoreRegistry**: Stores per-transaction risk scores
- **FraudFlagRegistry**: Records fraud alerts
- **AuditTrail**: Immutable logs for investigations
- Simulated immutability and transparency

### Interactive Dashboard
- Real-time risk score graphs
- Fraud alerts table
- Wallet connect simulation
- Smart contract interaction panel
- Cyberpunk/neon UI theme

## 📁 Project Structure

```
fraudguard-labs/
├── app.py                    # Main Streamlit application
├── fraudguard_app/          # Application modules
│   ├── components/
│   │   └── fraud_detector.py  # AI fraud detection model
│   ├── blockchain_sim/
│   │   └── registry.py        # Blockchain registry simulation
│   ├── data/
│   │   └── data_generator.py  # Transaction data generation
│   ├── models/                # Trained ML models (created on first run)
│   ├── pages/                 # Additional Streamlit pages
│   └── utils/                 # Utility functions
├── datasets/                  # Sample datasets
├── docs/                      # Documentation
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🛠️ Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/fraudguard-labs.git
   cd fraudguard-labs
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

## 🎯 Usage

1. Open the dashboard in your browser (typically http://localhost:8501)
2. Adjust simulation parameters in the sidebar:
   - Number of transactions to process
   - Processing speed
   - Fraud sensitivity
3. Click "Generate Transactions" to start the simulation
4. Monitor real-time updates in the dashboard
5. View blockchain registry data in the simulation panel

## 🧠 AI Model Details

The fraud detection model uses an **Isolation Forest** algorithm, which is particularly effective for anomaly detection. The model considers:

- Transaction amount
- Merchant risk profile
- Time of day
- Account age
- Transaction history
- Category risk

## 🔗 Blockchain Simulation

The blockchain component simulates three key registries:

1. **RiskScoreRegistry**: Stores risk scores for each transaction
2. **FraudFlagRegistry**: Records flagged fraudulent transactions
3. **AuditTrail**: Maintains immutable logs of all transactions

## 📊 Visualization Features

- Real-time risk score distribution histograms
- Fraud trends over time
- Transaction tables with fraud highlighting
- Interactive fraud alerts
- Registry status indicators

## 🏆 Hackathon Features

This project is specifically designed for hackathon judging criteria:

### Innovation (25%)
- Novel combination of AI and blockchain concepts
- Real-time processing with simulation
- Interactive visualization

### Impact (25%)
- Addresses critical financial security needs
- Demonstrates scalability potential
- Practical application for fintech

### Technical Execution (25%)
- Clean, modular code architecture
- Well-documented components
- Production-quality implementation

### Presentation (15%)
- Polished, professional UI
- Clear dashboard organization
- Comprehensive visualization

### Bonus Features (10%)
- Cyberpunk/neon aesthetic
- Simulated token creation concepts
- Validator checkpoint simulation

## 👤 Author

**Tanu Chandravanshi**

This project was created for the QIE Blockchain Hackathon 2025.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by real-world fraud detection systems
- Built with Streamlit for rapid prototyping
- Uses scikit-learn for machine learning algorithms