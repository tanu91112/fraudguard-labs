# FraudGuard Labs - Quick Start Script

import os
import subprocess
import sys

def main():
    """Run the FraudGuard Labs Streamlit application"""
    print("🛡️ FraudGuard Labs - Real-Time Fraud Detection with Blockchain Simulation")
    print("=" * 70)
    print("Starting the Streamlit dashboard...")
    print("")
    print("The dashboard will be available at: http://localhost:8501")
    print("Press Ctrl+C to stop the application")
    print("")
    
    try:
        # Run the Streamlit app
        subprocess.run(["streamlit", "run", "app.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running the application: {e}")
        return 1
    except KeyboardInterrupt:
        print("\nApplication stopped by user")
        return 0

if __name__ == "__main__":
    sys.exit(main())