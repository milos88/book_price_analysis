from tkinter import *
from tkinter import ttk
from models.dataset import Dataset
from models.linear_reg import LinearRegression

def submit():
    pass
    # name = name_entry.get()

    # result_label.config(text=f"Result: {name}")

def train_model():
    db_file = "../db/cleaned_books.db"
    data = Dataset(db_file)
    model = LinearRegression()

    model.train(data.x, data.y)
    #result_label.config(text=f"Result: {model.w}")

if __name__=="__main__":
    train_model()
# if __name__=="__main__":
#     root = Tk()
#     frm = ttk.Frame(root, padding=10)
#     frm.grid()

#     ttk.Label(frm, text="Broj strana").grid(column=0, row=0)
#     name_entry = ttk.Entry(frm, font=('calibre',10,'normal'))
#     name_entry.grid(column=1, row=0)

#     ttk.Button(frm, text="Predvidi cenu", command=submit).grid(column=0, row=1)
#     ttk.Button(frm, text="Treniraj", command=train_model).grid(column=0, row=1)
#     ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=1)
#     result_label = ttk.Label(frm, text="")
#     result_label.grid(column=0, row=2)
#     root.mainloop()