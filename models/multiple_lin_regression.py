# autor, kategorija, izdavac, godina_izdanja, broj_strana, tip_poveza, format
# not     not         not        number        number        not       number
import numpy as np
import sqlite3
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

Y_MAX = 22000
cat_map = {}
autor_map = {}
izdavac_map = {}
povez_map = {"Broš": 1, "Tvrd": 2}
y_mean = None
y_std = None

def predict(w, x):
    # np.mean(y) / np.std(y)
    # return np.sum(w * x) * Y_MAX
    print(y_mean)
    return np.sum(w * x) * y_mean + y_std # np.std(y) + np.mean(y)

def calculate_parameters(w, x, y, lr):
    # w = mean((sum_row(w*x)-y)*x, axis=1)
    # return w - lr * np.mean((np.sum(w * x, axis=1) - y) * np.transpose(x), axis=1)
    m = len(y)
    for i in range(m):
        w = w - lr / m * (np.sum(w * x[i]) - y[i]) * x[i]
    return w

def mse(w, x, y):
    # print(x)
    # print("============y=========")
    # print(y)
    # print(np.sum(w * x, axis=1))
    # print("==========diff============")
    # print(np.sum(w * x, axis=1) - y)
    return np.mean((np.sum(w * x, axis=1) - y)**2) / 2

def prepare_dataset(data):
    clean_data = []
    y = []
    br = [1, 1, 1, 1]
    
    for d in data:
        arr = [1]
        if not d[1] in cat_map.keys():
            cat_map[d[1]] = br[0]
            br[0] += 1
        arr.append(cat_map[d[1]])

        if not d[2] in autor_map.keys():
            autor_map[d[2]] = br[1]
            br[1] += 1
        arr.append(autor_map[d[2]])

        if not d[4] in izdavac_map.keys():
            izdavac_map[d[4]] = br[3]
            br[3] += 1
        arr.append(izdavac_map[d[4]])

        arr.append(d[5])
        arr.append(d[6])

        if not d[7] in povez_map.keys():
            povez_map[d[7]] = br[3]
            br[3] += 1
        arr.append(povez_map[d[7]])
        arr.append(float(d[8].split('x')[0]))
        clean_data.append(arr)
        x = np.array(clean_data)
        # np.insert(arr, 0, 1, axis=1)
        # x_max = x.max(axis=0)
        # x_min = x.min(axis=0)
        # x_max[x_max == 0] = 1
        std_x = np.std(x, axis=0)
        std_x[std_x == 0] = 1
        y.append(d[3])
        global y_mean
        global y_std 
        y_mean = np.mean(y)
        y_std = np.std(y)
        # y_max = max(y)
    return (x - np.mean(x, axis=0)) / std_x, (y - y_mean) / y_std
    # return (x - x_min + 1) / (x_max - x_min + 1), np.array(y) / Y_MAX

def plot_data(x,y):
    
    with PdfPages('plot_data.pdf') as pdf:
        plt.figure()
        plt.plot(x[:, 1], y, 'o')
        plt.xlabel('Kategorija')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos kategorije i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        #plt.show()

        plt.figure()
        plt.plot(x[:, 2], y, 'o')
        plt.xlabel('Autor')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos autor i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

        plt.figure()
        plt.plot(x[:, 3], y, 'o')
        plt.xlabel('Izdavac')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos izdavac-cena')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

        plt.figure()
        plt.plot(x[:, 4], y, 'o')
        plt.xlabel('Godina izdanja')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos godine izdanja i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

        plt.figure()
        plt.plot(x[:, 5], y, 'o')
        plt.xlabel('Broj strana')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos broj strana i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

        plt.figure()
        plt.plot(x[:, 6], y, 'o')
        plt.xlabel('Tip poveza')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos tip poveza i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

        plt.figure()
        plt.plot(x[:, 7], y, 'o')
        plt.xlabel('format')  # Add your x-axis label here
        plt.ylabel('Cena')  # Add your y-axis label here
        plt.title('Odnos formata i cene')     # Optional: Add a title to your plot
        pdf.savefig()
        # plt.show()

if __name__=="__main__":
    db_file = "../db/cleaned_books.db"
    conn = sqlite3.connect(db_file)
    rows = conn.execute('select * from Knjige order by cena').fetchall()
    conn.close()

    lr = 0.1
    epsilon=1e-8
    x, y = prepare_dataset(rows)
    np.save("x_all.npy", x)
    np.save("y_all.npy", y)
    # x = np.load("x_all.npy")
    # y = np.load("y_all.npy")
    plot_data(x, y)
    w = np.zeros(np.shape(x[0]))
    i = 0
    prev_mse = 0
    new_mse = 100
    while True: #abs(prev_mse - new_mse) > epsilon:
        print(f"Iteration: {i}")
        i += 1
        print("======================================================")
        prev_mse = new_mse # mse(w,x,y)
        w = calculate_parameters(w, x, y, lr)
        new_mse = mse(w,x,y)
        print(f"Coef: {w}")
        print(f"MSE: {new_mse}")
        print("======================================================")
        
        if i == 500:
            break
    
    print("DONE")

    regressor = LinearRegression()
    regressor.fit(x, y)
    print("REGRESSOR")
    print(f"REGRESSOR COEF: {regressor.coef_}")
    print(f"REGRESSOR MSE: {mse(regressor.coef_, x, y)}")
    print("======================================================\n\n")

    price = predict(w, np.ones(np.shape(x[0])))
    print(f"Predicted price: {price}")
    price = predict(regressor.coef_, np.ones(np.shape(x[0])))
    print(f"Predicted price: {price}")