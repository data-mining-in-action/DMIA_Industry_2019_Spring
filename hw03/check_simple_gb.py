import os
import json
import re
from gb_impl_checker import Checker


if __name__ == '__main__':
    checker = Checker()
    scores = {}
    results = {}
    folder_path = 'hw_data/gb_impl/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            score = None
            name, score = checker.check(folder_path + filename)
            print(name, score)
            if name is not None and score is not None:
                results[name] = score
            elif name is not None:
                scores[name] = 0.025

    best_neg_mse = max(results.values())
    for name in results:
        scores[name] = max(round(2 ** (10. * (results[name] - 0.779)), 3), 0.05)

    with open('hw_data/gb_impl_results.json', 'w') as f:
        json.dump(scores, f, indent=4)

    with open('hw_data/gb_impl_results.csv', 'w') as f:
        f.write('email, score\n')
        for name in sorted(scores):
            f.write('{},{}\n'.format(name, scores[name]))
