import pandas as pd
import requests
from tqdm import tqdm
from bs4 import BeautifulSoup

# reference code > 1_data_update > process_scrapy_data__generate_dti 

def find_protein(hsa_list,dataset='NR'):
    df = pd.DataFrame(columns=['hsa_id','protein'])
    error = pd.DataFrame(columns=['drug_id'])

    for hsa_id in tqdm(hsa_list):
        id = hsa_id.split('hsa')[1] # hsa0001 -> 0001
        req = requests.get('https://www.kegg.jp/dbget-bin/www_bget?-f+-n+a+hsa:' + id)
        soup = BeautifulSoup(req.text,'html.parser')
        
        try:
            hsa = soup.select('body > div > pre')[0]
            hsa = str(hsa).split('(RefSeq)')[1].split(';')[0].replace(' ','') # protein list
            hsa = hsa.split(',')
        except:
            print(hsa_id)
            continue
            
        #for h in hsa:
        df = df.append({'hsa_id':hsa_id,'protein':hsa[0]},ignore_index=True)

    return df,error

data = pd.DataFrame(columns=['hsa_id'])
for dataset in ['E','NR','IC','GPCR']:
    file = pd.read_csv(f'./update_dataset/{dataset}.csv')
    file = file.loc[:,['hsa_id']]

    data = data.append(file,ignore_index=True)

data.drop_duplicates(keep='first',inplace=True)
data = list(data['hsa_id'])

df,error = find_protein(data,dataset=dataset)

df.to_csv('./data/hsa_id_protein.csv',index=False)