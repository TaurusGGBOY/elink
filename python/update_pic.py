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
import sys

logging.basicConfig(level=logging.DEBUG)

try:
    logging.info("epd5in65f Pic")
    
    epd = epd5in65f.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.Clear()
        
    logging.info("3.read bmp file")
    Himage = Image.open(sys.argv[1])
    epd.display(epd.getbuffer(Himage))
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd5in65f.epdconfig.module_exit()
    exit()
