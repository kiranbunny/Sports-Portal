import numpy as np
import pandas as pd
from sklearn.preprocessing import Normalizer
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

def train_linear_regression(dataset_file, target_column, test_size=0.3, random_state=42, new_data_point=None):
    # Read the dataset
    dataset = pd.read_csv("newinjury.csv")
    df = pd.DataFrame(dataset)

    # Convert DataFrame to numpy array
    dfarray = df.values

    # Normalize the data
    Scaler = Normalizer().fit(dfarray)
    normalizedX = Scaler.transform(dfarray)
    Norm_Data = pd.DataFrame(normalizedX)

    # Splitting features and target variable
    X = Norm_Data[[i for i in range(6)]]
    y = df[target_column]

    # Splitting the dataset into the Training set and Test set
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)

    # Training the Linear Regression model
    regr = LinearRegression()
    regr.fit(X_train, y_train)

    # Predicting for new data point
    if new_data_point:
        X2_array = np.array(new_data_point).reshape(1, -1)
        scaler1 = Normalizer().fit(X2_array)
        normalizedX1 = scaler1.transform(X2_array)
        X_Data = pd.DataFrame(normalizedX1)
        y2 = regr.predict(X_Data)
        return int(np.ceil(y2))

    # Display coefficients and bias
    print('Coefficients: \n', regr.coef_)
    print('Bias: \n', regr.intercept_)

    # Return relevant outputs
    return {
        "X_train": X_train,
        "X_test": X_test,
        "y_train": y_train,
        "y_test": y_test,
        "coefficients": regr.coef_,
        "bias": regr.intercept_
    }


