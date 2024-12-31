# SMS Sender

A Python script to send SMS messages using the Textbelt API.

![image](https://i.imgur.com/Dezm3bM.png)

## Features

- Supports sending SMS messages using the Textbelt API.
- Colorful and customizable banner display.
- Supports sending single and mass SMS messages.
- Configurable via environment variables.

## Prerequisites

- Python 3.x
- Required Python packages: `aiohttp`, `colorama`, `python-dotenv`

## Installation

1. Clone this repository:

    ```bash
    git clone https://github.com/your_username/sms-sender.git
    ```

2. Install the required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

## Configuration

Create a `.env` file in the root directory of the project and add the following environment variables:

API_KEY1=your_api_key_1
API_KEY2=your_api_key_2
API_KEY3=your_api_key_3
RATE_LIMIT=10
RETRY_POLICY=3
TIMEOUT_DURATION=10
DEFAULT_SENDER_NAME=your_default_sender_name

## Usage

1. Run the script:

    ```bash
    python sms.py
    ```

2. Choose an option from the main menu:
    - `1`: SMS Menu
    - `0`: Quit

3. In the SMS Menu, choose an option:
    - `1`: Send a Single SMS
    - `2`: Send a Mass SMS
    - `0`: Main Menu

4. Follow the prompts to enter the target phone number, message body, sender ID, and optional file URL.

5. The script will send the SMS messages using the Textbelt API.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
