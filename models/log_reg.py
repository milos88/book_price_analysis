import numpy as np
import json

class LogisticRegression:
    def __init__(self, num_classes = 2, w = None):
        self.w = w
        self._num_classes = num_classes

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
        if self._num_classes == 2:
            exp = np.exp(np.sum(self.w * x))
            return exp / (exp + 1)
        else:
            exp = np.exp(np.sum(self.w * x, axis=1))
            return 1 / np.sum(exp) * exp

    def update_params(self, x, y, lr):
        m = len(y)
        if self._num_classes == 2:
            for i in range(m):
                self.w = self.w - lr / m * (self.predict(x[i]) - y[i]) * x[i]
        else:
            for i in range(m):
                arr_y = np.zeros(self._num_classes)
                arr_y[y[i]] = 1
                self.w = self.w + lr / m * (arr_y - self.predict(x[i])).reshape([-1, 1]) * x[i]


    def error(self, x, y):
        pred = np.array([self.predict(d) for d in x])
        if self._num_classes == 2:
            return -np.mean(y * np.log(pred) + (1 - y) * np.log(1 - pred))
        else:
            pred = [pred[d] for d in y]
            return -np.mean(np.log(pred))

    def train(self, x, y, lr = 0.01, epochs = 500):
        x, y = self.normalize_data(x,y)
        if self.w is None:
            if self._num_classes > 2:
                self.w = np.zeros([np.shape(x[0]), self._num_classes])
            else:
                self.w = np.zeros(np.shape(x[0]))

        for i in range(epochs):
            print(f"Iteration: {i + 1}")
            # print("======================================================")
            self.update_params(x, y, lr)
            self._error = self.error(x,y)
            print(f"Error: {self._error}")
            print("======================================================")
        
        #self.save_model("pretrained_data/lin_regr_model.json")
        
    
    def test(self, x, y):
        return self.error(x, y)
