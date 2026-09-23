import pandas as pd, numpy as np
D = 'hydrogels/data/'
F = ['Nucleophilic-HEA','Hydrophobic-BA','Acidic-CBEA','Cationic-ATAC','Aromatic-PEA','Amide-AAm']
def keys(df): return list(map(tuple, np.round(df[F].values, 6)))
d = {n: pd.read_csv(D + f'df_{n}.csv') for n in (180, 289, 316, 341)}
big = d[341].copy()
prev, rounds = set(), {}
for r, n in enumerate((180, 289, 316, 341)):
    cur = set(keys(d[n]))
    for k in cur - prev:
        rounds[k] = r
    prev = cur
big['round'] = ['round_%d' % rounds[k] for k in keys(big)]
big['family'] = [F[i].split('-')[1] for i in np.argmax(big[F].values, axis=1)]
big = big.rename(columns={'Glass (kPa)_max': 'adhesion_kpa'}).drop(columns=['Unnamed: 0'])
big.to_csv('liao2025_adhesion.csv', index=False)
print(big.groupby('round').size().to_string(), '\n')
print(big.groupby('family').size().to_string(), '\n')
print('rows %d | target %.1f-%.1f kPa' % (len(big), big.adhesion_kpa.min(), big.adhesion_kpa.max()))
