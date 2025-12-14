import random
import uuid
from datetime import datetime, timedelta
import pandas as pd

def generate_sample_dataset(num_records=5000):
    """
    Generate a sample dataset for testing and demonstration
    
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

# Generate a sample dataset
if __name__ == "__main__":
    print("Generating sample dataset...")
    df = generate_sample_dataset(5000)
    
    # Save to CSV
    df.to_csv('sample_transactions.csv', index=False)
    
    print(f"Generated dataset with {len(df)} records")
    print(df.head())
    print(f"\nDataset saved to sample_transactions.csv")