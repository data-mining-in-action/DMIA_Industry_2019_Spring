import os
import json
import re
from xgboost_params_checker import Checker


if __name__ == '__main__':
    checker = Checker()
    scores = {}
    results = {}
    folder_path = 'hw_data/xgboost_params/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.json'):
            name, score = checker.check(folder_path + filename)
            print(name, score)
            if name is not None and score is not None:
                results[name] = score
            elif name is not None:
                scores[name] = 0.025

    best_accuracy = max(results.values())
    for name in results:
        scores[name] = max(round(2 ** (30 * (results[name] - 0.783)), 2), 0.05)

    with open('hw_data/xgboost_params_results.json', 'w') as f:
        json.dump(scores, f, indent=4)

    with open('hw_data/xgboost_params_results.csv', 'w') as f:
        f.write('email, score\n')
        for name in sorted(scores):
            f.write('{},{}\n'.format(name, scores[name]))
