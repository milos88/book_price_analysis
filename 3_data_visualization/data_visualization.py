from matplotlib import pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import sqlite3
import numpy as np


def save_image(filename): 
    
    p = PdfPages(filename)
    fig_nums = plt.get_fignums()
    figs = [plt.figure(n) for n in fig_nums]
    for fig in figs:
        fig.savefig(p, format='pdf')
    p.close()

def create_plt_figure(name, data, title):
    """From here: https://www.geeksforgeeks.org/bar-plot-in-matplotlib/"""
    # Figure Size
    fig, ax = plt.subplots(figsize =(16, 9))
    
    # Horizontal Bar Plot
    ax.barh(name, data)
    
    # Remove axes splines
    for s in ['top', 'bottom', 'left', 'right']:
        ax.spines[s].set_visible(False)
    
    # Remove x, y Ticks
    ax.xaxis.set_ticks_position('none')
    ax.yaxis.set_ticks_position('none')
    
    # Add padding between axes and labels
    ax.xaxis.set_tick_params(pad = 5)
    ax.yaxis.set_tick_params(pad = 10)
    
    # Add x, y gridlines
    ax.grid(visible = True, color ='grey', linestyle ='-.', linewidth = 0.5, alpha = 0.2)
    
    # Show top values 
    ax.invert_yaxis()
    
    # Add annotation to bars
    for i in ax.patches:
        plt.text(i.get_width()+0.2, i.get_y()+0.5, 
                str(round((i.get_width()), 2)),
                fontsize = 10, fontweight ='bold',
                color ='grey')
    
    # Add Plot Title
    ax.set_title(title, loc ='center', )


def filter_books(rows, index):
    data = {}
    for row in rows:
        if row[index] in data.keys():
            data[row[index]] += 1
        else:
            data[row[index]] = 1
    data_list = sorted(data.items(), key=lambda x:x[1], reverse=True)
    return data_list

def absolute_value(val, data):
    a  = np.round(val/100.*data.sum(), 0)
    return a

def top_10_publishers(rows):
    data_list = filter_books(rows, 4)[:10]

    create_plt_figure([d[0] for d in data_list], [d[1] for d in data_list], '10 najzastupljenijih izdavača koji imaju najveći broj knjiga u ponudi')


def books_per_category(rows):
    data_list = filter_books(rows, 1)[:30]

    create_plt_figure([d[0] for d in data_list], [d[1] for d in data_list], 'Broj knjiga po kategorijama (žanrovima)')


def books_per_decades(rows):
    data_list = filter_books(rows, 5)
    start_year = 1961
    new_data_list = []
    for i in range(7):
        year = start_year + 10 * i
        new_data_list.append((f'{year}-{year + 9 if i < 6 else "danas"}', sum([d[1] for d in data_list if int(d[0]) >= year and int(d[0]) <= year + 9])))

    create_plt_figure([d[0] for d in new_data_list], [d[1] for d in new_data_list], 'Broj izdatih knjiga po dekadama')

def top_5_publishers(rows):
    total_books = len(rows)
    data_list = filter_books(rows, 4)[:5]
    top5_total = sum([d[1] for d in data_list])
    data_percent = []
    for d in data_list:
        data_percent.append((d[0], round(d[1] * 100 / top5_total, 2)))

    create_plt_figure([d[0] for d in data_list], [d[1] for d in data_list], 'Broj knjiga koje se prodaju, za prvih 5 izdavačkih kuća sa najvećimbrojem knjiga')
    #create_plt_figure([d[0] for d in data_percent], [d[1] for d in data_percent], 'Procentualni odnos knjiga koje se prodaju, za prvih 5 izdavačkih kuća sa najvećimbrojem knjiga')
    _, ax = plt.subplots(figsize =(16, 9))
    plt.pie([d[1] for d in data_percent], labels=[d[0] for d in data_percent], autopct='%.2f')
    ax.set_title('Procentualni odnos knjiga koje se prodaju, za prvih 5 izdavačkih kuća sa najvećimbrojem knjiga', loc ='center', )
    plt.legend()

def books_per_prices(rows):
    data_list = filter_books(rows, 3)
    new_data_list = [
        (f'Manje od 500', sum([d[1] for d in data_list if int(d[0]) <= 500])),
        (f'501-1500', sum([d[1] for d in data_list if int(d[0]) >= 501 and int(d[0]) <= 1500])),
        (f'1501-3000', sum([d[1] for d in data_list if int(d[0]) >= 1501 and int(d[0]) <= 3000])),
        (f'3001-5000', sum([d[1] for d in data_list if int(d[0]) >= 3001 and int(d[0]) <= 5000])),
        (f'5001-10000', sum([d[1] for d in data_list if int(d[0]) >= 5001 and int(d[0]) <= 10000])),
        (f'10001-15000', sum([d[1] for d in data_list if int(d[0]) >= 10001 and int(d[0]) <= 15000])),
        (f'Vise od 15001', sum([d[1] for d in data_list if int(d[0]) >= 15001]))
    ]

    total_num = sum([d[1] for d in new_data_list])
    data_percent = []
    for d in new_data_list:
        data_percent.append((d[0], round(d[1] * 100 / total_num, 2)))

    create_plt_figure([d[0] for d in new_data_list], [d[1] for d in new_data_list], 'Broj svih knjiga za prodajupo opsezima:')
    #create_plt_figure([d[0] for d in data_percent], [d[1] for d in data_percent], 'Procentualni odnos svih knjiga za prodajupo opsezima:')
    _, ax = plt.subplots(figsize =(16, 9))
    plt.pie([d[1] for d in data_percent], labels=[d[0] for d in data_percent], autopct='%.2f')
    ax.set_title('Procentualni odnos svih knjiga za prodaju po opsezima', loc ='center', )
    plt.legend()

def books_hardcover(rows):
    data_list = filter_books(rows, 7)

    total_num = sum([d[1] for d in data_list])
    data_percent = []
    for d in data_list:
        data_percent.append((d[0], round(d[1] * 100 / total_num, 2)))

    create_plt_figure([d[0] for d in data_list], [d[1] for d in data_list], 'Broj knjiga po Tipu poveza')
    # create_plt_figure([d[0] for d in data_percent], [d[1] for d in data_percent], 'Procentualni odnos knjiga prema tipu poveza')
    _, ax = plt.subplots(figsize =(16, 9))
    plt.pie([d[1] for d in data_percent], labels=[d[0] for d in data_percent], autopct='%.2f')
    ax.set_title('Procentualni odnos knjiga prema tipu poveza', loc ='center', )
    plt.legend()

if __name__=="__main__":
    db_file = "../db/cleaned_books.db"
    conn = sqlite3.connect(db_file)
    rows = conn.execute('select * from Knjige').fetchall()
    # rows = cursor.fetchall()
    conn.close()

    top_10_publishers(rows)
    books_per_category(rows)
    books_per_decades(rows)
    top_5_publishers(rows)
    books_per_prices(rows)
    books_hardcover(rows)
    
    save_image('results.pdf')

    print('Finished')
