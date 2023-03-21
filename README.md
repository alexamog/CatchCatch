# CatchCatch
## Introduction
CatchCatch is a bot that operates on Discord's platform and utilizes an asynchronous design to enable smooth and efficient user interactions. The primary function of the bot is to facilitate virtual number rolls, which give users a chance to win rare characters in the context of the game or activity that the bot is being used for. The rarity of the characters available for winning is predetermined and varies based on the specific game or activity that the bot is being used for.

# Getting started

## Creating a Discord API
<ol>
 <li>Sign in with your Discord credentials on <a href="https://discord.com">Discord</a> </li>
 <li>Go to the Discord <a href=https://discord.com/developers/applications>API page </a></li>
  <li> Click on new application and provide a name for your API </li>
  <li>Click on "Bot" on the left sidebar and create a bot</li>
  <li>Click "copy" under the Token section and add it to the .env file provided</li>
 </ol>
  
  ### Adding the CatchCatch into your server</h3>
  Click on this link and replace "CLIENT_ID_HERE" with your bot's client ID.
  https://discord.com/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=2048&scope=bot%20applications.commands


### Installing dependencies
<ul>
  <li>Type in: "pip install -r requirements.txt" to install dependencies</li>
  </ul>
 
  Once you have done all the steps above, in your terminal, you can now run the bot by typing in the command: python app.py
