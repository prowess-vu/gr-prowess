import sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
from csv import DictReader
from sklearn.linear_model import LinearRegression

def main():
    for file in sys.argv[1:]:
        with open(file, 'r') as f:
            d = DictReader(f)
            cols = d.fieldnames

            data = {key: [] for key in cols}
            for row in d:
                for key, value in row.items():
                    #if key == "Samples Consumed":
                        #data[key].append(8*float(value))
                    #else:
                    data[key].append(float(value))

        plt.figure(figsize=(8, 4))
        plt.plot(data["Samples Consumed"], data["Work Time"], 'b--o', linewidth=1.0)
        #plt.plot(data["Samples Consumed"], data["Work Time Total"], 'r--o', linewidth=1.0, label = "Work Time Total")

        # Calculate and plot linear regression line
        X = np.array(data["Samples Consumed"]).reshape(-1, 1)
        y = np.array(data["Work Time"])
        model = LinearRegression()
        model.fit(X, y)
        slope = model.coef_[0]
        intercept = model.intercept_
        plt.plot(X, model.predict(X), 'r-', label=f'Linear Regression (Slope: {slope:.2f}, Intercept: {intercept:.2f})')

        #plt.yticks(np.arange(0, max(data["Clock Cycles"]), step=max(data["Clock Cycles"]) / 10))
        plt.xlabel("Number of Samples Consumed")
        plt.ylabel("Clock Cycles")
        plt.legend()

        plt.savefig(file[:-4] + '_exec.png')

if __name__ == '__main__':
    main()
