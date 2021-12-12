# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

plt.style.use("netflix.mplstyle")
# QRELS_FILE = ...
# QUERY_URL = ...

# Read qrels to extract relevant documents
# relevant = list(map(lambda el: el.strip(), open(QRELS_FILE).readlines()))
# Get query results from Solr instance
# results = requests.get(QUERY_URL).json()['response']['docs']

RESULT_LEN = 10
query_results = [
    ['R', 'R', 'R', 'R', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'R'],
    ['R', 'R', 'R', 'R', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'R'],
    ['R', 'R', 'R', 'R', 'N', 'N', 'R', 'R', 'N', 'N', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N']
]


def ap(results):
    """Average Precision"""
    precision_values = [
        (results[:idx].count("R") / idx) for idx in range(1, RESULT_LEN)
    ]
    return sum(precision_values)/len(precision_values)


def p10(results):
    """Precision at N"""
    return results[:RESULT_LEN].count("R")/10

def r10(results):
    """Precision at N"""
    return results[:RESULT_LEN].count("R")/results.count("R")


# def calculate_metric(key, results):
#     return metrics[key](results)


# # Define metrics to be calculated
# evaluation_metrics = {
#     'ap': 'Average Precision',
#     'p10': 'Precision at 10 (P@10)'
# }

# # Calculate all metrics and export results as LaTeX table
# df = pd.DataFrame([['Metric', 'Value']] +
#                   [
#     [evaluation_metrics[m], calculate_metric(m, results)]
#     for m in evaluation_metrics
# ]
# )

# with open('results.tex', 'w') as tf:
#     tf.write(df.to_latex())

fig, ax = plt.subplots()
labels = [
    "Retrieval Method 1",
    "Retrieval Method 2",
    "Retrieval Method 3",
]
for i in range(len(query_results)):

    results = query_results[i]

    print("P@10:", p10(results))
    print("R@10:", r10(results))
    print("AP:", ap(results))
    print("-----------------")


    # PRECISION-RECALL CURVE
    # Calculate precision and recall values as we move down the ranked list
    precision_values = [
        (results[:idx].count("R") / idx) for idx in range(1, RESULT_LEN)
    ]

    recall_values = [
        (results[:idx].count("R") / results.count("R")) for idx in range(1, RESULT_LEN)
    ]

    precision_recall_match = {k: v for k,
                            v in zip(recall_values, precision_values)}

    # Extend recall_values to include traditional steps for a better curve (0.1, 0.2 ...)
    recall_values.extend([step for step in np.arange(
        0.1, 1.1, 0.1) if step not in recall_values])
    recall_values = sorted(set(recall_values))

    # Extend matching dict to include these new intermediate steps
    for idx, step in enumerate(recall_values):
        if step not in precision_recall_match:
            if recall_values[idx-1] in precision_recall_match:
                precision_recall_match[step] = precision_recall_match[recall_values[idx-1]]
            else:
                precision_recall_match[step] = precision_recall_match[recall_values[idx+1]]

    disp = PrecisionRecallDisplay(
        [precision_recall_match.get(r) for r in recall_values], recall_values)
    disp.plot(ax=ax, label=labels[i])


ax.set_ylim((-0.05, 1.05))
ax.set_title("Precision-Recall Curve")
ax.legend()
# plt.show()
plt.savefig('precision_recall.png')
