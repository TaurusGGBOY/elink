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
from PIL import Image,ImageDraw,ImageFont
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
        font24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24)
        font18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18)
        font30 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 40)
        
        inputfile = ''
        outputfile = ''
        try:
           opts, args = getopt.getopt(argv,"",["name=","level=","pos=","email=","state=","waitfor=","other="])
        except getopt.GetoptError:
           logging.info("info run wrong")
           sys.exit(2)
        
              
        logging.info("1.Drawing on the Horizontal image...")
        Himage = Image.new('RGB', (epd.width, epd.height), 0xffffff)  # 255: clear the frame
        draw = ImageDraw.Draw(Himage)
        for opt, arg in opts:
           if opt == '--name':
              draw.text((10, 160), arg, font = font30, fill = epd.BLACK)
           elif opt == '--level':
              draw.text((10, 200), arg, font = font30, fill = epd.ORANGE)
           elif opt == '--pos':
              draw.text((10, 240), arg, font = font30, fill = epd.GREEN)
           elif opt == '--email':
              draw.text((10, 280), arg, font = font30, fill = epd.BLUE)
           elif opt == '--state':
              draw.text((10, 320), arg, font = font30, fill = epd.RED)
           elif opt == '--waitfor':
              draw.text((10, 360), arg, font = font30, fill = epd.YELLOW)
           elif opt == '--other':
              draw.text((10, 400), arg.replace("_"," "), font = font30, fill = epd.BLACK)
        draw.line((20, 50, 70, 100), fill = 0)
        draw.line((70, 50, 20, 100), fill = 0)
        draw.rectangle((20, 50, 70, 100), outline = 0)
        draw.line((165, 50, 165, 100), fill = 0)
        draw.line((140, 75, 190, 75), fill = 0)
        draw.arc((140, 50, 190, 100), 0, 360, fill = 0)
        draw.rectangle((80, 50, 130, 100), fill = 0)
        draw.chord((200, 50, 250, 100), 0, 360, fill = 0)
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
