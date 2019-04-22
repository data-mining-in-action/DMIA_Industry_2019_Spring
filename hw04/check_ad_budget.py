import os
import json
import re
from ad_budget_checker import Checker


if __name__ == '__main__':
    checker = Checker()
    scores = {}
    results = {}
    folder_path = 'hw_data/ad_budget/'
    for filename in os.listdir(folder_path):
        if filename.endswith('.py'):
            name, score = checker.check(folder_path + filename)
            print(name, score)
            if name is not None and score is not None:
                print('score is', max(round(score / 7.5, 2), 0.05))
                results[name] = score
            elif name is not None:
                scores[name] = 0.05

    best_accuracy = max(results.values())
    for name in results:
        scores[name] = max(round(results[name] / 7.5, 2), 0.05)

    with open('hw_data/ad_budget_results.json', 'w') as f:
        json.dump(scores, f, indent=4)

    with open('hw_data/ad_budget_results.csv', 'w') as f:
        f.write('email, score\n')
        for name in sorted(scores):
            f.write('{},{}\n'.format(name, scores[name]))
