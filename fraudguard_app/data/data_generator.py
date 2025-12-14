import random
import uuid
from datetime import datetime, timedelta
import pandas as pd

def generate_transaction_stream(num_transactions=10):
    """
    Generate a stream of simulated transactions
    
    Args:
        num_transactions (int): Number of transactions to generate
        
    Returns:
        list: List of transaction dictionaries
    """
    # Sample merchants
    merchants = [
        "Amazon", "Walmart", "Target", "Starbucks", "McDonald's",
        "Shell", "Chevron", "Apple Store", "Google Play", "Netflix",
        "Uber", "Lyft", "Airbnb", "Expedia", "Best Buy",
        "Home Depot", "Wells Fargo", "Chase", "Bank of America",
        "Suspicious Merchant", "Unknown Merchant"
    ]
    
    # Transaction categories
    categories = ["groceries", "entertainment", "shopping", "travel", "utilities"]
    
    transactions = []
    
    for i in range(num_transactions):
        # Generate transaction ID
        tx_id = str(uuid.uuid4())
        
        # Random amount between $5 and $5000
        amount = round(random.uniform(5, 5000), 2)
        
        # Select random merchant
        merchant = random.choice(merchants)
        
        # Select random category
        category = random.choice(categories)
        
        # Random time of day (0-24)
        time_of_day = random.uniform(0, 24)
        
        # Account age in days (random between 1 day and 5 years)
        account_age_days = random.randint(1, 365*5)
        
        # Previous transactions (random between 0 and 100)
        previous_transactions = random.randint(0, 100)
        
        # Create transaction dictionary
        transaction = {
            "transaction_id": tx_id,
            "amount": amount,
            "merchant": merchant,
            "category": category,
            "time_of_day": time_of_day,
            "account_age_days": account_age_days,
            "previous_transactions": previous_transactions,
            "timestamp": datetime.now() - timedelta(minutes=random.randint(0, 60))
        }
        
        transactions.append(transaction)
    
    return transactions

def generate_sample_dataset(num_records=10000):
    """
    Generate a larger sample dataset for training/testing
    
    Args:
        num_records (int): Number of records to generate
        
    Returns:
        pandas.DataFrame: DataFrame with transaction data
    """
    # Sample merchants
    merchants = [
        "Amazon", "Walmart", "Target", "Starbucks", "McDonald's",
        "Shell", "Chevron", "Apple Store", "Google Play", "Netflix",
        "Uber", "Lyft", "Airbnb", "Expedia", "Best Buy",
        "Home Depot", "Wells Fargo", "Chase", "Bank of America",
        "Suspicious Merchant", "Unknown Merchant"
    ]
    
    # Transaction categories
    categories = ["groceries", "entertainment", "shopping", "travel", "utilities"]
    
    # Generate data
    data = []
    
    for i in range(num_records):
        # Random amount between $1 and $10000
        amount = round(random.uniform(1, 10000), 2)
        
        # Select random merchant
        merchant = random.choice(merchants)
        
        # Select random category
        category = random.choice(categories)
        
        # Random time of day (0-24)
        time_of_day = random.uniform(0, 24)
        
        # Account age in days (random between 1 day and 10 years)
        account_age_days = random.randint(1, 365*10)
        
        # Previous transactions (random between 0 and 500)
        previous_transactions = random.randint(0, 500)
        
        # Create record
        record = {
            "transaction_id": str(uuid.uuid4()),
            "amount": amount,
            "merchant": merchant,
            "category": category,
            "time_of_day": time_of_day,
            "account_age_days": account_age_days,
            "previous_transactions": previous_transactions,
            "timestamp": datetime.now() - timedelta(hours=random.randint(0, 720))
        }
        
        data.append(record)
    
    return pd.DataFrame(data)

# Example usage
if __name__ == "__main__":
    # Generate a small stream
    transactions = generate_transaction_stream(5)
    for tx in transactions:
        print(tx)
    
    print("\n" + "="*50 + "\n")
    
    # Generate a larger dataset
    df = generate_sample_dataset(100)
    print(df.head())
    print(f"\nGenerated {len(df)} records")