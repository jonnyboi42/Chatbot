import pandas as pd

def clean_amount(value):
    if(pd.isnull(value)):
        return 0.0
    value = str(value).replace('$', '').replace(',','').strip()  
    if '(' in value:
        return -float(value.replace('(', '').replace(')',''))
    return float(value)

def clean_price(value):
    if(pd.isnull(value)):
        return None
    return float(str(value).replace('$','').strip())

def clean_quantity(value):
    if pd.isnull(value):
        return 0
    try:
        return int(value) 
    except ValueError:
        return 0  

def load_trading_data(csv_path):
    df = pd.read_csv(csv_path)
    df.columns = df.columns.str.strip() 
    
    df['Amount_clean'] = df['Amount'].apply(clean_amount)
    df['Price_clean'] = df['Price'].apply(clean_price)
    df['Quantity_clean'] = df['Quantity'].apply(clean_quantity)
    df['Activity Date'] = pd.to_datetime(df['Activity Date'], errors='coerce')  
    
    return df













