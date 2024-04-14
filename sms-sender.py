import sys
import pyfiglet
import requests
from termcolor import colored
from colorama import init
from twilio.rest import Client
import os


init(strip=not sys.stdout.isatty()) # strip colors if stdout is redirected

def print_banner():
    custom_fig = pyfiglet.Figlet(font='small', width=200)
    banner_text = custom_fig.renderText('\tPORTLORDS')
    banner = colored(banner_text, 'green', 'on_black', ['bold'])
    print(banner)
    sub_banner_text = "\t   https://t.me/mulicious\n\n"
    sub_banner = colored(sub_banner_text, 'green', 'on_black', ['bold'])
    print(sub_banner)

def send_sms_twilio(to, from_, body, client):
    message = client.messages \
                    .create(
                         body=body,
                         from_=from_,
                         to=to
                     )
    print(f"Message sent to {to} using Twilio")

def send_sms_telnyx(to, from_, body, auth_key):
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json', 'Authorization': f"Bearer {auth_key}"
    }

    messaging_profile_id = input("Enter the messaging profile ID: ")
    payload = {
        'to': to,
        'from': from_,
        'text': body, # added message content
        'messaging_profile_id': messaging_profile_id
    }
    response = requests.post("https://api.telnyx.com/v2/messages", headers=headers, json=payload)
    if response.status_code == 201:
        print(f"Message sent to {to} using Telnyx")
    else:
        print(f"Failed to send message to {to}. Error: {response.text}")


def send_sms_nexmo(to, from_, body, api_key, api_secret):
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'application/json'
    }
    payload = {
        'api_key': api_key,
        'api_secret': api_secret,
        'to': to,
        'from': from_,
        'text': body
    }
    response = requests.post('https://rest.nexmo.com/sms/json', headers=headers, data=payload)
    if response.status_code == 200:
        print(f"Message sent to {to} using Nexmo")
    else:
        print(f"Failed to send message to {to}. Error: {response.text}")


def send_sms_private(to, from_, body, key):

    payload = {
        'to': to,
        'body': body,
        'key': key,
        'from': from_,
    }

    response = requests.post("https://textbelt.com/text", json=payload)
    if response.status_code == 200:
        print(f"Message sent to {to}")
    else:
        print(f"Failed to send message to {to}. Error: {response.text}")


def import_numbers(file_path):
    with open(file_path, 'r') as file:
        numbers = file.readlines()
    return [number.strip() for number in numbers]
from termcolor import colored

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def main(file_path):
    clear_screen()
    print_banner()
    service = input(colored(" Please Choose an SMS API:\n\n [1]: Twilio\n [2]: Telnyx\n [3]: Nexmo\n [4]: Private\n", "green", attrs=["bold"]))
    if service == '1':
        account_sid = input("Enter your Twilio account SID: ")
        auth_token = input("Enter your Twilio Auth Token: ")
        client = Client(account_sid, auth_token)
        body = input("Enter Message Body: ")
        from_ = input("Enter Sender ID: ")
        numbers = import_numbers(file_path)
        for number in numbers:
            send_sms_twilio(number, from_, body, client)
    elif service == '2':
        auth_key = input("Enter your Telnyx API Key: ")
        body = input("Enter Message Body: ")
        from_ = input("Enter Sender ID: ")
        numbers = import_numbers(file_path)
        for number in numbers:
            send_sms_telnyx(number, from_, body, auth_key)
    elif service == '3':
        api_key = input("Enter your Nexmo API Key: ")
        api_secret = input("Enter your Nexmo API Secret: ")
        body = input("Enter Message Body: ")
        from_ = input("Enter Sender ID: ")
        numbers = import_numbers(file_path)
        for number in numbers:
            send_sms_nexmo(number, from_, body, api_key, api_secret)
    elif service == '4':
        key = input("Enter your Textbelt API Key: ")
        body = input("Enter Message Body: ")
        from_ = input("Enter Sender ID: ")
        numbers = import_numbers(file_path)
        for number in numbers:
            send_sms_private(number, from_, body, key)
    else:
        print("Invalid input, please choose a valid option (1-4)")

if __name__ == '__main__':
    file_path = input("Enter file path containing list of phone numbers: ")
    main(file_path)
