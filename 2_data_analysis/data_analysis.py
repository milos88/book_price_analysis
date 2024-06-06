import sqlite3
import pandas as pd
from functools import cmp_to_key
import re

def convert_to_float(number_str):
    try:
        number_str = number_str.replace(',', '.')
        number = float(number_str)
    except:
        number = None
    return number

def fix_format(x):
    x = x.lower()
    x = x.replace("xx", 'x')
    x_strings = x.split('x')
    pattern = r'[\d]+[.,]?[\d]*'

    x_strings[0] = re.search(pattern, x_strings[0]).group()
    x_strings[1] = re.search(pattern, x_strings[1]).group()

    x_sizes = [convert_to_float(x_strings[0]), convert_to_float(x_strings[1])]

    return f"{x_sizes[0]}x{x_sizes[1]}"


def clean_dataset(conn, conn_claened_db):
    
    cursor = conn.execute(r'SELECT * FROM Knjige WHERE naziv is not null and kategorija is not null and autor is not null and cena is not null and izdavac is not null and broj_strana is not null and tip_poveza is not null and format is not null and  godina_izdanja is not NULL and opis is not NULL and format like "%x%" and naziv not like "%BOJANKA%" and not broj_strana == 1 and godina_izdanja between 1900 and 2030 and cena < 10000 and broj_strana < 1400')
    rows = cursor.fetchall()
    for row in rows:
        row_list = list(row)
        row_list[8] = fix_format(row[8])
        row = tuple(row_list)
        if convert_to_float(row[8].split('x')[0]) > 100:
            continue
        conn_claened_db.execute("INSERT INTO Knjige (naziv, kategorija, autor, cena, izdavac, godina_izdanja, broj_strana, tip_poveza, format, opis) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                        row)
    conn_claened_db.commit()

def clean_new_dataset(conn):
    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE kategorija LIKE ? or kategorija like ?',
                 ("PSIHOLOGIJA", r"%psihijatrija%", r"%psihologija%"))
    
    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE kategorija LIKE ?',
                 ("UMETNOST", r"%umetnost%"))

    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE kategorija LIKE ? or kategorija like ?',
                 ("ZDRAV ZIVOT I ISHRANA", r"%zdrav%", r"%ishrana%"))
    
    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE (kategorija LIKE ? or kategorija like ?) and kategorija not like ?',
                 ("ZA DECU", r"%decu%", r"%uzrast%", r"%roman%"))
    
    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE kategorija LIKE ? and kategorija like ?',
                 ("ROMAN ZA DECU", r"%roman%", r"%decu%"))
    
    conn.execute('UPDATE Knjige \
                 SET kategorija = ? \
                 WHERE kategorija LIKE ?',
                 ("JEZICI", r"%jezi%"))

    conn.execute('update Knjige \
                set kategorija = "OSTALO" \
                where kategorija in \
                (select kategorija \
                from Knjige \
                group by kategorija \
                having count(*) < 30)')
    
    conn.execute('update Knjige \
                set autor = "Grupa autora" \
                where autor like "Grupa Autora"')
    
    conn.commit()

#a
def num_of_books_per_category(conn):
    cursor = conn.execute('select kategorija, count(*) from Knjige \
                           group by kategorija \
                           order by count(*) desc')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Kategorija', 'Broj knjiga'])
    return data_frame

#b
def num_of_books_per_publisher(conn):
    cursor = conn.execute('select izdavac, count(*) from Knjige \
                           group by izdavac \
                           order by count(*) desc')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Izdavac', 'Broj knjiga'])
    return data_frame

#c
def books_contain_ljubav(conn):
    cursor = conn.execute('select * from Knjige \
                           where opis like "%ljubav%"')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Naziv', 'Kategorija', 'Autor', 'Cena', 'Izdavac', 'Godina izdanja', 'Broj Strana', 'Tip poveza', 'Format', 'Opis'])
    return data_frame

#d
def num_of_books_per_year_last_7_years(conn):
    cursor = conn.execute('select godina_izdanja, count(*) from Knjige \
                           where godina_izdanja is not null and godina_izdanja > 2017 and godina_izdanja < 2025 \
                           group by godina_izdanja \
                           order by godina_izdanja desc')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Godina izdanja', 'Broj knjiga'])
    return data_frame

#e
def top_30_most_expensive(conn):
    cursor = conn.execute('select * from Knjige \
                           order by cena desc \
                           limit 30')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Naziv', 'Kategorija', 'Autor', 'Cena', 'Izdavac', 'Godina izdanja', 'Broj Strana', 'Tip poveza', 'Format', 'Opis'])
    return data_frame

#f
def get_new_books(conn):
    cursor = conn.execute('select * from Knjige \
                           where godina_izdanja==2023 or godina_izdanja==2024 \
                           order by cena')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Naziv', 'Kategorija', 'Autor', 'Cena', 'Izdavac', 'Godina izdanja', 'Broj Strana', 'Tip poveza', 'Format', 'Opis'])
    return data_frame

#g
def get_top30_most_pages(conn):
    cursor = conn.execute('select * from Knjige \
                           order by broj_strana desc \
                           limit 30')
    rows = cursor.fetchall()
    data_frame = pd.DataFrame(rows, columns=['Naziv', 'Kategorija', 'Autor', 'Cena', 'Izdavac', 'Godina izdanja', 'Broj Strana', 'Tip poveza', 'Format', 'Opis'])
    return data_frame


def get_top30_large_format(conn):
    cursor = conn.execute('select * from Knjige')
    rows = cursor.fetchall()
    sorted_rows = sorted(rows, key=lambda x: convert_to_float(x[8].split('x')[0]), reverse=True)#cmp_to_key(lambda x, y: is_bigger(x[8].lower(), y[8].lower())), reverse=True)
    data_frame = pd.DataFrame(sorted_rows[:30], columns=['Naziv', 'Kategorija', 'Autor', 'Cena', 'Izdavac', 'Godina izdanja', 'Broj Strana', 'Tip poveza', 'Format', 'Opis'])
    return data_frame


if __name__ == "__main__":
    db_file = "../db/books.db"
    db_cleaned_file = "../db/cleaned_books.db"
    excel_file = "results.xlsx"
    
    conn = sqlite3.connect(db_file)
    conn_cleaned_db = sqlite3.connect(db_cleaned_file)
    print(f"Creating new db {db_cleaned_file} to store clean data")
    conn_cleaned_db.execute("CREATE TABLE Knjige (naziv text, kategorija text, autor text, cena float, izdavac text, godina_izdanja int, broj_strana int, tip_poveza text, format text, opis text);")
    print("Cleaning dataset")
    clean_dataset(conn, conn_cleaned_db)
    clean_new_dataset(conn_cleaned_db)
    conn.close()

    print("Fetching data")
    b_per_cat = num_of_books_per_category(conn_cleaned_db)
    b_per_pub = num_of_books_per_publisher(conn_cleaned_db)
    b_ljubav = books_contain_ljubav(conn_cleaned_db)
    b_per_year_7 = num_of_books_per_year_last_7_years(conn_cleaned_db)
    top_30_price = top_30_most_expensive(conn_cleaned_db)
    new_books = get_new_books(conn_cleaned_db)
    top30_pages = get_top30_most_pages(conn_cleaned_db)
    top30_format = get_top30_large_format(conn_cleaned_db)
    print("Fetching done")

    print("Storing data in the Excel file {excel_file}")
    with pd.ExcelWriter(excel_file) as f:
        b_per_cat.to_excel(f, sheet_name=('a'))
        b_per_pub.to_excel(f, sheet_name=('b'))
        b_ljubav.to_excel(f, sheet_name=('c'))
        b_per_year_7.to_excel(f, sheet_name=('d'))
        top_30_price.to_excel(f, sheet_name=('e'))
        new_books.to_excel(f, sheet_name=('f'))
        top30_pages.to_excel(f, sheet_name=('g_1'))
        top_30_price.to_excel(f, sheet_name=('g_2'))
        top30_format.to_excel(f, sheet_name=('g_3'))

    conn_cleaned_db.close()

    print("Finished successfully!!!")
