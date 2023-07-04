## Tutorial on how to build an RFID scanner with a servo lock using MQTT, Adafruit & Webhooks to transmit and visualize data over the internet

Author: Fredrik Jonsson
Student ID: fj222un



### Overview
In this project we will build an RFID scanner that uses a servo as a locking device. When authorized cards/tags are presented to the RFID scanner the servo will unlock, if the card/tag is not authorized nothing will happen. Info about the card ID, authorization and unauthorized access will be sent to a platform where it is visualized and logged. A remote unlock feature will also be implemented via the platform. Locally the info as stated above will be presented on a small oled screen. Lastly a webhook is used to send notifications about authorized, remote and unauthorized access to a discord server. 
The estimated time to complete this tutorial is roughly 8-10 hours.

### Objective
I want a box, a secure box. A box that lets me know who is accessing it and when. The 'secure' part is so that I can store belongings such as passports, jewelry or maybe the TV remote. That way I wont find my kids looking at weird youtube videos in the morning.
Since I want to send data about card/tag ID, log the scans and the failed access attempts I think it will give insight as to who is opening the box and how often it is used. Therefore a proven use case will present itself over time, if there is one. 


### Material
The microcontroller used in this project is the [Raspberry Pi Pico WH](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html). It has built in wifi , (2,4 GHz), capabilities which will be essential for this build. It also comes with 26 × multi-function GPIO pins, some of which we'll need.

To be able to scan our tags and cards we will need an RFID scanner-module. In this case we'll be using the [RFID-RC522](https://components101.com/wireless/rc522-rfid-module) sensor.

Our locking function will be provided by a servo motor. In this case it is the [SG90 micro servo](https://components101.com/motors/servo-motor-basics-pinout-datasheet).

For the local visualization of the card/tag ID:s, access type, and remote unlocks we will use the [SSD 1306 OLED](https://datasheethub.com/ssd1306-128x64-mono-0-96-inch-i2c-oled-display/) screen.

Since all this is to be mounted in a box we'll need some kind of battery. I used this [battery pack](https://www.netonnet.se/art/nosection/andersson-prb-2-8-15-000-mah-blackgrey/1002025.5149/). This particular model is no longer available to buy but the important thing is that the output is 5V & 2.1A max.

To connect all of this we'll need a standard large breadboard, jumper cables and a micro USB to be able to flash our Pico.

See the table below for price information about the various components:



| Image                                                  | Material             | Price (SEK) |
| ------------------------------------------------------ | -------------------- | ----------- |
| ![](https://hackmd.io/_uploads/SJK4u7qOn.jpg =150x120) | Raspberry Pi Pico WH | 109 SEK     |
| ![](https://hackmd.io/_uploads/Hyj6u7qOh.jpg =150x120) | RFID-RC522           | 229 SEK     |
| ![](https://hackmd.io/_uploads/S1WTslidh.jpg =150x150) | SG90 Servo           | 49 SEK      |
| ![](https://hackmd.io/_uploads/SyxGalj_2.jpg =150x150) | SSD 1306 OLED        | 107 SEK     |
| ![](https://hackmd.io/_uploads/HJH0alj_3.jpg =150x120) | Battery Pack         |~350 SEK     |
| ![](https://hackmd.io/_uploads/S1pS1-sO2.jpg =150x120) | Breadboard           | 69 SEK      |
| ![](https://hackmd.io/_uploads/Bk_AyWsdn.jpg =150x120) | Jumper cables        | 49 SEK      |
| ![](https://hackmd.io/_uploads/SJTz--jdh.jpg =150x120) | Micro USB Cable      | 19 SEK      |
                                                  

### Computer Setup
I chose to do this project in the [Thonny IDE](https://thonny.org/), download it via the link provided. After that we will have to install the micropython firmware on the Pico. To do this first connect the usb cable into the Pico. Then, while holding the BOOTSEL button, connect the other end of the usb to your computer.
In the bottom right corner of the Thonny IDE the current version of python is shown. Click on it and select "MicroPython (Raspberry Pi Pico)". After this a popup window will appear that wants you to install the latest version of the Micropython Firmware. Click install and you should be good to go after that. 
When you click 'save as' a popup window will ask you where you want to save the code.
Make sure that you save your code onto the Raspberry Pi Pico and not the computer. This is important for the program to be able to run on the Pico on its own. Also it is important that you name the main program file 'main.py' as this ensures that it'll run on its own on the pico once powered up. To run the program while developing/connected to the computer simply press the play button in Thonny.


### Putting everything together
All the connections are shown in the diagram below:

![](https://hackmd.io/_uploads/SJQ1zzou2.jpg)

The VCC (pin 36) & GND (pin 38) connections are made at the top two rows of the breadboard.

Connecting the RFID RC522:


| RC522    | Pico     |
| -------- | -------- |
|    SDA   |   Pin 7  |
|    SCK   |   Pin 9  |
|    MOSI  |   Pin 10 |
|    MISO  |  Pin 6   |
|   GND    | GND on breadboard         |
|    RST   | Pin 29   |
|  VCC     | VCC on breadboard     |


Connecting the Oled:


| Oled     | Pico     |
| -------- | -------- |
|   GND       |  GND on breadboard        |
|   VDD       |  VCC on breadboard        |
|   SCK     |  Pin 19        |
|   SDA     | Pin 20     |


Connecting the servo:



| Servo    |   Pico   |
| -------- | -------- |
|VCC (Red) | VCC on breadboard         |
|GND (Black)  |GND on breadboard          |
| PWM     | Pin 1    |


### Platform

I have chosen the Adafruit platform for this project. The reason being that it is very user friendly and straight forward. In other words, perfect for beginners.
Start with making an account on [adafruit IO](https://io.adafruit.com/). After that we'll need to figure out what we want to send/receive. In this case we want to be able to send data from our Pico to the adafruit IO platform so that the logins can be visualized. We also want to receive data from the platform so that we can unlock the box remotely.
For this we will need to set up two feeds. We'll call them "Remote unlock" and "card id". Follow this [link](https://learn.adafruit.com/adafruit-io-basics-feeds/creating-a-feed) to learn how to set up a feed in adafruit IO.

### The code
We are going to utilize several libraries. These include the library for the SSD1306 oled screen, RFID RC522 scanner, SG90 servo and the library for the MQTT protocol. For decluttering purposes we'll be separating the different libraries into the 'lib' folder.

The images below show the filestructure:

![](https://hackmd.io/_uploads/BJ5ms9eY2.png)

And the files in the 'lib' folder:

![](https://hackmd.io/_uploads/B1Zis9xK2.png)

Furthermore we are going to break out the code that handles the wifi connection into a separate file called 'boot.py'. 



![](https://hackmd.io/_uploads/r1E79O-Fh.png)



The 'main.py' file contains the rest of the code that handles all the functionality. Below is a snippet that shows the connection to Adafruit IO using MQTT, handling of subscriptions, setup of the RFID scanner and the loop that contains the authorized card ID:s.

![](https://hackmd.io/_uploads/ry8mW5WFh.png)





There are two files in the 'lib' folder that I haven't mentioned. The 'keys' file contains all the necessary info, such as the configuration of Adafruit. This includes port number, information about feeds, IO key, etc. It also contains the SSID and password credentials to the wifi network.
The other file called 'data_read.py' isn't used in the main program. It is only used to read new cards and displays the ID in the terminal. You can run this program when you want to add new cards, copy the displayed ID and then incorporate that in the 'main.py' file. 

### Transmitting the data
We use wifi to connect our pico to the internet. MQTT is used for the data transmission. Data is sent when an event occurs such as unauthorized access, authorized access and remote unlock. We will also set up an action in adafruit IO that sends a webhook message to a discord server whenever there is a new event. 
To connect to the Adafruit IO MQTT server using the MQTTClient class we need to:

* Create an instance of MQTTClient with the provided client ID, server address, port, username, and key. ![](https://hackmd.io/_uploads/Hk8dJiZt2.png)

* Set the callback function for MQTT subscriptions using client.set_callback(sub_cb). ![](https://hackmd.io/_uploads/Hk6okj-t3.png)

* Connect to the MQTT server using client.connect(). ![](https://hackmd.io/_uploads/HyXJeiZK2.png)

* Subscribe to a specific MQTT topic for remote unlock commands using client.subscribe(keys.AIO_REMOTE_UNLOCK_FEED). This allows the device to receive messages related to remote unlocking. ![](https://hackmd.io/_uploads/H114esZt2.png)

* Publish whenever a card is used to unlock using client.publish(topic=keys.AIO_CARD_ID_FEED, msg=str("Unlocked by: 2246669956")). ![](https://hackmd.io/_uploads/H1CvxoZFh.png)


For the webhook setup we'll need to first create a new discord server.
* Open Discord and click on + on the left side to add a server.
* Select 'create my own'.
* Select 'for me and my friends'.
* Choose an appropriate name, I went with 'RFID Box', and click on 'create'.
* Click on the gear sign on the right hand side of your new channel.
* Select 'integrations' and in then on 'create webhook'.
* Click on the 'copy webhook URL' button. Save the URL as this is supposed to be pasted in the action setup in adafruit IO.

Now it's time to configure and set up the action in adafruit IO. First you'll need to login to your adafruit account. Then click on 'actions' >> 'view all' >> '+ new action'.
After this select 'reactive action' and fill out the boxes as it it shown below:

![](https://hackmd.io/_uploads/rJSS0qZF2.png)

Create another action and set it up in the same way for the 'remote unlock' feature.


### Presenting the data
For the dashboard I chose to add a stream window that shows logins and remote unlocks during the last 40 hours. That way we will have a visialization of the recent history. I also added a button that controls the 'remote unlock' feature.
The purpose of the webhook action is to view the login history over a greater time period using discord. This also sends notifications in real time whenever there's a recorded event. 
To set up a dashboard, please follow this [link](https://learn.adafruit.com/adafruit-io-basics-dashboards).
See image of dashboard and discord server below:

![](https://hackmd.io/_uploads/BJVYmsbF3.png)

![](https://hackmd.io/_uploads/B11JVobY2.png)



### Finalizing the design
Overall I think that the project went well. I had a lot of fun trying things that I hadn't done before. Sure, the code could probably use a few touch-ups and can surely be optimized further but all in all, I'm happy with it!

![](https://hackmd.io/_uploads/ByAfd2-Kn.jpg)


Follow this [link](https://www.youtube.com/shorts/8ixXdT1aL4U) for a short video demonstration.




