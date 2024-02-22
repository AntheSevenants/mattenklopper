import json
import time
import argparse
import pandas as pd

from mattenklopper.RoodGroen import RoodGroen

#
# Argument parsing
#

parser = argparse.ArgumentParser(description='mattenklopper RoodGroen - corpus filtering for the red and green word order')
parser.add_argument('closed_items_path', type=str,
					help='Path to the JSON file containing the closed items which will narrow down the search space')
parser.add_argument('alpino_corpus_path', type=str,
					help='Path to the Alpino corpus files')
parser.add_argument('--output_path', type=str, nargs='?', default='RoodGroenAnthe.csv', help='Name of the output file')

args = parser.parse_args()

# Start the performance counter
t1 = time.perf_counter()

print("[Data] Loading closed items")

# We use the "closed items" class as a way to narrow down the search space
with open(args.closed_items_path, "rt") as reader:
    closed_class_items = json.loads(reader.read())

# Find corpus hits
rood_groen = RoodGroen(args.alpino_corpus_path, closed_class_items)
print("[Filter]: Filtering red and green items")
results = rood_groen.filter("red_green")

print("[Pandas] Preparing output")

def results_to_dataframe(results, order):
    df_dict = []
    for result in results:
        row = {"sentence": result[0],
               "participle": result[3][0],
               "auxiliary": result[3][1],
               "participle_lemma": result[3][2],
               "auxiliary_lemma": result[3][3],
               "participle_index": result[3][4],
               "auxiliary_index": result[3][5],
               "file": result[1],
               "sentence_id": result[2],
               "order": result[3][6]}
        df_dict.append(row)        
 
    return pd.DataFrame.from_dict(df_dict)

# Convert results to dataframes
df = results_to_dataframe(results, "red")

# Remove duplicates (they exist now)
print("[Pandas] Removing duplicates")
df = df.drop_duplicates(subset=["sentence", "participle_index", "auxiliary_index"])

print(f"[Pandas] Writing CSV file {args.output_path}")

# Write to CSV
df.to_csv(args.output_path, index=False)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')
