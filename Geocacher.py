"""Geocaching online finder"""

import requests
from bs4 import BeautifulSoup

geoladak = []


def recGeocache(url):
    """A rekurzív függvény, ami egy URL-t kap stringként, majd ebben keres, és ha megtalál egy helyes taget,
    akkor abban újra keres.
    Helyes a tag, ami a tag, class attribútuma geocache, van data-treasure attribútuma,
    tag szövege egy pozíció, href attribútuma pedig a következő oldalra vezet """
    try:
        # Lekérjük az URL-t
        data = requests.get(url)
    except:
        return
    # Inicializáljuk a html-parsert
    soup = BeautifulSoup(data.text, "html.parser")
    # Végignézzük az a tageket rekurzívan az oldalon
    for tag in soup.find_all('a'):
        try:
            # Ha létezik a ceocache class attribútum, akkor továbbmegyünk, egyébként nem találtuk meg
            if 'geocache' in tag['class']:
                try:
                    # Geoládákhoz hozzáadjuk a data-treasure attribútum értékét és a pozíciót a tag szövegéből
                    geoladak.append({'data-treasure': tag['data-treasure'], 'position': tag.text})
                    # A href attribútum url-ével meghívjuk rekurzívan a függvényt
                    recGeocache(tag['href'])
                # Ha KeyError-t kapunk, az azt jelenti, hogy az a tagnek nem volt data-treasure vagy href attribútuma
                except KeyError:
                    pass
                finally:
                    # Mivel megtaláltuk a geocaching class-t, amiből csak egy van ezért visszatérünk
                    return
        # Ha KeyError-t kapunk, az azt jelenti, hogy az a tagnek nem volt class attribútuma
        except KeyError:
            pass


if __name__ == "__main__":
    # Kezdő URL beolvasása
    URL = str(input("Adja meg a kezdo url-t: "))
    # Rekurzív függvény meghívása a kezdő URL-lel
    recGeocache(URL)
    # Megtalált kincsek és pozícióik kiíratása
    print("Megtalalt geoladak kincsei és pozicioi: ")
    for i in geoladak:
        print("Pozicio: ", i["position"], "\tKincs: ", i["data-treasure"])
