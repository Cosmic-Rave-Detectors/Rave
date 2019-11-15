import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np

df = pd.read_csv(r"H:\3rdYearLabs\CosmicRaveDetectors\LabviewResultsWeek6\Book1.csv",header=None,
                 keep_default_na = True, names = ['Angle','RunTime','Counts','Rate','Uncertainty'])


def cossquaredfit():
    xfit=[]
    yfit=[]
    start = -90
    finish = 90
    Amplitude = 2.75
    for i in range(start,finish,1):
        xfit.append(i)
        yfit.append(((Amplitude*np.cos(i/55)*np.cos(i/55))+(0.5*(np.sin(i/55)*np.sin(i/55))))-0.25)
    return([xfit,yfit])

def test_func(x, a, b):
    return a * (np.cos(b*x)*np.cos(b*x)*(0.5*(np.sin(b * x)*np.sin(b*x))))

params, params_covariance = optimize.curve_fit(test_func, df['Angle'], df['Rate'],
                                               p0=[2, 2])

def plot():
    #fittingdata = cossquaredfit()
    plt.errorbar(df['Angle'],df['Rate'],xerr=1,yerr=df['Uncertainty'],fmt='o',linewidth=1,markersize=4)
    plt.plot(df['Angle'],test_func(xlist,params[0],params[1]))
    plt.legend(loc = 1)
    plt.show
   
plot()



