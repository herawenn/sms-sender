import os
import aiohttp
import asyncio
import logging
import traceback
from colorama import init, Fore, Style
import dotenv

dotenv.load_dotenv()

logging.basicConfig(filename='logs.log', level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

init()
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
P = Fore.MAGENTA
C = Fore.CYAN
X = Fore.RESET

banner = f"""
  ___ __  __ ___   ___ ___ _  _ ___  ___ ___
 / __|  \\/  / __| / __| __| \\| |   \\| __| _ \\
 \\__ \\ |\\/| \\__ \\ \\__ \\ _|| .` | |) | _|| /
 |___/_|  |_|___/ |___/___|_|\\_|___/|___|_|_\\

              From {G}PortLords{X} w Love © 2024
"""

def get_env_var(var_name, default=None, var_type=str):
    value = os.getenv(var_name, default)
    try:
        return var_type(value)
    except (ValueError, TypeError):
        logging.error(f"Invalid or missing environment variable: {var_name}")
        return default

api_keys = [
    get_env_var("API_KEY1", var_type=str),
    get_env_var("API_KEY2", var_type=str),
    get_env_var("API_KEY3", var_type=str)
]

RATE_LIMIT = get_env_var("RATE_LIMIT", 10, int)
RETRY_POLICY = get_env_var("RETRY_POLICY", 3, int)
TIMEOUT_DURATION = get_env_var("TIMEOUT_DURATION", 10, int)
DEFAULT_SENDER_NAME = get_env_var("DEFAULT_SENDER_NAME", var_type=str)

async def send_sms(target, message, sender_name=None, file_url=None, max_retries=3, api_keys=None):
    if api_keys is None:
        api_keys = []

    for key in api_keys:
        retries = 0
        while retries < max_retries:
            try:
                url = "https://textbelt.com/text"
                payload = {
                    "phone": target,
                    "message": message,
                    "key": key,
                }
                if sender_name:
                    payload["sender"] = sender_name
                if file_url:
                    payload["mediaUrl"] = file_url

                async with aiohttp.ClientSession() as session:
                    async with session.post(url, json=payload, timeout=TIMEOUT_DURATION) as response:
                        if response.status == 200:
                            response_data = await response.json()
                            if response_data.get("success"):
                                return True, f"Message to {target} sent successfully! Key: {key}"
                            else:
                                logging.error(f"Message send failed: {response_data.get('error')}")
                                return False, f"Message send failed: {response_data.get('error')}"

                        else:
                            logging.error(f"API request failed with status code: {response.status}")
                            retries += 1
                            await asyncio.sleep(2 ** retries)

            except aiohttp.ClientError as e:
                logging.warning(f"Network error: {e}")
                retries += 1
                await asyncio.sleep(2 ** retries)
            except Exception as e:
                logging.error(f"An unexpected error occurred: {e}")
                return False, f"An unexpected error occurred."

    return False, "All keys exhausted or failed."

def get_choice(prompt, valid_choices):
    while True:
        choice = input(prompt).strip()
        if choice in valid_choices:
            return choice
        print("Invalid choice. Please try again.")

def get_int_input(prompt, min_value, max_value):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value <= value <= max_value:
                return value
            print(f"Please enter a number between {min_value} and {max_value}.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")

async def sms_menu():
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print(banner)
        print(f"{P}[{G}1{P}]{X} Send a Single SMS")
        print(f"{P}[{G}2{P}]{X} Send a Mass SMS")
        print(f"{P}[{G}0{P}]{X} Main Menu")
        print()
        choice = get_choice("\nChoose: ", ['1', '2', '0'])

        if choice == '1':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            target = input("Target Phone Number: ")
            message = input("Message: ")
            sender = input("Sender Name (optional, leave blank for default): ") or DEFAULT_SENDER_NAME
            file_url = input("File URL (optional): ")
            success, result = await send_sms(target, message, sender_name=sender, file_url=file_url, api_keys=api_keys)
            print(result)

        elif choice == '2':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            target = input("Target Phone Number: ")
            message = input("Message: ")
            sender = input("Sender Name (optional, leave blank for default): ") or DEFAULT_SENDER_NAME
            number = get_int_input("Number of Messages: ", 1, RATE_LIMIT)

            tasks = []
            for i in range(number):
                tasks.append(send_sms(target, message, sender_name=sender, api_keys=[api_keys[i % len(api_keys)]]))

            results = await asyncio.gather(*tasks)
            for success, result in results:
                print(result)

        elif choice == '0':
            return

async def main():
    while True:
        try:
            os.system('cls' if os.name == 'nt' else 'clear')
            print(banner)
            print(f"{P}[{G}1{P}]{X} SMS Menu")
            print(f"{P}[{G}0{P}]{X} Quit")
            print()
            choice = get_choice("Choose an option: ", ['1', '0'])

            if choice == '1':
                await sms_menu()
            elif choice == '0':
                print("Exiting program.")
                break
            else:
                print("Invalid choice. Try again.")

        except Exception as e:
            logging.error(f"Unexpected error in main: {e}\n{traceback.format_exc()}")
            print("An unexpected error occurred in the main menu. Please try again later.")

if __name__ == "__main__":
    asyncio.run(main())
