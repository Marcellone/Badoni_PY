#!/usr/bin/env python

import requests
import time
from bs4 import BeautifulSoup
from discord_webhooks import DiscordWebhooks
webhook=DiscordWebhooks("https://discord.com/api/webhooks/760050656542326785/rDFVNuo953TiTgWSqTeJG12NiggjiFjwmb7ukP6CjEApa73qCW6BEJLsgrOPLy65cAmV")
urlBadoni = "https://www.iisbadoni.edu.it/categoria/circolari"


def scrape():
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


def sendWebhook(entry):
    webhook.set_content(title=entry["titolo"],
                        description=entry["sommario"]+"\nData: "+entry["data"],
                        url=entry["url"],
                        color=0xFF0000)
    webhook.set_author(name="Nuova circolare")
    webhook.set_footer(text="Badoni circolari")
    webhook.send()   
    return True


def isLast(url):
    with open("lastEntry.txt", "r") as f:
        lastEntry = f.read()
    return url == lastEntry


def setLast(url):
    with open("lastEntry.txt", "w+") as f:
        f.write(url)


while True:
    isNew = False
    scraped = scrape()
    print("scraped")
    #for entry in reversed(scraped):
        #if isNew:
            #sendWebhook(entry)
        #if isLast(entry["url"]):
            #isNew = True


    setLast(scraped[2]["url"])
    print("writed last")
    time.sleep(240)

