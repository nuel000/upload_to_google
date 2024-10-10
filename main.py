import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas as pd
import os
import json
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google.oauth2 import service_account

def scrape_lagos_time():
    url = 'https://www.timeanddate.com/worldclock/nigeria/lagos'
    r = requests.get(url)
    s = BeautifulSoup(r.content, 'html.parser')
    time_now = s.find('div', class_='bk-focus__qlook').find('span', class_='h1').text
    return time_now

def append_to_sheet(df):
    # Load credentials from the environment variable
    creds_json = os.environ.get('GOOGLE_SHEETS_CREDENTIALS')
    creds_dict = json.loads(creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict)

    # Build the Sheets API service
    service = build('sheets', 'v4', credentials=creds)

    # Your Google Sheet ID
    SHEET_ID = '1Es7yGQ5FN_233-MYQHacjlBfZpq45kbp7Gcdzc6DFAY'

    # Prepare the data
    data = df.values.tolist()

    # Specify the range where you want to append the data
    range_name = 'Sheet1!A:B'  # This will append to the first empty row in columns A and B

    # Prepare the value range object
    value_range_body = {
        'values': data
    }

    # Make the API call to append the data
    request = service.spreadsheets().values().append(
        spreadsheetId=SHEET_ID,
        range=range_name,
        valueInputOption='USER_ENTERED',
        body=value_range_body
    )
    response = request.execute()

    print(f"Data appended successfully. {response.get('updates').get('updatedCells')} cells updated.")

def main():
    # Scrape the time
    current_time = scrape_lagos_time()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Create a DataFrame
    df = pd.DataFrame({'timestamp': [timestamp], 'time_now': [current_time]})
    
    # Upload to Google Sheets
    append_to_sheet(df)

if __name__ == "__main__":
    main()
