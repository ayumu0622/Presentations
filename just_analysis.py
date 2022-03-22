# -*- coding: utf-8 -*-
"""Just analysis.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1xXCbQwBkZkAmKhM2xz8uGmueSzni_BAB

#Presentation 
###by Ayumu Ueda
###In this presentaion, I give you my analysis for the 2020 Congressional Race between Anna Eshoo and Rishi Kumar in Mountain View which belong to 18th Congressional Precinct. 
###First of all, I show the relationship between racial makeup and the percentage of the votes obtained by Anna, and then I make prediction model that can predict how much votes she can get in each precinct from the racial makeup.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
pd.set_option('display.max_columns', None)
df = pd.read_csv("/content/drive/MyDrive/Volunteering/final.csv")
df_1 = df.copy()
df_4 = df.copy()

df_1["Total Population"]  -= df_1["White"]
df_1["Total Population"]  -= df_1["Other"]
df_1 = df_1.drop(["White","Other"], axis=1)

def funcA(x):
  x["Black_ratio"] = x["Black"] / x["Total Population"]
  x["Indian_ratio"] = x["Indian"] / x["Total Population"]
  x["Asian_ratio"] = x["Asian"] / x["Total Population"]
  x["Islander_ratio"] = x["Islander"] / x["Total Population"]
  x["Vacant_ratio"] = x["Vacant"] / x["Total house"]
  x["Vote_By_Mail_ratio_a"] = x["Vote By Mail_a"] / x["Total Votes_a"]
  x["Vote_By_Mail_ratio_r"] = x["Vote By Mail_r"] / x["Total Votes_r"]
  x["Vote for a rate"] = x["Total Votes_a"] / x["Total"]
  return x

def funcB(x):
  x["White_ratio"] = x["White"] / x["Total Population"]
  x["Black_ratio"] = x["Black"] / x["Total Population"]
  x["Indian_ratio"] = x["Indian"] / x["Total Population"]
  x["Asian_ratio"] = x["Asian"] / x["Total Population"]
  x["Islander_ratio"] = x["Islander"] / x["Total Population"]
  x["Other_ratio"] = x["Other"] / x["Total Population"]
  x["Vote for a rate"] = x["Total Votes_a"] / x["Total"]
funcA(df_1)
funcB(df_4)
df_1 = df_1.set_index("precinct")
df_4 = df_4.set_index("precinct")
df_1 = df_1.loc[:,"Black_ratio":]
df_4 = df_4.loc[:,"White_ratio":]

"""##Here is the explanation of each column
####Index = Precinct in 18th congressional district in Moutain View
####Black_ratio = the proportion of Black or African American alone in a precinct
####Indian_ratio = the proportion of American Indian and Alaska Native alone in a precinct 
####Asian_ratio = the proportion of Asian alone in a precinct
####Islander_ratio = the proportion of Native Hawaiian and Other Pacific Islander alone in a precinct
####Vote for a rate = the percentage of the votes obtained by Anna in a precinct.

##In this presentation, I consider only 4 alone above races(Black,Indian,Asian,Islander)
"""

df_1

"""##1.There is a correlation between Asian_ratio and Vote for a rate, it means that Asian people tend to support her.







"""

corr = df_1[["Asian_ratio","Vote for a rate"]].corr()
print(corr)
sns.heatmap(corr)
plt.show()

"""##2.Indian_ratio have a negative correlation with Vote for a rate, therefore Anna tend not to be supported in the area where more American Indian people live.

"""

corr = df_1[["Indian_ratio","Vote for a rate"]].corr()
print(corr)
sns.heatmap(corr)
plt.show()

"""
##3.There is strong negative correlation between Black_ratio and Vote for a rate, it explain that Anna is struggle with collecting votes in precinct where  more Black or African American alone people live.
"""

corr = df_1[["Black_ratio","Vote for a rate"]].corr()
print(corr)
sns.heatmap(corr)
plt.show()

"""##4.There is a negative correlation between Islander_ratio and Vote for a rate, which shows that Anna tend to gather less votes in a precinct where more Native Hawaiian and Other Pacific Islander alone people live.


"""

corr = df_1[["Islander_ratio","Vote for a rate"]].corr()
print(corr)
sns.heatmap(corr)
plt.show()

"""##From 1,2,3,4, I can say that Anna have tendency to get less votes where less Asian alone live and more other races alone live.

##Let's take a look at precinct 2951 and 3409 as a good example shows that tendency

###below pictures shows that more Asian people live in 3409 precinct than 2951 precinct
"""

df_2 = df_1.iloc[:,:4].T 
df_2 = df_2[[3409, 2951]]
df_2 = df_2.T
label = list(df_2.columns)

x = df_2.T[2951].to_numpy()
plt.pie(x, labels=label, counterclock=False, startangle=90, autopct="%1.1f%%")
plt.title("2951 Precinct")
plt.show()

x = df_2.T[3409].to_numpy()
plt.pie(x, labels=label, counterclock=False, startangle=90, autopct="%1.1f%%")
plt.title("3409 Precinct")
plt.show()

"""##below picture shows that Anna gather more votes in precinct 3409 than 2951"""

df_3 = df_1.loc[[2951, 3409],["Vote for a rate"]]
df_3.plot.bar()

"""##From the above reason, I think there is some relationship between racial makeup and how much votes she can get.

##Prediction model by ElasticnetCV
##I use ElasticNetCV for model. I split 15 datasets into 12 train data and 3 test data.
"""

df_4

from sklearn.model_selection import train_test_split
from sklearn.linear_model import ElasticNetCV
from sklearn.preprocessing import StandardScaler
df_4 = df_4.drop(3402) #same census tract with 2018
X = df_4.iloc[:, :-1]
Y = df_4.iloc[:, -1:]
train_x, test_x, train_y, test_y = train_test_split(X, Y, test_size = 0.2, shuffle=True, random_state=67)

clf = ElasticNetCV()
clf = clf.fit(train_x,train_y)
preds = clf.predict(test_x)
#rmse 0.074
#R2 0.06
#mae 0.057

"""##Loss is 0.04 in mae"""

from sklearn.metrics import mean_absolute_error as MAE
mae = MAE(test_y, preds)
mae

"""##Here is Prediction and actual Score(Vote for a rate)

---


"""

test_y["Prediction"]  = preds
test_y

"""# **Thank you for checking my presentation. I couldn't spend much time on this assignment because I need to prepare for the next quarter in college. But If I had time, I could correct more data from other cities, use LightGBM and KfoldStratified to improve accuracy of this model. Anyway, I hope I can do volunteering in city concil. Thanks!**"""