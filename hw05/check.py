import os
import json
import re
from checker import Checker


if __name__ == '__main__':
    checker = Checker()
    scores = {}
    results = {}
    folder_path = 'hw_data/significance/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            name, score = checker.check(folder_path + filename)
            print(name, score)
            if name is not None and score is not None:
                print('score is', min(max(round(2 ** (6 * (score - 2.8)), 2), 0.05), 2))
                results[name] = score
            elif name is not None:
                scores[name] = 0.05

    best_accuracy = max(results.values())
    for name in results:
        scores[name] = max(round(2 ** (6 * (results[name] - 2.8)), 2), 0.05)

    with open('hw_data/significance.json', 'w') as f:
        json.dump(scores, f, indent=4)

    with open('hw_data/significance.csv', 'w') as f:
        f.write('email, score\n')
        for name in sorted(scores):
            f.write('{},{}\n'.format(name, scores[name]))
