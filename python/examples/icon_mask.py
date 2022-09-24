from PIL import Image, ImageDraw, ImageFilter
im2 = Image.open('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/icon.jpg')
mask_im = Image.new("L", im2.size, 0)
draw = ImageDraw.Draw(mask_im)
draw.ellipse((0, 0, 320, 320), fill=255)
mask_im.save('/home/pi/e-Paper/RaspberryPi_JetsonNano/python/pic/mask.jpg', quality=95)
