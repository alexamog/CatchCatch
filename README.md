# CatchCatch

CatchCatch is a Discord gacha bot where players roll to collect virtual characters, build a collection, and compete for the highest point total. Characters are added by admins and drawn randomly from a shared pool.

---

## Project structure

```
CatchCatch/
├── app.py                  Entry point — starts the bot
├── requirements.txt        Python dependencies
├── .env                    Bot token (not committed)
├── cogs/
│   ├── user_commands.py    Player-facing commands
│   └── admin_commands.py   Admin-only commands
├── models/
│   └── characters.py       Character data model
└── database/
    ├── db.py               Shared data-access layer
    ├── character_db.json   Character state (auto-managed)
    └── user_db.json        Registered players (auto-managed)
```

---

## Setup

### 1. Create a Discord bot

1. Sign in at [discord.com](https://discord.com)
2. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
3. Click **New Application** and give it a name
4. Go to the **Bot** tab and click **Add Bot**
5. Under the **Token** section, click **Copy**

### 2. Configure the token

Paste your token into the `.env` file:

```
DISCORD_TOKEN=your_token_here
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Invite the bot to your server

Replace `CLIENT_ID_HERE` with your bot's application ID:

```
https://discord.com/oauth2/authorize?client_id=CLIENT_ID_HERE&permissions=2048&scope=bot%20applications.commands
```

### 5. Run the bot

```bash
python app.py
```

---

## Commands

### Player commands

| Command | Description |
|---|---|
| `!register` | Register your account to start playing |
| `!roll` | Roll for a random available character |
| `!discard [name]` | Return a character you own back to the pool |
| `!info [name]` | Look up a character's value and ownership status |
| `!collection` | View your characters and total points |
| `!available` | List all unclaimed characters |
| `!slap [@user]` | Slap another server member (easter egg) |

### Admin commands

These commands require the **Admin** role in your Discord server.

| Command | Description |
|---|---|
| `!create [name] [value]` | Add a new character to the gacha pool |

### Bot owner commands

| Command | Description |
|---|---|
| `!load [cog]` | Load a cog at runtime |
| `!unload [cog]` | Unload a cog at runtime |

---

## Notes

- Character names must contain only letters.
- Character values must be positive integers.
- Players must `!register` before they can `!roll`.
- If a character name already exists, `!create` will reject the duplicate.
