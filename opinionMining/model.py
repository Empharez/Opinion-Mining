import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB, BernoulliNB
import pickle
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix




data = pd.read_csv('opinion.csv')
df = pd.DataFrame(data)
headers = ['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
               'q10', 'opinion']
df.columns = headers
"""opinion_mapping = {'Satisfactory': 1, 'Not Satisfactory': 0}
df['opinion'] = df['opinion'].map(opinion_mapping)"""
X = df[['q1', 'q2', 'q3', 'q4', 'q5', 'q6', 'q7', 'q8', 'q9',
            'q10']]
y = df['opinion']
# Spilt the data set for training and testing
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.85, test_size=0.15, random_state=1)
nb = GaussianNB()
print(nb)
nb.fit(X_train, y_train)
print(nb.predict([[1,3,2,4,5,2,3,1,2,4]]))
with open('opinionMining.pkl', 'wb') as f:
    pickle.dump(nb, f)

prediction_nb = nb.predict(X_test)
#print(accuracy_score(y_true, y_pred))
print(accuracy_score(y_test, prediction_nb))
cm = confusion_matrix(y_test, prediction_nb)
print(cm)