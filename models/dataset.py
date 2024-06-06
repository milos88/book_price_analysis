import sqlite3
import numpy as np

class Dataset:
    def __init__(self, db_file = None):
        self.cat_map = self.map_data(db_file, "kategorija")
        self.autor_map = self.map_data(db_file, "autor")
        self.izdavac_map = self.map_data(db_file, "izdavac")
        self.povez_map = {"Broš": 0, "Tvrd": 1}
        # self.y_mean = None
        # self.y_std = None
        # self.x_mean = None
        # self.x_std = None
        if db_file:
            x, y = self.prepare_dataset(db_file)
        else:
            x = np.load("pretrained_data/x.npy")
            y = np.load("pretrained_data/y.npy")
        self.split_dataset(x,y)
    
    def map_data(self, db_file, name):
        conn = sqlite3.connect(db_file)
        rows = conn.execute(f'select {name}, avg(cena) as avg from Knjige group by {name} order by avg').fetchall()
        conn.close()
        
        mapping_data = {}
        br = 0
        for row in rows:
            if not row[0] in mapping_data.keys():
                mapping_data[row[0]] = br
                br += 1
        
        return mapping_data

    def split_dataset(self, x, y, test_size = 0.2):
        indices = np.arange(x.shape[0])
        np.random.shuffle(indices)
        
        x = x[indices]
        y = y[indices]

        split_idx = int(x.shape[0] * (1 - test_size))
        self.x, self.x_test = x[:split_idx], x[split_idx:]
        self.y, self.y_test = y[:split_idx], y[split_idx:]

    def get_data_from_db(self, db_file):
        conn = sqlite3.connect(db_file)
        rows = conn.execute('select * from Knjige order by cena').fetchall()
        conn.close()
        return rows

    def prepare_dataset(self, db_file):
        x = []
        y = []
        data = self.get_data_from_db(db_file)

        for d in data:
            arr = [1]
            # if not d[1] in self.cat_map.keys():
            #     self.cat_map[d[1]] = br[0]
            #     br[0] += 1
            arr.append(self.cat_map[d[1]])

            # if not d[2] in self.autor_map.keys():
            #     self.autor_map[d[2]] = br[1]
            #     br[1] += 1
            arr.append(self.autor_map[d[2]])

            # if not d[4] in self.izdavac_map.keys():
            #     self.izdavac_map[d[4]] = br[3]
            #     br[3] += 1
            arr.append(self.izdavac_map[d[4]])

            arr.append(d[5])
            arr.append(d[6])

            # if not d[7] in self.povez_map.keys():
            #     self.povez_map[d[7]] = br[3]
            #     br[3] += 1
            arr.append(self.povez_map[d[7]])
            arr.append(float(d[8].split('x')[0]))
            x.append(arr)
            y.append(d[3])

            # self.x_std = np.std(x, axis=0)
            # self.x_std[self.x_std == 0] = 1
            # self.x_mean = np.mean(x, axis=0)
            
            # self.y_mean = np.mean(y)
            # self.y_std = np.std(y)

        return np.array(x), np.array(y) #(x - self.x_mean) / self.x_std, (y - self.y_mean) / self.y_std