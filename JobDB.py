import cx_Oracle
import os

# Define the Oracle wallet location
wallet_location = r"C:\Users\mekhi\Downloads\Wallet_JobMarketAnalysisDB2"

# Set the TNS_ADMIN environment variable to the wallet location
os.environ['TNS_ADMIN'] = wallet_location

# Connect to the Oracle Autonomous Database using the TNS alias from tnsnames.ora
try:
    connection = cx_Oracle.connect(
        user="Admin",
        password="Mekhiavery2004",
        dsn="jobmarketanalysisdb2_high",  # Use the alias defined in tnsnames.ora
        encoding="UTF-8"
    )
    print("Successfully connected to Oracle Autonomous Database")
    
    # You can start working with the database here
    cursor = connection.cursor()

except cx_Oracle.DatabaseError as e:
    print(f"An error occurred: {e}")

finally:
    if 'connection' in locals():
        connection.close()
