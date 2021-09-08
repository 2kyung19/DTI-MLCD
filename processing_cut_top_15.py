import pandas as pd

file = pd.read_csv('./data/multi_class_full_data.csv')

result = file
col_sum = result.iloc[:,1:].sum() # drop count 0 columns
col_sum = col_sum.sort_values(ascending=False)

index = list(col_sum.index)
df = file.loc[:,['SMILES']]
for i in range(0,15):
    df.insert(len(df.columns),index[i],list(result.loc[:,index[i]]),True)

data = df
data.insert(len(data.columns),'sum',list(data.iloc[:,1:].sum(axis=1)),True)

data = data.loc[data['sum'] > 0] # drop sum 0 class
data = data.iloc[:,:len(data.columns)-1]
    
data.to_csv('./data/multi_class_top_10.csv',index=False)

