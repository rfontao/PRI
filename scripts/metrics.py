# SETUP
import matplotlib.pyplot as plt
from sklearn.metrics import PrecisionRecallDisplay
import numpy as np
import json
import requests
import pandas as pd

plt.style.use("netflix.mplstyle")

RESULT_LEN = 10
# SEARCH NEED 2
# query_results = [
#     ['R', 'R', 'R', 'R', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'R'],
#     ['R', 'R', 'R', 'R', 'R', 'N', 'R', 'N', 'R', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'R'],
#     ['R', 'R', 'R', 'R', 'N', 'N', 'R', 'R', 'N', 'N', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N']
# ]

# SEARCH NEED 3
query_results = [
    ['R', 'N', 'N', 'N', 'N', 'N', 'R', 'N', 'N', 'R', 'R', 'R', 'R', 'R', 'N', 'N', 'N', 'N', 'N', 'R'],
    ['R', 'R', 'R', 'R', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'N', 'R', 'N', 'N', 'N', 'N', 'N'],
    ['R', 'R', 'N', 'N', 'N', 'N', 'N', 'N', 'R', 'N', 'R', 'R', 'N', 'R', 'N', 'N', 'N', 'N', 'N', 'N']
]


def ap(results):
    """Average Precision"""
    precision_values = [
        (results[:idx].count("R") / idx) for idx in range(1, RESULT_LEN + 1) if results[idx - 1] == "R"
    ]
    print(precision_values)

    return sum(precision_values)/len(precision_values)


def p10(results):
    """Precision at N"""
    return results[:RESULT_LEN].count("R")/10

def r10(results):
    """Precision at N"""
    return results[:RESULT_LEN].count("R")/results.count("R")

def make_metrics_plots(query_results, prefix):
    fig, ax = plt.subplots()
    labels = [
        "Retrieval Method 1",
        "Retrieval Method 2",
        "Retrieval Method 3",
    ]
    ls = ["-", ":", "-"]

    for i in range(len(query_results)):

        results = query_results[i]

        print("P@10:", p10(results))
        print("R@10:", r10(results))
        print("AP:", ap(results))
        print("-----------------")


        # PRECISION-RECALL CURVE
        # Calculate precision and recall values as we move down the ranked list
        precision_values = [
            (results[:idx].count("R") / idx) for idx in range(1, RESULT_LEN + 1) if results[idx - 1] == "R"
        ]

        recall_values = [
            # (results[:idx].count("R") / results.count("R")) for idx in range(1, RESULT_LEN + 1) if results[idx - 1] == "R"
            (results[:idx].count("R") / results[:RESULT_LEN].count("R")) for idx in range(1, RESULT_LEN + 1) if results[idx - 1] == "R"
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
        disp.plot(ax=ax, label=labels[i], ls=ls[i])


    ax.set_ylim((-0.05, 1.05))
    ax.set_title("Precision-Recall Curve")
    ax.legend()
    # plt.show()
    fig.savefig(f'images/svg/{prefix}_precision_recall.svg', format="svg")
    fig.savefig(f'images/png/{prefix}_precision_recall.png', format="png", dpi=150, bbox_inches="tight")

if __name__ == "__main__":
    make_metrics_plots(query_results, "search_3")