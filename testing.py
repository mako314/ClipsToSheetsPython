import os.path
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import os
import sys
import webbrowser    
from google.oauth2 import service_account
import json

#####################
######
#Global Variables 
#######
#######
# https://developers.google.com/sheets/api/quickstart/python
# https://developers.google.com/sheets/api/guides/values#python_3
# https://stackoverflow.com/questions/48056052/webbrowser-get-could-not-locate-runnable-browser
urL='https://www.google.com'
chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
webbrowser.get('chrome').open_new_tab(urL)

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
# Current Spread Sheet ID 
# Testing Twitch Clips
# 1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE
TWITCH_SPREADSHEET_ID = "1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE"
TWITCH_RANGE_NAME = "A2:C16"
#######
#######
##############
#######
##############
#######
#######




def justRan():
   pass
# Function to create a JSON file
# https://www.geeksforgeeks.org/json-dump-in-python/
# https://stackoverflow.com/questions/64196315/json-dump-into-specific-folder
def create_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Function to read a JSON file
def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to authenticate with Google

def append_my_clip(
      spreadsheet_id, range_name, value_input_option, insertDataOption, _values
  ):
  print("Script is starting...")

  """Shows basic usage of the Sheets API.
  Prints values from a sample spreadsheet.
  """
  
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.

  if os.path.exists("token.json"):
    print("token.json exists, attempting to load credentials...")
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    print("Credentials loaded successfully.")
  else:
    print("token.json does not exist, proceeding to authenticate...")

  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    print("Checking credentials validity...")
    if creds and creds.expired and creds.refresh_token:
      print("Credentials expired, refreshing...")
      creds.refresh(Request())
      print("Credentials refreshed.")
    else:
      print("No valid credentials, need to authenticate...")
      flow = InstalledAppFlow.from_client_secrets_file(
          "credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
      print("Authentication completed, credentials obtained.")
    # Save the credentials for the next run
    with open("token.json", "w") as token:
      token.write(creds.to_json())
      print("Credentials saved for next run.")

    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    # print("Building the Google Sheets service...")
  try:
      print("Building the Google Sheets service...")
      service = build("sheets", "v4", credentials=creds)
      print("Connecting with sheet")
      values = [
          [
              # Cell values ...
          ],
          # Additional rows
      ]

      print("Values being appended:", _values)
      body = {"values": _values}
      print("Request body:", body)
      result = (
          service.spreadsheets()
          .values()
          .append(
            spreadsheetId=spreadsheet_id, 
            range=range_name,
            valueInputOption=value_input_option,
            insertDataOption=insertDataOption,
            body=body)
          .execute()
      )
      print(f"{(result.get('updates').get('updatedCells'))} cells appended.")
      print("API Response:", result)
      return result
  except Exception as error:
      print(f"An error occurred: {error}")
      return error
  

# https://stackoverflow.com/questions/21082037/when-making-a-very-simple-multiple-choice-story-in-python-can-i-call-a-line-to --- reminded me to do loop
# https://www.w3schools.com/python/python_operators.asp
# https://www.freecodecamp.org/news/python-do-while-loop-example/
# Holy cow haha this reminded me of isinstance() 
# https://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
if __name__ == '__main__':
    exit = False
    intro = True
    while exit == False:
        if intro == True:
            print( """
                                |               ___       #   ___      
                    )))         |.===.         /\#/\      #  <_*_>     
                    (o o)        {}o o{}       /(o o)\     #  (o o)     
                ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo--8---(_)--Ooo-
                        
                ▄▀▀▄ ▄▀▄  ▄▀▀█▄   ▄▀▀▄ █  ▄▀▀▀▀▄  
                █  █ ▀  █ ▐ ▄▀ ▀▄ █  █ ▄▀ █      █ 
                ▐  █    █   █▄▄▄█ ▐  █▀▄  █      █ 
                █    █   ▄▀   █   █   █ ▀▄    ▄▀ ▄
                ▄▀   ▄▀   █   ▄▀  ▄▀   █    ▀▀▀▀   
                █    █    ▐   ▐   █    ▐           
                ▐    ▐            ▐                
                                |               ___       #   ___      
                    )))         |.===.         /\#/\      #  <_*_>     
                    (o o)        {}o o{}       /(o o)\     #  (o o)     
                ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo--8---(_)--Ooo-
        """)
            
        first_run = input("""
        Hey qt3.14, first time running me?
        [1] : Yes 
        [2] : Mako please stop making me view this window
        [3] : Exit 😎
                        """)
        if first_run:
            intro = False

            if first_run == '1':
                print('Basic CLI incorported?')




        # Can use this data to send whatever is needed. Will need to look in Streamer.bot
        data = {"example": "data"}
        create_json(data, 'output.json')
        print("Created JSON file")

        read_data = read_json('output.json')
        print("Read JSON data:", read_data)

        # creds = google_authenticate()
        print("Authenticated with Google")















# # Function to get the path to the credentials file
# def get_credentials_path(filename):
#     # Check if the script is running as a bundled executable
#     if getattr(sys, 'frozen', False):
#         # If running as a bundle, the PyInstaller bootloader sets sys._MEIPASS
#         base_path = sys._MEIPASS
#     else:
#         # If running in a normal Python environment
#         base_path = os.path.dirname(os.path.abspath(__file__))

#     return os.path.join(base_path, filename)