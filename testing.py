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
import webbrowser    
from google.oauth2 import service_account
import asyncio
import websockets



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
# 1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE
# Testing Twitch Clips
# twitch_spreadsheet_id = "1jy-WrBstbUP_BJ8-5l41mIYBgZr-SGmJeGTkZdZJ-QE"
# twitch_range_name = "A2:C16"
twitch_spreadsheet_id = None
twitch_range_name = None
sheet_creds_set = False
# ready_to_run = False

def start_app():
    pass

def set_global_vars():
    global twitch_spreadsheet_id, twitch_range_name, sheet_creds_set
    # https://www.w3schools.com/python/ref_func_all.asp
    details_set = {
        'spread_id' : False,
        'range_name' : False,
    }
    # https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0
    # all(value == 0 for value in your_dict.values())
    while all(value == True for value in details_set.values()) == False:
        set_personal_vars = input(f"""
        Alright, lets set these variables. If at any moment you are not sure, please, please read the documentation again! Remember, this applications goal is to WRITE to your google sheet, so it needs that permission!  
        [1] : {"SET my Spreadsheet ID." if twitch_spreadsheet_id == None else f"SPREAD ID = {twitch_spreadsheet_id}. CHANGE?" } 
        [2] : {"SET my SPREADSHEET RANGE." if twitch_range_name == None else f"RANGE = {twitch_range_name}. CHANGE?"} 
        [3] : Return 😎
        [4] : Exit 😎
        """)

        if set_personal_vars == '1':
            twitch_spreadsheet_id = input(f"Current SPREADSHEET_ID: {twitch_spreadsheet_id}. Please refer to docs if you're not sure what this is. \n")
            details_set['spread_id'] = True
            # print(f"The details_set spread id is now {details_set['spread_id'] }")
        
        if set_personal_vars == '2':
            twitch_range_name = input(f"Current RANGE_NAME:{twitch_range_name}. Please refer to docs if you're not sure what this is. \n")
            details_set['range_name'] = True
            # print(f"The details_set range_name is now {details_set['range_name'] }")

        if set_personal_vars == '3':
            start_app()
        
        if set_personal_vars == '4':
            quit()
    sheet_creds_set = True
    print("reached pause point")




# Function to authenticate with Google
# https://www.geeksforgeeks.org/json-dump-in-python/
# https://stackoverflow.com/questions/64196315/json-dump-into-specific-folder
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

        print("Seeing this messsage means you were succesfully able to authenticate with Google!")
        ready_to_run = True
        start_app(ready_to_run)
        



    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """
    # creds, _ = google.auth.default()
    # pylint: disable=maybe-no-member
    # print("Building the Google Sheets service...")






# --- Websocket Stuff --- #
def append_my_clip(
      spreadsheet_id, range_name, value_input_option, insertDataOption, _values, creds
  ): 
  #creds, _ = google.auth.default()
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
    global twitch_spreadsheet_id, twitch_range_name, creds
    print("===================SERVER STARTED================.")
    data = await websocket.recv()
    print(f"<<< {data}")
    clip_url, clip_time = data.split(" @ ", 1)
    print("SHOULD BE CLIP URL:", clip_url)
    print("SHOULD BE CLIP TIME:", clip_time)

    # testywesty()
    # Pass: spreadsheet_id, range_name value_input_option and _values)
    append_my_clip(
      twitch_spreadsheet_id,
      twitch_range_name,
      "USER_ENTERED",
      "INSERT_ROWS",
      [[clip_url, clip_time]],
    #   [clip_url, clip_time],
      creds
    )

    greeting = f"Hello I've got your data. Lets get to processing it now!"
    await websocket.send(greeting)
    print(f">>> {greeting}")
    
async def mako_socket():
    print(" Hope this works ! @@@@@@@@@@@")
    async with websockets.serve(twitchUploader, "localhost", 8765):
        await asyncio.Future()  # run forever

def run_websocket():
    asyncio.run(mako_socket())
# --- Websocket Stuff --- #

def consent_to_websocket():
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

def start_app(ready_to_run = False):
    # global ready_to_run

    run_socket = None
    first_run = None
    start_var_inputs =  None

    if ready_to_run != False:
        while run_socket not in ['1','2',3]:
            run_socket = input("""
                Okay, ready to run? \n
                [1] : Yes 
                [2] : No
                """)
            if run_socket == '1':
                consent_to_websocket()
            if run_socket == '2':
                quit()
            

    while first_run not in ['1','2','3']:
            if sheet_creds_set == False:
                first_run = input("""
                Hey qt3.14, first time running Mako.0 ?
                [1] : Yes 
                [2] : No, I have a credentials.json already.
                [3] : Exit 😎
                """)

                if first_run == '1':
                    while start_var_inputs not in ['1','2']:
                        start_var_inputs = input("""
                        That's fine. \n This applications uses some global variables (Remember math X = 2?), this variable is going to be unique to you, and local to you. \n We also set up some API keys. While this can be scary, rest assured that we can place limits and much more!
                        [1] : I'm ready! 
                        [2] : Exit 😎
                        """)
                        # data = {"example": "data"}
                        if start_var_inputs == '1':
                            set_global_vars()
                        if start_var_inputs == '2':
                            quit()
                    
                    
                if first_run == '2' or sheet_creds_set == True:
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





# https://stackoverflow.com/questions/21082037/when-making-a-very-simple-multiple-choice-story-in-python-can-i-call-a-line-to --- reminded me to do loop
# https://www.w3schools.com/python/python_operators.asp
# https://www.freecodecamp.org/news/python-do-while-loop-example/
# Holy cow haha this reminded me of isinstance() 
# https://stackoverflow.com/questions/2225038/determine-the-type-of-an-object
if __name__ == '__main__':
    # exit = False
    # first_run = None
    # start_var_inputs =  None
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
            █    █    ▐   ▐   █    ▐           . 0
            ▐    ▐            ▐                
                            |               ___       #   ___      
                )))         |.===.         /\#/\      #  <_*_>     
                (o o)        {}o o{}       /(o o)\     #  (o o)     
            ooO--(_)--Ooo-ooO--(_)--Ooo-ooO--(_)--Ooo--8---(_)--Ooo-
    """)
    start_app()