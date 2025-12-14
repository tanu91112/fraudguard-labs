# FraudGuard Labs API Documentation

## Overview

FraudGuard Labs provides a comprehensive API for fraud detection and blockchain registry management. This documentation covers the main components and their usage.

## Core Components

### 1. Fraud Detection Engine

The fraud detection engine provides real-time fraud analysis for financial transactions.

#### Methods

**`predict(transaction_data)`**
- **Description**: Analyze a transaction and return fraud prediction
- **Parameters**: 
  - `transaction_data` (dict): Transaction information containing:
    - `amount` (float): Transaction amount
    - `merchant` (str): Merchant name
    - `category` (str): Transaction category
    - `time_of_day` (float): Hour of day (0-24)
    - `account_age_days` (int): Account age in days
    - `previous_transactions` (int): Number of previous transactions
- **Returns**: Tuple of (is_fraud: bool, risk_score: float)
- **Example**:
  ```python
  detector = FraudDetector()
  transaction = {
      'amount': 1500.0,
      'merchant': 'Amazon',
      'category': 'shopping',
      'time_of_day': 14,
      'account_age_days': 365,
      'previous_transactions': 20
  }
  is_fraud, risk_score = detector.predict(transaction)
  ```

### 2. Blockchain Registry Simulation

The blockchain registry simulation provides immutable storage for fraud detection data.

#### RiskScoreRegistry

**`store_risk(tx_id, risk_score)`**
- **Description**: Store a risk score for a transaction
- **Parameters**:
  - `tx_id` (str): Transaction ID
  - `risk_score` (float): Risk score between 0 and 1

**`get_risk(tx_id)`**
- **Description**: Retrieve the risk score for a transaction
- **Parameters**:
  - `tx_id` (str): Transaction ID
- **Returns**: Dict containing risk score data

**`get_all_risks()`**
- **Description**: Get all stored risk scores
- **Returns**: Dict of all risk scores

#### FraudFlagRegistry

**`flag_fraud(tx_id, reason)`**
- **Description**: Flag a transaction as fraudulent
- **Parameters**:
  - `tx_id` (str): Transaction ID
  - `reason` (str): Reason for flagging

**`is_flagged(tx_id)`**
- **Description**: Check if a transaction is flagged as fraudulent
- **Parameters**:
  - `tx_id` (str): Transaction ID
- **Returns**: Boolean indicating if transaction is flagged

**`get_flag(tx_id)`**
- **Description**: Get fraud flag details for a transaction
- **Parameters**:
  - `tx_id` (str): Transaction ID
- **Returns**: Dict containing flag data

#### AuditTrail

**`log_audit(tx_id, risk_score, timestamp)`**
- **Description**: Log an audit entry for a transaction
- **Parameters**:
  - `tx_id` (str): Transaction ID
  - `risk_score` (float): Risk score
  - `timestamp` (datetime): Timestamp of the transaction

**`get_logs_for_transaction(tx_id)`**
- **Description**: Get all audit logs for a specific transaction
- **Parameters**:
  - `tx_id` (str): Transaction ID
- **Returns**: List of audit logs for the transaction

**`get_all_logs()`**
- **Description**: Get all audit logs
- **Returns**: List of all audit logs

## Data Generation

### Transaction Stream Generation

**`generate_transaction_stream(num_transactions)`**
- **Description**: Generate a stream of simulated transactions
- **Parameters**:
  - `num_transactions` (int): Number of transactions to generate
- **Returns**: List of transaction dictionaries

### Sample Dataset Generation

**`generate_sample_dataset(num_records)`**
- **Description**: Generate a larger sample dataset for training/testing
- **Parameters**:
  - `num_records` (int): Number of records to generate
- **Returns**: Pandas DataFrame with transaction data

## Error Handling

All components include appropriate error handling:
- Invalid transaction data will raise ValueError
- Missing parameters will raise TypeError
- Registry operations will handle missing keys gracefully

## Performance Considerations

- The fraud detection model is optimized for real-time inference
- Registry operations use efficient data structures for quick lookups
- Memory usage is minimized through proper data management

## Testing

Unit tests are provided for all components in the `tests/` directory:
- `test_components.py`: Tests for fraud detection and registry components

Run tests with:
```bash
python -m pytest fraudguard_app/tests/
```