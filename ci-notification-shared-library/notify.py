import pandas as pd
import smtplib
from email.mime.text import MIMEText
import json
from jinja2 import Template

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

# Read the Excel file and extract data from a particular sheet
df1 = pd.read_excel('ci-notification-shared-library\DependencyMappingSheet.xlsx', sheet_name='SL01')
df2 = pd.read_excel('ci-notification-shared-library\DependencyMappingSheet.xlsx', sheet_name='UserData')

# Extract data from a specific column
dependent_microservices = df1['Shared Library-01']
filtered_df = df2[df2['Service name'].isin(dependent_microservices)]
user_ids = filtered_df['User-ID']

# Read the HTML template from the file
with open('ci-notification-shared-library\index.html') as f:
    template_str = f.read()

# Convert the column data to an HTML table
table_html = filtered_df.to_html(index=False)

# Replace the placeholder in the HTML template with the HTML table
html = template_str.replace('{table}', table_html)

# Compose the email message using the HTML template
#send_email(user_ids)

# Render the HTML template using Jinja2
template = Template(template_str)
html = template.render(services=dependent_microservices, table=table_html)

# Write the rendered HTML to a file
with open('index.html', 'w') as f:
    f.write(html)







