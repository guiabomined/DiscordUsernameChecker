"""Cloud Checker by Cloudzik1337 DC: byid"""

import itertools
import string
import queue
import threading
from time import sleep, time
import traceback
import random
import os
import tls_client

lock = threading.Lock()
with open("names.txt",              "a",        encoding='utf-8') as f: f.close()
with open("proxies.txt",            "a",        encoding='utf-8') as f: f.close()
with open("unchecked_names.txt",    "a",        encoding='utf-8') as f: f.close()
with open("errors.txt",             "a",        encoding='utf-8') as f: f.close()
with open("proxies.txt",            "r",        encoding='utf-8')as proxies:proxies= proxies.read().splitlines()





if len(proxies) == 0:
    proxies = [None]
proxy_cycle = itertools.cycle(proxies)
REQUETS_CLIENT_IDENTIFIER = "chrome_113"

#Globals
RPS =       0
REQUESTS =  0
WORKS =     0
TAKEN =     0







class _Colors:
    """Menu colors"""
    @staticmethod
    def _color_code(code):
        """Static method to format color codes"""
        return f'\033[{code}m'


    ENDC: str =         _color_code(0)
    BOLD: str =         _color_code(1)
    UNDERLINE: str =    _color_code(4)
    BLACK: str =        _color_code(30)
    RED: str =          _color_code(31)
    GREEN: str =        _color_code(32)
    YELLOW: str =       _color_code(33)
    BLUE: str =         _color_code(34)
    MAGENTA: str =      _color_code(35)
    CYAN: str =         _color_code(36)
    WHITE: str =        _color_code(37)
    REDBG: str =        _color_code(41)
    GREENBG: str =      _color_code(42)
    YELLOWBG: str =     _color_code(43)
    BLUEBG: str =       _color_code(44)
    MAGENTABG: str =    _color_code(45)
    CYANBG: str =       _color_code(46)
    WHITEBG: str =      _color_code(47)
    GREY: str =         _color_code(90)


Colors = _Colors()







def clear():
    """Clear the screen"""
    os.system('cls' if os.name=='nt' else 'clear')
clear()
class Pomelo:
    """Cloud Checker"""
    def __init__(self):
        """Initiate the class"""
        self.endpoint = "https://discord.com/api/v9"
        self.headers_post = {"Content-Type": "application/json"}
        self.session = tls_client.Session(
            client_identifier=REQUETS_CLIENT_IDENTIFIER,
            random_tls_extension_order=True
        )  

    def restart_session(self):
        """Restart the session"""
        self.session = tls_client.Session(
            client_identifier=REQUETS_CLIENT_IDENTIFIER,
            random_tls_extension_order=True            
        )

    def check(self, name: list):
        """Check if the name is available"""
        self.restart_session()
        global RPS, REQUESTS, WORKS, TAKEN
        while True:
            try:
                try:
                    name, proxy = name

                except Exception as e:
                    if proxy_cycle is None:
                        proxy = None
                    else:
                        proxy = next(proxy_cycle)
                if proxy is not None:
                    proxy = f"http://{str(proxy).strip()}"
                r = self.session.post(
                    url=self.endpoint + "/unique-username/username-attempt-unauthed",
                    headers = self.headers_post,
                    json={"username": name},
                    proxy = proxy
                ) 
                REQUESTS += 1

                if r.status_code in [200, 201, 204]:
                    if r.json()["taken"]:
                        TAKEN += 1
                        return False, r.json(), r.status_code

                    WORKS += 1
                    if str(r.json()) in ["", None, "{}"]:
                        return False, None, r.status_code
                    return True, r.json(), r.status_code

                #rate limited
                elif r.status_code == 429:
                    if proxy is None or proxy == "None" or proxy == "":

                        print("PROXYLESS RATELIMITED SLEEPING")
                        sleep(r.json()["retry_after"]/1000)
                        name = [name, next(proxy_cycle)]
                        self.check(name)


            except:
            # timeout
                with lock:
                    try:
                        exception = traceback.format_exc()
                        with open("errors.txt", "w") as f:
                            f.write(f"{exception}\n")
                            f.close()
                        sleep(1) # rest for 1s
                    except:
                        pass


g = Colors.GREY
r = Colors.RED
x = Colors.ENDC
ASCII = f"""
{g}                      :::!~!!!!!:.
                .xUHWH!! !!?M88WHX:.
                .X*#M@$!!  !X!M$$$$$$WWx:.
            :!!!!!!?H! :!$!$$$$$$$$$$8X:
            !!~  ~:~!! :~!$!#$$$$$$$$$$8X:
            :!~::!H!<   ~.U$X!?R$$$$$$$$MM!
            ~!~!!!!~~ .:XW$$$U!!?$$$$$$RMM!
            !:~~~ .:!M"T#$$$$WX??#MRRMMM!
            ~?WuxiW*`   `"#$$$$8!!!!??!!!
            :X- M$$$$       `"T#$T~!8$WUXU~
            :%`  ~#$$$m:        ~!~ ?$$$$$$
        :!`.-   ~T$$$$8xx.  .xWW- ~""##*"
.....   -~~:<` !    ~?T#$$@@W@*?$$      /`
W$@@M!!! .!~~ !!     .:XUW$W!~ `"~:    :
#"~~`.:x%`!!  !H:   !WM$$$$Ti.: .!WUn+!`
:::~:!!`:X~ .: ?H.!u "$$$B$$$!W:U!T$$M~
.~~   :X@!.-~   ?@WTWo("*$$$W$TH$! `
Wi.~!X$?!-~    : ?$$$B$Wu("**$RM!
$R@i.~~ !     :   ~$$$$$B$$en:``
?MXT@Wx.~    :     ~"##*$$$$M~

                    {r}@{x}  Cloud 2023                  {r}@{x}
                    {r}@{x}  github.com/cloudzik1377     {r}@{x}
                    {r}@{x}  discord.cloudzik.me         {r}@{x}
        """
clear()
print(ASCII)

CLOUDCHECKER = Pomelo()

# username can contain letters, numbers, and underscores
CHARS = string.ascii_lowercase + string.digits + "_" + '.'

with open("unchecked_names.txt", "r") as f:
    combos = f.read().splitlines()
    f.close()

if len(combos) == 0:
    combos = itertools.product(CHARS, repeat=int(input("Length of username: ")))
    with open("unchecked_names.txt", "w", encoding='utf-8') as f:
        
        for i in combos:
            f.write("".join(i))
            f.write("\n")
        f.close()
    with open("unchecked_names.txt", "r", encoding='utf-8') as f:
        combos = f.read().splitlines()
        f.close()
queue = queue.Queue()
# actually load only random 50k line (Long list will take too long to load)
try:
    combos = random.sample(combos, 50000)
except ValueError:
    pass
for name in combos:
    print(f"[{Colors.YELLOW}+{Colors.ENDC}] Adding username = {Colors.CYAN}{name}{Colors.ENDC}", end="\r")
    name = [name.strip(), next(proxy_cycle)]
    queue.put(name)


def worker():
    """Thread worker function"""
    while queue.qsize() > 0:
        
        name = queue.get()
        try:
            available, json, status_code = CLOUDCHECKER.check(name)
        except:
            with lock:
                exception = traceback.format_exc()
                with open("errors.txt", "a") as f:
                    f.write(f"{exception}\n")
                    f.close()
            available, json, status_code = "ERROR", None, None
        name, proxy = name

        proxy_formated = str(proxy[:10]+'*'*10) if proxy else 'Proxyless'

        with lock:

            if available is True:
                print(f"[{Colors.GREEN}+{Colors.ENDC}] Available  : {Colors.CYAN}{name}{Colors.ENDC},    RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC}, proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
                
                with open("names.txt", "a", encoding='utf-8') as f:
                    f.write(name)
                    f.write("\n")
                    f.close()

            elif available == "RATELIMITED":
                
                print(f"[{Colors.YELLOW}?{Colors.ENDC}] TIMEOUT    : {Colors.CYAN}{json}{Colors.ENDC},{' '*(8-int(len(str(json))))}RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC},{' '*(18-int(len(str(json)))-1)}proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
            
            elif available == "ERROR":
               
                with open("errors.txt", "a", encoding='utf-8') as f:
                    f.write(f"{name, json, status_code}\n")
            
            else:
                print(f"[{Colors.RED}-{Colors.ENDC}]   Taken    : {Colors.CYAN}{name}{Colors.ENDC},    RPS : {Colors.CYAN}{RPS} / s{Colors.ENDC},  resp : {Colors.CYAN}{json}{Colors.ENDC},  proxy : {Colors.CYAN}{proxy_formated}{Colors.ENDC}")
       
        queue.task_done()                



def RPS_CALCULATOR():
    """Calculate RPS (Requests per second)"""
    global RPS
    while True:
        RPS_BEFORE = REQUESTS
        sleep(1)
        RPS = REQUESTS - RPS_BEFORE
start_time = time()        
def TITLE_SPINNER():
    """Fix for windows 11 console"""
    TITLE = ["CloudChecker", "Avaible : {WORKS}", "Taken : {TAKEN}", "Requests : {REQUESTS}", "RPS : {RPS}", "Elapsed : {ELAPSED}s"]
    while True:
        for i in TITLE:
            edited = i          
            for _ in range(50):
                edited = i.format(WORKS=WORKS, TAKEN=TAKEN, REQUESTS=REQUESTS, RPS=RPS, ELAPSED=round(time()-start_time))
                os.system(f'title {edited}')
                sleep(0.01)
            sleep(1)

threading.Thread(target=RPS_CALCULATOR, daemon=True).start()
threading.Thread(target=TITLE_SPINNER, daemon=True).start()


clear()
print(ASCII)

print(f"[{Colors.YELLOW}+{Colors.ENDC}] Loaded {Colors.CYAN}{len(combos)}{Colors.ENDC} combos")
ask = input(f"How many threads {Colors.YELLOW}>>>{Colors.ENDC} ")
for _ in range(5):
    print(f"Starting in {5-_}s. with {ask} threads (Ctrl+c Abort)", end="\r")
    sleep(1)
ths = []

for i in range(int(ask)):
    t = threading.Thread(target=worker)
    t.daemon = True   
    t.start()
    ths.append(t)
    


queue.join()

print(f"[{Colors.GREEN}+{Colors.ENDC}] Done")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total requests = {Colors.CYAN}{REQUESTS}{Colors.ENDC}")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total valid names = {Colors.CYAN}{WORKS}{Colors.ENDC}")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total invalid names = {Colors.CYAN}{TAKEN}{Colors.ENDC}")
print(f"[{Colors.GREEN}+{Colors.ENDC}] Total time = {Colors.CYAN}{round(time()-start_time)}{Colors.ENDC} seconds")
