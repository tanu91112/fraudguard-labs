class RiskScoreRegistry:
    def __init__(self):
        """
        Initialize the Risk Score Registry to store transaction risk scores
        """
        self.scores = {}
    
    def store_risk(self, tx_id, risk_score):
        """
        Store a risk score for a transaction
        
        Args:
            tx_id (str): Transaction ID
            risk_score (float): Risk score between 0 and 1
        """
        self.scores[tx_id] = {
            'risk_score': risk_score,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
    
    def get_risk(self, tx_id):
        """
        Retrieve the risk score for a transaction
        
        Args:
            tx_id (str): Transaction ID
            
        Returns:
            dict: Risk score data or None if not found
        """
        return self.scores.get(tx_id)
    
    def get_all_risks(self):
        """
        Get all stored risk scores
        
        Returns:
            dict: All risk scores
        """
        return self.scores
    
    def clear(self):
        """
        Clear all stored risk scores
        """
        self.scores = {}


class FraudFlagRegistry:
    def __init__(self):
        """
        Initialize the Fraud Flag Registry to store fraud alerts
        """
        self.flags = {}
    
    def flag_fraud(self, tx_id, reason):
        """
        Flag a transaction as fraudulent
        
        Args:
            tx_id (str): Transaction ID
            reason (str): Reason for flagging
        """
        self.flags[tx_id] = {
            'reason': reason,
            'timestamp': __import__('datetime').datetime.now().isoformat()
        }
    
    def is_flagged(self, tx_id):
        """
        Check if a transaction is flagged as fraudulent
        
        Args:
            tx_id (str): Transaction ID
            
        Returns:
            bool: True if flagged, False otherwise
        """
        return tx_id in self.flags
    
    def get_flag(self, tx_id):
        """
        Get fraud flag details for a transaction
        
        Args:
            tx_id (str): Transaction ID
            
        Returns:
            dict: Flag data or None if not found
        """
        return self.flags.get(tx_id)
    
    def get_all_flags(self):
        """
        Get all fraud flags
        
        Returns:
            dict: All fraud flags
        """
        return self.flags
    
    def clear(self):
        """
        Clear all fraud flags
        """
        self.flags = {}


class AuditTrail:
    def __init__(self):
        """
        Initialize the Audit Trail to store immutable logs
        """
        self.logs = []
    
    def log_audit(self, tx_id, risk_score, timestamp):
        """
        Log an audit entry for a transaction
        
        Args:
            tx_id (str): Transaction ID
            risk_score (float): Risk score
            timestamp (datetime): Timestamp of the transaction
        """
        self.logs.append({
            'tx_id': tx_id,
            'risk_score': risk_score,
            'timestamp': timestamp.isoformat()
        })
    
    def get_logs_for_transaction(self, tx_id):
        """
        Get all audit logs for a specific transaction
        
        Args:
            tx_id (str): Transaction ID
            
        Returns:
            list: List of audit logs for the transaction
        """
        return [log for log in self.logs if log['tx_id'] == tx_id]
    
    def get_all_logs(self):
        """
        Get all audit logs
        
        Returns:
            list: All audit logs
        """
        return self.logs
    
    def clear(self):
        """
        Clear all audit logs
        """
        self.logs = []


# Example usage
if __name__ == "__main__":
    # Risk Score Registry
    risk_registry = RiskScoreRegistry()
    risk_registry.store_risk("tx_001", 0.85)
    print("Risk for tx_001:", risk_registry.get_risk("tx_001"))
    
    # Fraud Flag Registry
    fraud_registry = FraudFlagRegistry()
    fraud_registry.flag_fraud("tx_001", "High risk score")
    print("Is tx_001 flagged?", fraud_registry.is_flagged("tx_001"))
    
    # Audit Trail
    audit_trail = AuditTrail()
    audit_trail.log_audit("tx_001", 0.85, __import__('datetime').datetime.now())
    print("Audit logs:", audit_trail.get_all_logs())