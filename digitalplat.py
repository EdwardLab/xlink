import json
import time 
import network
import random
import machine
from machine import Pin
import urequests
import gc
import boostsms
from microdot import Microdot
import os
from machine import I2C,Pin 
from ssd1306 import SSD1306_I2C
from microdot import send_file
from microdot import redirect
from microdot_utemplate import render_template
def makedashboradap():
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
makedashboradap()
def df():
  s = os.statvfs('//')
  return ('{0} MB'.format((s[0]*s[3])/1048576))
try:
    with open('wifi_config.json','r') as f:
        config = json.loads(f.read())
except:
    pass
try:
    wifissid = config['essid']
except:
    wifissid = 'Not connected - AP Mode'
app = Microdot()
@app.get('/')
def indexredirect(request):
    return redirect('/xlink/dashboard/main')

@app.get('/static/bootstrap.min.css')
def index(request):
    return send_file('/static/bootstrap.min.css')
@app.get('/static/bootstrap.bundle.min.js')
def index(request):
    return send_file('/static/bootstrap.bundle.min.js')
@app.route('/xlink/dashboard/main')

def index(request):
    return f'''
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>DigitalPlat-XLink</title>
    <link href="/static/bootstrap.min.css" rel="stylesheet">

    </head>
  <body>
    <!-- As a heading -->
<nav class="navbar bg-light">
    <div class="container-fluid">
      <span class="navbar-brand mb-0 h1">DigitalPlat XLink Dashboard</span>
    </div>
  </nav>
    <h1>Welcome to DigitalPlat XLink Dashboard!</h1>
    <div class="alert alert-primary" role="alert">
      It is recommended that you access the device through the API or unified control panel. If already connected, please ignore
    </div>
  <div class="card" style="width: 18rem;">
  <div class="card-header">
    Device Overview
  </div>
  <ul class="list-group list-group-flush">
    <li class="list-group-item">Model: DigitalPlat-XLink-P1</li>
    <li class="list-group-item">Firmware version: DigitalPlat_XLink_IOT_global</li>
    <li class="list-group-item">Device uname: {os.uname()}</li>
    <li class="list-group-item">Free RAM: {str(gc.mem_free())}</li>
    <a href="/api/system/gccollect" class="btn btn-info" role="button">RAM Garbage cleanup</a>
    <li class="list-group-item">Free Storage: {df()} Total: 4MB</li>
    <li class="list-group-item">Connected WIFI SSID: {wifissid}</li>
    <a href="/xlink/dashboard/connectwifi" class="btn btn-info" role="button">connect/reconnect WIFI</a>
  </ul>
</div>
    <a href="/api/blueled/1" class="btn btn-info" role="button">Board LED ON</a>
    <a href="/api/blueled/0" class="btn btn-info" role="button">Board LED OFF</a>
    <a href="/api/reset" class="btn btn-info" role="button">Reboot Device</a>
  <h3>Device API Control</h3>
  <a href="/xlink/dashboard/control/pin" class="btn btn-info" role="button">PIN</a>
  <a href="/xlink/dashboard/control/oled" class="btn btn-info" role="button">OLED</a>
  <a href="/api/system/webrepl/start" class="btn btn-info" role="button">Start WebRepl Service (will stop the Dashboard service and API)</a>
</div>
    <script src="/static/bootstrap.bundle.min.js"></script>
  </body>
</html>
''', {'Content-Type': 'text/html'}

@app.route('/xlink/dashboard/control/pin')

def index(request):
    return send_file('/html/pin.html')
@app.route('/xlink/dashboard/control/oled')

def index(request):
    return send_file('/html/oled.html')

@app.route('/xlink/dashboard/connectwifi')

def index(request):
   return send_file('/html/connectwifi.html')
def writewifi(essid, password):
    try:
        os.remove("/apmodeonly", "w")
    except:
        pass
    config = dict(essid=essid, authmode=network.AUTH_WPA_WPA2_PSK, password=password)
    with open('wifi_config.json','w') as f:
        f.write(json.dumps(config))
@app.get('/api/connectwifi/')
def get_writewifi(request):
    writewifi(request.args['ssid'], request.args['password'])
    try:
        os.remove("/apmodeonly", "w")
    except:
        pass
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/connectwifi/apmodeonly')
def get_skipwifi(request):
    open("/apmodeonly", "w")
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data) + machine.reset()
@app.get('/api/reset')
def get_reset(request):
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data) + machine.reset()
@app.get('/api/shutdown')
def shutdown(request):
    request.app.shutdown()
    return 'The server is shutting down...'

def blueled(flashtime, fornumber):
    for i in range(fornumber):
        led.value(1)
        time.sleep(flashtime)
        led.value(0)
        time.sleep(flashtime)
@app.get('/api/blueled/<onoff>')
def get_writewifi(request, onoff):
    controlpin = machine.Pin(2,Pin.OUT)
    controlpin.value(int(onoff))
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)

@app.get('/api/boostsms/config/<server>/<port>/<getnumber>/<getpassword>/<sendtowho>')
def get_boostconfig(request, server, port, getnumber, getpassword, sendtowho):
    sendto = open("/data/boostsms/sendto.txt", "w")
    boostserver = open("/data/boostsms/boostserver.txt", "w")
    number = open("/data/boostsms/number.txt", "w")
    password = open("/data/boostsms/password.txt", "w")
    sendto.write(sendtowho)
    boostserver.write(server + ':' + port)
    number.write(getnumber)
    password.write(getpassword)
    data = {'code': 200, 'text': 'success', 'sendto' : sendtowho, 'boostserver' : server, 'port' : port, 'number' : getnumber, 'password' : getpassword}
    return json.dumps(data)
@app.get('/api/boostsms/send/<sendto>/<sendcontent>')
def get_boostconfig(request, sendto, sendcontent):
    boostserver = open("/data/boostsms/boostserver.txt", "r")
    boostnumber = open("/data/boostsms/number.txt", "r")
    boostpassword = open("/data/boostsms/password.txt", "r")
    content = f"http://{boostserver.read()}/infosms?number={boostnumber.read()}&password={boostpassword.read()}&send={sendto}&content={sendcontent}".replace(" ", "%20")
    boostsmsget = urequests.get(content)
    print(boostsmsget.content)
    return {'code': 200, 'text': 'success', 'return' : boostsmsget.content}
    boostsmsget.close()
@app.get('/api/boostsms/enablebootsendmsg')
def get_enablebootsend(request):
    open("/data/boostsms/bootsend.txt", "w")
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/boostsms/disablebootsendmsg')
def get_disablebootsend(request):
    os.remove("/data/boostsms/bootsend.txt")
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/pin/')
def get_pin(request):
    if request.args['outorin'] == '0':
        pin=Pin(int(request.args['gpionum']),Pin.OUT)
    if request.args['outorin'] == '1':
        pin=Pin(int(request.args['gpionum']),Pin.IN)
    pin.value(int(request.args['value']))
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/oled/init')
def get_setoledtext(request):
    global getoled
    i2c = I2C(sda=Pin(18), scl=Pin(19))  
    getoled = SSD1306_I2C(128, 64, i2c, addr=0x3c)
    getoled.fill(0)
    led=Pin(2,Pin.OUT)
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/oled/settext/')
def get_setoledtext(request):
    getoled.text(request.args['text'],  int(request.args['setx']), int(request.args['sety']))
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/oled/show')
def get_oledshow(request):
    getoled.show()
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/api/system/info')
def get_sysinfo(request):
    data = {'code': 200, 'model' : 'DigitalPlat-Assisant-P1', 'firmware_version' : 'DigitalPlat_XLink_IOT_global', 'interpreterinfo': os.uname()}
    return json.dumps(data)
@app.get('/api/system/webrepl/start')
def get_startwebrepl(request):
    import webrepl  
    webrepl.start()
    request.app.shutdown()
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
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
@app.get('/api/system/gccollect')
def get_gccollect(request):
    import gc
    gc.collect()
    data = {'code': 200, 'text': 'success'}
    return json.dumps(data)
@app.get('/text/logs')
def get_sysreset(request):
    try:
        f = open("logs.txt", "r")
        return f.read()
    except:
        return "No logs"
@app.errorhandler(404)
def not_found(request):
    return {'code': 404, 'text': 'resource not found'}, 404
@app.errorhandler(500)
def not_syserror(request):
    return {'code': 500, 'text': 'internal program error'}, 500
app.run(port=80)