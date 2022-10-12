# %%
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler,StandardScaler
import warnings
warnings.filterwarnings('ignore')
import matplotlib.pyplot as plt 
import seaborn as sns
from sklearn.model_selection import train_test_split
import statsmodels.api as sm

# %%
dff=pd.read_excel("p2021.xlsx")
df=pd.read_excel("p2020.xlsx")
k=dff['Name']


# %%
df=df.set_index('Name')
dff=dff.set_index('Name')

# %%
scaler1=MinMaxScaler()
scaler2=StandardScaler()
df1=pd.DataFrame(scaler2.fit_transform(df))
dff=pd.DataFrame(scaler2.fit_transform(dff))
#df1=df
#df2=df

# %%
df1.set_axis(['TWS','SS','FSR','FQE','FRU','PU','QP','IPR','FPPP','GPHE','GUE','GMS','GPHD','RD','WD','ESCS','PCS'], axis=1, inplace=True)
dff.set_axis(['TWS','SS','FSR','FQE','FRU','PU','QP','IPR','FPPP','GPHE','GUE','GMS','GPHD','RD','WD','ESCS','PCS'], axis=1, inplace=True)

# %%
dff['Name']=k
dff=dff.set_index('Name')
dff

# %%
df1.corr().to_csv('corr.csv')
fig, ax = plt.subplots(figsize=(20,20)) 
sns.heatmap(df1.corr(), cmap="YlGnBu", annot = True,ax=ax)
plt.show()

# %%
pd.plotting.scatter_matrix(df1, alpha=0.2,figsize=(34,34))


# %%
X = df1.drop(columns='TWS')
y = df1['TWS']
X.info()


# %%
X.to_csv('x.csv')

# %%

# Train-test Split
X_train, X_test, y_train, y_test = train_test_split(X, y, train_size = 0.7, test_size = 0.3, random_state = 100)

# %%
X_train_sm = sm.add_constant(X_train)
lr = sm.OLS(y_train, X_train_sm).fit()
lr.params
print(lr.summary())

# %%
X1 = df1.drop(columns=['TWS','FSR','QP','FPPP','GUE','ESCS','PCS','GMS','WD','FRU','SS'])
y1 = df1['TWS']
#print(lr.summary())

# Train-test Split
X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, train_size = 0.7, test_size = 0.3, random_state = 100)
X1_train_sm = sm.add_constant(X1_train)
lr1 = sm.OLS(y1_train, X1_train_sm).fit()
lr1.params
print(lr1.summary())


# %%
from statsmodels.stats.outliers_influence import variance_inflation_factor
vif_data = pd.DataFrame()
vif_data['Features']=X1.columns
vif_data["VIF"] = [variance_inflation_factor(X1.values, i)
                          for i in range(len(X1.columns))]
vif_data

# %%
y1_train_pred = lr1.predict(X1_train_sm)
res = (y1_train - y1_train_pred)
res

# %%
fig = plt.figure()
sns.distplot(res, bins = 15)
fig.suptitle('Error Terms', fontsize = 15)                  # Plot heading 
plt.xlabel('y1_train - y1_train_pred', fontsize = 15)         # X-label
plt.show()

# %%
# Add a constant to X_test
X1_test_sm = sm.add_constant(X1_test)

# Predict the y values corresponding to X_test_sm
y1_pred = lr1.predict(X1_test_sm)

# %%
X1_test_sm

# %%
dff

# %%
xp=dff.drop(columns=['TWS','FSR','QP','FPPP','GUE','ESCS','PCS','GMS','WD','FRU','SS'])
yp=dff['TWS']
xp_sm=sm.add_constant(xp)
yp_pred = lr1.predict(xp_sm)

# %%
kkn=pd.DataFrame(yp_pred)

# %%
kkn.sort_values(by=0,ascending=False,inplace=True)

# %%
kkn.to_csv('final_result.csv')

# %%
y1_pred

# %%
yk=pd.DataFrame(y1_pred)
yk

# %%
yk[0].max()

# %%
from sklearn.metrics import mean_squared_error
from sklearn.metrics import r2_score

# %%
#Returns the mean squared error; we'll take a square root
np.sqrt(mean_squared_error(y1_test, y1_pred))

# %%
np.sqrt(mean_squared_error(yp, yp_pred))

# %%
r_squared = r2_score(y1_test, y1_pred)
r_squared

# %%
r_squared = r2_score(yp, yp_pred)
r_squared

# %%



