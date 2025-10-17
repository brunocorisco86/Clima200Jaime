import sqlite3
import os
import glob
import re

class SQLScriptExecutor:
    def __init__(self, db_path, sql_directories):
        self.db_path = db_path
        self.sql_directories = sql_directories

    def _execute_single_script(self, cursor, sql_script_content, file_path):
        """
        Executes SQL statements from a given string content.
        """
        cursor.executescript(sql_script_content)

    def execute_scripts(self):
        """
        Runs SQL files from specified directories, prioritizing CREATE TABLE statements.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()

            create_statements_files = [] # Renamed to include views
            insert_data_files = []

            for sql_dir in self.sql_directories:
                for file_path in glob.glob(os.path.join(sql_dir, '*.sql')):
                    # Skip create_amonia_table.sql
                    if "create_amonia_table.sql" in os.path.basename(file_path):
                        print(f"Skipping {file_path} as requested.")
                        continue

                    with open(file_path, 'r') as f:
                        content = f.read()
                        if "CREATE TABLE" in content.upper() or "CREATE VIEW" in content.upper(): # Added CREATE VIEW
                            create_statements_files.append(file_path)
                        elif "INSERT INTO" in content.upper():
                            insert_data_files.append(file_path)
                        else:
                            print(f"Skipping {file_path}: Not a CREATE TABLE, CREATE VIEW or INSERT INTO script.")
            
            # Execute CREATE TABLE and CREATE VIEW statements first
            for file_path in create_statements_files:
                try:
                    with open(file_path, 'r') as f:
                        sql_script = f.read()
                    self._execute_single_script(cursor, sql_script, file_path)
                    conn.commit()
                    print(f"Successfully executed CREATE statement script: {file_path}")
                except sqlite3.Error as e:
                    print(f"Error executing CREATE statement script {file_path}: {e}")

            for file_path in insert_data_files:
                try:
                    with open(file_path, 'r') as f:
                        sql_script = f.read()
                    
                    if "INSERT INTO lote_composto" in sql_script:
                        sql_script = re.sub(r"INSERT INTO lote_composto", "INSERT OR IGNORE INTO lote_composto", sql_script, flags=re.IGNORECASE)
                        print(f"Modified INSERT statement for lote_composto in {file_path} to INSERT OR IGNORE INTO.")

                    self._execute_single_script(cursor, sql_script, file_path)
                    conn.commit()
                    print(f"Successfully executed INSERT INTO script: {file_path}")
                except sqlite3.Error as e:
                    print(f"Error executing INSERT INTO script {file_path}: {e}")

        except sqlite3.Error as e:
            print(f"SQLite error: {e}")
        finally:
            if conn:
                conn.close()

if __name__ == "__main__":
    # Example usage if run directly (for testing)
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    db_path = os.path.join(project_root, 'database', 'clima.db')
    sql_dirs = [
        os.path.join(project_root, 'database'),
        os.path.join(project_root, 'database', 'sql')
    ]
    
    # Ensure the database is clean for testing
    if os.path.exists(db_path):
        os.remove(db_path)

    executor = SQLScriptExecutor(db_path, sql_dirs)
    executor.execute_scripts()
