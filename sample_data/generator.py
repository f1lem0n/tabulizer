import numpy as np

array = np.random.rand(8, 12)
np.savetxt("random3.tsv", array, delimiter="\t")
