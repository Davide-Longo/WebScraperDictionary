import time
import requests
import mysql.connector
from bs4 import BeautifulSoup

#Dichiarazione delle variabili per l'inserimento

#Parola:
#id_parola, termine_parola, definizione_parola, categoria_parola

#Citazione:
#documento_citazione, parola_citazione, testo_citazione

#Immagine:
#URL_immagine, parola_immagine, descrizione_immagine

#Fonte:
#documento_fonte, parola_fonte, URL_fonte

#Recupero del primo URL
page = requests.get("https://www.um.es/lexico-comercio-medieval/index.php/v/letra/a/")
soup = BeautifulSoup(page.content, "html.parser")
nextURL = soup.find("li", class_="resultado even").find("a")["href"]

#Connessione al database
connection = mysql.connector.connect(
  host="localhost",
  user="dbuser",
  password="dbpassword",
  database="dizionario"
)

cursor = connection.cursor()

#Inserimento nel database
while(nextURL != None):

    time.sleep(1)

    page = requests.get(nextURL)
    soup = BeautifulSoup(page.content, "html.parser")

    #Insermento della parola
    id_parola = nextURL.split("/")[len(nextURL.split("/"))-2]
    termine_parola = soup.find("h3", class_="lexema_title").text
    if(soup.find("p", class_="descripcion") != None):
        if(soup.find("nav", class_="breadcrumbs").next_sibling.next_sibling["class"] == ["descripcion"]):
            definizione_parola = soup.find("p", class_="descripcion").text
        else:
            definizione_parola = None
    else:
        definizione_parola = None
    if(soup.find("span", class_="tipo") == None):
        categoria_parola = None
    else:
        categoria_parola = soup.find("span", class_="tipo").text
    cursor.execute("INSERT INTO parola (id, termine, definizione, categoria) VALUES (%s, %s, %s, %s)",
                   (id_parola, termine_parola, definizione_parola, categoria_parola))
    print(id_parola)
    print(termine_parola)
    print(definizione_parola)
    print(categoria_parola)

    #Inserimento delle citazioni
    complementariaIterable = soup.find_all("h4", class_="complementaria")
    if(complementariaIterable != None):
        descripcionIterator = iter(soup.find_all("p", class_="descripcion"))
        if(definizione_parola != None):
            next(descripcionIterator)
        for cit in complementariaIterable:
            documento_citazione = cit.find("em").text
            parola_citazione = id_parola
            testo_citazione = next(descripcionIterator).text
            cursor.execute("INSERT INTO citazione (documento, parola, testo) VALUES (%s, %s, %s)",
                           (documento_citazione, parola_citazione, testo_citazione))

    #Inserimento delle immagini
    imagen_lexemaIterable = soup.find_all("p", class_="imagen_lexema")
    if(imagen_lexemaIterable != None):
        for img in imagen_lexemaIterable:
            URL_immagine = img.find("a")["href"]
            parola_immagine = id_parola
            descrizione_immagine = img.find("a")["alt"]
            cursor.execute("INSERT INTO immagine (URL, parola, descrizione) VALUES (%s, %s, %s)",
                           (URL_immagine, parola_immagine, descrizione_immagine))
    
    #Inserimento delle fonti
    bibliografia = soup.find("ul", class_="bibliografia")
    if(bibliografia != None):
        bibliografiaIterable = bibliografia.find_all("li")
        for src in bibliografiaIterable:
            documento_fonte = ""
            for elem in src.find_all("span"):
                if(elem.find("a") != None):
                    continue
                documento_fonte += elem.text
                documento_fonte += ","
            documento_fonte = documento_fonte[:-1]
            parola_fonte = id_parola
            if(src.find("span", class_="coleccion") == None):
                URL_fonte = None
            else:
                URL_fonte = src.find("span", class_="coleccion").find("a")["href"]
            cursor.execute("INSERT INTO fonte (documento, parola, URL) VALUES (%s, %s, %s)",
                           (documento_fonte, parola_fonte, URL_fonte))
    connection.commit()
    print("Inserita la parola:", termine_parola)
    if(soup.find("span", class_="siguiente") == None):
        nextURL = None
    else:
        nextURL = soup.find("span", class_="siguiente").find("a")["href"]
if(connection.is_connected()):
    connection.close()
print("Estrazione terminata")
