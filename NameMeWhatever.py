import os.path
import google.auth
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import asyncio
import json
import websockets


# https://developers.google.com/sheets/api/quickstart/python
# https://developers.google.com/sheets/api/guides/values#python_3
# https://stackoverflow.com/questions/48056052/webbrowser-get-could-not-locate-runnable-browser
import webbrowser    

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
  except HttpError as error:
      print(f"An error occurred: {error}")
      return error
   

# https://wiki.streamer.bot/en/Servers-Clients/WebSocket-Server
# https://websockets.readthedocs.io/en/stable/


async def twitchUploader(websocket):
    print("===================SERVER STARTED================.")
    name = await websocket.recv()
    print(f"<<< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")

async def main():
    async with websockets.serve(twitchUploader, "localhost", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())


# if __name__ == "__main__":
#   # Pass: spreadsheet_id, range_name value_input_option and _values)
#   append_my_clip(
#       TWITCH_SPREADSHEET_ID,
#       TWITCH_RANGE_NAME,
#       "USER_ENTERED",
#       "INSERT_ROWS",
#       [["F", "B"], ["C", "D"]],
#   )