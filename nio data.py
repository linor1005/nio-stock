import matplotlib
from colorama import Fore
from colorama import Style
import numpy as np
import scipy.stats


def The_most_change(file):
    f = None
    try:
        if file == '':
            raise IOError("you didn't enter any file")
        d = {}
        f = open(file, 'r')
        if not f:
            raise ValueError('invalid file name')
        f.readline()
        # In the first part the user puts how many days he want to see and if he wants the gains or losses
        x = input("Please enter how many days you want to see\n")
        while x.isnumeric() is False or int(x) <= 0:
            print("Please Enter a real number that is larger than 0")
            x = input()
        x = int(x)
        up_down = input(
            f"Please enter {Fore.GREEN}'won'{Style.RESET_ALL} if you want to see the top gains or type {Fore.RED}'lost'{Style.RESET_ALL} for the top losses\n")
        while up_down not in ('won', 'lost'):
            print(f"Please type {Fore.GREEN}'won'{Style.RESET_ALL} or {Fore.RED}'lost'{Style.RESET_ALL}")
            up_down = input()
        for line in f:
            cline = line.rstrip().split(',')
            if '' in (cline[0], cline[1], cline[4], cline[-1]):
                continue
            change = ((float(cline[4]) - float(cline[1])) / float(cline[1])) * 100
            # This is a calculation of the daily change
            d[cline[0]] = [int(change), cline[-1]]
        if up_down == 'won':  # In the second part  we distinguish between the top gainer days and the top losers days
            for date in sorted(d, key=d.get, reverse=True)[:x]:
                print("At the date :", date, 'the stock has gained ', d[date][0], '%  and ', d[date][1] + '',
                      'shares have been traded this day')
        if up_down == 'lost':
            for date in sorted(d, key=d.get)[:x]:
                print("At the date :", date, 'the stock has lost ', d[date][0], '%  and ', d[date][1] + '',
                      'shares have been traded this day')
    except IOError:
        print('IOE error! check you file')
    finally:
        if f is not None:
            f.close()


#The_most_change('NIO stock data.csv')


def nio_vs_DRIV(nio_file, driv_file, result_file, date):
    f = None
    t = None
    try:
        if nio_file == '' or driv_file == '':
            raise IOError("you didn't enter any file")
        f = open(nio_file, 'r')
        t = open(driv_file, 'r')
        if f == [] or t == []:
            raise ValueError('invalid file name')
        f.readline()
        t.readline()
        # calculate the Normalized volume of the date NIO
        a_nio = 0
        a_driv = 0
        x = 0
        for line in f:
            lines = line.rstrip().split(',')
            a_nio = a_nio + float(lines[6])
            # x is the number of the trade days in NY stock exchange and in NASDAQ
            x = x + 1
            if lines[0] == date:
                v_nio = lines[6]
        a_nio = a_nio / x
        Normalized_v_nio = round(float(v_nio) / a_nio, 3)
        # calculate the Normalized volume of the date DRIV
        for line in t:
            lines = line.rstrip().split(',')
            a_driv = a_driv + float(lines[6])
            if lines[0] == date:
                v_driv = lines[6]
        a_driv = a_driv / x
        Normalized_v_DRIV = round(float(v_driv) / a_driv, 3)
        if Normalized_v_nio > Normalized_v_DRIV:
            the_most_atractive = 'NIO'
        else:
            the_most_atractive = 'DRIV'
        o = open(result_file, 'w')
        o.write(
            'Date,The Normalized volume of NIO stock,The Normalized volume of DRIV etf,The most attractive Securities')
        o.write('\n')
        o.write(date)
        o.write(',')
        o.write(str(Normalized_v_nio))
        o.write(',')
        o.write(str(Normalized_v_DRIV))
        o.write(',')
        o.write(the_most_atractive)
        o.close()
        print("The function worked!")
    except IOError:
        print('IOE error! check you file')
        print("The function didn't work!")
    finally:
        if f is not None and t is not None:
            f.close()
            t.close()


#nio_vs_DRIV('NIO stock data.csv', 'DRIV.csv','result.csv', '18/02/2020')

import matplotlib.pyplot as plt


def stock_volatility(file):
    f = None
    try:
        if file == '':
            raise IOError("you didn't enter any file")
        x = []
        y = []
        s = 0
        i = 0
        f = open(file, 'r')
        if not f:
            raise ValueError('invalid file name')
        f.readline()
        # In the first type we would like to know what is the average change in nio stock
        for line in f:
            cline = line.strip().split(',')
            if '' in (cline[2], cline[3]):
                continue
            change = float(cline[2]) - float(cline[3])
            i = i + 1
            s = s + change
        avg = s / i # This is the average change in a day of trading HIGH - LOW 
        f = open(file, 'r')
        f.readline()
        # In the second part we calculate the Standard Deviation ,the Standard Deviation is a measure to stock volatility
        for line in f:
            cline = line.strip().split(',')
            if '' in (cline[2], cline[3], cline[-1]):
                continue
            change = float(cline[2]) - float(cline[3])
            variance = (change - avg) ** 2  # this is calculation of the variance
            sd = variance ** 0.5
            x.append(int(cline[-1]))
            y.append(sd)
        plt.plot(x, y, 'r.')
        plt.title('Volatility Of Nio Stock')
        plt.xlabel('Volume In Hundred Millions ')
        plt.ylabel('The Standard Deviation')
        Pearson_R = round(scipy.stats.pearsonr(x, y)[0], 2)
        plt.legend(title= "Data about")
        plt.plot([],[],' ',label="hey")
        print("The p value is : ", scipy.stats.pearsonr(x, y)[1], 9)
        plt.scatter(x, y)
        plt.show()
    except IOError:
        print('IOE error! check you file')
    finally:
        if f is not None:
            f.close()
stock_volatility('NIO stock data.csv')
