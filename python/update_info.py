#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd5in65f
import time
from PIL import Image,ImageDraw,ImageFont,ImageGrab
import traceback
import sys, getopt

def main(argv):
    logging.basicConfig(level=logging.DEBUG)

    try:
        logging.info("epd5in65f info")
        
        epd = epd5in65f.EPD()
        logging.info("init and Clear")
        epd.init()
        epd.Clear()
        font20 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 32)
        font40 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 48)
        font60 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 64)
        
        try:
           opts, args = getopt.getopt(argv,"",["icon=", "seat=","name=","rank=","team=","available=","position=","phone=","email=","qrcode="])
        except getopt.GetoptError:
           logging.info(e)
           sys.exit(2)
        
              
        logging.info("1.Drawing with info")
        Himage = Image.new('RGB', (epd.width, epd.height), 0xffffff)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        
        for opt, arg in opts:
           if opt == '--icon':
              icon_pic = Image.open(arg).convert("RGBA").resize((200,200), Image.ANTIALIAS)
              mask_pic = Image.open("/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/mask.jpg").convert("RGBA").resize((200,200))
              Himage.paste(icon_pic, (20, 40), mask=mask_pic) 
           elif opt == '--seat':
              draw.text((480,  10), arg, font = font40, fill = epd.BLACK)
           elif opt == '--name':
              draw.text((240,  40), arg.replace("_"," "), font = font60, fill = epd.BLACK)
           elif opt == '--rank':
              draw.text((240, 130), arg.replace("_"," "), font = font20, fill = epd.BLACK)
           elif opt == '--team':
              draw.text((240, 170), arg.replace("_"," "), font = font20, fill = epd.BLACK)
           elif opt == '--available':
              ava_color = epd.RED
              if arg.lower().startswith("ava"):
                  ava_color = epd.GREEN
              draw.text((240, 210), arg.replace("_"," "), font = font20, fill = ava_color)
              draw.chord((170, 200, 210, 240), 0, 360, fill = ava_color)
              draw.chord((180, 210, 200, 230), 0, 360, fill = epd.WHITE)
           elif opt == '--position':
              pos_image = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/site.png').convert("RGB").resize((30,30), Image.ANTIALIAS)
              Himage.paste(pos_image, (10, 270))
              draw.text((50, 265), arg, font = font20, fill = epd.BLACK)
           elif opt == '--phone':
               pic1 = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/phone.png').convert("RGB").resize((30,30), Image.ANTIALIAS)
               Himage.paste(pic1, (10, 310))
               draw.text((50, 305), arg, font = font20, fill = epd.BLACK)
           elif opt == '--email':
              email_pic = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/email.png').convert("RGB").resize((30,30), Image.ANTIALIAS)
              Himage.paste(email_pic, (10, 350))
              draw.text((50, 345), arg, font = font20, fill = epd.BLACK)
           elif opt == '--qrcode':
              qr_image = Image.open(arg).convert("RGB").resize((200,200), Image.ANTIALIAS)
              Himage.paste(qr_image, (380, 240))
        
        # two rectangle
        draw.rectangle((0, 250, 600, 255), outline = 0, fill = epd.YELLOW)
        draw.rectangle((350, 255, 355, 448), outline = 0, fill = epd.YELLOW)
        
        # microsoft
        mic_image = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/window.png').convert("RGB").resize((30,30), Image.ANTIALIAS)
        Himage.paste(mic_image, (10, 420))
        draw.text((50, 415), "Microsoft", font = font20, fill = epd.BLACK)
        
        # synced
        sync_pic = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/sync.png').convert("RGB").resize((30,30), Image.ANTIALIAS)
        Himage.paste(sync_pic, (550, 420))
        draw.text((440, 415), "Synced", font = font20, fill = epd.BLACK)
       
        # display
        epd.display(epd.getbuffer(Himage))
        epd.sleep()
        
    except IOError as e:
        logging.info(e)
        
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        epd5in65f.epdconfig.module_exit()
        exit()

if __name__ == "__main__":
    main(sys.argv[1:])
