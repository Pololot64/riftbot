#Looperman api 0.3 Copyright Paul-E 2019
import urllib.request
import bs4 as BeautifulSoup4
from bs4 import *


##################
categories = {"40":"Accordion",
    "35":"Bagpipe",
    "36":"Banjo",
    "2":"Bass",
    "43":"Bass Guitar",
    "44":"Bass Synth",
    "39":"Bass Wobble",
    "31":"Beatbox",
    "42":"Bells",
    "23":"Brass",
    "34":"Choir",
    "37":"Clarinet",
    "28":"Didgeridoo",
    "1":"Drum",
    "7":"Flute",
    "5":"Fx",
    "24":"Groove",
    "33":"Guitar Acoustic",
    "3":"Guitar Electric",
    "25":"Harmonica",
    "41":"Harp",
    "30":"Harpsichord",
    "32":"Mandolin",
    "22":"Orchestral",
    "26":"Organ",
    "11":"Pad",
    "20":"Percussion",
    "21":"Piano",
    "46":"Rhodes Piano",
    "12":"Scratch",
    "9":"Sitar",
    "45":"Soundscapes",
    "10":"Strings",
    "4":"Synth",
    "8":"Tabla",
    "38":"Ukulele",
    "29":"Violin",
    "6":"Vocal",
    "27":"Woodwind"}

genres = {"56":"8Bit Chiptune",
    "52":"Acid",
    "3":"Acoustic",
    "2":"Ambient",
    "66":"Big Room",
    "33":"Blues",
    "65":"Boom Bap",
    "37":"Breakbeat",
    "21":"Chill Out",
    "36":"Cinematic",
    "13":"Classical",
    "51":"Comedy",
    "44":"Country",
    "39":"Crunk",
    "17":"Dance",
    "55":"Dancehall",
    "30":"Deep House",
    "23":"Dirty",
    "18":"Disco",
    "11":"Drum And Bass",
    "5":"Dub",
    "49":"Dubstep",
    "64":"EDM",
    "42":"Electro",
    "16":"Electronic",
    "15":"Ethnic",
    "25":"Folk",
    "19":"Funk",
    "46":"Fusion",
    "24":"Garage",
    "31":"Glitch",
    "43":"Grime",
    "53":"Grunge",
    "48":"Hardcore",
    "61":"Hardstyle",
    "27":"Heavy Metal",
    "7":"Hip Hop",
    "22":"House",
    "63":"Indie",
    "38":"Industrial",
    "6":"Jazz",
    "10":"Jungle",
    "62":"Lo-Fi",
    "57":"Moombahton",
    "34":"Orchestral",
    "50":"Pop",
    "60":"Psychedelic",
    "14":"Punk",
    "8":"Rap",
    "20":"Rave",
    "4":"Reggae",
    "32":"Reggaeton",
    "45":"Religious",
    "12":"RnB",
    "1":"Rock",
    "29":"Samba",
    "41":"Ska",
    "59":"Soul",
    "47":"Spoken Word",
    "9":"Techno",
    "28":"Trance",
    "54":"Trap",
    "58":"Trip Hop",
    "35":"Weird"}

def cids():
    return categories
def gids():
    return genres
##################

print("RESTART")

def search(cid="", gid="", keywords="", page=""):
    """Search for loops with cid-category, gid-genre, and keywords-search term."""
    """Returns a dictionary of loop names and their urls."""
    try:
        categories = ids.cids()
        genres = ids.gids()
        if cid != "":
            for i in list(categories):
                if cid.lower() in categories[i].lower():
                    cid = "cid=" + str(i) + "&"
                    break
        if gid != "":
            for i in list(genres):
                if gid.lower() in genres[i].lower():
                    gid = "gid=" + str(i) + "&"
        if keywords != "":
            keywords = "keys=" + str(keywords) + "&"
            keywords = keywords.replace(" ", "+")
        #Generate URL
        base_page = "https://www.looperman.com/loops?"
        if page != "":
            page_num = page
        else:
            page_num = 0
        url_searches = ""
        url = base_page + "page=" + str(page_num) + "&" + str(cid) + str(gid) + str(keywords) + "order=name&dir=d"

        ##print(url)
        #Open page in bs4
        print("url generated: " + str(url))
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        tags = soup('a')
        print("html loaded...")
        #Get loops off that page
        hashtags = {}
        for tag in tags:
            tag_str = str(tag.get('href', None))
            term = "https://www.looperman.com/loops/detail/"
            if term in tag_str:
                name = tag_str[len(term):]
                if "/" in name:
                    loop_num = str(name)[:name.index("/")]
                    loop_id = str(name)[name.index("/") + 1:] 
                    loop_bpm = str(name)[:name.index("bpm")]
                    if loop_id not in hashtags:
                        hashtags.update({loop_id:{"url":tag_str, "id":loop_num}})
        if len(list(hashtags)) < 1:
            print("Cannot find any loops...")   
        print("There are " + str(len(hashtags)) + " loops.")    
        return hashtags
    except:
        print("Page Error...Cannot find any loops.")
        return {}

def get_info(url, loop_id):
    if True:
        """returns download url, bpm, artist, and copyright"""
        html = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html, features="html.parser")
        tags = soup('div')

        #Find Download Link
        for tag in tags:
            tag_str = str(tag)
            if "www.looperman.com/media/loops" in tag_str and loop_id in tag_str and ".mp3" in tag_str:
                code = tag_str[:tag_str.index(".mp3") + 4]
                break 
        dl = code[code.index("rel=") + 5:]

        #Find BPM
        for tag in tags:
            tag_str = str(tag)
            if "tempo=" in tag_str:
                code = tag_str[tag_str.index("tempo=") + 6:tag_str.index("tempo=") + 9]
                break 
        tempo = code

        #Find Artist
        for tag in tags:
            tag_str = str(tag)
            if "Verified Member" in tag_str:
                tag_str = tag_str[tag_str.index("Verified Member") + 17:]
                code = tag_str[:tag_str.index("</a>")]
                break 
        artist = code

        #Find Artist Profile
        for tag in tags:
            tag_str = str(tag)
            if "So, who is " in tag_str:
                code = tag_str[tag_str.index("So, who is ") + 11:]
                #code = tag_str[:tag_str.index("</a>")]
                break 
        artist_url = code

        return {"tempo":tempo, "dl":dl, "artist":artist, "profile":artist_url}
    else:
        print("Loop does not exist")
        return {"tempo":0, "dl":""}

async def cmd_looperman(message):
    channel = message.channel
    content = message.content
    
    cmds = content[9:] #This line needs tweaking
    await send(channel, ("Searching Looperman..."))
    if "search" in cmds:
        term = cmds[9:]
        loops = search(keywords=str(term), page=0)
    if "genre" in cmds:
        genre = cmds[8:]
        loops = search(gid=str(genre), page=0)
    if "category" in cmds:
        category = cmds[11:]
        loops = search(cid=str(category), page=0)

    await send(channel, (str(len(loops)) + " matching loop(s): "))
    message_list = []
    for loop in list(loops):
        url = loops[loop]["url"]
        loop_id = loops[loop]["id"]
        loop_info = get_info(url, loop_id)
        download_url = loop_info["dl"]
        artist = loop_info["artist"]
        txt = "Name: " + str(loop_id)[:20] + " by " + str(artist) + ". \n" + str(download_url) + "\n"
        await send(channel, (txt))
     
    
    
register_command("looperman", cmd_looperman)
