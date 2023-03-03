import json
import time
import argparse
import pandas as pd

from mattenklopper.Participles import Participles

#
# Argument parsing
#

parser = argparse.ArgumentParser(description='mattenklopper Participles - corpus filtering for searching all possible participles')
parser.add_argument('alpino_corpus_path', type=str,
					help='Path to the Alpino corpus files')
parser.add_argument('--output_path', type=str, nargs='?', default='ParticiplesAnthe.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

# Find corpus hits
participles = Participles(args.alpino_corpus_path)
print("[Filter]: Filtering for participles")
results = participles.filter()

print("Found", len(results), "attestations")

print("[Pandas] Preparing output")

def results_to_dataframe(results):
    df_dict = []
    for result in results:
        row = {"sentence": result[0],
               "participle": result[3][0],
               "participle_lemma": result[3][1],
               "file": result[1],
               "sentence_id": result[2] }
        df_dict.append(row)        
 
    return pd.DataFrame.from_dict(df_dict)

# Convert results to dataframes
df = results_to_dataframe(results)

print(f"[Pandas] Writing CSV file {args.output_path}")

# Write to CSV
df.to_csv(args.output_path, index=False)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')
