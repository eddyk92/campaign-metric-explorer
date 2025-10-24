# Put all data handling and metric calculations HERE


import pandas as pd
import sys
print(sys.path)
import pandas as pd 

def load_data(path: str) -> pd.DataFrame:
    # Load campaign data from CSV
    df = pd.read_csv(path)
    return df

def compute_metrics(df: pd.DataFrame) -> pd.DataFrame:
    # Compute campaign performance metrics
    df['CTR'] = df['Clicks'] / df['Impressions']
    df['CVR'] = df['Conversions'] / df['Clicks']
    df['CPC'] = df['Spend'] / df['Clicks']
    df['CPM'] = df['Spend'] / (df['Impressions'] / 1000)
    df['ROAS'] = df['Revenue'] / df['Spend']
    return df