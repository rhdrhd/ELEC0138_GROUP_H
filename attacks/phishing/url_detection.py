from model.feature import FeatureExtraction
import numpy as np
import pandas as pd
import pickle
import warnings
warnings.filterwarnings('ignore')

url = input("Enter the URL: ")
obj = FeatureExtraction(url)

with open('model/mlp_model.pkl', 'rb') as file:
    mlp = pickle.load(file)

x = np.array(obj.getFeaturesList()).reshape(1,30) 
y_pred =mlp.predict(x)[0]
y_pro_phishing = mlp.predict_proba(x)[0,0]
y_pro_non_phishing = mlp.predict_proba(x)[0,1]
print("The probability of the URL being a phishing URL is: ", y_pro_phishing)
