# Import necessary libraries and modules
from mfrc522 import MFRC522
from servo import Servo
from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from mqtt import MQTTClient
import keys
import boot
import utime
import micropython

# Set up the display dimensions
WIDTH = 128
HEIGHT = 64

# Initialize the I2C interface and the SSD1306 OLED display
i2c=I2C(0,scl=Pin(17),sda=Pin(16),freq=400000)
oled = SSD1306_I2C(WIDTH,HEIGHT,i2c)

# Initialize the MFRC522 RFID reader
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

# Initialize the servo motor
s1 = Servo(0)
 


# Display initial instructions on the OLED screen
oled.fill(0) 
oled.text("Bring RFID TAG", 0, 0)
oled.text("Closer...", 0, 20)
oled.show()

# Callback function for MQTT subscription
def sub_cb(topic, msg):          
    print((topic, msg))          
    if msg == b"ON":
        # If message says "ON", update the OLED display and activate the servo
        oled.fill(0)             
        oled.text("Remote unlock", 0, 0)
        oled.text("Activated", 0, 20)
        oled.show()
        
        s1.goto(512)     # Move the servo to position 512        
        utime.sleep(5)
        s1.goto(0)    # Move the servo back to the original position           
        
        oled.fill(0) 
        oled.text("Bring RFID TAG", 0, 0)  
        oled.text("Closer...", 0, 20)
        oled.show()
                    
    elif msg == b"OFF":
         # If message says "OFF", move the servo to position 0
        s1.goto(0)                                
    else:
         # If any other message is received, print a message indicating an unknown message
        print("Unknown message") 
        

try:
    # Connect to Wi-Fi network and get the IP address
    ip = boot.connect(oled)
                
    # Connect to Adafruit IO using the MQTT protocol
    client = MQTTClient(keys.AIO_CLIENT_ID, keys.AIO_SERVER, keys.AIO_PORT, keys.AIO_USER, keys.AIO_KEY)

    # Set the callback function for MQTT subscriptions
    client.set_callback(sub_cb)
    client.connect()
    
    # Subscribe to a specific MQTT topic for remote unlock commands
    client.subscribe(keys.AIO_REMOTE_UNLOCK_FEED)
    print("Connected to %s, subscribed to %s topic" % (keys.AIO_SERVER, keys.AIO_REMOTE_UNLOCK_FEED))        
 
 
    while True:
        # Initialize the RFID reader    
        reader.init()
        
        # Request the ID of a RFID tag in the vicinity
        (stat, tag_type) = reader.request(reader.REQIDL)
        if stat == reader.OK:
            # If a tag is detected, select its serial number
            (stat, uid) = reader.SelectTagSN()
            if stat == reader.OK:
                # Convert the tag's serial number to an integer (card ID)
                card = int.from_bytes(bytes(uid),"little",False)
                
                if card == 2246669956:
                    # If the card ID matches a known authorized ID, update the OLED display,
                    # activate the servo, and publish a message to the dashboard
                    oled.fill(0)
                    oled.text("Card ID: ", 0, 0)    
                    oled.text(str(card), 0, 20)
                    oled.text("Authorized", 0, 40)
                    oled.show()
                    
                    s1.goto(512)
                    utime.sleep(5)
                    s1.goto(0)         # Servo goes back to original position after 5 seconds
                    
                    oled.fill(0) 
                    oled.text("Bring RFID TAG", 0, 0)    
                    oled.text("Closer...", 0, 20)
                    oled.show()
                    
                    client.publish(topic=keys.AIO_CARD_ID_FEED, msg=str("Unlocked by: 2246669956")) #Message to be sent to the dashboard
                    
                    
                    
                elif card == 865390835:
                    # If the card ID matches another known authorized ID, perform similar actions as above
                    oled.fill(0)
                    oled.text("Card ID: ", 0, 0)
                    oled.text(str(card), 0, 20)
                    oled.text("Authorized", 0, 40)
                    oled.show()
                    
                    s1.goto(512)
                    utime.sleep(5)
                    s1.goto(0)
                    
                    oled.fill(0) 
                    oled.text("Bring RFID TAG", 0, 0)
                    oled.text("Closer...", 0, 20)
                    oled.show()
                    
                    client.publish(topic=keys.AIO_CARD_ID_FEED, msg=str("Unlocked by: 865390835")) #Message to be sent to the Adafruit IO dashboard
                    
                    
                else:
                    # If the card ID is not authorized, display a message and publish to the dashboard
                    oled.fill(0)
                    oled.text("Card ID: ", 0, 0)
                    oled.text(str(card), 0, 20)
                    oled.text("Not Authorized", 0, 40)
                    oled.show()
                    utime.sleep(5)
                    oled.fill(0) 
                    oled.text("Bring RFID TAG", 0, 0)
                    oled.text("Closer...", 0, 20)
                    oled.show()
                    
                    client.publish(topic=keys.AIO_CARD_ID_FEED, msg=str("Attempted access by unauthorized card ID")) #Message to be sent to the Adafruit IO dashboard
                    
        # Check for any incoming MQTT messages        
        client.check_msg()
        

except KeyboardInterrupt:
    # Handle keyboard interrupt
    print("Keyboard interrupt")        

