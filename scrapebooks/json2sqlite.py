import sqlite3
import json

def convert_to_float(number_str):
    try:
        number_str = number_str.replace('.', '')
        number_str = number_str.replace(',', '.')
        number = float(number_str)
    except:
        number = None
    return number

conn = sqlite3.connect('books.db')
conn.execute("CREATE TABLE Knjige (naziv text, kategorija text, autor text, cena float, izdavac text, godina_izdanja int, broj_strana int, tip_poveza text, format text, opis text);")
with open('books.json', 'r', encoding="utf8") as json_file:
    books = json.load(json_file)
    for book in books:
        conn.execute("INSERT INTO Knjige (naziv, kategorija, autor, cena, izdavac, godina_izdanja, broj_strana, tip_poveza, format, opis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                      (book["naziv"], book["kategorija"], book["autor"], convert_to_float(book["cena"]), book["izdavac"], book["godina_izdanja"], book["broj_strana"], book["tip_poveza"], book["format"], book["opis"]))
conn.commit()
conn.close()
