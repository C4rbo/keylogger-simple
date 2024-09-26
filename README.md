# Keylogger-Simple

A simple keylogger written in Python, designed for educational purposes and to demonstrate how keylogging and encryption work together. This keylogger captures both keyboard inputs and mouse movements, encrypts the log files, and sends them via email. It is intended for ethical testing, privacy research, or security analysis purposes only.

## Features

- **Keyboard and Mouse Logging**: Records every key pressed and logs mouse movements with timestamps.
- **Encryption with RSA and Fernet**: The logs are encrypted using a symmetric key (Fernet), which is then encrypted using RSA for added security.
- **Log Compression**: The encrypted log files are compressed into a ZIP file for easier storage and sending.
- **Email Integration**: Automatically sends encrypted logs to a configured email address periodically.
- **RSA Key Generation**: Automatically generates RSA key pairs if they don’t already exist.
- **Threaded Log Sending**: Log files are sent in the background every hour without interrupting the keylogging process.

## Installation

To get started, clone the repository and navigate into the project directory:

```bash
git clone https://github.com/yourusername/keylogger-simple.git
cd keylogger-simple
```

### Dependencies

Before running the script, install the required libraries using pip:

```bash
pip install cryptography pynput keyboard pyautogui
```

These libraries are necessary for cryptographic functions, input logging, and other utilities.

## Configuration

Edit the script to configure the email settings for sending logs. Replace the placeholders with your actual email credentials:

```python
emailUser = 'insertEmail'
emailPass = 'insertPassword'
emailRecipient = 'insertEmailRecipient'
```

These settings will allow the keylogger to send logs to the specified email address.

## Usage

Run the script using Python 3 to start logging keyboard and mouse events.

```bash
python keyloggerSimple.py
```

The program will generate a log file (`myLogFile.txt`) which contains all the captured keypresses and mouse movements. Every hour, the log will be encrypted, compressed, and sent to the configured email address. The original log file will be deleted afterward.

### Example Output

```
2024-09-26 14:23:05 - [KEY] a
2024-09-26 14:23:07 - [KEY] s
2024-09-26 14:23:09 - [MOUSE] Moved to (450, 200)
2024-09-26 14:23:12 - [MODIFIER] SHIFT
2024-09-26 14:23:13 - [SPECIAL] SPACE
```

## Legal Disclaimer

**Use responsibly and legally.** This tool is designed for educational purposes and ethical security research only. Unauthorized keylogging of any system is illegal and unethical. Always obtain explicit permission from the system owner before using this tool.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

## Contributing

Contributions are welcome! If you have suggestions for improvements, new features, or find bugs, please open an issue or submit a pull request on GitHub.

## Author

- C4rbo (https://github.com/C4rbo)