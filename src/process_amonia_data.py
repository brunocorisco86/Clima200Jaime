import pandas as pd
import sqlite3
import os
import re

def process_amonia_data():
    db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'database', 'clima.db'))
    amonia_data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'raw', 'Amonia'))

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    csv_files = [f for f in os.listdir(amonia_data_dir) if f.endswith('.csv')]

    for csv_file in csv_files:
        file_path = os.path.join(amonia_data_dir, csv_file)
        
        # Extract lot number from filename (e.g., Sensores_lote_19.csv -> 19)
        match = re.search(r'lote_(\d+)', csv_file)
        if not match:
            print(f"Skipping {csv_file}: Could not extract lot number.")
            continue
        lot_number = match.group(1)

        try:
            column_names = ['Grandeza', 'Coletor', 'Dispositivo', 'ID_longa', 'ID_curta', 'Canal', 'Local', 'Valor', 'Data', 'Hora']
            df = pd.read_csv(file_path, sep=';', decimal=',', skiprows=1, names=column_names)

            # Extract aviary number from 'Coletor' column (e.g., CTRONICS 1282 -> 1282)
            # Assuming 'Coletor' column exists and has the format 'CTRONICS XXXX'
            df['Aviario'] = df['Coletor'].apply(lambda x: re.search(r'\\d+', x).group(0) if isinstance(x, str) and re.search(r'\\d+', x) else None)
            df['lote_composto'] = df['Aviario'].astype(str) + '_' + str(lot_number)

            # Combine 'Data' and 'Hora' into a single datetime column
            df['DataHora'] = pd.to_datetime(df['Data'] + ' ' + df['Hora'], format='%d/%m/%Y %H:%M:%S')
            
            # Select and reorder columns to match the database schema
            df = df[['Grandeza', 'Coletor', 'Dispositivo', 'ID_longa', 'ID_curta', 'Canal', 'Local', 'Valor', 'DataHora', 'lote_composto']]

            # Insert data into the database
            df.to_sql('amonia_data', conn, if_exists='append', index=False)
            print(f"Successfully processed and loaded data from {csv_file}")

        except Exception as e:
            print(f"Error processing {csv_file}: {e}")

    conn.close()

if __name__ == '__main__':
    process_amonia_data()