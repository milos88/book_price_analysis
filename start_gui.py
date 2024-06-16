from tkinter import *
from tkinter import ttk
from models.dataset import Dataset
from models.linear_reg import LinearRegression
from models.log_reg import LogisticRegression, OneVsAll
from models.k_means import KMeans
from sklearn.linear_model import LogisticRegression as LogReg
import numpy as np
import matplotlib.pyplot as plt

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
    x = np.array([1,data.cat_map[category], data.autor_map[author], data.izdavac_map[publisher], year, num_pages, data.povez_map[povez], float(format.lower().split('x')[0]) * float(format.lower().split('x')[1])])
    x = model.transform(x)
    y = model.transform_back(model.predict(x))

    result_label.config(text=f"Predvidjena cena: {y}")

def train_log_reg(data: Dataset):
    log_reg_type = radio_var.get()
    if log_reg_type == "multi":
        model = LogisticRegression(num_classes=5)
        yc = Dataset.map_y_class(data.y)
        model.train(data.x, yc)
        sk_model = LogReg(multi_class="multinomial")
        sk_model.fit(data.x, yc)
        print(f"COEF {sk_model.coef_}")
        print(f"COEF MY: {model.w}")
        # model.w = sk_model.coef_

        yc_test = Dataset.map_y_class(data.y_test)
        mse = model.test(model.transform(data.x), yc_test)

        model.save_model("pretrained_data/log_regr_model.json")
        result_label.config(text=f"Error: {mse}")
    elif log_reg_type == "one_vs_all":
        model = OneVsAll(num_classes=5)
        yc = Dataset.map_y_class(data.y)
        model.train(data.x, yc)
        

        yc_test = Dataset.map_y_class(data.y_test)
        mse = model.test(model.transform(data.x_test), yc_test)

        model.save_model("pretrained_data/log_regr_model_one_vs_all.json")
        result_label.config(text=f"Error: {mse}")
    else:
        result_label.config(text=f"Izaberite tip logisticke regresije")

def predict_log_reg(data: Dataset):

    category = cat_var.get()
    author = aut_var.get()
    publisher = pub_var.get()
    year = int(year_entry.get())
    num_pages = int(page_entry.get())
    povez = povez_menu.get()
    format = format_entry.get()
    x = np.array([1,data.cat_map[category], data.izdavac_map[publisher], year, num_pages, data.povez_map[povez], float(format.lower().split('x')[0]) * float(format.lower().split('x')[1])])
    

    log_reg_type = radio_var.get()
    if log_reg_type == "multi":
        model = LogisticRegression(num_classes=5)
        model.load_model("pretrained_data/log_regr_model.json")
        
        x = model.transform(x)
        y = model.predict(x)

        result_label.config(text=f"Predvidjena cena: {np.argmax(y)}")
    elif log_reg_type == "one_vs_all":
        model = OneVsAll(num_classes=5)
        model.load_model("pretrained_data/log_regr_model_one_vs_all.json")

        x = model.transform(x)
        y = model.predict(x)

        result_label.config(text=f"Predvidjena cena: {np.argmax(y)}")
        
    else:
        result_label.config(text=f"Izaberite tip logisticke regresije")
    
def kmeans(data):
    err = []
    test_k = range(1,9)
    
    for k in test_k:
        model = KMeans(k)
        x = model.normalize_data(data.x[:, [1, 2, 6]])
        model.train(x)
        err.append(model.error_)
    # k = 2
    # for i, e in enumerate(err):
    #     if e < 1:
    #         k = i
    #         break

    model = KMeans(6)
    x = model.normalize_data(data.x[:, [1, 2, 6]])
    model.train(x)

    plt.figure(figsize=(10, 8))
    plt.plot(test_k, err, 'bo-')
    plt.grid(True)
    plt.show()

    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    sc = ax.scatter(x[:, 0], x[:, 1], x[:, 2], c=model.clusters ,cmap='viridis', marker='o')

    ax.set_title('3D K-means Clustering on Book Data')
    ax.set_xlabel('Kategorija')
    ax.set_ylabel('Godina izdanja')
    ax.set_zlabel('broj strana')
    plt.colorbar(sc)
    plt.show()

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
    ttk.Button(frm, text="Quit", command=root.destroy).grid(column=1, row=12)
    ttk.Button(frm, text="Treniraj Log Reg", command=lambda: train_log_reg(data)).grid(column=0, row=9)
    ttk.Button(frm, text="Predvidi Cenu", command=lambda: predict_log_reg(data)).grid(column=1, row=9)
    ttk.Button(frm, text="k Means", command=lambda: kmeans(data)).grid(column=0, row=10)

    # checkbox_var = BooleanVar()
    # checkbox = Checkbutton(root, text="Modify Result", variable=checkbox_var)
    # checkbox.grid(row=9, column=3, columnspan=2, padx=10, pady=10)

    radio_var = StringVar(value="multi")
    multi_radio_button = Radiobutton(root, text="Multinomijalna logisticka regresija", variable=radio_var, value="multi")
    vs_radio_button = Radiobutton(root, text="Jedan nasuprot svima", variable=radio_var, value="one_vs_all")
    multi_radio_button.grid(row=10, column=1, columnspan=2, padx=10, pady=10)
    vs_radio_button.grid(row=11, column=1, columnspan=2, padx=10, pady=10)

    result_label = ttk.Label(frm, text="")
    result_label.grid(column=0, row=8)
    root.mainloop()