from ising_1d import Ising1D
import numpy as np
import matplotlib.pyplot as plot
from utils import majority, ud_to_value

# majority()


def block_1d(chain: Ising1D, l):
    out = Ising1D(chain.gridSize / l, chain.T)
    for i in range(out.gridSize):
        out.set(i, ud_to_value(majority(chain.state_at(i * l))))
    return out


chain = Ising1D(90, 5)
chain.loop(10000000)
Ts = np.linspace(5, 0.1, 30)

before = {
    "uuu": [],
    "uud": [],
    "dud": [],
}

after = {"uuu": [], "uud": [], "dud": []}

for t in Ts:
    print(t)
    chain.T = t
    chain.loop(1000000)

    blocked = block_1d(chain, 3)
    print(chain.count_normalized_states(), blocked.count_normalized_states())

    for state in ["uuu", "uud", "dud"]:
        before[state].append(chain.count_normalized_states()[state])
        after[state].append(blocked.count_normalized_states()[state])

plot.plot(Ts, before["uuu"], label="before_uuu")
plot.plot(Ts, before["uud"], label="before_uud")
plot.plot(Ts, before["dud"], label="before_dud")
plot.plot(Ts, after["uuu"], label="after_uuu")
plot.plot(Ts, after["uud"], label="after_uud")
plot.plot(Ts, after["dud"], label="after_dud")

plot.legend()
plot.show()
plot.pause()
