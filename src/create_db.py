import sqlite3
import os

script_dir = os.path.dirname(__file__)
db_path = os.path.join(script_dir, '..', 'database', 'clima.db')
sql_script_path = os.path.join(script_dir, '..', 'database', 'sql', 'create_lote_composto_table.sql')

# Garante que o diretório do banco de dados exista
os.makedirs(os.path.dirname(db_path), exist_ok=True)

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    with open(sql_script_path, 'r') as f:
        sql_script = f.read()
        
    cursor.execute(sql_script)
    conn.commit()
    print(f"Tabela 'lote_composto' criada ou já existente em {db_path}")

    sql_script_amonia_path = os.path.join(script_dir, '..', 'database', 'sql', 'create_amonia_table.sql')
    with open(sql_script_amonia_path, 'r') as f:
        sql_script_amonia = f.read()
    cursor.execute(sql_script_amonia)
    conn.commit()
    print(f"Tabela 'amonia_data' criada ou já existente em {db_path}")

except sqlite3.Error as e:
    print(f"Erro ao criar o banco de dados ou tabela: {e}")
finally:
    if conn:
        conn.close()
