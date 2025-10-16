import sqlite3
import os
import csv
import re

# --- Configuration ---
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(PROJECT_ROOT, 'database', 'clima.db')
DATA_DIR = os.path.join(PROJECT_ROOT, 'data', 'raw', 'Exports_Acompanhamento_Lotes')
SQL_CREATE_TABLE_PATH = os.path.join(PROJECT_ROOT, 'database', 'sql', 'create_dados_lotes_table.sql')

def process_exports():
    """
    Reads data from CSV files, merges them by lot and day, and inserts them 
    into the 'dados_lotes' table in the SQLite database.
    """
    print("Starting data processing...")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Drop the old table to ensure the new schema is applied
        cursor.execute("DROP TABLE IF EXISTS dados_lotes")
        print("Old 'dados_lotes' table dropped.")

        with open(SQL_CREATE_TABLE_PATH, 'r') as f:
            create_table_sql = f.read()
        cursor.executescript(create_table_sql)
        print("Table 'dados_lotes' created with the new schema.")

    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return
    except FileNotFoundError:
        print(f"Error: SQL script not found at {SQL_CREATE_TABLE_PATH}")
        return

    # --- Data Processing ---
    merged_data = {}
    # Regex to capture aviario and lote from filename (e.g., export_..._1282_19.csv)
    file_pattern = re.compile(r'.*_(\d+)_(\d+)\.csv')

    try:
        for filename in os.listdir(DATA_DIR):
            if not filename.endswith('.csv'):
                continue

            match = file_pattern.search(filename)
            if not match:
                print(f"Skipping file with unexpected name format: {filename}")
                continue
            
            aviario, lote = map(int, match.groups())
            lote_composto = f"{aviario}_{lote}"

            file_path = os.path.join(DATA_DIR, filename)

            with open(file_path, 'r', encoding='utf-8') as f:
                reader = csv.reader(f)
                next(reader)  # Skip header

                for row in reader:
                    if not row or len(row) < 2:
                        continue

                    try:
                        idade = int(row[0])
                        data_val = row[1]
                    except (ValueError, IndexError):
                        print(f"Skipping malformed row in {filename}: {row}")
                        continue

                    key = (lote_composto, idade)
                    if key not in merged_data:
                        merged_data[key] = {'data': data_val}

                    def to_float(value):
                        try: return float(value) if value else None
                        except ValueError: return None

                    def to_int(value):
                        try: return int(value) if value else None
                        except ValueError: return None

                    # Process based on file type
                    if 'consumo_energia' in filename:
                        merged_data[key]['energia_referencia_kwh'] = to_float(row[2])
                        merged_data[key]['energia_consumo_automatico_kwh'] = to_float(row[3])
                    elif 'peso' in filename:
                        merged_data[key]['peso_referencia_g'] = to_float(row[2])
                        merged_data[key]['peso_automatico_g_ave'] = to_float(row[3])
                    elif 'consumo_racao' in filename:
                        merged_data[key]['racao_referencia_kg'] = to_float(row[2])
                        merged_data[key]['racao_automatica_kg'] = to_float(row[3])
                        if len(row) > 5: merged_data[key]['racao_manual_kg'] = to_float(row[5])
                    elif 'mortalidade' in filename:
                        merged_data[key]['mortalidade_un'] = to_int(row[2])
                        merged_data[key]['mortalidade_percent'] = to_float(row[3])
                        if len(row) > 4: merged_data[key]['mortalidade_referencia_percent'] = to_float(row[4])

    except Exception as e:
        print(f"An error occurred during file processing: {e}")
        if conn: conn.close()
        return

    # --- Database Insertion ---
    if not merged_data:
        print("No data to insert.")
        conn.close()
        return

    insert_sql = """
    INSERT OR REPLACE INTO dados_lotes (
        lote_composto, idade, data,
        energia_referencia_kwh, energia_consumo_automatico_kwh,
        peso_referencia_g, peso_automatico_g_ave, racao_referencia_kg, racao_automatica_kg,
        racao_manual_kg, mortalidade_un, mortalidade_percent, mortalidade_referencia_percent
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
    """

    try:
        for (lote_composto, idade), data in sorted(merged_data.items()):
            cursor.execute(insert_sql, (
                lote_composto, idade, data.get('data'),
                data.get('energia_referencia_kwh'),
                data.get('energia_consumo_automatico_kwh'), data.get('peso_referencia_g'),
                data.get('peso_automatico_g_ave'), data.get('racao_referencia_kg'),
                data.get('racao_automatica_kg'), data.get('racao_manual_kg'),
                data.get('mortalidade_un'), data.get('mortalidade_percent'),
                data.get('mortalidade_referencia_percent')
            ))

        conn.commit()
        print(f"Data inserted/updated for {len(merged_data)} records.")

    except sqlite3.Error as e:
        print(f"Database error during insertion: {e}")
    finally:
        if conn:
            conn.close()
            print("Database connection closed.")

if __name__ == '__main__':
    process_exports()