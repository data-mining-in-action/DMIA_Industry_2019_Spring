from scipy.stats import ttest_ind
import numpy as np


AUTHOR_EMAIL = 'ivanov@gmail.com'

def evaluate(
	train_conversions, 
    train_indices,
    test_conversions,
    test_indices
):
	# return ttest_ind(train_conversions, test_conversions, equal_var=False).pvalue
	return np.random.uniform()
