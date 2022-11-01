import os
from machine import Pin, SoftSPI
from sdcard import SDCard
# 接线说明:
# MISO -> GPTO13
# MOSI -> GPIO12
# SCK -> GPIO 14
# CS -> GPIO27
spisd=SoftSPI(-1, miso=Pin(13), mosi=Pin(12), sck=Pin(14))
sd=SDCard(spisd, Pin(27))
print('Root directory:{}'.format(os.listdir()))
vfs=os.VfsFat(sd)
os.mount(vfs,'/sd')
print('Root directory:{}'.format(os.listdir()))
os.chdir('sd')
print('SD Card contains:{}'.format(os.listdir()))

