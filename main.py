# Dependencies
import discord
from discord import app_commands
from discord.ext import commands
import db, ai, json, os
from dotenv import load_dotenv

load_dotenv()
db.init_db()

max_quota = 25 # rate limit per day

class AmadeusBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        await self.tree.sync()

bot = AmadeusBot()

# Slash commands

@bot.tree.command(name="persona", description="Change the Amadeus personality")
async def persona(interaction: discord.Interaction, description: str):
    db.update_user(interaction.user.id, persona=description, history='[]')
    
    # creating embed message
    embed = discord.Embed(
        title="🎭 Persona Configuration",
        description=f'Persona has been configured!',
        color=discord.Color.green()
    )
    embed.set_footer(text="-# sorry but memory has been wiped out for the synchronization 💔🥀")
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="status", description="Check your Amadeus profiles & quota")
async def status(interaction: discord.Interaction):
    data = db.get_user(interaction.user.id)

    # creating embed message
    embed = discord.Embed(
        title=f'👤 Your Amadeus Status',
        color=discord.Color.dark_gray()
    )

    embed.add_field(
        name="Daily Quota",
        value=f"{data['daily_count']} / {max_quota}",
        inline = True
    )

    embed.add_field(
        name="Persona",
        value=data['persona'],
        inline = False
    )

    embed.set_footer(
        text="Quota will resets every day"
    )

    await interaction.response.send_message(embed=embed)

# Chatbot

@bot.event
async def on_message(message):
    if message.author.bot: 
        return

    is_mentioned = bot.user in message.mentions
    is_reply = message.reference and message.reference.resolved and message.reference.resolved.author == bot.user

    if is_mentioned or is_reply:
        print(f"🎯 triggered from {message.author}!")
        user_data = db.get_user(message.author.id)

        # 1. Cek Kuota
        if user_data['daily_count'] >= max_quota:
            print("🚫 quota limit reached.")
            embed = discord.Embed(
                title="💀 Quota Limit",
                description="Try again tommorrow.",
                color=discord.Color.red()
            )
            return await message.reply(embed=embed)

        clean_text = message.content.replace(f'<@!{bot.user.id}>', '').replace(f'<@{bot.user.id}>', '').strip()
        if not clean_text:
            return

        async with message.channel.typing():
            try:
                print("🧠 calling the groq api...")
                history = json.loads(user_data['history'])
                
                answer = await ai.ask_amadeus(user_data['persona'], history, clean_text)

                # Updating the database
                history.append({"role": "user", "content": clean_text})
                history.append({"role": "assistant", "content": answer})

                db.update_user(
                    message.author.id,
                    daily_count=user_data['daily_count'] + 1,
                    history=json.dumps(history[-8:])
                )

                footer = f"\n\n-# [daily: {user_data['daily_count'] + 1}/{max_quota}] | ID: {message.author.id}"
                await message.reply(f"{answer}{footer}")
                print("✅ message succesfully sent.")

            except Exception as e:
                print(f"❌ err: {e}")
                await message.reply(f'system is overload {e}')
# ~

bot.run(os.getenv('DISCORD_TOKEN'))
print("amadeus stopped!")