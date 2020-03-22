import pandas as pd
import numpy as np
import statistics as st


# calculating return using last day price.
def calc_return(arr):
    ret = [];

    if len(arr) == 1:
        ret.append(0)
        ret.append(0)
        return ret

    for i in range(len(arr)-1):
        ret.append(arr[i+1]/arr[i]-1)

    return ret

'''
Update function
New val based on return and var upto last day(today variations are not playing any role, i know it's very faulty but that's how it is)
It is not used at start of trading because High and Low will be same as new_val, so a different is handling that case.
'''
def update_data(stk):
    #print(stk)
    curr_val = stk['Curr']
    new_val = curr_val*np.exp((stk['mean']-(1/2)*(stk['var'])**2) + stk['var']*np.random.normal(0, 1))
    #print(new_val)
    open_val = stk['Open']
    high = max(new_val, stk['High'])
    low = min(new_val, stk['Low'])
    return [open_val, high, low, new_val]

## Here is that different function.
def update_data_start(frame, m, v):
    arr = frame["Curr"]
    curr_val = arr[len(arr) - 1]
    new_val = curr_val*np.exp((m-1/2*v*v) + v*np.random.normal(0, 1))
    open_val = new_val
    high = new_val
    low =  new_val
    return [open_val, high, low, new_val]
