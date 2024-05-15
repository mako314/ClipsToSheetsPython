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
import asyncio
import websockets


#####################
######
#Global Variables 
#######
#######
# https://developers.google.com/sheets/api/quickstart/python
# https://developers.google.com/sheets/api/guides/values#python_3
# https://stackoverflow.com/questions/48056052/webbrowser-get-could-not-locate-runnable-browser
# https://stackoverflow.com/questions/75454425/access-blocked-project-has-not-completed-the-google-verification-process 

chrome_path = None
creds = None


# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
# Current Spread Sheet ID 
# Testing Twitch Clips
# 1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE
# TWITCH_SPREADSHEET_ID = "1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE"
TWITCH_SPREADSHEET_ID = None
# TWITCH_RANGE_NAME = "A2:C16"
TWITCH_RANGE_NAME = None
creds_set = False
#######
#######
##############
#######
##############
#######
#######

def set_global_vars():
    global TWITCH_SPREADSHEET_ID, TWITCH_RANGE_NAME, chrome_path, creds_set
    # https://www.w3schools.com/python/ref_func_all.asp
    details_set = {
        'spread_id' : False,
        'range_name' : False,
        'chrome_path': False,
    }
    # https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0
    # all(value == 0 for value in your_dict.values())
    while all(value == True for value in details_set.values()) == False:
        set_personal_vars = input(f"""
        Alright, lets set these variables. If at any moment you are not sure, please, please read the documentation again! Remember, this applications goal is to WRITE to your google sheet, so it needs that permission!  
        [1] : {"I'm ready to set my SPREADSHEET ID." if TWITCH_SPREADSHEET_ID == None else "I need to CHANGE my SPREADSHEET ID variable." } 
        [2] : {"I'm ready to set my SPREADSHEET RANGE." if TWITCH_RANGE_NAME == None else "I need to CHANGE my SPREADSHEET RANGE variable." } 
        [3] : {"Some of us may get a chrome error. Lets be safe, we can set that variable too." if chrome_path == None else "I need to change my chrome variable." } 
        [4] : Return 😎
        [5] : Exit 😎
        """)

        if set_personal_vars == '1':
            TWITCH_SPREADSHEET_ID = input(f"This is your SPREADSHEET_ID: {TWITCH_SPREADSHEET_ID}. Please refer to docs if you're not sure what this is.")
            details_set['spread_id'] = True
            print(f"The details_set spread id is now {details_set['spread_id'] }")
        
        if set_personal_vars == '2':
            TWITCH_RANGE_NAME = input(f"This is your RANGE_NAME:{TWITCH_RANGE_NAME}. Please refer to docs if you're not sure what this is.")
            details_set['range_name'] = True
            print(f"The details_set range_name is now {details_set['range_name'] }")

        if set_personal_vars == '3': 
            chrome_path = input(f"This is your CHROME_PATH {chrome_path}. Please refer to docs if you're not sure what this is. It looks something like this \n C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe")
            details_set['chrome_path'] = True
            print(f"The details_set chrome_path is now {details_set['chrome_path'] }")
            
        if set_personal_vars == '4':
            pass
        
        if set_personal_vars == '5':
            quit()
    creds_set = True
    print("reached pause point")



# Function to read a JSON file
def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)

# Function to create a JSON file
# https://www.geeksforgeeks.org/json-dump-in-python/
# https://stackoverflow.com/questions/64196315/json-dump-into-specific-folder

# Function to authenticate with Google
# https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html
def google_authentication():
    global SCOPES, creds
    
    urL='https://www.google.com'
    chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
    webbrowser.get('chrome').open_new_tab(urL)
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        print("token.json exists, attempting to load credentials...")
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        print("Credentials loaded successfully.")
    else:
        print("token.json does not exist, proceeding to authenticate...")

    # If there are no (valid) credentials available, prompt the user to log in.
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

def testywesty():
    print('hello')

def append_my_clip(
      spreadsheet_id, range_name, value_input_option, insertDataOption, _values, creds
  ):
  
#   creds, _ = google.auth.default()
  print("We're going to try and append your clip now...")
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


# def do_some_work():
#     pass

# async def handler(websocket):
#     await do_some_work()


# https://wiki.streamer.bot/en/Servers-Clients/WebSocket-Server
# https://websockets.readthedocs.io/en/stable/
# https://learn.microsoft.com/en-us/dotnet/csharp/how-to/concatenate-multiple-strings
# https://docs.streamer.bot/api/csharp/core/websocket#WebsocketSend
# https://www.w3schools.com/python/ref_string_split.asp
# https://docs.python.org/2/library/stdtypes.html#str.split
# please, if you make changes to ur code, restart ur websocket LOL
# I was about to do some complicated things due to my limited understanding and everything.
# https://websockets.readthedocs.io/en/stable/faq/server.html#how-do-i-close-a-connection
async def twitchUploader(websocket):
    global TWITCH_SPREADSHEET_ID, TWITCH_RANGE_NAME, creds
    print("===================SERVER STARTED================.")
    data = await websocket.recv()
    print(f"<<< {data}")
    clip_url, clip_time = data.split(" @ ", 1)
    print("SHOULD BE CLIP URL:", clip_url)
    print("SHOULD BE CLIP TIME:", clip_time)

    testywesty()
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    append_my_clip(
      TWITCH_SPREADSHEET_ID,
      TWITCH_RANGE_NAME,
      "USER_ENTERED",
      "INSERT_ROWS",
      [[clip_url, clip_time]],
    #   [clip_url, clip_time],
      creds
    )

    greeting = f"Hello {data}!"

    await websocket.send(greeting)
    print(f">>> {greeting}")
    



async def mako_socket():
    print(" Hope this works ! @@@@@@@@@@@")
    async with websockets.serve(twitchUploader, "localhost", 8765):
        await asyncio.Future()  # run forever

def run_websocket():
    asyncio.run(mako_socket())

  

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
        if creds_set == False:
            first_run = input("""
            Hey qt3.14, first time running me?
            [1] : Yes 
            [2] : Mako please stop making me view this window
            [3] : Exit 😎
                            """)
            if first_run:
                intro = False

            if first_run == '1':
                start_var_inputs = input("""
                That's fine, but first and foremost, this applications uses some global variables (Remember math X = 2?), this variable is going to be unique to you, and local to you. While API keys can be scary, rest assured that we can place limits and much more!
                [1] : I'm ready! 
                [2] : Exit 😎
                """)
                # data = {"example": "data"}
                if start_var_inputs == '1':
                    set_global_vars()
                if start_var_inputs == '2':
                    quit()
                
                
            if first_run == '2' or creds_set == True:
                account_authed = input("""
        Sweet, what do you want to do?
        [1] : Run ! 🤖 
        [2] : Exit 😎
                        """)
                if account_authed == '1':
                    google_authentication()
                if account_authed == '2':
                    quit()

            if first_run == '3':
               quit()



        # Can use this data to send whatever is needed. Will need to look in Streamer.bot

        running_web_socket = input("""
            Okay mate, everythings good, lets get this websocket running and then it'll be automated.
            [1] : Start Websocket
            [2] : Exit
        """)
        # data = {"example": "data"}
        if running_web_socket == '1':
            run_websocket()
        if running_web_socket == '2':
            quit()
