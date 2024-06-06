import numpy as np
import json

class LinearRegression:
    def __init__(self, w = None):
        self.w = w

    def load_model(self, model_path):
        with open(model_path, "r") as outfile: 
            model = json.load(outfile)
        if model:
            self.w = np.array(model["coef"])
            self.x_mean = np.array(model["x_mean"])
            self.x_std = np.array(model["x_std"])
            self.y_mean = model["y_mean"]
            self.y_std = model["y_std"]

    def save_model(self, model_path):
        model = {}
        model["coef"] = self.w.tolist()
        model["x_mean"] = self.x_mean.tolist()
        model["x_std"] = self.x_std.tolist()
        model["y_mean"] = self.y_mean 
        model["y_std"] = self.y_std

        with open(model_path, "w") as outfile: 
            json.dump(model, outfile)

    def transform_full(self, x, y):
        return (x - self.x_mean) / self.x_std, (y - self.y_mean) / self.y_std

    def transform(self, x):
        return (x - self.x_mean) / self.x_std

    def transform_back(self, y):
        return y * self.y_std + self.y_mean

    def normalize_data(self, x, y):
        self.x_std = np.std(x, axis=0)
        self.x_std[self.x_std == 0] = 1
        self.x_mean = np.mean(x, axis=0)
        
        self.y_mean = np.mean(y)
        self.y_std = np.std(y)
        return self.transform_full(x, y)

    def predict(self, x):
        return np.sum(self.w * x) # * self.data.y_mean + self.data.y_std # np.std(y) + np.mean(y)

    def update_params(self, x, y, lr):
        m = len(y)
        for i in range(m):
            self.w = self.w - lr / m * (np.sum(self.w * x[i]) - y[i]) * x[i]

    def mse(self, x, y):
        return np.mean((np.sum(self.w * x, axis=1) - y)**2) / 2

    def train(self, x, y, lr = 0.01, epochs = 500):
        x, y = self.normalize_data(x,y)
        if self.w is None:
            self.w = np.zeros(np.shape(x[0]))

        for i in range(epochs):
            print(f"Iteration: {i + 1}")
            # print("======================================================")
            self.update_params(x, y, lr)
            self._mse = self.mse(x,y)
            print(f"MSE: {self._mse}")
            print("======================================================")
        
        #self.save_model("pretrained_data/lin_regr_model.json")
        
    
    def test(self, x, y):
        return self.mse(x, y)
