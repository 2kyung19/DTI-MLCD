import pandas as pd
import requests
from tqdm import tqdm
import rdkit
from rdkit import Chem
import time

# search smiles
# reference code > 1_data_update > process_scrapy_data__generate_dti 

def find_drug_smiles(data,dataset='NR'):
    df = pd.DataFrame(columns=['drug_id','smiles'])
    error = pd.DataFrame(columns=['drug_id'])
    e = pd.read_csv('./update_dataset/E.csv')

    for i in tqdm(range(0,len(data))):
        drug_id = data.loc[i,'drug_id']
        protein = data.loc[i,'protein']

        if (len(e.loc[e['drug_id']==drug_id])>0): # E 에서 찾음
            smiles = e.loc[e['drug_id']==drug_id,['smiles']].values[0][0]
            df = df.append({'drug_id':drug_id,'smiles':smiles,'protein':protein},True)
            continue

        if(drug_id.find('DB')==-1): # kegg_retrieve_drug
            req = requests.get('http://www.kegg.jp/dbget-bin/www_bget?-f+m+compound+' + drug_id)
            
            if(len(req.text)==0): # exception
                error = error.append({'drug_id':drug_id},ignore_index=True)
                continue

            mol = open(f'./mol/{drug_id}.mol','w')
            mol.write(req.text)
            mol.close()
            
            mol_file = Chem.MolFromMolFile(f'./mol/{drug_id}.mol')
            smiles = Chem.MolToSmiles(mol_file)
            
        else: # drugbank_retrieve_drug
            req = requests.get(f'https://go.drugbank.com/structures/small_molecule_drugs/{drug_id}.smiles')
            smiles = req.text
            if(len(smiles)==0): # exception
                error = error.append({'drug_id':drug_id},ignore_index=True)
                continue
                
        df = df.append({'drug_id':drug_id,'smiles':smiles,'protein':protein},True)
       
    return df,error

for dataset in ['group2']:
    data = pd.read_csv(f'./data/drug_protein.csv')
    df,error = find_drug_smiles(data,dataset=dataset)

    df.to_csv(f'./data/full_data.csv',index=False)
    error.to_csv(f'./data/error.csv',index=False)