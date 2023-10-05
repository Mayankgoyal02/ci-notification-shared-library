import pandas as pd
from jinja2 import Environment, FileSystemLoader
from datetime import datetime

# Read the SMTP server configuration from the JSON file
# with open('config.json') as f:
#     config = json.load(f)

# Store the SMTP server configuration as variables
# smtp_server = config['SMTP_SERVER']
# smtp_port = config['SMTP_PORT']
# smtp_username = config['SMTP_USERNAME']
# smtp_password = config['SMTP_PASSWORD']
# sender_email = config['SENDER_EMAIL']

# Function to send email notifications
# def send_email(user_ids):
#     # Compose the email message
#     msg = MIMEText('Hello, this is a test email.')
#     msg['Subject'] = 'Test email'
#     msg['From'] = sender_email
#     msg['To'] = ', '.join(user_ids)

    # Connect to the SMTP server and send the email message
    # with smtplib.SMTP(smtp_server, smtp_port) as smtp:
    #     smtp.starttls()
    #     smtp.login(smtp_username, smtp_password)
    #     smtp.send_message(msg)

    # print('Email sent successfully.')

# Define the Excel file name
excel_file = 'ci-notification-shared-library\DependencyMappingSheet.xlsx'  # Change this to your Excel file's name


# Load data from the "SL01" and "userdata" sheets into DataFrames
try:
    sl01_df = pd.read_excel(excel_file, sheet_name='SL01', engine='openpyxl')
    userdata_df = pd.read_excel(excel_file, sheet_name='UserData', engine='openpyxl')
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit(1)

# Check if the required columns exist in the DataFrames
if 'Shared Library-01' not in sl01_df.columns:
    print("Required column 'Shared Library-01' not found in the 'SL01' sheet.")
    exit(1)

if 'Service name' not in userdata_df.columns or 'User-ID' not in userdata_df.columns:
    print("Required columns 'Service name' and 'User-ID' not found in the 'UserData' sheet.")
    exit(1)

# Create a dictionary to store the mapping of Service Name to User ID
service_to_user_mapping = {}

# Populate the dictionary by iterating through the "userdata" DataFrame
for index, row in userdata_df.iterrows():
    service_name = row['Service name']
    user_id = row['User-ID']
    service_to_user_mapping[service_name] = user_id

# Load the HTML template from the template.html file
template_loader = FileSystemLoader(searchpath='./')
env = Environment(loader=template_loader)
template = env.get_template('ci-notification-shared-library/index.html')

# Create a dictionary with Service Name and User ID separated by full stops
data_dict = {}
for service_name in sl01_df['Shared Library-01']:
    user_id = service_to_user_mapping.get(service_name, '')
    data_dict[service_name] = user_id

# Render the template with the data
rendered_html = template.render(data_dict=data_dict)

# Generate a unique file name with a timestamp
build_number = datetime.now().strftime("%Y%m%d%H%M%S")
output_file_name = f"output_{build_number}.html"

# Save the rendered HTML to the unique output file
with open(output_file_name, 'w', encoding='utf-8') as output_file:
    output_file.write(rendered_html)

print(f"HTML file '{output_file_name}' generated successfully.")
