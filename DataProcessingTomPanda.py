import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"H:\3rdYearLabs\CosmicRaveDetectors\Data.csv",header=None,
                 keep_default_na = False, names = ['numbers','squares'])


df.plot(kind = 'line', x='numbers',y='squares')
