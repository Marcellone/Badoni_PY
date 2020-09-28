# scraper per circolari Badoni, caso coronavirus, data 23/02/2020 Marcellino Alessandro

#----------------------import dell librerie-----------------------

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from discord_webhooks import DiscordWebhooks
import time

#---------impostazioni di selenium per i chrome webdriver---------

chrome_options = Options()
# chrome_options.add_argument("--headless") #Per farlo eseguire in background
chrome_options.add_argument("disable-gpu") #Per evitare bugs
chrome_options.add_argument("log-level=3") #Solo errori (Rimuove logs inutili)
chrome_options.add_argument("window-size=1920,1080") #Imposta dimensione finestra essendo headless
driver=webdriver.Chrome(executable_path="chromedriver",chrome_options=chrome_options) #Load per google chrome come webdriver

#-------------------carica il webhook di discord------------------

webhook=DiscordWebhooks("https://discord.com/api/webhooks/760050656542326785/rDFVNuo953TiTgWSqTeJG12NiggjiFjwmb7ukP6CjEApa73qCW6BEJLsgrOPLy65cAmV")  #Link webhook discord

#---------------------carica l'url del sito-----------------------

driver.get("https://www.iisbadoni.edu.it/categoria/circolari") #Url da caricare

#-----------------------------------------------------------------

def getNumeroCircolari():
    n = 0
    for i in driver.find_elements_by_xpath("//span[@class='field-content']"):
        try:
            titolo = i.find_element_by_xpath(".//a").text
            if titolo != "Leggi tutto ...":
                n = n + 1
        except:
            continue
    return n

#-----------------------------------------------------------------

def getTitoli(i):
    titoli = []
    for l in driver.find_elements_by_xpath("//span[@class='field-content']"):
        try:
            titolo = l.find_element_by_xpath(".//a").text
            if titolo != "Leggi tutto ...":
                titoli.append(titolo)       #.append inserisce il valore nella lista() 
        except:
            continue
    res = titoli[i]
    return res

#-----------------------------------------------------------------

def getLinks(i):
    links = []    
    for l in driver.find_elements_by_xpath("//span[@class='field-content']"):
        try:
            link = l.find_element_by_xpath(".//a").get_attribute("href")
            if link != "Leggi tutto ...":
                links.append(link)
        except:
            continue
    return links[i]

#-----------------------------------------------------------------

def getDate(i):
    date = []
    for l in driver.find_elements_by_xpath("//span[@class='field-content']"):
        data = l.text
        if data != "Leggi tutto ..." and len(data) == 10:
            date.append(data)
    return date[i]

#---------------------------discord web hook----mette tutto quello che abbiamo estratto dal sito assieme------------------------

while True:
    time.sleep(120)
    circolari = {}
    for i in range(getNumeroCircolari()):
        circolari[i] = {"titolo":getTitoli(i),"link":getLinks(i),"data":getDate(i)}
 
    with open("ultimacirc.txt",'r') as f:
        if f.read() != circolari[0]["titolo"]:
            webhook.set_content(title=circolari[0]["titolo"],
                                description="Data: "+circolari[0]["data"],
                                url=circolari[0]["link"],
                                color=0xFF0000)

            webhook.set_author(name="Nuova circolare")
            webhook.set_footer(text="Badoni circolari")
            webhook.send()   
            print("webhook inviato")

    with open("ultimacirc.txt", 'w+') as f:
        f.write(circolari[0]["titolo"])

#---------------------------------------------------------------------------------------------------------------------------------

