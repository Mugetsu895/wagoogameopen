import requests
import json
import webbrowser
import os
import time
from colorama import init, Fore

# Initialize colorama to support colored text in the console
init()

# Set to keep track of opened links
opened_links = set()


def retrieve_latest_message(channel_id, token):
    headers = {
        'authorization': token
    }
    params = {
        'limit': 1
    }
    r = requests.get(f'https://discord.com/api/v8/channels/{channel_id}/messages', headers=headers, params=params)
    messages = json.loads(r.text)

    if not isinstance(messages, list) or len(messages) == 0:
        return

    latest_message = messages[0]  # The latest message is the first in the list

    embeds = latest_message.get('embeds')
    if embeds:
        for embed in embeds:
            if 'roblox.com/catalog/' in embed.get('url', '') and embed.get('type') == 'rich':
                if 'in-game only' not in embed.get('description', '').lower():  # Check if "experience" is in the description
                    roblox_url = embed.get('url')
                    if roblox_url and roblox_url not in opened_links:
                        opened_links.add(roblox_url)  # Add the link to the set
                        message_to_send = "Opened a link: " + roblox_url
                        print(f"{Fore.CYAN}{message_to_send}{Fore.RESET}")
                        open_in_browser('roblox://experiences/start?placeId=975820487')



    content = latest_message.get('content')
    if content and 'roblox.com/catalog/' in content:
        if 'in-game only' not in content.lower():  # Check if "experience" is in the content text
            roblox_links = find_roblox_links(content)
            for roblox_url in roblox_links:
                if roblox_url and roblox_url not in opened_links:
                    opened_links.add(roblox_url)
                    message_to_send = "Opened a link: " + roblox_url
                    print(f"{Fore.CYAN}{message_to_send}{Fore.RESET}")
                    open_in_browser('roblox://experiences/start?placeId=975820487')

def open_in_browser(url):
    webbrowser.open(url, new=0, autoraise=True)

def find_roblox_links(text):
    import re
    return re.findall(r'https?://(?:www\.)?roblox\.com/catalog/\d+', text)

def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
            return config
    except FileNotFoundError:
        print("Config file 'config.json' not found.")
        return None
    except json.JSONDecodeError:
        print("Invalid JSON format in 'config.json'.")
        return None

def main():
    config = load_config()
    if config is None:
        return

    channel_id = config.get('channel_id')
    token = config.get('bot_token')

    if not channel_id or not token:
        print("Missing required variables in 'config.json'.")
        return

    # Clear the console and print "The bot is working, there's just nothing to open" in yellow
    os.system('cls' if os.name == 'nt' else 'clear')
    print(f"{Fore.CYAN}Autosearch V2 is working, there's just nothing to open.{Fore.RESET}")

    # Set the loop to run indefinitely with a 0.2 seconds wait
    while True:
        retrieve_latest_message(channel_id, token)
        time.sleep(0.2)

if __name__ == "__main__":
    main()
