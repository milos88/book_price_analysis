import numpy as np
import json

class LogisticRegression:
    def __init__(self, num_classes = 2, w = None):
        self.w = w
        self._num_classes = num_classes
    
    def to_json(self):
        model = {}
        model["coef"] = self.w.tolist()
        model["x_mean"] = self.x_mean.tolist()
        model["x_std"] = self.x_std.tolist()
        model["y_mean"] = self.y_mean 
        model["y_std"] = self.y_std
        return model
    
    def from_json(self, model):
        self.w = np.array(model["coef"])
        self.x_mean = np.array(model["x_mean"])
        self.x_std = np.array(model["x_std"])
        self.y_mean = model["y_mean"]
        self.y_std = model["y_std"]

    def load_model(self, model_path):
        with open(model_path, "r") as outfile: 
            model = json.load(outfile)
        if model:
            self.from_json(model)

    def save_model(self, model_path):
        
        with open(model_path, "w") as outfile: 
            json.dump(self.to_json(), outfile)

    def transform_full(self, x, y):
        return (x - self.x_mean) / self.x_std, (y - self.y_mean) / self.y_std

    def transform(self, x):
        return (x - self.x_mean) / self.x_std

    def transform_back(self, y):
        return y * self.y_std + self.y_mean1

    def normalize_data(self, x, y):
        self.x_std = np.std(x, axis=0)
        self.x_std[self.x_std == 0] = 1
        self.x_mean = np.mean(x, axis=0)
        
        self.y_mean = np.mean(y)
        self.y_std = np.std(y)
        return self.transform(x)

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
                arr_y[int(y[i])] = 1
                # print(f"DATA: {self.predict(x[i])}")
                self.w = self.w + lr / m * (arr_y - self.predict(x[i])).reshape([-1, 1]) * x[i]


    def error(self, x, y):
        pred = np.array([self.predict(d) for d in x])
        if self._num_classes == 2:
            return -np.mean(y * np.log(pred) + (1 - y) * np.log(1 - pred))
        else:
            pred = [pred[int(d)] for d in y]
            
            return -np.mean(np.log(pred))

    def train(self, x, y, lr = 0.1, epochs = 500):
        # x = self.transform(x)
        x = self.normalize_data(x,y)
        if self.w is None:
            if self._num_classes > 2:
                self.w = np.zeros((self._num_classes,) + np.shape(x[0]))
            else:
                self.w = np.zeros(np.shape(x[0]))

        for i in range(epochs):
            # print(f"Iteration: {i + 1}")
            # print("======================================================")
            self.update_params(x, y, lr)
            # self._error = self.error(x,y)
            # print(f"Error: {self._error}")
            # print("======================================================")
        
        #self.save_model("pretrained_data/lin_regr_model.json")
        
    
    def test(self, x, y):
        return self.error(x, y)


class OneVsAll:
    def __init__(self, num_classes) -> None:
        self.models = []
        for _ in range(num_classes):
            self.models.append(LogisticRegression())

    def save_model(self, model_path):
        json_data = []
        for model in self.models:
            json_data.append(model.to_json())

        with open(model_path, "w") as outfile: 
            json.dump(json_data, outfile)

    def load_model(self, model_path):
        with open(model_path, "r") as outfile: 
            saved_models = json.load(outfile)
        
        if saved_models:
            for i, model in enumerate(saved_models):
                self.models[i].from_json(model)

    def train(self, x, y):

        for i, model in enumerate(self.models):
            y_new = np.where(y == i, 1, 0)
            model.train(x, y_new)
    
    def predict(self, x):
        predictions = []
        for model in self.models:
            predictions.append(model.predict(x))
        return predictions
    
    def error(self, x, y):
        return np.mean([model.error(x, y) for model in self.models])
    
    def test(self, x, y):
        return self.error(x, y)
    
    def transform(self, x):
        return (x - self.models[0].x_mean) / self.models[0].x_std
