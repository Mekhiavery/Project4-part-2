from bs4 import BeautifulSoup
import cx_Oracle
import os

# Path to your LinkedIn HTML file
file_path = r'C:\Users\mekhi\Downloads\Linkedin.html'

# Load the HTML content of the LinkedIn page
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Lists to store extracted data
job_titles = []
company_names = []
locations = []

# Loop through each job card
for job_card in soup.find_all('div', class_='base-search-card__info'):
    # Extract job title
    title_tag = job_card.find('h3', class_='base-search-card__title')
    title = title_tag.get_text().strip() if title_tag else 'N/A'
    job_titles.append(title)
    
    # Extract company name
    company_tag = job_card.find('a', class_='hidden-nested-link')
    company = company_tag.get_text().strip() if company_tag else 'N/A'
    company_names.append(company)
    
    # Extract location
    location_tag = job_card.find('span', class_='job-search-card__location')
    location = location_tag.get_text().strip() if location_tag else 'N/A'
    locations.append(location)

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
    for i in range(len(job_titles)):
        cursor.execute("""
            INSERT INTO job_listings (job_title, company_name, location)
            VALUES (:1, :2, :3)
        """, (job_titles[i], company_names[i], locations[i]))

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

# Combine extracted data for output (optional)
print("\nJob Listings and Details:\n")
for i in range(len(job_titles)):
    print(f"Job Title: {job_titles[i]}")
    print(f"Company: {company_names[i]}")
    print(f"Location: {locations[i]}")
    print("---")
