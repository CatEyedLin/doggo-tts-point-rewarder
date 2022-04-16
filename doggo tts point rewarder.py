import sys, irc.bot, requests, pyttsx3, pygame, threading

ge = []
gc = None

""" TO DO
force_tts_allow_vip
""" 
        
class TwitchBot(irc.bot.SingleServerIRCBot):
    def __init__(self, username, token, channel):
        self.token = token
        self.channel = '#' + channel

        server = 'irc.chat.twitch.tv'
        port = 6667
        print ('Connecting ' + server + ':' + str(port) + '...')
        irc.bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:'+token)], username, username)
        

    def on_welcome(self, connection, event):
        global gc
        gc = connection
        print( 'Joining ' + self.channel, event)

        #connection.cap('REQ', ':twitch.tv/membership')
        connection.cap('REQ', ':twitch.tv/tags')
        #connection.cap('REQ', ':twitch.tv/commands')
        connection.join(self.channel)
        while not connection.connected:
            print(".",end="")
            pass
        print( 'Joined ' + self.channel)

    def on_pubmsg(self, connection, event):
        global ge, tts_custom_reward_id, tts_engine, tss_wait_list, tts_custom_reward_id, force_tts_prefix 
        ge = event
        #print(connection,"\n\n",event)

        for tag in event.tags:
            if tag['key'] == 'custom-reward-id':#check for a tts point redeem
                if (tag['value']) == tts_custom_reward_id:
                    tss_wait_list.append(event.arguments[0])
                else:
                    print("received reward id:", tag['value'])
                           
            if event.arguments[0][:1] == force_tts_prefix:
                if force_tts_allow_all:
                    tss_wait_list.append(event.arguments[0])
                    break

                #print(tag["key"] == 'display-name', tag["value"], self.channel[1:])
                elif tag["key"] == 'display-name' and tag["value"].lower() == self.channel[1:]:
                    tss_wait_list.append(event.arguments[0])
                    break

                elif force_tts_allow_mod and tag['key'] == "mod" and tag["value"] =="1" :
                    tss_wait_list.append(event.arguments[0])
                    break
                    

def speach_thread():
    global tss_wait_list, speaking
    tss_wait_list = []
    while True:
         #print("s")
         #time.sleep(10)
         if len(tss_wait_list) > 0:
             text = tss_wait_list.pop(0)
             tts_engine.say(text,text )
             speaking = True
             tts_engine.runAndWait()
             speaking = False
         #print("e")
             
def pygame_start():
    global speaking
    display = pygame.display.set_mode([winX,winY], flags = pygame.RESIZABLE)
    pygame.display.set_caption("doggo tts")
    
    running = True
    while running:
        #print (speaking)
        display.fill([128,128,128])
        if speaking:
            display.blit(open_image, [0,0])
        else:
            display.blit(idle_image, [0,0])
            
        
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
                bot.stop()
                break
            else:
                pass

pygame.init()
tts_engine = pyttsx3.init('sapi5')
config = None
speaking = False

if 1:
    if len(sys.argv) >= 2:
        if sys.argv[1].endswith(".cfg"):
            config = open(sys.argv[1] ,mode = "r")
        #print ( sys.argv[1])
    else:
        config = open("./doggo tts point rewarder.cfg",mode = "r")
        print("normal")
        
    for line in config.readlines():
        if line.startswith("channel"):
            channel = line.split("=")[1].strip()
        elif line.startswith("bot_user_name "):
            bot_user_name = line.split("=")[1].strip()
        elif line.startswith("bot_login_token "):
            bot_login_token = line.split("=")[1].strip().strip("oauth:")
            
        elif line.startswith("tts_custom_reward_id "):
            tts_custom_reward_id = line.split("=")[1].strip()
            
        elif line.startswith("force_tts_prefix "):
            force_tts_prefix  = line.split("=")[1].strip()
        elif line.startswith("force_tts_allow_mod "):
            force_tts_allow_mod = line.split("=")[1].strip().lower() in ["1","true"]
        elif line.startswith("force_tts_allow_vip "):
            force_tts_allow_vip  = line.split("=")[1].strip().lower() in ["1","true"]
        elif line.startswith("force_tts_allow_all "):
            force_tts_allow_all  = line.split("=")[1].strip().lower() in ["1","true"]
            
        elif line.startswith("winX"):
            winX = int(line.split("=")[1].strip())
        elif line.startswith("winY"):
            winY = int(line.split("=")[1].strip())
            
        elif line.startswith("idle_image"):
            idle_image = pygame.image.load(line.split("=")[1].strip())
        elif line.startswith("open_image"):
            open_image = pygame.image.load(line.split("=")[1].strip())

        elif line.startswith("volume"):
            tts_engine.setProperty('volume', float(line.split("=")[1].strip()))
        elif line.startswith("words_per_minute"):
            tts_engine.setProperty('rate', int(line.split("=")[1].strip()))
        elif line.startswith("voice_id"):
           #tts_engine.setProperty('voice', int(line.split("=")[1].strip()))
           tts_engine.setProperty('voice', tts_engine.getProperty('voices')[int(line.split("=")[1].strip())].id)
            
        config.close()

    print("config loaded:",channel,bot_user_name,bot_login_token[0:3]+"*" * (len(bot_login_token) - 3),
          tts_custom_reward_id, winX, winY, idle_image, open_image, tts_engine.getProperty("voice"))
    
if False: 
    if config != None: config.close()
    config = open("./default.cfg",mode = "w")
    config.writelines("""channel = |your channel's name|
bot_user_name = |your bot's name|
bot_login_token = |bot token|

tts_custom_reward_id = |your tts reward id, you can find to by redeeming your tts, and reading it from the terminal|
force_tts_prefix = §
force_tts_allow_mod = True
force_tts_allow_vip = True //does not work yet
force_tts_allow_all = False

winX = 160
winY = 160

idle_image = .\idle.png
open_image = .\open.png

voice_id = 0
volume = 0.75
words_per_minute = 300""")
    config.close()
    sys.exit("broken config file, please fix, if you don't know what to do read the readme or go to github.com/CatEyedLin/Doggo-TTS-Point-Rewarder")

bot = TwitchBot(bot_user_name, bot_login_token, channel)
bot_thread = threading.Thread(target=bot.start,daemon=True)
bot_thread.start()

spea_thread = threading.Thread(target=speach_thread,daemon=True)
spea_thread.start()
pygame_start()
