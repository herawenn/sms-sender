# SMS Sender

This is a Python script to send SMS messages using various SMS APIs including Twilio, Telnyx, Nexmo, or your own private gateway.

## Features

- Supports sending SMS messages using Twilio, Telnyx, Nexmo, and a private SMS gateway.
- Imports phone numbers from a file.
- Colorful and customizable banner display.

## Prerequisites

- Python 3.x
- Required Python packages: `pyfiglet`, `requests`, `termcolor`, `twilio`

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/sms-sender.git
    ```

2. Install the required Python packages:

    ```bash
    pip install pyfiglet requests termcolor twilio
    ```

## Usage

1. Run the script:

    ```bash
    python sms-sender.py
    ```

2. Enter the file path containing the list of phone numbers.
3. Choose an SMS API (Twilio, Telnyx, Nexmo, Private) by selecting the corresponding number.
4. Follow the prompts to enter API credentials, message body, and sender ID.
5. The script will send the SMS messages to the phone numbers listed in the file.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

