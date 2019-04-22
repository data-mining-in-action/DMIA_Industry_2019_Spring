#coding=utf-8

from sklearn.datasets import make_classification
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_error
import numpy as np
import os
import imp
import signal
import traceback
import sys
import json


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))


def signal_handler(signum, frame):
    raise Exception("Timed out!")


class Checker(object):
    def __init__(self):
        self.applications = 0

    def check(self, script_path):
        AUTHOR_EMAIL = None
        try:
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(240)
            algo_impl = imp.load_source('algo_impl_{}'.format(self.applications), script_path)
            self.applications += 1
            AUTHOR_EMAIL = algo_impl.AUTHOR_EMAIL
            
            
            saved_moneys = 0.

            random_gen = np.random.RandomState(68)
            for _ in range(5):
                weights = (0.05 + random_gen.exponential(0.75, size=15)) * 2
                X_data = random_gen.uniform(0., 4, size=(40, 15))
                errors = random_gen.normal(0., 2., size=40)
                split_pos = 25
                X_train = X_data[:split_pos]
                errors_train = errors[:split_pos]
                X_test = X_data[split_pos:]
                errors_test = errors[split_pos:]
                weights = weights

                algo = algo_impl.Optimizer()
                algo.fit(np.array(X_train), np.dot(X_train, weights) + errors_train)
                
                for budget, target_error in zip(X_test, errors_test):
                    origin_budget = np.array(budget)
                    optimized_budget = np.array(algo.optimize(origin_budget))

                    if ((origin_budget * 0.95 <= optimized_budget) & (optimized_budget <= origin_budget * 1.05)).all():
                        if np.dot(optimized_budget, weights) >=  np.dot(origin_budget, weights):
                            saved_moneys += np.sum(origin_budget) - np.sum(optimized_budget)

            return AUTHOR_EMAIL, saved_moneys / 5.
        except:
            traceback.print_exception(*sys.exc_info())
            return AUTHOR_EMAIL, None


if __name__ == '__main__':
    print(Checker().check(SCRIPT_DIR + '/ad_budget_example.py'))
