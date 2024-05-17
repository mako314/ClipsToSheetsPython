<!-- Improved compatibility of back to top link: See: https://github.com/othneildrew/Best-README-Template/pull/73 -->
<a name="readme-top"></a>
<!--
*** Thanks for checking out the Best-README-Template. If you have a suggestion
*** that would make this better, please fork the repo and create a pull request
*** or simply open an issue with the tag "enhancement".
*** Don't forget to give the project a star!
*** Thanks again! Now go create something AMAZING! :D
-->



<!-- PROJECT SHIELDS -->
<!--
*** I'm using markdown "reference style" links for readability.
*** Reference links are enclosed in brackets [ ] instead of parentheses ( ).
*** See the bottom of this document for the declaration of the reference variables
*** for contributors-url, forks-url, etc. This is an optional, concise syntax you may use.
*** https://www.markdownguide.org/basic-syntax/#reference-style-links
-->

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/mako314/ClipsToSheetsPython">
    <img src="https://github.com/mako314/ClipsToSheetsPython/assets/119079347/c58a8b3c-df07-4379-8980-5fc1fbf1f69a" alt="Twitch to Sheets" width="80" height="80">
  </a>

<h3 align="center"> Welcome to Clips to Sheets (Python v.0) </h3>

  <p align="center">
     Proud to introduce CipsToSheets (CTS), a simple python script solving a major problem. I undertook this project to help a few streamer clients and their editors.
     I try to write about most of my projects so I can avoid the hurdles on the run back.
     <br/>
     The application in itself will not have any major updates in the coming days, however I may update the readMe. I've made some proper documentation on how to use the app from a beginners standpoint.
    <br />
    <a href="https://github.com/mako314/ClipsToSheetsPython"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    ·
    <a href="https://github.com/mako314/ClipsToSheetsPython/issues/new?labels=bug&template=bug-report---.md">Report Bug</a>
    ·
    <a href="https://github.com/mako314/ClipsToSheetsPython/issues/new?labels=enhancement&template=feature-request---.md">Request Feature</a>
  </p>
</div>



<!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Pasted image 20240517103624](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/67243401-5e87-4c21-8770-b615ea8be172)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



### Built With

Built with Python 3.10.12

<!-- [Python]: https://img.shields.io/pypi/pyversions/Python%203.10.12?logo=python
[Python-url]: https://www.python.org/ -->


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- GETTING STARTED -->
## Getting Started 

This is an example of how you may give instructions on setting up your project locally.
To get a local copy up and running follow these simple example steps.



##### ONLY WINDOWS ATM EXE WISE 😢


### <a name="pre-req"> Prerequisites</a>

### Prerequisites

This setup was built using Python 3.10.12 on Windows 10 Home. It should yield similar results on compatible systems. If you requested the executable version, it will only work if we're on the same OS.

You will need a few tools for this specific setup:

1. **OBS Studio**
   - **Download and Setup**: Download [OBS Studio here](https://obsproject.com/). Create an account and follow the basic setup instructions.

2. **Twitch**
   - **Account Setup**: Set up a [Twitch account](https://www.twitch.tv/). This does not need to be the same email as your Google account. It will post to any Google Sheet as long as it is authorized to do so.

3. **Streamer.bot**
   - **Download**: Get [Streamer.bot](https://streamer.bot/) here. This was the preferred application used by a majority of clients for Google Sheets communication.

4. **Google Account**
   - **Account Creation**: Create a [Google account](https://support.google.com/accounts/answer/27441?hl=en).
   - **Google Developer Console**: Configure your [Google Developer Console](https://console.cloud.google.com/). Once logged in, your page should resemble the image below:
   ![Google Developer Console](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/99fa322c-8aaa-44ab-a2e8-84e36beb08e9)

   - **Create a Project**: Name it whatever you like and hit 'Create'.
   - **Configure Your Consent Screen**: 
     - Choose 'External' since 'Internal' requires an organization.
     - Fill out your application name.
     ![Consent Screen Setup](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/df45e5f9-345a-4d6f-bd93-756b74e65b59)
     - Developer contact information is required.
     - Scopes: This can be left empty if preferred.
     - **Test Users**: Very important to add your email (or the email hosting the Google Sheet) to the test users list for later adjustments.

#### Creating Credentials

To create OAuth credentials for your application, follow these steps:

1. **Navigate to the Dashboard**: From the Google Developer Console, click on 'Credentials' on the left-hand side menu.

2. **Create OAuth Client ID**:
   - Click on 'Create Credentials', then choose 'OAuth Client ID' from the options.
   - ![Create Credentials](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/5755d99e-d124-4145-ac17-b21ef84da971)
   - **Name Your Application & Application Type**: Enter a name for your OAuth client that will help you identify it later. Select 'Desktop' from the dropdown. This option is suited for applications running on a user's desktop.
   - ![Pasted image 20240516195817](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/07949c41-964d-4f95-9b83-4cfc5319eec8)

   

This sets up the authentication framework your application will use to interact with Google services.

3. **Download JSON**:
   - After creation, download the JSON file.
   - ![Pasted image 20240516195928](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/7abe3cba-d117-4cf8-9777-87e7b745a0f8)
   - The file name will look something like the image below. Rename it to `credentials`. Include `.json` if present in the original filename.
   - ![Pasted image 20240516200021](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/c6497c87-b54a-49ad-aa02-f0460034c25a)
   - Store it in the same folder as your repository or executable.




### <a name="install"> Installation</a>
1. **Make sure you've completed the (<a href="#pre-req"> prerequisites</a>)**
2. **Clone the repo**
   ```sh
   git clone https://github.com/mako314/ClipsToSheetsPython.git
   ```
3. 
   ```Run the script
   python3 script_name.py 
   python script_name.py 
   ```
4. **Grab your "spreadsheet id" and "named range / spread range"**
 
**Finding my Spreadsheet Id**:
   - First it'll help to explain what the spreadhseet is, and where exactly to find the ID.
   - ![Pasted image 20240516171035](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/9cca3f58-3f76-4d97-8365-0732bb36469c)
   -  So in the example below, our Spreadsheet Id is: 1sQ_IkgaJls2gpW4zBbSSfuzDnqjqyB_tJ_wIwgvvRHM
   - ![Pasted image 20240516190147](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/66ce0521-5e2d-4a68-8a09-a350c1c7729b)
   - Store it in the same folder as your repository or executable.


**Finding my range**:
- I know I specifically state range, but if you'd like a deeper understanding, this is what I'm actually requesting.
   - ![Pasted image 20240516171102](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/0b349353-ba3e-4eb5-b9ae-1ab85bab54e8)
   -  Setting the range you would like rows appended to is easy. You can just click and drag from where you'd like to start. In the example below I start at A2, and I drag my cursor all the way to the cell found in C16:
   - ![Pasted image 20240516171605](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/1410096f-83fc-4579-8ce9-da0bb31ba00a)
   - our **rangename** = A2:C16




 #### Okay, but what does that mean?
This is the area that we will be able to make changes to!

so for our example, these are our variables:
spreadsheetId = 1sQ_IkgaJls2gpW4zBbSSfuzDnqjqyB_tJ_wIwgvvRHM
rangeName = A2:C16

It's okay if you forget them, they're easy reacquire and are replaceable

<p align="right">(<a href="#readme-top">back to top</a>)</p>


<!-- USAGE EXAMPLES -->
## Usage


**Integrating with Streamerbot**:
- Easy way:
   -  Click Import > Paste into the import string box > Import > Close
   -  ```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```
   

   - ![image](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/3ff0a15c-9a40-4589-8d3f-41e188f120a7)
   - Import, close, and *ENABLE* the command

   
**With the Script Running**:
- If you haven't navigate to the Servers/Clients > Websocket Clients > Right Click the Existing One > Connnect (Optional: Enable auto and reconnect)
   - ![Pasted image 20240516192259](https://github.com/mako314/ClipsToSheetsPython/assets/119079347/310a41b7-77bb-4c63-aa76-fa4d9a620199)
   -  Setting the range you would like rows appended to is easy. You can just click and drag from where you'd like to start. In the example below I start at A2, and I drag my cursor all the way to the cell found in C16:

### While streaming and connected to the server, execute the command!


<!-- USAGE EXAMPLES -->
## Usage

### Timestamp In Use
<center>
<img src="https://github.com/mako314/ClipsToSheetsPython/assets/119079347/a3d9f529-7279-47cd-8707-e4a1b277a5fd" alt="Timestamp In Use GIF" width="60%"><br>
<strong>Description:</strong> This GIF demonstrates the practical application of timestamps within the system, showcasing how events are logged and tracked with precision.
</center>

### Random User Timestamp
<center>
<img src="https://github.com/mako314/ClipsToSheetsPython/assets/119079347/b0988669-9ae9-42f3-b641-0edb501693fb" alt="Random User Timestamp GIF" width="60%"><br>
<strong>Description:</strong> This GIF provides a visual walkthrough of a random user's timestamp data, highlighting how it appears and functions within the platform.
</center>

### Organize Clips By Time
<center>
<img src="https://github.com/mako314/ClipsToSheetsPython/assets/119079347/cbcf93db-6aa0-4312-897e-3321c978810b" alt="Organize Clips By Time GIF" width="60%"><br>
<strong>Description:</strong> Observe the organizational features of the system in this GIF, showcasing the methodical sorting of clips by their timestamps for enhanced navigation and efficiency.
</center>



_For more examples, please refer to the [Documentation](https://example.com)_

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ROADMAP -->
## Roadmap

- [ 1 ] Mac Support
- [ 2 ] Linux support
- [ 3 ] Add custom message with clip
    <!-- - [ 4 ] Nested Feature -->

See the [open issues](https://github.com/mako314/ClipsToSheetsPython/issues) for a full list of proposed features (and known issues).

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTRIBUTING -->
## Contributing

Originally I had intended for this project to remain private. However I've taken a turn in the world of building in public. That being said, this will remain free, forever. That being said, I wont't have as much time to maintain this as I'd like. I'm truly passionate about full stack development but I learned a tremendous amount in the development of this app. 

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. You can also simply open an issue with the tag "enhancement".
Don't forget to give the project a star! Thanks again!

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- CONTACT -->
## Contact

<!-- Your Name - [@twitter_handle](https://twitter.com/twitter_handle) - bispo.swe@gmail.com -->
Discord: makocodesnow
Email: Bispo.swe@gmail.com
Portfolio: [Macolister](https://macolister.com)
Project Link: [https://github.com/mako314/ClipsToSheetsPython](https://github.com/mako314/ClipsToSheetsPython)


<p align="right">(<a href="#readme-top">back to top</a>)</p>



<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Everyone over at Best-README-Template for the inspiration](https://github.com/othneildrew/Best-README-Template/graphs/contributors)
* [Lovely folks over at Self-Taught Devs for encouraging me to build in public (particularly episode 5 haha)](https://open.spotify.com/episode/5RSmtS2DOv07b3hWEbqfw4?si=338c35f783834de7)
* [streamer.bot, for having the perfect bot already made](https://streamer.bot/)


<p align="right">(<a href="#readme-top">back to top</a>)</p>
