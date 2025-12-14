import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import joblib
import os

class FraudDetector:
    def __init__(self):
        """
        Initialize the Fraud Detector with a pre-trained model or train a new one
        """
        self.model = None
        self.scaler = StandardScaler()
        self.is_trained = False
        self._load_or_train_model()
    
    def _generate_sample_data(self, n_samples=1000):
        """
        Generate sample transaction data for training
        """
        np.random.seed(42)  # For reproducible results
        
        # Normal transactions (80% of data)
        normal_count = int(n_samples * 0.8)
        normal_data = {
            'amount': np.random.lognormal(3, 1, normal_count),
            'merchant_risk_score': np.random.beta(2, 5, normal_count),
            'time_of_day': np.random.uniform(0, 24, normal_count),
            'account_age_days': np.random.exponential(365, normal_count),
            'previous_transactions': np.random.poisson(5, normal_count),
            'category_encoded': np.random.choice([1, 2, 3, 4, 5], normal_count, p=[0.3, 0.25, 0.2, 0.15, 0.1])
        }
        
        # Fraudulent transactions (20% of data)
        fraud_count = n_samples - normal_count
        fraud_data = {
            'amount': np.random.lognormal(5, 2, fraud_count),  # Higher amounts
            'merchant_risk_score': np.random.beta(5, 2, fraud_count),  # Higher merchant risk
            'time_of_day': np.concatenate([
                np.random.uniform(0, 6, fraud_count//2),  # Unusual hours
                np.random.uniform(22, 24, fraud_count//2)
            ]),
            'account_age_days': np.random.exponential(30, fraud_count),  # New accounts
            'previous_transactions': np.random.poisson(1, fraud_count),  # Few previous transactions
            'category_encoded': np.random.choice([1, 2, 3, 4, 5], fraud_count, p=[0.1, 0.15, 0.2, 0.25, 0.3])  # Riskier categories
        }
        
        # Combine data
        data = {}
        for key in normal_data:
            data[key] = np.concatenate([normal_data[key], fraud_data[key]])
        
        # Create labels (0 for normal, 1 for fraud)
        labels = np.concatenate([np.zeros(normal_count), np.ones(fraud_count)])
        
        df = pd.DataFrame(data)
        df['is_fraud'] = labels
        
        return df
    
    def _load_or_train_model(self):
        """
        Load a pre-trained model or train a new one if it doesn't exist
        """
        model_path = "models/fraud_model.pkl"
        scaler_path = "models/scaler.pkl"
        
        if os.path.exists(model_path) and os.path.exists(scaler_path):
            # Load existing model
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.is_trained = True
        else:
            # Train new model
            print("Training new fraud detection model...")
            self._train_model()
    
    def _train_model(self):
        """
        Train the fraud detection model
        """
        # Generate training data
        df = self._generate_sample_data(2000)
        
        # Prepare features
        feature_columns = ['amount', 'merchant_risk_score', 'time_of_day', 
                          'account_age_days', 'previous_transactions', 'category_encoded']
        X = df[feature_columns]
        y = df['is_fraud']
        
        # Scale features
        X_scaled = self.scaler.fit_transform(X)
        
        # Train isolation forest model
        self.model = IsolationForest(
            contamination=0.1,  # Expected proportion of outliers
            random_state=42,
            n_estimators=100
        )
        self.model.fit(X_scaled)
        
        # Mark as trained
        self.is_trained = True
        
        # Save model and scaler
        os.makedirs("models", exist_ok=True)
        joblib.dump(self.model, "models/fraud_model.pkl")
        joblib.dump(self.scaler, "models/scaler.pkl")
        
        print("Model trained and saved successfully!")
    
    def predict(self, transaction_data):
        """
        Predict if a transaction is fraudulent and return risk score
        
        Args:
            transaction_data (dict): Transaction data with keys:
                - amount: Transaction amount
                - merchant: Merchant name
                - category: Transaction category
                - time_of_day: Hour of day (0-24)
                - account_age_days: Age of account in days
                - previous_transactions: Number of previous transactions
                
        Returns:
            tuple: (is_fraud: bool, risk_score: float)
        """
        if not self.is_trained:
            raise Exception("Model is not trained yet!")
        
        # Map merchant to risk score (in a real system, this would come from a database)
        merchant_risk_map = {
            'Amazon': 0.1, 'Walmart': 0.05, 'Target': 0.08,
            'Suspicious Merchant': 0.9, 'Unknown Merchant': 0.7,
            'PayPal': 0.2, 'Apple Store': 0.1, 'Google Play': 0.15,
            'Gas Station': 0.3, 'Restaurant': 0.25
        }
        
        # Map category to encoded value
        category_map = {
            'groceries': 1, 'entertainment': 2, 'shopping': 3,
            'travel': 4, 'utilities': 5
        }
        
        # Extract features
        amount = transaction_data.get('amount', 0)
        merchant = transaction_data.get('merchant', 'Unknown Merchant')
        category = transaction_data.get('category', 'shopping')
        time_of_day = transaction_data.get('time_of_day', 12)
        account_age_days = transaction_data.get('account_age_days', 365)
        previous_transactions = transaction_data.get('previous_transactions', 10)
        
        # Get merchant risk score
        merchant_risk_score = merchant_risk_map.get(merchant, 0.5)
        
        # Get category encoding
        category_encoded = category_map.get(category, 3)
        
        # Prepare feature vector
        features = np.array([[
            amount, merchant_risk_score, time_of_day,
            account_age_days, previous_transactions, category_encoded
        ]])
        
        # Scale features
        features_scaled = self.scaler.transform(features)
        
        # Get prediction (-1 for anomaly, 1 for normal)
        prediction = self.model.predict(features_scaled)[0]
        
        # Get anomaly score (lower scores indicate higher anomaly probability)
        anomaly_score = self.model.decision_function(features_scaled)[0]
        
        # Convert to risk score (0-1 scale, where 1 is high risk)
        # Transform anomaly score to 0-1 range
        risk_score = 1 / (1 + np.exp(anomaly_score))  # Sigmoid transformation
        
        # Adjust risk score based on known high-risk factors
        if merchant_risk_score > 0.7:
            risk_score = min(1.0, risk_score + 0.3)
        elif merchant_risk_score > 0.4:
            risk_score = min(1.0, risk_score + 0.1)
            
        # Very new accounts are riskier
        if account_age_days < 30:
            risk_score = min(1.0, risk_score + 0.2)
            
        # Very few previous transactions are riskier
        if previous_transactions < 3:
            risk_score = min(1.0, risk_score + 0.15)
        
        # Transaction is fraudulent if prediction is -1 (anomaly)
        is_fraud = (prediction == -1)
        
        return is_fraud, float(risk_score)

# Example usage
if __name__ == "__main__":
    detector = FraudDetector()
    
    # Test transaction
    test_transaction = {
        'amount': 1500.0,
        'merchant': 'Amazon',
        'category': 'shopping',
        'time_of_day': 14,
        'account_age_days': 365,
        'previous_transactions': 20
    }
    
    is_fraud, risk_score = detector.predict(test_transaction)
    print(f"Transaction is {'fraudulent' if is_fraud else 'legitimate'} with risk score: {risk_score:.3f}")