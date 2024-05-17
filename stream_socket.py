import os.path
from googleapiclient.discovery import build
import googleapiclient
# print(googleapiclient.__path__)
import __future__
# print(__future__.__all__)
import google
# print(google.__path__)

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import asyncio
import websockets
import json
# https://developers.google.com/sheets/api/quickstart/python
# https://developers.google.com/sheets/api/guides/values#python_3
# https://stackoverflow.com/questions/48056052/webbrowser-get-could-not-locate-runnable-browser
# https://stackoverflow.com/questions/75454425/access-blocked-project-has-not-completed-the-google-verification-process 
# Global Variables
# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# Used to hold your credentials for Google Auth
creds = None

# Holds the spreadsheet id that can be found in the URL for the spreadsheet you'd like to use.
twitch_spreadsheet_id = None

# Holds the range name that can be found in the spreadsheet you'd like to use.
twitch_range_name = None


# This funciton simply handles setting the users variables. We need a range name and a spreadsheet id to do anything.
def set_global_vars(check_for_creddies = False):
    global twitch_spreadsheet_id, twitch_range_name
    # https://www.w3schools.com/python/ref_func_all.asp

    # If user presses 3, we check for google creddies!
    if check_for_creddies:
        if os.path.exists("google_creddies"):
                with open('google_creddies', 'r') as f:
                    json_data = json.load(f)
                    twitch_spreadsheet_id = json_data['twitch_spreadsheet_id']
                    twitch_range_name = json_data['twitch_range_name']


    details_set = {
        'spread_id' : False,
        'range_name' : False,
        'exit': False,
    }
    data_to_send = {
    "twitch_spreadsheet_id": "",
    "twitch_range_name" : ""
    }
    # https://stackoverflow.com/questions/35253971/how-to-check-if-all-values-of-a-dictionary-are-0
    # all(value == 0 for value in your_dict.values())
    while all(value == True for value in details_set.values()) == False:
        set_personal_vars = input(f"""
        \nAlright, lets set these variables. If at any moment you are not sure, please, please read the documentation again! Remember, this applications goal is to WRITE to your google sheet, so it needs that permission! \n 
        [1] : {"SET my Spreadsheet ID." if twitch_spreadsheet_id == None else f"SPREAD ID = {twitch_spreadsheet_id}. CHANGE?" } 
        [2] : {"SET my SPREADSHEET RANGE." if twitch_range_name == None else f"RANGE = {twitch_range_name}. CHANGE?"} 
        [3] : Return 😎
        [4] : Continue 😎
        [5] : Exit 😎
        \n
        """)

        # https://stackoverflow.com/questions/24579896/how-to-update-a-json-file-by-using-python
        if set_personal_vars == '1':
            twitch_spreadsheet_id = input(f"Current SPREADSHEET_ID: {twitch_spreadsheet_id}. Please refer to docs if you're not sure what this is. \n \n")
            details_set['spread_id'] = True
            # print(f"The details_set spread id is now {details_set['spread_id'] }")
            data_to_send['twitch_spreadsheet_id'] = twitch_spreadsheet_id
            if os.path.exists("google_creddies"):
                with open('google_creddies', 'r') as f:
                    json_data = json.load(f)
                    json_data['twitch_spreadsheet_id'] = twitch_spreadsheet_id
                    
                with open('google_creddies', 'w') as f:
                    f.write(json.dumps(json_data))
            
        if set_personal_vars == '2':
            twitch_range_name = input(f"Current RANGE_NAME:{twitch_range_name}. Please refer to docs if you're not sure what this is. \n \n")
            details_set['range_name'] = True
            # print(f"The details_set range_name is now {details_set['range_name'] }")
            data_to_send['twitch_range_name'] = twitch_range_name
            if os.path.exists("google_creddies"):
                print('existed')
                with open('google_creddies', 'r') as f:
                    json_data = json.load(f)
                    json_data['twitch_range_name'] = twitch_range_name
                    
                with open('google_creddies', 'w') as f:
                    f.write(json.dumps(json_data))

        if set_personal_vars == '3':
            start_app()
        if set_personal_vars == '4':
            details_set['exit'] = True
            print("Creating your personal google JSON...")
            print("The Data to dump:", data_to_send)
            create_json(data_to_send, 'google_creddies')
            # 2: Whether or not a user finished setting their credentials in the app.
            start_app(ready_to_run = False, creds_set = True)
        if set_personal_vars == '5':
            quit()
    
# Function to authenticate with Google
# I didn't really end up needing this link, my goal was to see if there was a way I could grab something from InstalledAppFlow to launch the URL, but I may prefer the click.
# https://google-auth-oauthlib.readthedocs.io/en/latest/reference/google_auth_oauthlib.flow.html
# I'm leaving this in because it's funny. I worried about this for a solid 2 hours or so. Asked GPT what I could do, just for it to work FLAWLESSLY on desktop app. LOL.

# https://developers.google.com/sheets/api/quickstart/python
# I took what I needed from above and combined it with a batch update. Take what works you know? A lot of the commented stuff in here explains the creds variable and what scopes aims to do.
# Authenticate with google, also primarily taken from the quickstart python example. I took what worked and left out what didnt. In a standalone script with Virtual Studio Code, this works rather well. However here I'm having issues with it all broken apart and webbrowser? Not sure.
# Not 100000% certain what is happening under the hood of from authroized user file, creds, installedAppFlow, from_client_secrets_file either. I just know all of this together worked. If it breaks I'd start there. I tried something with installedAppFlow and accessing the url but Im moving on for various reasons now.
def google_authentication():
    global SCOPES, creds
    # urL='https://www.google.com'
    # chrome_path="C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
    # webbrowser.register('chrome', None,webbrowser.BackgroundBrowser(chrome_path))
    # webbrowser.get('chrome').open_new_tab(urL)
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
        print("\nChecking credentials validity...")
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
        print("Seeing this messsage means you were successfully able to authenticate with Google!")
        ready_to_run = True
        start_app(ready_to_run)
        
    """
    Creates the batch_update the user has access to.
    Load pre-authorized user credentials from the environment.
    TODO(developer) - See https://developers.google.com/identity
    for guides on implementing OAuth2 for the application.
    """

# --- Websocket Stuff --- #
# The fun stuff, this was primarily ripped from the python batchupdate example google had. I did some research, INSERT ROWs best option. Otherwise everything here was putting the proper things where they belong.
def append_my_clip(
      spreadsheet_id, range_name, value_input_option, insertDataOption, _values, creds
  ): 
  #creds, _ = google.auth.default()
  print("We're going to try and append your clip now...")
  try:
      print("Building the Google Sheets service...")
      service = build("sheets", "v4", credentials=creds)
      print("Connecting with sheet")
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

# A part of me would like to just start filming my devlopment process entirely so I can capture reaons I typed this. I was likely making changes with the server running, saving, and testing it in a websocket that was running old code.
# please, if you make changes to ur code, restart ur websocket LOL
# I was about to do some complicated things due to my limited understanding and everything.

# https://websockets.readthedocs.io/en/stable/faq/server.html#how-do-i-close-a-connection
# https://stackoverflow.com/questions/71618699/is-there-a-way-to-have-optional-arguments-in-a-function-in-python

# So we take use of the global variables. We send everything to append_my_clip and this is primarily used to give visual feedback of the data moving
async def twitchUploader(websocket):
    global twitch_spreadsheet_id, twitch_range_name, creds
    print("===================SERVER STARTED================")
    data = await websocket.recv()
    print(f"<<< {data}")
    clip_url, clip_time = data.split(" @ ", 1)
    print("SHOULD BE CLIP URL:", clip_url)
    print("SHOULD BE CLIP TIME:", clip_time)

    # Pass: spreadsheet_id, range_name value_input_option and _values)
    append_my_clip(
      twitch_spreadsheet_id,
      twitch_range_name,
      "USER_ENTERED",
      "INSERT_ROWS",
      [[clip_url, clip_time]],
      creds
    )

    greeting = f"\n ✅ YOUR DATA SHOULD BE DONE PROCESSING ✅!"
    await websocket.send(greeting)
    print(f">>> {greeting}")
    
# Run websocket infinitely,
async def mako_socket():
    print(""" \n Please wait a few seconds...""")
    async with websockets.serve(twitchUploader, "localhost", 8765):
        await asyncio.Future()  # run forever

# Start the websocket!
def run_websocket():
    asyncio.run(mako_socket())
# --- Websocket Stuff --- #


# One last check to start the Websocket.
def consent_to_websocket():
    running_web_socket = input("""
        Okay mate, everythings good, lets get this websocket running and then it'll be automated.\n
        [1] : Start Websocket
        [2] : Exit \n
    """)
    # data = {"example": "data"}
    if running_web_socket == '1':
        run_websocket()
    if running_web_socket == '2':
        quit()


# https://docs.python.org/2/library/functions.html#open
# Function to read a JSON file
def read_json(filename):
    with open(filename, 'r') as f:
        return json.load(f)
    # read_data = read_json('output.json')
    #     print("Read JSON data:", read_data)

# Function to write a JSON file
# w is to write file
def create_json(data, filename):
    with open(filename, 'w') as f:
        json.dump(data, f)

# Start app begins the CLI application and starts the process. A lot of ifs and while, but gets the job done.
def start_app(ready_to_run = False, creds_set = False):
    global twitch_spreadsheet_id, twitch_range_name


    # Holds whether or not the user would like to run the socket.
    run_socket = None

    # first time user to google being tracked
    first_to_google = None

    # First run ? Set to None as it's just holding options 1-3
    first_run = None

    # Holds the values such as spreadsheet id and range name
    start_var_inputs =  None

    # If the WEBSOCKET is not ready to run (by default it is not), skip this. Otherwise this handles taking us to the consent_to_websocket() function
    if ready_to_run != False:
        while run_socket not in ['1','2']:
            run_socket = input("""
                Okay, ready to run? \n
                [1] : Yes 
                [2] : No \n
                """)
            if run_socket == '1':
                consent_to_websocket()
            if run_socket == '2':
                quit()
    
    if creds_set == True:
        while first_to_google not in ['1','2',]:
            first_to_google = input("""
                Okay, ready to run? \n
                [1] : Yes 
                [2] : No \n
                """)
            if first_to_google == '1':
                google_authentication()
            if first_to_google == '2':
                pass

            
    # Otherwise, this is the function that will be ran first, we're in a loop for input until the user selects something 1-3.
    while first_run not in ['1','2','3','4']:
            first_run = input("""
            Hey qt3.14, first time running Mako.0 ? \n
            [1] : Yes 
            [2] : No, I have a credentials.json and the google_creddies already.
            [3] : Change my google_creddies
            [4] : Exit 😎 \n
            """)

            # If It's a users first time running this application, we'll go ahead and set up their spreadsheet_id and range_name. We'll need to make this create a json_dump or something, then read it. 
            # Selecting 1 takes you to the function (more inputs yay!)
            if first_run == '1':
                while start_var_inputs not in ['1','2']:
                    start_var_inputs = input(""" 
                    \n This applications uses some global variables (Remember math X = 2?), this variable is going to be unique to you, and local to you. \n We also set up some API keys. While this can be scary, rest assured that we can place limits and much more! \n
                    [1] : I'm ready! 
                    [2] : Exit 😎 \n
                    """)
                    # data = {"example": "data"}
                    if start_var_inputs == '1':
                        set_global_vars()
                    if start_var_inputs == '2':
                        quit()
                
            # If you've set up before, this ideally where i'd call a function that reads the json, returns it, and then sets the variables and proceeds to google authorization
            if first_run == '2':
                account_authed = input("""
                Sweet, what do you want to do? \n
                [1] : Run ! 🤖 ( You may still need to re-verify as my App is not verified with oogle )
                [2] : Exit 😎 \n
                """)
                if account_authed == '1':
                    data = read_json('google_creddies')
                    if data:
                        twitch_spreadsheet_id = data['twitch_spreadsheet_id']
                        twitch_range_name = data['twitch_range_name']
                    else:
                        print("Please make sure you didn't change the file name.")
                    google_authentication()
                if account_authed == '2':
                    quit()

            # Option 3 re-write their json
            if first_run == '3':
                set_global_vars(check_for_creddies=True)
            # Option 4 quit the application
            if first_run == '4':
                quit()


# https://stackoverflow.com/questions/21082037/when-making-a-very-simple-multiple-choice-story-in-python-can-i-call-a-line-to --- reminded me to do loop
# https://www.w3schools.com/python/python_operators.asp
# https://www.freecodecamp.org/news/python-do-while-loop-example/
# Holy cow haha this reminded me of isinstance() 
# https://stackoverflow.com/questions/2225038/determine-the-type-of-an-object

if __name__ == '__main__':

    # Just a little artwork for when the script starts.
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
    
    # Run start app and start application
    start_app()