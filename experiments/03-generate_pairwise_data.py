import argparse
import json
import collections
import itertools
import random
import csv

args = argparse.ArgumentParser()
args.add_argument("data_in")
args.add_argument("data_out")
args.add_argument("-s", "--subsample", default=0.5, type=float)
args.add_argument("-c", "--crop", default=1, type=float)
args = args.parse_args()

with open(args.data_in) as f:
    data = [json.loads(line) for line in f]
data = data[:int(len(data)*args.crop)]

# match based on the source
src_to_tgts = collections.defaultdict(list)
for x in data:
    src_to_tgts[x["src"]].append((x["tgt"], x["score"]))


data_out = []
for src, l in src_to_tgts.items():
    for (mt1, score1), (mt2, score2) in itertools.combinations(l, 2):
        # prune some pairs
        if random.random() >= args.subsample:
            continue
        # randomly flip coin which one is better
        tmp = [(mt1, score1), (mt2, score2)]
        random.shuffle(tmp)
        (mt1, score1), (mt2, score2) = tmp
        data_out.append({
            "src": src,
            "mt1": mt1,
            "mt2": mt2,
            "score": (score1 > score2)*1,
        })


with open(args.data_out, "w") as f:
    writer = csv.DictWriter(f, fieldnames=["src", "mt1", "mt2", "score"])
    writer.writeheader()
    writer.writerows(data_out)


# python3 experiments/03-generate_pairwise_data.py data/jsonl/train.jsonl data/csv/train_pairwise.csv -s 1 -c 0.1
# python3 experiments/03-generate_pairwise_data.py data/jsonl/test.jsonl data/csv/test_pairwise.csv
# python3 experiments/03-generate_pairwise_data.py data/jsonl/dev.jsonl data/csv/dev_pairwise.csv
