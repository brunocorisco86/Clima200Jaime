import os
import sqlite3
from src.process_csv_data import CSVProcessor
from src.populate_db import DBPopulator
from src.execute_sql_files import SQLScriptExecutor
from src.export_summarized_data import DataExporter # New import

def main():
    # Define paths
    project_root = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(project_root, 'database', 'clima.db')
    csv_directory = os.path.join(project_root, 'data', 'raw', 'exportEprodutorIOT')
    sql_directories = [
        os.path.join(project_root, 'database'),
        os.path.join(project_root, 'database', 'sql')
    ]
    processed_data_directory = os.path.join(project_root, 'data', 'processed') # New path

    # 1. Delete clima.db if it exists
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f"Deleted existing database: {db_path}")

    # 2. Process CSV data
    print("Processing CSV data...")
    csv_processor = CSVProcessor(csv_directory)
    csv_processor.process_files()
    print("CSV data processing complete.")

    # 3. Populate database from processed CSVs
    print("Populating database from CSVs...")
    db_populator = DBPopulator(db_path, csv_directory)
    db_populator.populate()
    print("Database population from CSVs complete.")

    # 4. Execute SQL files (CREATE TABLE, CREATE VIEW, INSERT)
    print("Executing SQL files...")
    sql_executor = SQLScriptExecutor(db_path, sql_directories)
    sql_executor.execute_scripts()
    print("SQL file execution complete.")

    # 5. Export summarized data from views
    print("Exporting summarized data...")
    data_exporter = DataExporter(db_path, processed_data_directory)
    data_exporter.export_all_summarized_data()
    print("Summarized data export complete.")

    print("All tasks completed successfully!")

if __name__ == "__main__":
    main()