import os
import json
import youtube_dl
import telepotpro
import time
from random import randint
from multiprocessing import Process
from youtubesearchpython import SearchVideos

bot = telepotpro.Bot("1820845651:AAGAyijLVzcITjyGCdRT2cl-wcJE9lgNpt4")

class Music:
    def __init__(self, user_input, msg):
        self.chat = Chat
        self.user_input = user_input[6:]

    def search_music(self, user_input):
        search = SearchVideos(user_input, offset = 1, mode = "json", max_results = 1)
        
        return json.loads(search.result())

        pass

    def get_link(self, result):
        return result['search_result'][0]['link']

        pass

    def get_title(self, result):
        return result['search_result'][0]['title']

        pass

    def get_duration(self, result):
        result = result['search_result'][0]['duration'].split(':')
        min_duration = int(result[0])
        split_count = len(result)
        
        return min_duration, split_count

        pass

    def download_music(self, file_name, link):
        ydl_opts = {
            'outtmpl': './'+file_name,
            'format': 'bestaudio/best',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '256',
            }],
            'prefer_ffmpeg': True
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(link, download=True)

        pass

class Chat:
    def __init__(self, msg):
        self.chat_id = msg['chat']['id']
        self.user_input = msg['text']
        self.user_input = self.user_input.replace('@TLMusicDownloader_bot', '')
        self.user_name = msg['from']['first_name']

        self.messages = {
            'start':'ei ga wari sana ba da lowercase haidi macha ngakta oina sijan nabiyu\n\n '
                     'Kei takpigadabno? Nungaibiribo? \n\n  Hwjik ki Oinadi bot se feature ayamba yadri under development leiri warwbiroi .\n\n Eshei tase hi hairkoh'    
                    '!!!!!!! BOT ASI UNDER DEVELOPMENT NI ASOIBA NUNGAITABA YWRDI PLZ CONTACT ME - https://t.me/boenmay \n\n ' 
                    'https://wa.me/message/CXMFXKLEEQODP1 \n\n'
                    'commands menu gi damak "*/commands*" nmbiyu',
            'greet':'ei ga wari sana ba da lowercase haidi macha ngakta oina sijan nabiyu\n\n'
                    'Kei takpigadabno? Nungaibiribo?   \n\n Hwjik ki Oinadi bot se feature ayamba yadri under development leiri warwbiroi . \n\nEshei tase hi hairkoh'
                    'commands menu gi damak "*/commands*" nmbiyu'
                    '!!!!!!! BOT ASI UNDER DEVELOPMENT NI ASOIBA NUNGAITABA YWRDI PLZ CONTACT ME - https://t.me/boenmay \n\n\ '
                    'https://wa.me/message/CXMFXKLEEQODP1 \n\n'
                  ,
            'sleep':'Tumbiro2 Phone pai leiranu Nongmada 6hrs ti Yamdrba da Tumbiyo! \n\n '
                    'https://media.tenor.com/images/df51877535a3e38c9cccd2f23ff154a2/tenor.gif',
             
             'song':'Hello? Eshei ama Tasiro \n\n'
                    ' 🤖  '+ self.user_name +'!\n\n'
                    '📩 Sumaina Khllakoh Eshei Apamba:\n\n'
                    '"*/eshei* _song name_"  or\n'
                    '"*/eshei* _seisakpa - song name_"\n\n'
                    'Adom gi ningba thungnaba ei semjarkke. 🎶',
              
            
             
             'movies':'Sombu Taram Na okchari !   \n\n Adom2 gi apam ba movies or series sing */movies<apamba_movie_maming>* space amta ywdana asigi format ta thabirkoh \n\n Ei 24hrs ki manungda adom gi apamba movies to update twjarkke \n\n use function movies where *<apamba_movie_maming>* should be replaced by the desired name ! \n\n\n\n NOTE:Adom gi movie to kari gumba leiba tarbdi \n\n */uploads* nmaga download twbiyu \n\n Remember it usually takes 24hrs ! \n\n  If u get this menu again,I have recieved your order and will be uploaded on the */uploads* secion', 
             
             
                        
 #_This method takes 24hrs to update ur movie !_ \n\n _if u want to download any movies fast,_ \n\n type or click on */tutorial*            
                   
                         
            
            
            
            


        }

        self.check_input(self.user_input, msg)

        pass

    def send_message(self, content):
        return bot.sendMessage(self.chat_id, content, parse_mode='Markdown')

        pass

    def delete_message(self, message):
        chat_id = message['chat']['id']
        message_id = message['message_id']
        bot.deleteMessage((chat_id, message_id))

        pass

    def send_audio(self, file_name):
        bot.sendAudio(self.chat_id,audio=open(file_name,'rb'))

        pass

    def process_request(self, user_input):
        result = Music.search_music(self, user_input[6:])
        min_duration, split_count = Music.get_duration(self, result)

        if int(min_duration) < 30 and split_count < 3:
            file_name = Music.get_title(self, result) +' - @TLMusicDownloader_bot '+str(randint(0,999999))+'.mp3'
            file_name = file_name.replace('"', '')

            self.send_message(['🎵 '+ Music.get_title(self, result) +'\n'+'🔗 '+Music.get_link(self, result)])
            downloading_message = self.send_message('⬇️ Downloading.....\n_(Ngak Ngaibiyuko.)_')

            Music.download_music(self, file_name, Music.get_link(self, result))

            try:
                self.send_audio(file_name)
                self.delete_message(downloading_message)
                self.send_message('✅ \n\n  https://i.makeagif.com/media/3-10-2017/H8pTi0.gif  \n\n ')
                print ("\nSucess!\n")
            except:
                print("\nError")

            os.remove(file_name)
        pass
         
#greetings lines
    def check_input(self, user_input, msg):
        if user_input.startswith('/start'):
            self.send_message(self.messages['start'])
        if 'Hi' in user_input:
            self.send_message(self.messages['greet']) 
        if "hii" in user_input:
            self.send_message(self.messages['greet'])
        if "hiii" in user_input:
            self.send_message(self.messages['greet']) 
        if user_input.startswith('bina'):
            self.send_message("Kei takpigadabno? Nungaibiribo? \n\n Ming ga kwbirkeh ne ngasidi  🤗🤗🤗 \n\n Hwjik ki Oinadi bot se feature ayamba yadri under development leiri warwbiroi . Eshei tase hi hairkoh ") 
        if user_input.startswith('Bina'):
            self.send_message("Kei takpigadabno? Nungaibiribo? \n\n Ming ga kwbirkeh ne ngasidi  🤗🤗🤗 \n\n Hwjik ki Oinadi bot se feature ayamba yadri under development leiri warwbiroi . Eshei tase hi hairkoh ")                                  
        if user_input.startswith('hi'):
            self.send_message(self.messages['greet'])   
        if user_input.startswith('Oi'):
            self.send_message(self.messages['greet']) 
  #flirting lines           
        if "i love you" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine")
        if "i love u" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine") 
        if "I love you" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine") 
        if "I love u" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine")   
        if "iloveU" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine")
        if "i love U" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine")  
        if "I love U" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine") 
        if "IloveU" in user_input:
            self.send_message("Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine")              
                 
        if "tlle" in user_input:
            self.send_message("Tangano ! Tnle na hanna hekta haido ftte yam na ! Hotnaba Kallo")
        if "tle" in user_input:
            self.send_message("Tangano ! Tnle na hanna hekta haido ftte yam na ! Hotnaba Kallo") 
        if "talle" in user_input:
            self.send_message("Tangano ! Tnle na hanna hekta haido ftte yam na ! Hotnaba Kallo")
        if "Talle" in user_input:
            self.send_message("Tangano ! Tnle na hanna hekta haido ftte yam na ! Hotnaba Kallo")           
            
            
 #ver3           
        if "/commands" in user_input:
            self.send_message("The following are the commands for Bina: \n\n *@binaocr_bot* - Select this to convert any text in a picture to text format and send it to u \n\n /movies - shows the movie menu \n\n /audio - shows the song menu \n\n /book - shows books menu \n\n /motivate - sends daily updated motivational lines \n\n /hatlo<_usernamewithoutspace_> - kills the target for fun /wallpaper - gets new wallpaper daily \n\n /corona - gets corona updates daily")  
        if "/movies" in user_input: 
            self.send_message(self.messages['movies'])
        if "/uploads" in user_input:
            self.send_message("1) */nomadland* - Nomadland is a 2020 American film  \n\n 2) */league* - Zack Snyder's Justice League \n\n 3) */dil* - Dil Bechara (transl. The helpless heart) is a 2020 Indian Hindi film \n\n 4)*/fault*- Fault in the stars \n\n 5) */feet* - Five Feet Apart is a 2019 American romantic film   \n\n 6) Joker is a 2019 American psychological thriller film \n\n 7) */war* - War is a 2019 Indian Hindi film        \n\n 7) ...... ") 
        
               
        if "/audio" in user_input:
            self.send_message(self.messages['song'])
        if "/book" in user_input:
            self.send_message("Sombu Taram Na okchari ! \n\n Adom2 gi apam ba books sing /books<apamba_book_maming> space amta ywdana asigi format ta thabirkoh \n\n Ei 24hrs ki manungda adom gi apamba books to update twjarkke \n\n use function movies where <apamba_book_maming> should be replaced by the desired name ! \n\n\n\n NOTE:Adom gi book to kari gumba leiba tarbdi /library nmaga download twbiyu \n\n Remember it usually takes 24hrs ! If u get this menu again,I have recieved your order and will be uploaded on the */library* secion")    
        if "/library" in user_input:
             self.send_message("1) /sample3 \n\n 2) File name 3)..... no one has requested so it appears as file name") 
        if "/motivate" in user_input:
             self.send_message("Many of life’s failures are people who did not realize how close they were to success when they gave up.\n\n – Thomas A. Edison")
        if "/corona" in user_input:
             self.send_message("*as of 22th May, 2021* \n\n Tested positive today - 757 \n\n Deaths - 13 \n\n Discharged - 500 ")       
        
            
        if "kei chage yam fajeise" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai \n 🤔🤔 ')
        if "kei chage yam fajeiC" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng yam fjeise" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng yam fjei se" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng yam fajei C" == user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng yam fjei C" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng suk fajeise" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage ng fajeise" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage nask yam fajeiC" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage nashk yam fajeiC" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ')
        if "kei chage nashk yam fajeise" in user_input:
            self.send_message('Maybe Ei bu saba Programmer do mashk fajaramba yai 🤔🤔 ') 
       
        Hello = user_input    
        print(user_input) 
        print(self.user_name)       
     
        if "oi bina" in user_input:
            self.send_message('Keino Mi khu kw lak kw lude yaroi😆😆 fagi twbnida kei haige?')
        if "Oi bina" in user_input:
            self.send_message('Keino Mi khu kw lak kw lude yaroi😆😆 fagi twbnida kei haige?')
        if "Oii bina" in user_input:
            self.send_message('Keino Mi khu kw lak kw lude yaroi😆😆 fagi twbnida kei haige?')
        if "oii bina" in user_input:
            self.send_message('Keino Mi khu kw lak kw lude yaroi😆😆 fagi twbnida kei haige?')
        if user_input.startswith("ok"):
            self.send_message("Keino, OK tarise ?")
        if user_input.startswith("/hatlo"):
            
            self.send_message("Aye...Boss")
            self.send_message("Getting Ready")
            kill = self.send_message(" https://thumbs.gfycat.com/DeadImpeccableCardinal-max-1mb.gif " )
            time.sleep(2)
            self.delete_message(kill)            
            dead = self.send_message("https://bit.ly/2SVQKCh")  
            self.send_message("Killing....")
            time.sleep(2)
            self.delete_message(dead)
            user = user_input.replace("/hatlo","")
            if user.startswith(" "):
                self.send_message("I was shooting for nothing ! At least specifiy the target")       
            else:
                 if user_input.startswith("/hatlo"):
                     user = user_input.replace("/hatlo","")
                     self.send_message(user)
                     self.send_message("_Almost complete....._")
                     self.send_message(user)
                     self.send_message("_is dead_")
                     self.send_message("_RIP_")
                     self.send_message("https://bit.ly/3yjzSFy")
                     self.send_message("⚰️")
                     self.send_message("😎️😎️😎️😎️")
                    

       
           
           
       
            
            
       


        if "/nomadland" in user_input:
            self.send_message("https://mega.nz/file/oO4kHLBZ#328Wl3zaMa6hFnW13Rg10UoQTJtnXzVyoEP57ZWILOw") 
        if "/league" in user_input:
            self.send_message("https://mega.nz/file/Vbw1DaiD#sPl6dFj536kgpsYM45wxAlSe6bYqbkDHECAo8NMSoEA")
        if "/dil" in user_input:
            self.send_message("\n\n https://bit.ly/3oqkcvH \n\n") 
        if "/fault" in user_input:
            self.send_message("https://bit.ly/2RkPFDI")  
        if "/feet" in user_input:
            self.send_message("https://bit.ly/3fqE79P")  
        if "/joker" in user_input:
            self.send_message("Come back after 24hrs Updating database")  
        if "/war" in user_input:
            self.send_message("https://bit.ly/2QsZe2V \n\n _for srt(sub)_ Click below link \n\n https://bit.ly/3wb6fVh")                  
        if "/tutorial" in user_input:
            self.send_message("Sending.... \n\n ") 
        if "/tutorial" in user_input:
            self.send_message("Steps : 1st -Download ADM from play store \n\n ") 
        if "/tutorial" in user_input:
            self.send_message("2nd - *@Binamagnet_bot*   \n\n click on the highlighted text and follow next steps ") 
        if "/tutorial" in user_input:
            self.send_message("3rd - type any file you wanna search \n\n 4th - choose the file which u like _size,date_ ,etc \n\n 5th step - copy the text on the magnet link part \n\n 6th - On google search \n\n http://magnet2torrent.com \n\n 7th step - paste what u copied and it should download a file \n\n 8th step - open the downloaded file \n\n 9th step- on the ADM interface choose start")
        if "/tutorial" in user_input:     
            bot.sendVideo(self.chat_id,video=open('lisa.mp4','rb'), supports_streaming=True) 
        if "/wallpaper" in user_input:
            bot.sendPhoto(self.chat_id,photo=open('lisa.jpg','rb'))
        if "/sample3" in user_input:
            self.send_message("Sending....")
            bot.sendDocument(self.chat_id,document=open('lisa.pdf','rb'))    
                
           
           
            
            
            
                
           
        if "Ok bina" in user_input:
            self.send_message("Keino, OK tarise ?")
        if "Okay" in user_input:
            self.send_message("Keino, OK tarise ?")
        if "Okhay" == user_input:
            self.send_message("Keino, OK tarise ?")
        if "ehey" in user_input:
            self.send_message("Eisu Khire Ng da nTe")
        if "Ehey" in user_input:
            self.send_message("Eisu Khire Ng da nTe")
        if "Eheyy" in user_input:
            self.send_message("Eisu Khire Ng da nTe")
        if "thank you" in user_input:
            self.send_message("Welcome")
        if "Thank you" in user_input:
            self.send_message("Welcome")
            
        if "ntra bina" in user_input:
            hehe = self.send_message("Mani chummi")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.delete_message(hehe)
            time.sleep(1)
            self.send_message("100% chumme haige twne \n hehe")
            
        if "ntr bina" in user_input:
            hehe = self.send_message("Mani chummi")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.delete_message(hehe)
            time.sleep(1)
            self.send_message("100% chumme haige twne \n hehe")    
           
        if "ntr Bina" in user_input:
            hehe = self.send_message("Mani chummi")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.delete_message(hehe)
            time.sleep(1)
            self.send_message("100% chumme haige twne \n hehe")     
            
         
        if "ntra Bina" in user_input:
            hehe = self.send_message("Mani chummi")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.send_message("nte")
            time.sleep(1)
            self.delete_message(hehe)
            time.sleep(1)
            self.send_message("100% chumme haige twne \n hehe")  
            
            
        if "angry" in user_input:
            self.send_message("https://64.media.tumblr.com/b7257baff3c43dfc3f65c8ed99485a66/53670c51514f4659-30/s540x810/cb2a3d12722425d06b45f3a742e04d29c3876dfe.gifv") 
        if "saore" in user_input:
            self.send_message("https://64.media.tumblr.com/b7257baff3c43dfc3f65c8ed99485a66/53670c51514f4659-30/s540x810/cb2a3d12722425d06b45f3a742e04d29c3876dfe.gifv")     
        if "saogre" in user_input:
            self.send_message("https://64.media.tumblr.com/b7257baff3c43dfc3f65c8ed99485a66/53670c51514f4659-30/s540x810/cb2a3d12722425d06b45f3a742e04d29c3876dfe.gifv")   
        if "sorry" in user_input:
            self.send_message("It's Ok ! humans make mistakes")                
           
            
        if user_input.startswith("eh"):
            self.send_message("HAHA")    
        if "kei charge bina" in user_input: 
            self.send_message('keino haibirise AI bu pot ka chanabro ? Yes I do eat data. HEHE i mean i take in data but noot food !!')         
        if "nungC ye bina" in user_input:
            self.send_message('Esh Hwjik ki matam se thaja yapotte ne? Ei gi kei twba ngam gani')
        if "kei tw haino bina" in user_input:
            self.send_message('Lairik Yam heiyo Ema Epa Seba Ning thina twba ngmnaba, Aduga khnnase LOL')
        if "ngwre ei di ng ngonda" in user_input:
            self.send_message('Chtlo amta angang na ko Lairik to amta paocho mi amta hanna oigo , Thok mok  !! hayeng wai ng Gi adum oidoine')
        if "keidwse haino" in user_input:
            self.send_message('Song am request twrkoh dana')
                                
        if user_input.startswith('Oi'):
            self.send_message(self.messages['greet'])   
        if user_input.startswith('oii'):
            self.send_message(self.messages['greet'])   
        if user_input.startswith('Ui'):
            self.send_message(self.messages['greet'])
        if user_input.startswith('ui'):
            self.send_message(self.messages['greet'])    
        if user_input.startswith('uii'):
            self.send_message(self.messages['greet'])  
        if user_input.startswith('Hey'):
            self.send_message(self.messages['greet'])  
        if user_input.startswith('heyy'):
            self.send_message(self.messages['greet'])
        if user_input.startswith('heyy'):
            self.send_message(self.messages['greet']) 
        if user_input.startswith('What makes bina happy?'):
            self.send_message(self.messages['happy'])     
        if user_input.startswith('oye'):
            self.send_message(self.messages['greet'])  
        if user_input.startswith('Oye'):
            self.send_message(self.messages['greet'])                  
        if user_input.startswith('nyt'):
            self.send_message(self.messages['sleep'])   
        if user_input.startswith('night'):
            self.send_message(self.messages['sleep'])
        if user_input.startswith('good night'):
            self.send_message(self.messages['sleep'])     
        if user_input.startswith('Nyt'):
            self.send_message(self.messages['sleep'])    
        if user_input.startswith('Good night'):
            self.send_message(self.messages['sleep'])                 
                               
                          
       
       
        elif user_input.startswith('/eshei') and user_input[6:]!='':
            if 'open.spotify.com' in user_input[6:]:
            	self.send_message(self.messages['spotify_input_error'])

            else:
                self.process_request(user_input)

       

        pass 

def start_new_chat(msg):
    Process(target=Chat, args=(msg,)).start()
    

bot.message_loop(start_new_chat, run_forever=True)
