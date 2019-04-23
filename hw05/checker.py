import numpy as np
import os
import imp
import signal
import traceback
import sys


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))

LOW = 0.3
HIGH = 0.8
USERS_SIZE = 500
CONVERSIONS_SIZE = 10000


def signal_handler(signum, frame):
    raise Exception("Timed out!")


class Checker(object):
    def __init__(self):
        self.applications = 0

    @staticmethod
    def perform_test(random_gen, evaluate, effect):
        train_user_probs = random_gen.uniform(low=LOW, high=HIGH, size=USERS_SIZE)
        train_indices = random_gen.choice(USERS_SIZE, size=CONVERSIONS_SIZE, replace=True)
        train_conversions = (
            random_gen.uniform(size=CONVERSIONS_SIZE) < train_user_probs[train_indices]
        ).astype(int)

        test_user_probs = effect + random_gen.uniform(low=LOW, high=HIGH, size=USERS_SIZE)
        test_indices = random_gen.choice(USERS_SIZE, size=CONVERSIONS_SIZE, replace=True)
        test_conversions = (
            random_gen.uniform(size=CONVERSIONS_SIZE) < test_user_probs[test_indices]
        ).astype(int)

        pvalue = evaluate(
            test_conversions,
            test_indices,
            train_conversions, 
            train_indices
        )

        return pvalue

    @staticmethod
    def eval_hits_ratio(random_gen, evaluate, effect, significance):
        hits = 0
        for _ in range(1000):
            hits += Checker.perform_test(random_gen, evaluate, effect) < significance
        return hits / 1000.


    def check(self, script_path):
        AUTHOR_EMAIL = None
        random_gen = np.random.RandomState(75)
        try:
            signal.signal(signal.SIGALRM, signal_handler)
            signal.alarm(120)
            module = imp.load_source('significance_{}'.format(self.applications), script_path)
            AUTHOR_EMAIL = module.AUTHOR_EMAIL
            
            correctness = self.eval_hits_ratio(random_gen, module.evaluate, effect=0., significance=0.05)
            if correctness > 0.07:
                raise ValueError('Incorrect test: hits raitio is {}'.format(correctness))

            power_005 = self.eval_hits_ratio(random_gen, module.evaluate, effect=0.005, significance=0.05)
            power_010 = self.eval_hits_ratio(random_gen, module.evaluate, effect=0.01, significance=0.05)
            power_050 = self.eval_hits_ratio(random_gen, module.evaluate, effect=0.05, significance=0.05)

            print(correctness, power_005, power_010, power_050)

            return AUTHOR_EMAIL, float(power_050 + power_010 * 4 + power_005 * 16)
        except:
            traceback.print_exception(*sys.exc_info())
            return AUTHOR_EMAIL, None
        finally:
            self.applications += 1



if __name__ == '__main__':
    print(Checker().check(SCRIPT_DIR + '/example.py'))
