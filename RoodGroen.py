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
print("[Filter]: Filtering red items")
results_red = rood_groen.filter("red")
print("[Filter] Filtering green items")
results_green = rood_groen.filter("green")

print("[Pandas] Preparing output")

def results_to_dataframe(results, order):
    df_dict = []
    for result in results:
        row = {"sentence": result[0],
               "participle": result[2][0],
               "auxiliary": result[2][1],
               "participle_lemma": result[2][2],
               "auxiliary_lemma": result[2][3],
               "file": result[1],
               "order": order}
        df_dict.append(row)        
 
    return pd.DataFrame.from_dict(df_dict)

# Convert results to dataframes
df_red = results_to_dataframe(results_red, "red")
df_green = results_to_dataframe(results_green, "green")

# Combine both data frames
df = pd.concat([df_red, df_green])

print(f"[Pandas] Writing CSV file {args.output_path}")

# Write to CSV
df.to_csv(args.output_path, index=False)

t2 = time.perf_counter()

print(f'Finished in {t2-t1} seconds')