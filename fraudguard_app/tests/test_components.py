import unittest
import sys
import os
import pandas as pd
import numpy as np

# Add the components directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'fraudguard_app', 'components'))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'fraudguard_app', 'blockchain_sim'))

from fraud_detector import FraudDetector
from registry import RiskScoreRegistry, FraudFlagRegistry, AuditTrail

class TestFraudDetector(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.detector = FraudDetector()
        
    def test_model_initialization(self):
        """Test that the fraud detector model initializes correctly."""
        self.assertIsNotNone(self.detector.model)
        self.assertTrue(self.detector.is_trained)
        
    def test_fraud_prediction(self):
        """Test fraud prediction for a normal transaction."""
        normal_transaction = {
            'amount': 50.0,
            'merchant': 'Amazon',
            'category': 'shopping',
            'time_of_day': 14,
            'account_age_days': 365,
            'previous_transactions': 20
        }
        
        is_fraud, risk_score = self.detector.predict(normal_transaction)
        
        # Should return a boolean and a float
        self.assertIsInstance(is_fraud, bool)
        self.assertIsInstance(risk_score, float)
        
        # Risk score should be between 0 and 1
        self.assertGreaterEqual(risk_score, 0.0)
        self.assertLessEqual(risk_score, 1.0)
        
    def test_high_risk_transaction(self):
        """Test fraud prediction for a high-risk transaction."""
        high_risk_transaction = {
            'amount': 5000.0,
            'merchant': 'Suspicious Merchant',
            'category': 'travel',
            'time_of_day': 3,  # Unusual hour
            'account_age_days': 5,  # Very new account
            'previous_transactions': 1  # Very few transactions
        }
        
        is_fraud, risk_score = self.detector.predict(high_risk_transaction)
        
        # Should return a boolean and a float
        self.assertIsInstance(is_fraud, bool)
        self.assertIsInstance(risk_score, float)

class TestBlockchainRegistries(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.risk_registry = RiskScoreRegistry()
        self.fraud_registry = FraudFlagRegistry()
        self.audit_trail = AuditTrail()
        
    def test_risk_score_registry(self):
        """Test the risk score registry functionality."""
        # Store a risk score
        tx_id = "test_tx_001"
        risk_score = 0.85
        self.risk_registry.store_risk(tx_id, risk_score)
        
        # Retrieve the risk score
        stored_data = self.risk_registry.get_risk(tx_id)
        self.assertIsNotNone(stored_data)
        self.assertEqual(stored_data['risk_score'], risk_score)
        
        # Test getting all risks
        all_risks = self.risk_registry.get_all_risks()
        self.assertIn(tx_id, all_risks)
        
    def test_fraud_flag_registry(self):
        """Test the fraud flag registry functionality."""
        # Flag a transaction as fraud
        tx_id = "test_tx_002"
        reason = "High risk score detected"
        self.fraud_registry.flag_fraud(tx_id, reason)
        
        # Check if transaction is flagged
        self.assertTrue(self.fraud_registry.is_flagged(tx_id))
        
        # Retrieve flag details
        flag_data = self.fraud_registry.get_flag(tx_id)
        self.assertIsNotNone(flag_data)
        self.assertEqual(flag_data['reason'], reason)
        
    def test_audit_trail(self):
        """Test the audit trail functionality."""
        import datetime
        
        # Log an audit entry
        tx_id = "test_tx_003"
        risk_score = 0.92
        timestamp = datetime.datetime.now()
        self.audit_trail.log_audit(tx_id, risk_score, timestamp)
        
        # Retrieve logs for the transaction
        logs = self.audit_trail.get_logs_for_transaction(tx_id)
        self.assertEqual(len(logs), 1)
        self.assertEqual(logs[0]['tx_id'], tx_id)
        self.assertEqual(logs[0]['risk_score'], risk_score)
        
        # Retrieve all logs
        all_logs = self.audit_trail.get_all_logs()
        self.assertGreaterEqual(len(all_logs), 1)

if __name__ == '__main__':
    unittest.main()