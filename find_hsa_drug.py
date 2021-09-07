import pandas as pd

set = ['train','group1','group2']

data = pd.DataFrame(columns=['drug_id','hsa_id'])
for dataset in ['E','NR','IC','GPCR']:
    file = pd.read_csv(f'./update_dataset/{dataset}.csv')
    file = file.loc[:,['drug_id','hsa_id']]

    data = data.append(file,ignore_index=True)
data.drop_duplicates(keep='first',inplace=True)

for i in range(0,1):
    result = pd.DataFrame()
    file = pd.read_csv(f'./data/hsa_id_protein.csv')
    
    for j in range(0,len(file)):
        hsa = file.loc[j,'hsa_id']
        pro = file.loc[j,'protein']

        find = data.loc[data['hsa_id']==hsa,:]
        find.insert(1,'protein',pro,True)

        result = result.append(find.loc[:,['drug_id','protein']],ignore_index=True)

    result.to_csv(f'./data/drug_protein.csv',index=False)