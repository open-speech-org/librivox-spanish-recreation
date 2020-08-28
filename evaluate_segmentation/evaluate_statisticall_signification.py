from scipy import stats

precision_fixed_0_05 = [
89.74137931034483,
94.42105263157895,
70.94682230869002,
76.53910149750416,
86.34615384615385
]

precision_dynamic = [
88.46153846153845,
74.08963585434174,
69.78891820580475,
61.46993318485523,
67.15425531914893,
]


t, p = stats.ttest_ind(precision_fixed_0_05, precision_dynamic)
print("t = " + str(t))
# 1.818603087038002
print("p = " + str(p))
# 0.10647955235414566

# No statistical Signification
# https://towardsdatascience.com/inferential-statistics-series-t-test-using-numpy-2718f8f9bf2f

# import numpy as np
# N = 5
# #Gaussian distributed data with mean = 2 and var = 1
# a = np.random.randn(N) + 2
# #Gaussian distributed data with with mean = 0 and var = 1
# b = np.random.randn(N)
#
# ## Cross Checking with the internal scipy function
# t2, p2 = stats.ttest_ind(a,b)
# print("t = " + str(t2))
# print("p = " + str(p2))
