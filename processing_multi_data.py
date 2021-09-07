import pandas as pd

file = pd.read_csv('./data/full_data.csv')

columns = file['protein'].drop_duplicates(keep='first')

data = file.loc[:,['smiles']]

for col in columns:
    data.insert(len(data.columns),col,0,True)

data.drop_duplicates(subset=['smiles'],keep='first',inplace=True,ignore_index=True)
data.rename(columns={'smiles':'SMILES'},inplace=True)

for i in range(0,len(file)):
    smiles = file.loc[i,'smiles']
    protein = file.loc[i,'protein']

    data.loc[data['SMILES']==smiles,[protein]] = 1

print(data)
data.to_csv('./data/multi_class_full_data.csv',index=False)