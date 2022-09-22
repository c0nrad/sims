import numpy as np
import matplotlib.pyplot as plot

stm = np.loadtxt('./stm.txt')

plot.matshow(stm)
plot.pause(0)
