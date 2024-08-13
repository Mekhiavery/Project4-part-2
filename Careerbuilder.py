import cx_Oracle
from bs4 import BeautifulSoup
import os
from itertools import zip_longest

# Path to your CareerBuilder HTML file
file_path = r'C:\Users\mekhi\Downloads\CareerBuilder.html'

# Load the HTML content of CareerBuilder page
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Extract job titles
job_titles = [job.get_text().strip() for job in soup.find_all('div', class_='data-results-title')]

# Extract company names
company_names = [company.get_text().strip() for company in soup.find_all('span', class_='data-details')]

# Extract locations
locations = [location.get_text().strip() for location in soup.find_all('div', class_='data-location')]

# Extract salaries (if available)
salaries = [salary.get_text().strip() for salary in soup.find_all('div', class_='data-salary')]  # Adjust the class name based on the actual HTML structure

# Set the TNS_ADMIN environment variable to the wallet location
wallet_location = r"C:\Users\mekhi\Downloads\Wallet_JobMarketAnalysisDB2"
os.environ['TNS_ADMIN'] = wallet_location

# Initialize the cursor and connection variables
cursor = None
connection = None

# Connect to the Oracle database
try:
    connection = cx_Oracle.connect(
        user="Admin",
        password="Mekhiavery2004",
        dsn="jobmarketanalysisdb2_high",  # Use the alias defined in tnsnames.ora
        encoding="UTF-8"
    )
    cursor = connection.cursor()

    # Insert data into the database
    for title, company, location, salary in zip_longest(job_titles, company_names, locations, salaries, fillvalue=None):
        cursor.execute("""
            INSERT INTO job_listings (job_title, company_name, location, salary)
            VALUES (:1, :2, :3, :4)
        """, (title, company, location, salary))

    # Commit the transaction
    connection.commit()

    print("Data inserted successfully!")

except cx_Oracle.DatabaseError as e:
    print(f"Database connection error: {e}")
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()

# Combine extracted data for output
print("\nJob Listings and Details:\n")
for title, company, location, salary in zip_longest(job_titles, company_names, locations, salaries, fillvalue='N/A'):
    print(f"Job Title: {title}")
    print(f"Company: {company}")
    print(f"Location: {location}")
    print(f"Salary: {salary}")
    print("---")
