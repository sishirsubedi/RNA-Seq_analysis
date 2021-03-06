
import pandas as pd
import GPy, numpy as np
import math
from matplotlib import pyplot as plt
np.random.seed(1)
from numpy import unravel_index

##################################### 6:GPy package - COS/RV as two groups

cos_smooth = []
rv_smooth = []

X = [3.0, 6.5, 9.0, 12.0, 18.5, 21.0, 27.0, 31.0, 33.0, 36.0, 39.5, 42.0, 45.5, 52.0, 55.0, \
     3.0, 6.5, 9.0, 12.0, 18.5, 21.0, 27.0, 31.0, 33.0, 36.0, 39.5, 42.0, 45.5, 52.0, 55.0]


x_pred = X[0:15]
x_pred = np.atleast_2d(x_pred).T
X = np.atleast_2d(X).T


df_cos1 = pd.read_csv('4_cos1_logmean.csv', delimiter=',',header=0)
temp_cos1 = []
for row in df_cos1.iterrows():
    index, data = row
    temp_cos1.append(data.tolist())

df_cos2 = pd.read_csv('4_cos2_logmean.csv', delimiter=',',header=0)
temp_cos2 = []
for row in df_cos2.iterrows():
    index, data = row
    temp_cos2.append(data.tolist())

lenscales_cos =[]

for rv in range(0,len(temp_cos1)):
    ycos1= temp_cos1[rv]
    ycos2 = temp_cos2[rv]
    y1 = ycos1[1:] + ycos2[1:]
    Y = np.atleast_2d(y1).T

    res = []
    for l in range(1,50):
        kernel = GPy.kern.RBF(input_dim=1, variance=1.0, lengthscale=l)
        m = GPy.models.GPRegression(X, Y, kernel, noise_var=0.1)
        res.append( m.log_likelihood())

    lenscale = res.index(max(res))+1
    kernel = GPy.kern.RBF(input_dim=1, variance=1.0, lengthscale=lenscale)
    m = GPy.models.GPRegression(X, Y,kernel,noise_var=0.1)
    mu,C=m.predict(x_pred, full_cov=True)
    mu = [val for sublist in mu for val in sublist]

    temp=[]
    temp.append(ycos1[0])
    for items in mu:
        temp.append(items)
    cos_smooth.append(temp)


    lenscales_cos.append([ycos1[0],lenscale])


df_rv1 = pd.read_csv('4_rv1_logmean.csv', delimiter=',',header=0)
temp_rv1 = []
for row in df_rv1.iterrows():
    index, data = row
    temp_rv1.append(data.tolist())


df_rv2 = pd.read_csv('4_rv2_logmean.csv', delimiter=',',header=0)
temp_rv2 = []
for row in df_rv2.iterrows():
    index, data = row
    temp_rv2.append(data.tolist())


for rv in range(0,len(temp_rv1)):
    yrv1 = temp_rv1[rv]
    yrv2 = temp_rv2[rv]
    y = yrv1[1:] + yrv2[1:]

    #y= np.log(y)

    Y = np.atleast_2d(y).T

    res = []
    for l in range(1, 50):
        kernel = GPy.kern.RBF(input_dim=1, variance=1.0, lengthscale=l)
        m = GPy.models.GPRegression(X, Y, kernel, noise_var=0.1)
        res.append(m.log_likelihood())

    lenscale = res.index(max(res)) + 1
    kernel = GPy.kern.RBF(input_dim=1, variance=1.0, lengthscale=lenscale)
    m = GPy.models.GPRegression(X, Y,kernel,noise_var=0.01)
    mu,C=m.predict(x_pred, full_cov=True)

    mu = [val for sublist in mu for val in sublist]

    temp=[]
    temp.append(yrv1[0])
    for items in mu:
        temp.append(items)
    rv_smooth.append(temp)


smooth_rv = pd.DataFrame(rv_smooth)

smooth_cos = pd.DataFrame(cos_smooth)

smooth_cos.columns = ["Rv", "cos_sm_2", "cos_sm_3", "cos_sm_4", "cos_sm_5", "cos_sm_6", "cos_sm_7", "cos_sm_8", "cos_sm_9", \
                    "cos_sm_10", "cos_sm_11", "cos_sm_12", "cos_sm_13", "cos_sm_14", "cos_sm_15", "cos_sm_16"]

smooth_rv.columns = ["Rv", "rv_sm_2", "rv_sm_3", "rv_sm_4", "rv_sm_5", "rv_sm_6", "rv_sm_7", "rv_sm_8", "rv_sm_9", \
                   "rv_sm_10", "rv_sm_11", "rv_sm_12", "rv_sm_13", "rv_sm_14", "rv_sm_15", "rv_sm_16"]

smooth_rv.to_csv("final_rv_smooth.csv",index = False)
smooth_cos.to_csv("final_cos_smooth.csv", index = False)



