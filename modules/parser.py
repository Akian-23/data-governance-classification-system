import pandas as pd

def load_dataset(file_path):
    try:
        df = pd.read_csv(file_path)
        if df.empty:
            raise ValueError("Dataset is empty")
        
        print("Dataset loaded successfully\n")
        return df
    
    except Exception as e:
        print(f"Error loading dataset: {e}")
        return None