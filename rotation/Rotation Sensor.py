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
import os
import binascii
print(os.uname())

#Define pins and their initialization
right = machine.Pin(27, machine.Pin.IN)
left = machine.Pin(26, machine.Pin.IN)
down = machine.Pin(22, machine.Pin.IN)


right_assist = 0
count = 0             #Rotate the value of the encoder

def sendCMD_waitResp(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write((cmd+'\r\n').encode())
    waitResp(timeout)
    print()

def waitResp(timeout=2000):
    prvMills = utime.ticks_ms()
    resp = b""
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            resp = b"".join([resp, uart.read(1)])
    try: 
        print((resp).decode())
    except UnicodeError:
        pass

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

def sendCMD_waitRespLine(cmd, timeout=2000):
    print("CMD: " + cmd)
    uart.write((cmd+'\r\n').encode())
    waitRespLine(timeout)
    print()
    
def waitRespLine(timeout=2000):
    prvMills = utime.ticks_ms()
    while (utime.ticks_ms()-prvMills)<timeout:
        if uart.any():
            print((uart.readline()).decode())
                

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

#AT commands test
def atCommandTest():
    sendCMD_waitResp("AT")
    sendCMD_waitResp("ATE1")
    sendCMD_waitResp("AT+CGMM")
    sendCMD_waitResp("AT+CPIN?")        #whether some password is required or not
    sendCMD_waitResp("AT+CSQ")          #received signal strength
    sendCMD_waitResp("AT+CGREG?")        #the registration of the ME.
    sendCMD_waitResp("AT+CGATT?")       #GPRS Service’s status
    sendCMD_waitResp("AT+CGACT?")       #PDN active status
    sendCMD_waitResp("AT+COPS?")       #Query Network information
    sendCMD_waitResp("AT+CGCONTRDP")       #Attached PS domain and got IP address automatically
    
# HTTP GET TEST
def httpGetTest():
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://api.seniverse.com\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,0,\"/v3/weather/now.json?key=SwwwfskBjB6fHVRon&location=shenzhen&language=en&unit=c\"")  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance
    print(hexStr_to_str("7b22726573756c7473223a5b7b226c6f636174696f6e223a7b226964223a2257533130373330454d384556222c226e616d65223a225368656e7a68656e222c22636f756e747279223a22434e222c2270617468223a225368656e7a68656e2c5368656e7a68656e2c4775616e67646f6e672c4368696e61222c2274696d657a6f6e65223a22417369612f5368616e67686169222c2274696d657a6f6e655f6f6666736574223a222b30383a3030227d2c226e6f77223a7b2274657874223a22436c6f756479222c22636f6465223a2234222c2274656d7065726174757265223a223235227d2c226c6173745f757064617465223a22323032312d30332d31335431353a32303a30302b30383a3030227d5d7d"))
    print(str_to_hexStr("api_key=tPmAT5Ab3j888&value1=26.44&value2=57.16&value3=1002.95"))

# HTTP POST TEST
def httpPostTest():
    global i
    i=i+1
    sendCMD_waitResp("AT+CHTTPCREATE=\"http://pico.wiki/post-data.php\"")    #Create HTTP host instance
    sendCMD_waitResp("AT+CHTTPCON=0")           #Connect server
    sendCMD_waitRespLine("AT+CHTTPSEND=0,1,\"/post-data.php\",4163636570743a202a2f2a0d0a436f6e6e656374696f6e3a204b6565702d416c6976650d0a557365722d4167656e743a2053494d434f4d5f4d4f44554c450d0a,\"application/x-www-form-urlencoded\","+str_to_hexStr("api_key=tPmAT5Ab3j888&value1="+str(temperature)+"&value2="+str(reading)+"&value3="+str(i)))  #send HTTP request
    waitResp()
    sendCMD_waitResp("AT+CHTTPDISCON=0")      #Disconnected from server
    sendCMD_waitResp("AT+CHTTPDESTROY=0")      #Destroy HTTP instance

#APN Manual configuration
def apnConfig(APN):
    sendCMD_waitResp("AT+CFUN=0")        #Disable RF
    sendCMD_waitResp("AT*MCGDEFCONT=\"IP\",\""+ APN +"\"")        #Set the APN manually
    sendCMD_waitResp("AT+CFUN=1")        #Enable RF
    utime.sleep(1)
    sendCMD_waitResp("AT+CGATT?")        #Inquiry PS service
    sendCMD_waitResp("AT+CGCONTRDP")      #Attached PS domain and got IP address automatically

def hexStr_to_str(hex_str):
    hex = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

def str_to_hexStr(string):
    str_bin = string.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

right.irq(trigger=machine.Pin.IRQ_FALLING, handler=right_handler)
down.irq(trigger=machine.Pin.IRQ_FALLING, handler=down_handler)

# define uart
uart_port = 0
uart_baute = 115200
uart = machine.UART(uart_port, uart_baute, bits=8, parity=None, stop=1)

APN = "cmnbiot"

i=0
reading=0
temperature=0

# atCommandTest()
apnConfig(APN)
# httpPostTest()
httpGetTest()

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
    
    
    
    
    
    
   
