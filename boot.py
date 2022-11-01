import time
from machine import Pin 
import network
import random
import machine
from machine import I2C,Pin 
from ssd1306 import SSD1306_I2C
from microdot import send_file
import gc
import os
try:
    #for oled
    i2c = I2C(sda=Pin(18), scl=Pin(19))  
    oled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
    oled.fill(0)
except:
    pass


led=Pin(2,Pin.OUT)
def blueled(flashtime, fornumber):
    for i in range(fornumber):
        led.value(1)
        time.sleep(flashtime)
        led.value(0)
        time.sleep(flashtime)
blueled(0.5, 1)
def makeap():
    try:
        open("/apmodeonly", "r")
    except: 
        from microdot import Microdot
        import json
        oled.fill(0)
        for i in range(5):
            oled.text("DigitalPlat-P1", 0,  0)  
            oled.text("Please follow  ",  0, 20)
            oled.text("the instructions",  0, 30)
            oled.text("to activate the",  0, 40)
            oled.text("device",  0, 50)
            oled.show() 

        apcheck = open("makeapname.txt", "r")
        if apcheck.read() == '':
            makeapname = open("makeapname.txt", "w")
            randomnum = random.randint(1000,9999)
            makeapname.write(str(randomnum))
        apname = open("makeapname.txt", "r")
        ssid= 'DigitalPlat-XLink-P1_' + apname.read()
        password = 'digitalplat'
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=ssid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
        app = Microdot()
        @app.get('/static/bootstrap.min.css')
        def index(request):
            return send_file('/static/bootstrap.min.css')
        @app.get('/static/bootstrap.bundle.min.js')
        def index(request):
            return send_file('/static/bootstrap.bundle.min.js')
        @app.route('/')
        def index(request):
            return send_file('/html/connectwifi.html')
        def writewifi(essid, password):
            try:
                os.remove("/apmodeonly", "w")
            except:
                pass
            config = dict(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password) # 创建字典
            with open('wifi_config.json','w') as f:
                f.write(json.dumps(config))
        @app.get('/api/connectwifi/')
        def get_writewifi(request):
            writewifi(request.args['ssid'], request.args['password'])
            data = {'code': 200, 'text': 'success'}
            return json.dumps(data)
        @app.get('/api/reset')
        def get_reset(request):
            data = {'code': 200, 'text': 'success'}
            return json.dumps(data) + machine.reset()
        @app.get('/api/connectwifi/apmodeonly')
        def get_skipwifi(request):
            open("/apmodeonly", "w")
            data = {'code': 200, 'text': 'success'}
            return json.dumps(data) + machine.reset()
        @app.get('/api/system/wifireset')
        def get_sysreset(request):
            try:
                os.remove("/wifi_config.json")
                os.remove("/apmodeonly")
                data = {'code': 200, 'text': 'success'}
                return json.dumps(data) + machine.reset()
            except:
                data = {'code': 404, 'text': 'config file not found'}
                return json.dumps(data)
        app.run(port=80)
try:
    open("/apmodeonly", "r")
except:
    try:
        open("wifi_config.json", "r")
    except:
        makeap()
try:
    open("/apmodeonly", "r")
except:
    checkwifi = open("wifi_config.json", "r")
    if checkwifi.read() == '':
        makeap()
import sys

# 添加路径
sys.path.append('examples')

def is_legal_wifi(essid, password):
    '''
    判断WIFI密码是否合法
    '''
    if len(essid) == 0 or len(password) == 0:
        return False
    return True
def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))

def do_connect():
    try:
        open("/apmodeonly", "r")
    except:
        import json
        import network
        try:
            oled.fill(0)
            for i in range(6):
                oled.text("DigitalPlat-P1", 0,  0)
                oled.text('——————————',  0, 20)
                oled.text("Booting...",  0, 30)
                oled.text('——————————',  0, 40)
                oled.show() 
        except:
            pass
        # try read wifi_confi.json
        # wifi_config.json in root dir
        
        # Load config
        try:
            with open('wifi_config.json','r') as f:
                config = json.loads(f.read())
        # makeap      
        except:
            makeap()
        
        #Connect WIFI       
        wifi = network.WLAN(network.STA_IF)  
        if not wifi.isconnected(): 
            print('connecting to network...')
            wifi.active(True) 
            wifi.connect(config['essid'], config['password']) 
            import utime

            for i in range(280):
                print('Try {} Times to connect WIFI'.format(i))
                if wifi.isconnected():
                    break
                utime.sleep_ms(100) #sleep
            
            if not wifi.isconnected():
                wifi.active(False) #disable connections
                print('wifi connection error, please reconnect')
                import os
                try:
                    open("/apmodeonly", "r")
                except:  
                    do_connect() # retry
            else:
                print('network config:', wifi.ifconfig())
                try:
                    oled.fill(0)
                    for i in range(5):
                        oled.text("DigitalPlat-P1", 0,  0)  
                        oled.text("IP:",  0, 20)
                        oled.text(wifi.ifconfig()[0],  0, 30)
                        oled.text("Service started",  0, 40)
                        oled.show()
                    time.sleep(4)
                    oled.fill(0)
                    for i in range(5):
                        oled.text("DigitalPlat-P1", 0,  0)
                        oled.text(wifi.ifconfig()[0],  0, 20)
                        oled.text('Free RAM:' + str(gc.mem_free()),  0, 30)
                        oled.text('Free Storage:',  0, 40)
                        oled.text(df(),  0, 50)
                        oled.show()
                        oled.fill(0)
                except:
                    pass
if __name__ == '__main__':
    do_connect()