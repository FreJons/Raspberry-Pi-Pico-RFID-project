import ubinascii              # Conversions between binary data and various encodings
import machine                # To Generate a unique id from processor

# Wireless network
WIFI_SSID =  "SSID"
WIFI_PASS = "PASSWORD" 

# Adafruit IO (AIO) configuration
AIO_SERVER = "io.adafruit.com"
AIO_PORT = 1883
AIO_USER = "Username for Adafruit IO"
AIO_KEY = "Key from Adafruit IO"
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  
AIO_REMOTE_UNLOCK_FEED = "user/feeds/feedname"
AIO_CARD_ID_FEED = "user/feeds/feedname"