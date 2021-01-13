# Badoni_PY

Benvenuto in Badoni_PY, uno scraper per le circolari dell'istituto IIS A. Badoni che invia notifiche quando vengono pubblicate mediante i webhook di discord

Tutte le versioni sono state scritte per python 3

---

## Introduzione

Il progetto nasce durante l'inizio della quarantena, studiato per inviare notifiche quasi immediate riguardo a pubblicazioni di circolari sul sito


## Versione con Selenium

`pip install -r requirements.txt`

`python Badoni_PY.py`

richiede chrome webdriver, scricabili da `https://chromedriver.chromium.org/downloads`, in base alla versione di chrome installata.

- Inserire la path del webdriver (es: `C:/usr/Gianni/desktop/chromedriver.exe`) [Line 19]
  `driver=webdriver.Chrome(executable_path='webdriver_path',options=chrome_options)`

inserire il link del webhook nel file `webhook`

## versione con BeautifulSoup4 (più rapida)

`cd bs4`

inserire il link del webhook nel file `webhook`

`pip install -r requirements.txt`

`python main.py`
 
 
# Link utili

- matrix community: [https://matrix.to/#/+badonipy:matrix.org](https://matrix.to/#/+badonipy:matrix.org)
- discord server: [https://discord.gg/kFyuEECr6R](https://discord.gg/kFyuEECr6R)

Entrambi hanno un bridge, quindi i messaggi vengono inviati in entrambi i server.
Nel server discord è presente il feed per l'I.I.S. A. Badoni.
