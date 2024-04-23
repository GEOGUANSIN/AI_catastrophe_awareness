import ollama
import pandas as pd

social_factors = pd.read_csv('new/belief.csv')
output = {}
for index, row in social_factors.iterrows():
    information = f"Abstract: {row['abstract']}\nDescription: {row['description']}\n"
    em = ollama.embeddings(model='nomic-embed-text', prompt=information)
    if row['abstract'] in social_factors['abstract'].tolist():
        output[row['abstract']+' '+str(index)] = em['embedding']
    else:
        output[row['abstract']] = em['embedding']

output_df = pd.DataFrame(output).transpose()

output_df.to_csv('new/belief_embedding.csv')

