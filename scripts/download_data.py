import sys
sys.path.append('.')
 
from src.data_loader import DataLoader
import pandas as pd
 
# Initialize loader
loader = DataLoader()
 
 
def load_penguins():
    """Load penguin dataset from local raw CSV."""
    df = pd.read_csv(loader.raw_dir / "penguins_size.csv")
    return df
 
 
# Choose your dataset
df = load_penguins()
 
# Save raw data in the standardized location
loader.save_processed_data(df, "raw_data.csv")
print(f"Dataset loaded: {df.shape}")