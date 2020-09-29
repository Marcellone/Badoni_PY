#!/usr/bin/env python

import requests
import time
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
webhook=DiscordWebhooks("https://discord.com/api/webhooks/760050656542326785/rDFVNuo953TiTgWSqTeJG12NiggjiFjwmb7ukP6CjEApa73qCW6BEJLsgrOPLy65cAmV")
urlBadoni = "https://www.iisbadoni.edu.it/categoria/circolari"


def scrape():       #esegue lo scrape del sito e ritorna una lista di circolari dalla più recente alla più vecchia
    req = requests.get(urlBadoni)
    soup = BeautifulSoup(req.text, "lxml")

    itemsList = soup.find("div", {"class": "view-content"})
    circolari = []

    for item in itemsList.find_all("div", {"class": "views-row"}):
        for head in item.find_all("a"):
            if head:
                if head.text != "Leggi tutto ...":
                    titolo = head.text
        
                elif head.text == "Leggi tutto ...":
                    link = "https://www.iisbadoni.edu.it/" + head["href"]

        sommario = item.find("p").text
        dataEmissione = item.find("span", {"class": "views-field-created"})
        dataEmissione = dataEmissione.find("span", {"class": "field-content"}).text

        circolari.append({"titolo": titolo,
                          "sommario": sommario,
                          "data": dataEmissione,
                          "url": link})

    return circolari


def sendWebhook(entry):         #manda il webhook a discord
    webhook.set_content(title=entry["titolo"],
                        description=entry["sommario"]+"\nData: "+entry["data"],
                        url=entry["url"],
                        color=0xFF0000)
    webhook.set_author(name="Nuova circolare")
    webhook.set_footer(text="Badoni circolari")
    webhook.send()
    time.sleep(2)
    return True

def sendStartWebhook():
    webhook.set_content(title="Badoni_PY",
                        description="Script con BeautifulSoup4 avviato",
                        url="https://github.com/Marcellone/Badoni_PY",
                        color=0x00FF00)
    webhook.set_author(name="Script avviato")
    webhook.set_footer(text="Badoni circolari")
    webhook.send()   
    return True

def isLast(url):            #ritorna vero se l'url è l'ultimo inviato
    with open("lastEntry.txt", "r") as f:
        lastEntry = f.read()
    return url == lastEntry


def setLast(url):           #salva l'url come ultimo inviato
    with open("lastEntry.txt", "w+") as f:
        f.write(url)
    return True


if sendStartWebhook():
    print("webhook starting inviato")

while True:
    print("\n\nprogram started")
    isNew = False
    scraped = scrape()
    print("\n\nscraped")
    for entry in reversed(scraped):     #ciclo for con lista circolari invertita
        if isNew:                       #se le circolari sono nuove, le invia
            if sendWebhook(entry):
                print("\n\nwebhhok sent\n")
                print(entry)
        if isLast(entry["url"]):
            isNew = True                #se è l'ultima circolare, quelle dopo saranno nuove

    setLast(scraped[0]["url"])
    print("\n\nwrited last entry")
    time.sleep(240)

