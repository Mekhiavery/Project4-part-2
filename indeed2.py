from bs4 import BeautifulSoup
import cx_Oracle
import os

# Update the file path to the correct location
file_path = r'C:\Users\mekhi\Downloads\Indeed.html'  # Update this path to the actual location of your file

# Load the HTML content of the Indeed page
with open(file_path, 'r', encoding='utf-8') as file:
    content = file.read()

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(content, 'html.parser')

# Replace with the correct classes used in your HTML
company_class = 'company-name'
location_class = 'location-class-name'
salary_class = 'salary-class-name'

# Extract job titles
job_titles = [job.get_text().strip() for job in soup.find_all('h2', class_='jobTitle')]
print(f"Extracted {len(job_titles)} job titles: {job_titles}")

# Extract company names (if they exist)
company_names = [company.get_text().strip() for company in soup.find_all('span', class_=company_class)]
print(f"Extracted {len(company_names)} company names: {company_names}")

# Extract locations (if they exist)
locations = [location.get_text().strip() for location in soup.find_all('div', class_=location_class)]
print(f"Extracted {len(locations)} locations: {locations}")

# Extract salaries (if they exist)
salaries = [salary.get_text().strip() for salary in soup.find_all('div', class_=salary_class)]
print(f"Extracted {len(salaries)} salaries: {salaries}")

# Set the TNS_ADMIN environment variable to the wallet location
wallet_location = r"C:\Users\mekhi\Downloads\Wallet_JobMarketAnalysisDB2"
os.environ['TNS_ADMIN'] = wallet_location

# Initialize the cursor and connection variables
cursor = None
connection = None

# Connect to the Oracle database
try:
    # Use the alias from the tnsnames.ora file
    connection = cx_Oracle.connect(
        user="Admin",
        password="Mekhiavery2004",
        dsn="jobmarketanalysisdb2_high",  # Use the alias defined in tnsnames.ora
        encoding="UTF-8"
    )
    cursor = connection.cursor()

    # Insert data into the database
    for i in range(len(job_titles)):
        job_title = job_titles[i]
        company_name = company_names[i] if i < len(company_names) else None
        location = locations[i] if i < len(locations) else None
        salary = salaries[i] if i < len(salaries) else None

        # Insert the data
        cursor.execute("""
            INSERT INTO job_listings (job_title, company_name, location, salary)
            VALUES (:1, :2, :3, :4)
        """, (job_title, company_name, location, salary))

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
print("\nJob Listings and Salaries:\n")
for i in range(len(job_titles)):
    print(f"Job Title: {job_titles[i]}")
    if i < len(company_names):
        print(f"Company Name: {company_names[i]}")
    if i < len(locations):
        print(f"Location: {locations[i]}")
    if i < len(salaries):
        print(f"Salary: {salaries[i]}")
    print("---")
