import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np



#We start by reading in our csv file and saving it as a panda dataframe with name df.
df = pd.read_csv(r"H:\3rdYearLabs\CosmicRaveDetectors\LabviewResultsWeek6\Book1.csv",header=None,
                 keep_default_na = True, names = ['Angle','RunTime','Counts','Rate','Uncertainty'])


#Test function and parameters is set up to fit the data to an  a*(cos^2(bx) + 0.5sin^2(bx)) curve. It requires us
#to put in reasonalbe intial paramaters in p0 for the amplitude and frequency in order for it to find a fit.


def test_func(x, a, b):
    return (a * (np.cos(b*x)*np.cos(b*x)+(0.5*(np.sin(b * x)*np.sin(b*x)))))-2

params, params_covariance = optimize.curve_fit(test_func, df['Angle'], df['Rate'],
                                               p0=[10, 1/80])


#the plot function plots our data frame angle and rate with the uncertainty in rate as the error.
#it then plots the test function output as a line of best fit.
#We have to define xaxisfit to have a suitable number of points at which we want to calculate our line of best fit

def plot():
    xaxisfit = np.linspace(-90,90,num=18100000)
    plt.errorbar(df['Angle'],df['Rate'],xerr=1,yerr=df['Uncertainty'],fmt='o',linewidth=1,markersize=4, label = 'Datapoint')
    plt.plot(xaxisfit,test_func(xaxisfit,params[0],params[1]),label = 'line of best fit')
    plt.ylabel('Coincidence Frequency (Hz)')
    plt.xlabel('Angle from Vertical (Degrees)')
    plt.legend(loc = 'best')
    plt.show()
    

plot()