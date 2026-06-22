import nfl_data_py as nfl
import sqlite3
import os

def main():
    # 1. Define the years you want to analyze
    years = [2025,2024,2023]
    
    print(f"Fetching data for seasons: {years}...")
    
    # 2. Pull the play-by-play data
    # Note: cache=True helps speed this up if you run it multiple times
    pbp_data = nfl.import_pbp_data(years, cache=False)
    
    # 3. Connect to a local SQLite database
    # This will create 'nfl_data.db' in your project folder automatically
    db_path = 'nfl_data.db'
    conn = sqlite3.connect(db_path)
    
    # 4. Write the data to SQL
    # 'replace' means if the table exists, it will overwrite it with fresh data
    print("Writing to SQLite database...")
    pbp_data.to_sql('pbp_data', conn, if_exists='replace', index=False)
    
    # 5. Close the connection
    conn.close()
    print(f"Success! Data saved to {db_path}")

if __name__ == "__main__":
    main()