import discord
import json
import asyncio
from colorama import Fore, Style, init

init(autoreset=True)

with open('config.json') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
SERVER_ID = int(config['server_id'])
ROLE_ID = int(config['role_id'])

intents = discord.Intents.default()
intents.members = True  # Enable member intent to fetch members

client = discord.Client(intents=intents)

async def assign_role_to_member(member, role):
    if role not in member.roles and not member.bot:
        try:
            await member.add_roles(role)
            print(f"{Fore.GREEN}Assigned role to {member.display_name}")
        except discord.Forbidden:
            print(f"{Fore.RED}Permission error for {member.display_name}")
        except discord.HTTPException as e:
            print(f"{Fore.YELLOW}Failed to assign role to {member.display_name}: {e}")

@client.event
async def on_ready():
    print(f'{Fore.CYAN}Logged in as {client.user}')
    guild = client.get_guild(SERVER_ID)
    
    if not guild:
        print(f"{Fore.RED}Bot is not in the server with ID: {SERVER_ID}")
        return
    
    role = guild.get_role(ROLE_ID)
    if not role:
        print(f"{Fore.RED}Role with ID {ROLE_ID} not found.")
        return

    # Start the loop to periodically check and assign roles
    client.loop.create_task(periodic_role_assignment(guild, role))

@client.event
async def on_member_join(member):
    guild = member.guild
    if guild.id == SERVER_ID:
        role = guild.get_role(ROLE_ID)
        if role:
            await assign_role_to_member(member, role)

async def periodic_role_assignment(guild, role):
    while True:
        print(f"{Fore.BLUE}all members got the role already uwu..waiting for new members")
        human_members = [member for member in guild.members if not member.bot]
        
        if not human_members:
            print(f"{Fore.CYAN}No human members to assign roles to. Waiting for new people to join...")

        for member in human_members:
            await assign_role_to_member(member, role)

        await asyncio.sleep(600)  # Wait 10 minutes before checking again

client.run(TOKEN)
