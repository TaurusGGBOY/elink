'''
******************************************************************************
  * @file    Rotation Sensor.py
  * @author  Waveshare Team
  * @version 
  * @date    2021-02-08
  * @brief   Rotation Sensor
  ******************************************************************************
  * @attention
  *
  * THE PRESENT FIRMWARE WHICH IS FOR GUIDANCE ONLY AIMS AT PROVIDING CUSTOMERS
  * WITH CODING INFORMATION REGARDING THEIR PRODUCTS IN ORDER FOR THEM TO SAVE
  * TIME. AS A RESULT, WAVESHARE SHALL NOT BE HELD LIABLE FOR ANY
  * DIRECT, INDIRECT OR CONSEQUENTIAL DAMAGES WITH RESPECT TO ANY CLAIMS ARISING
  * FROM THE CONTENT OF SUCH FIRMWARE AND/OR THE USE MADE BY CUSTOMERS OF THE
  * CODING INFORMATION CONTAINED HEREIN IN CONNECTION WITH THEIR PRODUCTS.
  *
  ******************************************************************************
'''

from machine import Pin,ADC
import utime

#Define pins and their initialization
right = machine.Pin(27, machine.Pin.IN)
left = machine.Pin(26, machine.Pin.IN)
down = machine.Pin(22, machine.Pin.IN)


right_assist = 0
count = 0             #Rotate the value of the encoder

# if right set right_assist = 1
def right_handler(pin):
    global right_assist
    # invalid following signal
    right.irq(handler=None)
    right_assist = 1


def down_handler(pin):
    global count
    down.irq(handler=None)
    count = 0
    print("down",count)
    ava_http_get()
    down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)
    
def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write((cmd+'\r\n').encode())
    waitResp(timeout)
    print()

def busy_http_get():
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://192.168.31.163:8080\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,0,\"/update_info?icon=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/icon.jpg&seat=2885&name=Xinyu_Shan&rank=Support_Engineer&team=PaaS_Dev_Team&available=Busy-Next_60_mins&position=WFH&phone=12349567444&email=sky@microsoft.com&qrcode=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/qrcode.png\"")  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance
    
def ava_http_get():
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://192.168.31.163:8080\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,0,\"/update_info?icon=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/icon.jpg&seat=2885&name=Xinyu_Shan&rank=Support_Engineer&team=PaaS_Dev_Team&available=Available-Next_60_mins&position=WFH&phone=12349567444&email=sky@microsoft.com&qrcode=/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/qrcode.png\"")  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance


right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)

# define uart
uart_port = 0
uart_baute = 115200
uart = machine.UART(uart_port, uart_baute, bits=8, parity=None, stop=1)

while True :
    # wait for right_assist==1
    if (right_assist == 1 ):
        
        if (left.value() == 1 ):
            count = count - 1
            busy_http_get()
            print("left",  count)

        elif (left.value() == 0 ):
            count = count + 1
            print("right",  count)
        
        # sleep while no value
        while (left.value() == 0 ) | (right.value() == 0):
            utime.sleep_ms(1)
        # here is value
        right_assist = 0
        # set interupt
        right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
    
    
    
    
    
    
   
