import pandas as pd
import matplotlib.pyplot as plt
from scipy import optimize
import numpy as np



#We start by reading in our csv file and saving it as a panda dataframe with name df.
df = pd.read_csv(r"H:\3rdYearLabs\CosmicRaveDetectors\LabviewResultsWeek6\Book1.csv",header=None,
                 keep_default_na = True, names = ['Angle','RunTime','Counts','Rate','Uncertainty'])


#Test function and parameters is set up to fit the data to an  a*(cos^2(bx) + 0.5sin^2(bx)) curve. It requires us
#to put in reasonalbe intial paramaters in p0 for the amplitude and frequency in order for it to find a fit. p0s first
#argument is the guess of the amplitude and the second parameter is the guess of the frequency (of the fit not of the data)


def test_func(x, a, b, c, d, e,f):
    return (a * (f*np.cos(b*x+c)**2+(e*(np.sin(b*x+c)**2))))-d

params, params_covariance = optimize.curve_fit(test_func, df['Angle'], df['Rate'],
                                               p0=[10, 1/90,4,2,0.27,1])


#the plot function plots our data frame angle and rate with the uncertainty in rate as the error.
#it then plots the test function output as a line of best fit.
#We have to define xaxisfit to have a suitable number of points at which we want to calculate our line of best fit, we use linspace to make 1810 points equally
#spaced between -90 and 90.
#The resultant graph is saved as a png file in the same folder as the python file is located in.

def plot():
    xaxisfit = np.linspace(-90,90,num=1810)
    plt.errorbar(df['Angle'],df['Rate'],xerr=1,yerr=df['Uncertainty'],fmt='o',linewidth=1,markersize=4, label = 'Datapoint')
    plt.plot(xaxisfit,test_func(xaxisfit,params[0],params[1],params[2],params[3],params[4],params[5]),label = 'line of best fit')
    plt.ylabel('Coincidence Frequency (Hz)')
    plt.xlabel('Angle from Vertical (Degrees)')
    plt.legend(loc = 'best')
    plt.savefig('CoincidenceRateLabDetector.png')
    plt.show()
    print('Amplitude = ',params[0],'Hz')
    print('Frequency = ',params[1], 'ns^-1')
    print('Horizontal Shift = -',params[2])
    print('Vertical Shift = -', params[3], 'Hz')
    print(params[4])
    print(params[5])


plot()