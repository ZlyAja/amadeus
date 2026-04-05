<div align="center">
  <h1>Introducing "Amadeus"</h1>
  <p><i>Cool discord bot inspired by steins gate anime (i made ts just for fun btw n also learning purposes)</i></p>
  
  ![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)
  ![Discord.py](https://img.shields.io/badge/Discord.py-2.4.0-5865F2.svg)
  ![Groq](https://img.shields.io/badge/AI-Groq%20API-orange.svg)
  ![SQLite](https://img.shields.io/badge/Database-SQLite-lightgrey.svg)
</div>

## key features!
- **custom persona!!** users can inject their own personality into the bot via `/persona`.
- **daily quota limitation** Integrated sqlite database to limit daily chats (it will resets everyday btw)
- **context awareness!** it will remember the last 8 messages for context awareness!@!!!

## tech stack
- `discord.py` for discord api
- `groq` for llm model
- `sqlite3` for database handling 

## how to run?

1. **clone the repository:**
   ```bash
   git clone [https://github.com/ZlyAja/amadeus.git](https://github.com/ZlyAja/amadeus.git)
   cd amadeus

2. **install dependeencies:**
   ```bash
   pip install -r requirements.txt

3. **setting up env variables**
   ```bash
   DISCORD_TOKEN=your_discord_bot_token_here
   GROQ_API_KEY=your_groq_api_key_here
   
4. **run the bot**
   ```bash
   python main.py

## how to run it in docker

```bash
docker compose up -d --build
```

*the sqlite database is mapped as a volume, so ur data is safe during rebuilds!!!*
