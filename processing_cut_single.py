import pandas as pd

file = pd.read_csv('./data/multi_class_full_data.csv')

data = file
data.insert(len(data.columns),'sum',list(data.iloc[:,1:].sum(axis=1)),True)

data = data.loc[data['sum'] > 1]
result = data

col_sum = list(data.iloc[:,1:].sum())
for i in range(0,len(col_sum)):
    if (col_sum[i]==0):
        col = list(data.columns)[i+1]
        result = result.drop(columns=[col],axis=1)

result.to_csv('./data/multi_class_cut_single.csv',index=False)
len(result.columns)