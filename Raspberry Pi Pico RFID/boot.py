# Import necessary libraries
import keys
import network
from time import sleep




# Function to connect to Wi-Fi network
def connect(oled):
    # Create a WLAN object
    wlan = network.WLAN(network.STA_IF)
    
    if not wlan.isconnected():
        # If not connected to Wi-Fi, display a message on the OLED screen
        oled.fill(0)
        oled.text("Connecting to", 0, 0)
        oled.text("Network", 0, 20)
        oled.show()
        
        wlan.active(True)  # Activate the WLAN interface                     
        
        wlan.config(pm = 0xa11140)  # Configure power management
        wlan.connect(keys.WIFI_SSID, keys.WIFI_PASS) # Connect to the Wi-Fi network
        print('Waiting for connection...', end='')
        
        # Check if it is connected otherwise wait
        while not wlan.isconnected() and wlan.status() >= 0:
            print('.', end='')
            sleep(1)
    
    ip = wlan.ifconfig()[0] # Get the IP address of the network connection
    
    # Display the IP address on the OLED screen
    oled.fill(0)
    oled.text("Connected on: ", 0, 0)
    oled.text("{}".format(ip), 0, 20)
    oled.show()
    
    sleep(5) # Wait for 5 seconds
    
    oled.fill(0) 
    oled.text("Bring RFID TAG", 0, 0)
    oled.text("Closer...", 0, 20)
    oled.show()
    
    return ip  # Return the IP address

# Function to disconnect from the Wi-Fi network
def disconnect():
    wlan = network.WLAN(network.STA_IF)         
    wlan.disconnect()
    wlan = None 