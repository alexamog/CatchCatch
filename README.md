<h1>Gacha Discord Bot for ACIT2515</h1>
 <h2>What it is</h2>
 <p>This application is a asynchronous discord bot that lets users in a discord server interact with via commands.</p>
 
 
<h2>Getting started</h2>

<h3>Creating a Discord API </h3>
<ol>
 <li>Sign in with your Discord credentials on <a href="https://discord.com">Discord</a> </li>
 <li>Go to the Discord <a href=https://discord.com/developers/applications">API page </a></li>
  <li> Click on new application and provide a name for your API </li>
  <li>Click on "Bot" on the left sidebar and create a bot</li>
  <li>Click "copy" under the Token section and add it to the .env file provided</li>
 </ol>
  
  <h3>Adding the Discord Bot into your server</h3>
  <p>Click on this link and replace "CLIENT_ID_HERE" with your bot's client ID.</p>
  https://discord.com/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=2048&scope=bot%20applications.commands


<h3>Installing dependencies </h3>
<ul>
  <li>Type in: "pip install -r requirements.txt" to install dependencies</li>
  </ul>
 
  <p>Once you have done all the steps above, in your terminal, you can now run the bot by typing in the command: python app.py</p>
