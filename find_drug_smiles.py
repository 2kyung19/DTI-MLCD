import pandas as pd
import requests
from tqdm import tqdm
import rdkit
from rdkit import Chem
import time

# reference code > 1_data_update > process_scrapy_data__generate_dti 

def find_drug_smiles(drug_list,dataset='NR'):
    df = pd.DataFrame(columns=['drug_id','smiles'])
    error = pd.DataFrame(columns=['drug_id'])

    for drug_id in tqdm(drug_list):
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

        df = df.append({'drug_id':drug_id,'smiles':smiles},True)
       
    return df,error

# except E
for dataset in ['NR','IC','GRCR']:
    data = pd.read_csv(f'./update_dataset/{dataset}.csv')
    df,error = find_drug_smiles(list(data['drug_id']),dataset=dataset)

    df.to_csv(f'./dataset/{dataset}_drug_smiles.csv',index=False)
    error.to_csv(f'./dataset/{dataset}_error.csv',index=False)