import pandas as pd
from data_loader import clean_amount, clean_price, clean_quantity

def total_deposits(df):
    deposits = df[df['Trans Code'] == 'ACH']  
    total_deposit_amount = deposits['Amount_clean'].sum()  
    deposit_list = deposits[['Amount_clean', 'Activity Date']]  
    return total_deposit_amount, deposit_list

def get_most_profitable_trade(trades):
    most_profitable_trade = None
    highest_profit = 0.0

    for trade in trades:
        if trade['net_profit'] > highest_profit:
            highest_profit = trade['net_profit']
            most_profitable_trade = trade
    if most_profitable_trade:
        return most_profitable_trade
    else:
        print("No profitable trade found.")

def calculate_oexp_loss_percentage(trades):
    total_losses = 0  
    oexp_losses = 0  
    oexp_trades = []

    for trade in trades:
        if trade['net_profit'] < 0:  
            total_losses += 1
            if trade['oexp_loss']:  
                oexp_losses += 1
                oexp_trades.append(trade)
    if total_losses > 0:  
        loss_percentage = (oexp_losses / total_losses) * 100
    else:
        loss_percentage = 0.0
    loss_percentage = round(loss_percentage, 2)

    return loss_percentage, oexp_trades

def get_all_trades(df):
    open_positions = []  
    all_trades = []  
 
    for _, row in df.iloc[::-1].iterrows():
        if row['Trans Code'] == 'OEXP':  
            
            expiration_instrument = row['Instrument'].strip().lower()  
            expiration_description = row['Description'].strip().lower()  

            matching_bto = None
            for bto_row in open_positions:
                bto_instrument = bto_row['Instrument'].strip().lower()  
                bto_description = bto_row['Description'].strip().lower()  
                
                if bto_instrument == expiration_instrument and bto_description in expiration_description:
                    matching_bto = bto_row
                    break  

            if matching_bto is not None:
                oexp_net_profit = -abs(matching_bto['Amount_clean'])  

            else:
                oexp_net_profit = 0.0
            
            all_trades.append({
                "date": str(row["Activity Date"].date()),
                "instrument": row["Instrument"],
                "description": row["Description"],
                "gross_proceeds": 0.0,  
                "quantity": 0,  
                "price": clean_price(row["Price"]), 
                "net_profit": oexp_net_profit,  
                "oexp_loss": True  
            })
            continue  

        if row['Trans Code'] == 'BTO':  
            open_positions.append(row)
        elif row['Trans Code'] == 'STC':  
            total_bto_amount = 0.0
            total_bto_quantity = 0
            matched_bto = []

            for bto_row in open_positions:
                bto_instrument = bto_row['Instrument']
                stc_instrument = row['Instrument']

                bto_description = bto_row['Description']
                stc_description = row['Description']

                if bto_instrument == stc_instrument and bto_description == stc_description:
                    matched_bto.append(bto_row)  
                    total_bto_amount += bto_row['Amount_clean']
                    total_bto_quantity += bto_row['Quantity_clean']

            for bto in matched_bto:
                open_positions = [bto_item for bto_item in open_positions if not (bto_item['Instrument'] == bto['Instrument'] and bto_item['Description'] == bto['Description'])]

            if total_bto_amount != 0:
        
                net_profit = round(row['Amount_clean'] - abs(total_bto_amount), 2) 
                all_trades.append({
                    "date": str(row["Activity Date"].date()),
                    "instrument": row["Instrument"],
                    "description": row["Description"],
                    "gross_proceeds": float(row["Amount_clean"]),
                    "quantity": total_bto_quantity,
                    "price": float(row["Price_clean"]),
                    "net_profit": net_profit,
                    "oexp_loss": False  
                })

    return all_trades
