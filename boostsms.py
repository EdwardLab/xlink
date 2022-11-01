import gc
import urequests
try:
    open("/data/boostsms/bootsend.txt", "r")
    try:
        sendto = open("/data/boostsms/sendto.txt", "r")
        boostserver = open("/data/boostsms/boostserver.txt", "r")
        boostnumber = open("/data/boostsms/number.txt", "r")
        boostpassword = open("/data/boostsms/password.txt", "r")
        content = f"http://{boostserver.read()}/infosms?number={boostnumber.read()}&password={boostpassword.read()}&send={sendto.read()}&content=Your 'Digital-Assisant-P1' started".replace(" ", "%20")
        boostsmsget = urequests.get(content)
        print(boostsmsget.content)
        boostsmsget.close()
    except:
        pass
except:
    pass