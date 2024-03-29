import tkinter
from tkinter import *
from os.path import expanduser
from random import randint
import multiprocessing
from tkinter import filedialog
from tkinter.ttk import Progressbar
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import io
from mtranslate import translate
from playsound import playsound
import sys
import time
from threading import *
import os
from tkinter import messagebox
desktop = expanduser("~/Documents")
agency = "verge"

from asciimatics.effects import Cycle, Stars
from asciimatics.renderers import FigletText
from asciimatics.scene import Scene
from asciimatics.screen import Screen
def start_anim():
    Screen.wrapper(demo)
def sound():
    while True:
        playsound('tune.mp3', block=True)
        playsound(None)

def demo(screen):
    effects = [
        Cycle(
            screen,
            FigletText("ASCIIMATICS", font='big'),
            int(screen.height / 2 - 8)),
        Cycle(
            screen,
            FigletText("ROCKS!", font='big'),
            int(screen.height / 2 + 3)),
        Stars(screen, 200)
    ]
    screen.play([Scene(effects, 500)])

def chooseDirectory():
    currdir = os.getcwd()
    tempdir = filedialog.askdirectory(parent=root, initialdir=currdir, title='Please select a directory')
    program.directory = tempdir
currentAgency = 0
def switchAgencies(agencies):
    print("called Agencies")
    global currentAgency
    currentAgency = currentAgency + 1
    if currentAgency > 2:
        currentAgency = 0
    if currentAgency == 1:
        print("switching to techradar")
        agencies = "techradar"
    elif currentAgency == 2:
        print("switching to engadget")
        agencies = "engadget"
    elif currentAgency == 0:
        print("switching to verge")
        agencies = "verge"
    button4['text'] = agencies
class Scrapers(object):
    def __init__(self):
        global currentAgency
        currentAgency = 0
        self.thread1 = None
        self.stop_threads = Event()
        self.stopped = False
        self.CloseLabel = Label(root, text = "Finalizing before breaking!")
        self.directory = desktop
        self.needToSkip = False
    def waitandkill(self):
        time.sleep(1)
        if (self.stopped == True):
            print("DEAD")
        else:
            self.waitandkill
    def stopTheThread(self):
        print("CALLED ME TOO?")
        self.stop_threads.set()
        self.CloseLabel.pack()
        self.waitandkill
        print("calling wait")
    def skip(self):
        self.needToSkip = True
    def start_thread(self):
        
        print("thread started")
        Skip = Button(topFrame, text = "SKIP!", command = self.skip)
        Skip.pack(side = BOTTOM)
        try:
            f = io.open(self.directory + "/TranslatedNews.txt", "w", encoding="utf-8")
        except IOError:
            print("FILE ERROR!" + self.directory + "/TranslatedNews.txt")
            messagebox.showerror("ACCESS ERROR!", "We can't access "+ self.directory + "/TranslatedNews.txt")
            sys.exit()
        try:
            f = io.open(self.directory + "/News.txt", "w", encoding="utf-8")
        except IOError:
            print("FILE ERROR!" + self.directory + "/News.txt")
            messagebox.showerror("ACCESS ERROR!", "We can't access "+ self.directory + "/News.txt")
            sys.exit()
        if self.thread1!=None:
            print("NO!")
        else:
            self.thread1 = Thread(target = self.start_now)
            self.thread1.start()
            p.start()

            threadActive = 1
    def start_now(self):
        
        print("Getting" + button4['text'])
        if button4['text'] == "techradar":
            progress = Progressbar(topFrame, orient = HORIZONTAL, length = 100, mode = 'determinate')
            progress['value'] = 0
            progress.pack(side = TOP) 
            Labels = Label(topFrame, text = "SCRAPING")
            Labels.pack(side = TOP)
            texts = "change"
            main_url = 'https://www.techradar.com/news'
            uClient = uReq(main_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("div",{"class":"listingResult"})
            
            Articles = len(containers)
            print(Articles)
            filename = self.directory + "/News.txt"
            trans_filename = self.directory + "/TranslatedNews.txt"
            f = io.open(filename, "w", encoding="utf-8")
            f.write("ACTIVE")
            t = io.open(trans_filename, "w", encoding ="utf-8")
            t.write("ACTIVE")
            Labels.config(text = "setting file!")
            i = 0
            CurrentTitle = Label(topFrame, text = "Preparing...")
            CurrentTitle.pack(side = TOP)
            for container in containers:
                
                
           
                i = i + 1 
                Labels.config(text = "jumping to URL!")
                print(container["class"])
                if 'sponsored-post' in container["class"]:
                    print("\n WE'VE CATCHED AN AD!")
                    continue
                progress['value'] = i * 100 / Articles
                local_progress = Progressbar(topFrame, orient = HORIZONTAL, length = 120, mode = 'determinate')
                local_progress['value'] = 0
                local_progress.pack(side = BOTTOM)
                requiredURL = container.a["href"]
                secondary_URL = requiredURL
                print("Set target URL!" + requiredURL)
                secClient = uReq(secondary_URL)
                news_html = secClient.read()
                secClient.close()
                news_soup = soup(news_html, "html.parser")
                news_soup.decode('utf-8', 'ignore')
                squash = news_soup.findAll("div",{"class":"icon-plus_circle"})
                print(len(squash))
                if len(squash)>0:
                    print("\n WARNING! THIS IS NOT AN ARTICLE! ")
                    print(container.div["class"])
                    continue
                news_containers = news_soup.findAll("header")
                if len(news_containers)>0:
                    news_title = news_containers[0].h1.text
                    CurrentTitle.config(text = news_title)
                    Labels.config(text = "Extracted Title!")
                else:
                    print("ERROR! NO TITLE AT "+secondary_URL)
                    Labels.config(text = "Failed to extract title")
                news_body = news_soup.findAll("div", {"id":"article-body"})

                print("\n TITLE: " + news_title)
                f.write("\n \n" + news_title + "\n")
                print("Now translating...")
                translatedQuery = translate(news_title, "ru", "en")
                t.write("\n \n" + translatedQuery + "\n")
                paragraphs = news_body[0].findAll("p")
                print("Title Recorded!")
                local_progress['value'] = 10
                y = len(paragraphs)
                x = 0
                fullText = ""
                fullText2 = ""
                for paragraph in paragraphs:

                    x = x + 1
                    local_progress['value'] = x * 100 / y + 10
                    stringx = str(x)         
                    Labels.config(text = "Getting paragraph " + stringx + "...")
                    print(paragraph.text + "\n \n \n")
                    if x >= y/2:
                        fullText2 = fullText2 + paragraph.text.strip()
                    else:
                        fullText = fullText + paragraph.text.strip()
                    Labels.config(text = "Written and Translated Paragraph" + stringx + "!")
                    print("Writing Paragraph " + stringx + "...")
                    if self.needToSkip:
                        break
                    
                if self.needToSkip:
                    self.needToSkip = False
                    continue
                translatedQuery = translate(fullText, "ru", "en")
                completeText = translatedQuery
                translatedQuery = translate(fullText2, "ru", "en")
                completeText = completeText + translatedQuery
                f.write("\n" + fullText + fullText2)
                t.write("\n" + completeText)
                news_picture = news_soup.findAll("source", {"class":"hero-image"})
                Labels.config(text = "Getting image...")
                if len(news_picture) > 0:
                    article_pic = news_picture[0].get("data-original-mos")
                    Labels.config(text = "Picture recieved!")
                else:
                    print("\n THIS ARTICLE HAS NO PICTURE! ")
                    Labels.config(text = "Failed to locate picture :(")
                local_progress['value'] = 120
                f.write("\n PICTURE URL: " + article_pic)
                t.write("\n PICTURE URL: " + article_pic)
                if self.stop_threads.is_set():
                    p.terminate()
                    print("I SURRENDER!")
                    self.stopped = True
                    f.close()
                    t.close()
                    self.CloseLabel.config(text = "you may close now")
                    sys.exit() 
                    self.CloseLabel.config(text = "I tried, I failed")
                    break
                else:
                    print("NOTHING IS STOPPING ME!")
                    Labels.config(text = "Finished the article!")
            #brand = divWithInfo.div.a.img["title"]
            #title_container = divWithInfo.find("a", "item-title")
            #product_name = title_container.text
            #shipping_container = divWithInfo.find("li", "price-ship")
            #shipping_cost = shipping_container.text.strip()

            #print("brand:"+brand)
            #print("name:"+product_name)
            #print("shipping:"+shipping_cost)
            #print("\n")

            #f.write(brand + "," + product_name.replace(",", "|") + "," + shipping_cost + "\n")
            Labels.config(text = "All Done!")
            f.close()
            t.close()
        elif button4['text'] == "verge": 
            progress = Progressbar(topFrame, orient = HORIZONTAL, length = 100, mode = 'determinate')
            progress['value'] = 0
            progress.pack(side = TOP) 
            Labels = Label(topFrame, text = "SCRAPING")
            Labels.pack(side = TOP)
            texts = "change"
            main_url = 'https://www.theverge.com/tech'
            uClient = uReq(main_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("div",{"class":"c-compact-river__entry"})
            Articles = len(containers)
            filename = self.directory + "/News.txt"
            trans_filename = self.directory + "/TranslatedNews.txt"
            f = io.open(filename, "w", encoding="utf-8")
            f.write("ACTIVE")
            t = io.open(trans_filename, "w", encoding ="utf-8")
            t.write("ACTIVE")
            Labels.config(text = "setting file!")
            i = 0
            CurrentTitle = Label(topFrame, text = "Preparing...")
            CurrentTitle.pack(side = TOP)
            for container in containers:
                i = i + 1 
                Labels.config(text = "jumping to URL!")
                print(container["class"])
                if container["class"] == ['c-compact-river__entry', 'c-compact-river__entry--featured']:
                    print("\n WE'VE CATCHED A BUG!")
                    continue
                if container.div["class"] != ["c-entry-box--compact", "c-entry-box--compact--article"]:
                    print("\n WARNING! THIS IS NOT AN ARTICLE! ")
                    print(container.div["class"])
                    continue
                progress['value'] = i * 100 / Articles
                local_progress = Progressbar(topFrame, orient = HORIZONTAL, length = 120, mode = 'determinate')
                local_progress['value'] = 0
                local_progress.pack(side = BOTTOM)
                requiredURL = container.div.a["href"]
                secondary_URL = requiredURL
                print("Set target URL!")
                secClient = uReq(secondary_URL)
                news_html = secClient.read()
                secClient.close()
                news_soup = soup(news_html, "html.parser")
                news_soup.decode('utf-8', 'ignore')
                news_containers = news_soup.findAll("div", {"class":"c-entry-hero__header-wrap"})
                if len(news_containers)>0:
                    news_title = news_containers[0].h1.text
                    CurrentTitle.config(text = news_title)
                    Labels.config(text = "Extracted Title!")
                else:
                    print("ERROR! NO TITLE AT "+secondary_URL)
                    Labels.config(text = "Failed to extract title")
                news_body = news_soup.findAll("div", {"class":"c-entry-content"})
                print("\n TITLE: " + news_title)
                f.write("\n \n" + news_title + "\n")
                print("Now translating...")
                translatedQuery = translate(news_title, "ru", "en")
                t.write("\n \n" + translatedQuery + "\n")
                paragraphs = news_body[0].findAll("p")
                print("Title Recorded!")
                local_progress['value'] = 10
                y = len(paragraphs)
                x = 0
                fullText = ""
                fullText2 = ""
                for paragraph in paragraphs:

                    x = x + 1
                    local_progress['value'] = x * 100 / y + 10
                    stringx = str(x)         
                    Labels.config(text = "Getting paragraph " + stringx + "...")
                    print(paragraph.text + "\n \n \n")
                    if x >= y/2:
                        fullText2 = fullText2 + paragraph.text.strip()
                    else:
                        fullText = fullText + paragraph.text.strip()
                    Labels.config(text = "Written and Translated Paragraph" + stringx + "!")
                    print("Writing Paragraph " + stringx + "...")
                    if self.needToSkip:
                        break
                    
                if self.needToSkip:
                    self.needToSkip = False
                    continue
                translatedQuery = translate(fullText, "ru", "en")
                completeText = translatedQuery
                translatedQuery = translate(fullText2, "ru", "en")
                completeText = completeText + translatedQuery
                f.write("\n" + fullText + fullText2)
                t.write("\n" + completeText)
                news_picture = news_soup.findAll("picture", {"class":"c-picture"})
                Labels.config(text = "Getting image...")
                if (len(news_picture) > 0):
                    if news_picture[0].img != None:
                        article_pic = news_picture[0].img.get("src")
                        Labels.config(text = "Picture recieved!")
                    else:
                        print("\n THIS ARTICLE HAS NO PICTURE! ")
                        Labels.config(text = "Failed to locate picture :(")
                local_progress['value'] = 120
                f.write("\n PICTURE URL: " + article_pic)
                t.write("\n PICTURE URL: " + article_pic)
                if self.stop_threads.is_set():
                    print("I SURRENDER!")
                    self.stopped = True
                    f.close()
                    t.close()
                    self.CloseLabel.config(text = "you may close now")
                    sys.exit() 
                    self.CloseLabel.config(text = "I tried, I failed")
                    break
                else:
                    print("NOTHING IS STOPPING ME!")
                    Labels.config(text = "Finished the article!")
            #brand = divWithInfo.div.a.img["title"]
            #title_container = divWithInfo.find("a", "item-title")
            #product_name = title_container.text
            #shipping_container = divWithInfo.find("li", "price-ship")
            #shipping_cost = shipping_container.text.strip()

            #print("brand:"+brand)
            #print("name:"+product_name)
            #print("shipping:"+shipping_cost)
            #print("\n")

            #f.write(brand + "," + product_name.replace(",", "|") + "," + shipping_cost + "\n")
            Labels.config(text = "All Done!")
            f.close()
            t.close()
        else:
            progress = Progressbar(topFrame, orient = HORIZONTAL, length = 100, mode = 'determinate')
            progress['value'] = 0
            progress.pack(side = TOP) 
            Labels = Label(topFrame, text = "SCRAPING")
            Labels.pack(side = TOP)
            texts = "change"
            main_url = 'https://www.engadget.com/tomorrow'
            uClient = uReq(main_url)
            page_html = uClient.read()
            uClient.close()
            page_soup = soup(page_html, "html.parser")
            containers = page_soup.findAll("article",{"data-component":"PostCard"})
            Articles = len(containers)
            filename = self.directory + "/News.txt"
            trans_filename = self.directory + "/TranslatedNews.txt"
            f = io.open(filename, "w", encoding="utf-8")
            f.write("ACTIVE")
            t = io.open(trans_filename, "w", encoding ="utf-8")
            t.write("ACTIVE")
            Labels.config(text = "setting file!")
            i = 0
            CurrentTitle = Label(topFrame, text = "Preparing...")
            CurrentTitle.pack(side = TOP)
            for container in containers:
                i = i + 1 
                Labels.config(text = "jumping to URL!")
                progress['value'] = i * 100 / Articles
                local_progress = Progressbar(topFrame, orient = HORIZONTAL, length = 120, mode = 'determinate')
                local_progress['value'] = 0
                local_progress.pack(side = BOTTOM)
                requiredURL = container.div.a["href"]
                secondary_URL = 'https://www.engadget.com' + requiredURL
                print("Set target URL!" + secondary_URL)
                secClient = uReq(secondary_URL)
                news_html = secClient.read()
                secClient.close()
                news_soup = soup(news_html, "html.parser")
                news_soup.decode('utf-8', 'ignore')
                news_containers = news_soup.findAll("div", {"data-component":"ArticleHeader"})
                if len(news_containers)>0:
                    news_title = news_containers[0].div.h1.text
                    CurrentTitle.config(text = news_title)
                    Labels.config(text = "Extracted Title!")
                else:
                    print("ERROR! NO TITLE AT "+secondary_URL)
                    Labels.config(text = "Failed to extract title")
                    news_title = "Failed title extraction"
                news_body = news_soup.findAll("div", {"class":"article-text"})
                print("\n TITLE: " + news_title)
                f.write("\n \n" + news_title + "\n")
                print("Now translating...")
                translatedQuery = translate(news_title, "ru", "en")
                t.write("\n \n" + translatedQuery + "\n")
                paragraphs = news_body[0].findAll("p")
                print("Title Recorded!")
                local_progress['value'] = 10
                y = len(paragraphs)
                x = 0
                fullText = ""
                fullText2 = ""
                for paragraph in paragraphs:

                    x = x + 1
                    local_progress['value'] = x * 100 / y + 10
                    stringx = str(x)         
                    Labels.config(text = "Getting paragraph " + stringx + "...")
                    print(paragraph.text + "\n \n \n")
                    if x >= y/2:
                        fullText2 = fullText2 + paragraph.text.strip()
                    else:
                        fullText = fullText + paragraph.text.strip()
                    Labels.config(text = "Written and Translated Paragraph" + stringx + "!")
                    print("Writing Paragraph " + stringx + "...")
                    if self.needToSkip:
                        break
                    
                if self.needToSkip:
                    self.needToSkip = False
                    continue
                translatedQuery = translate(fullText, "ru", "en")
                completeText = translatedQuery
                translatedQuery = translate(fullText2, "ru", "en")
                completeText = completeText + translatedQuery
                f.write("\n" + fullText + fullText2)
                t.write("\n" + completeText)
                news_picture = news_soup.findAll("figure", {"data-component":"DefaultLede"})
                if len(news_picture) == 0:
                    news_picture = news_soup.findAll("figure")
                Labels.config(text = "Getting image...")
                if len(news_picture) > 0:
                    if news_picture[0].img != None:
                        article_pic = news_picture[0].img.get("src")
                        Labels.config(text = "Picture recieved!")
                    else:
                        print("\n THIS ARTICLE HAS NO PICTURE! ")
                        Labels.config(text = "Failed to locate picture :(")
                else:
                    print("\n THIS ARTICLE HAS NO PICTURE! ")
                    Labels.config(text = "Failed to locate picture :(")
                local_progress['value'] = 120
                f.write("\n PICTURE URL: " + article_pic)
                t.write("\n PICTURE URL: " + article_pic)
                if self.stop_threads.is_set():
                    print("I SURRENDER!")
                    self.stopped = True
                    f.close()
                    t.close()
                    self.CloseLabel.config(text = "you may close now")
                    sys.exit() 
                    self.CloseLabel.config(text = "I tried, I failed")
                    break
                else:
                    print("NOTHING IS STOPPING ME!")
                    Labels.config(text = "Finished the article!")
            #brand = divWithInfo.div.a.img["title"]
            #title_container = divWithInfo.find("a", "item-title")
            #product_name = title_container.text
            #shipping_container = divWithInfo.find("li", "price-ship")
            #shipping_cost = shipping_container.text.strip()

            #print("brand:"+brand)
            #print("name:"+product_name)
            #print("shipping:"+shipping_cost)
            #print("\n")

            #f.write(brand + "," + product_name.replace(",", "|") + "," + shipping_cost + "\n")
            Labels.config(text = "All Done!")
            f.close()
            t.close()
texts = "VERGE SCRAPPER"
root = Tk()
program = Scrapers()
mainT = Thread(target=program.start_now)
thread = Thread(target=sound)
animthread = Thread(target=start_anim)
try:
    texts
except NameError:
    theLabel = Label(root, text = "VERGE SCRAPER")
    theLabel.pack()
    print("NO TEXTS!")
else:
    theLabel = Label(root, text = texts)
    theLabel.pack()
    print("FOUND TEXTS!")

p = multiprocessing.Process(target=playsound, args=("tune.mp3",))
stop_thread = False
topFrame = Frame(root)
topFrame.pack()
bottomFrame = Frame(root)
bottomFrame.pack(side=BOTTOM)
button1 = Button(topFrame, text = "Start Scrapping!", command = program.start_thread)
button4 = Button(topFrame, text = agency, command = lambda: switchAgencies(button4['text']))
button2 = Button(topFrame, text = "Choose Text Location", fg = "black", command = chooseDirectory)
button3 = Button(topFrame, text = "STOP!", fg = "red", command = program.stopTheThread)
button3.pack(side = TOP)
button1.pack(side= TOP)
button4.pack(side= TOP)
button2.pack(side = TOP)
root.mainloop()
