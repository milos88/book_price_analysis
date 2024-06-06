from tkinter import *
from tkinter import ttk
from models.dataset import Dataset
from models.linear_reg import LinearRegression
import numpy as np

def submit():
    pass
    # name = name_entry.get()

    # result_label.config(text=f"Result: {name}")

def train_model(data):
    # db_file = "db/cleaned_books.db"
    # data = Dataset(db_file)
    model = LinearRegression()

    model.train(data.x, data.y)
    x_test, y_test = model.transform_full(data.x_test, data.y_test)
    mse = model.test(x_test, y_test)

    model.save_model("pretrained_data/lin_regr_model.json")
    result_label.config(text=f"MSE: {mse}")

def predict(data: Dataset):
    model = LinearRegression()
    model.load_model("pretrained_data/lin_regr_model.json")
    
    category = cat_var.get()
    author = aut_var.get()
    publisher = pub_var.get()
    year = int(year_entry.get())
    num_pages = int(page_entry.get())
    povez = povez_menu.get()
    format = format_entry.get()
    x = np.array([1,data.cat_map[category], data.autor_map[author], data.izdavac_map[publisher], year, num_pages, data.povez_map[povez], float(format.lower().split('x')[0])])
    x = model.transform(x)
    y = model.transform_back(model.predict(x))

    result_label.config(text=f"Predvidjena cena: {y}")


if __name__=="__main__":
    db_file = "db/cleaned_books.db"
    data = Dataset(db_file)
    root = Tk()
    frm = ttk.Frame(root, padding=10)
    frm.grid()
    
    ttk.Label(frm, text="Zanr (Kategorija)").grid(column=0, row=0)
    cat_var = StringVar(value="")
    cat_menu = ttk.Combobox(frm, textvariable=cat_var, values=list(data.cat_map.keys()))
    cat_menu.grid(row=0, column=1, columnspan=4, padx=10, pady=10)


    ttk.Label(frm, text="Autor").grid(column=0, row=1)
    aut_var = StringVar(value="")
    aut_menu = ttk.Combobox(frm, textvariable=aut_var, values=sorted(list(data.autor_map.keys())))
    aut_menu.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

    ttk.Label(frm, text="Izdavac").grid(column=0, row=2)
    pub_var = StringVar(value="")
    pub_menu = ttk.Combobox(frm, textvariable=pub_var, values=sorted(list(data.izdavac_map.keys())))
    pub_menu.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

    ttk.Label(frm, text="Godina izdanja").grid(column=0, row=3)
    year_entry = ttk.Entry(frm, font=('calibre',10,'normal'))
    year_entry.grid(column=1, row=3, padx=10, pady=10)

    ttk.Label(frm, text="Broj strana").grid(column=0, row=4)
    page_entry = ttk.Entry(frm, font=('calibre',10,'normal'))
    page_entry.grid(column=1, row=4, padx=10, pady=10)

    ttk.Label(frm, text="Tip poveza").grid(column=0, row=5)
    povez_var = StringVar(value="")
    povez_menu = ttk.Combobox(frm, textvariable=povez_var, values=list(data.povez_map.keys()))
    povez_menu.grid(row=5, column=1, columnspan=2, padx=10, pady=10)

    ttk.Label(frm, text="Format (brXbr)").grid(column=0, row=6)
    format_entry = ttk.Entry(frm, font=('calibre',10,'normal'))
    format_entry.grid(column=1, row=6)

    ttk.Button(frm, text="Predvidi cenu", command=lambda: predict(data)).grid(column=1, row=7)
    ttk.Button(frm, text="Treniraj", command=lambda: train_model(data)).grid(column=0, row=7)
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=9)
    result_label = ttk.Label(frm, text="")
    result_label.grid(column=0, row=8)
    root.mainloop()