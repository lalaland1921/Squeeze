# -*- ecoding: utf-8 -*-
# @ModuleName: filter
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/3/7 16:38
from collections import defaultdict
from kneed import KneeLocator
import numpy as np
import warnings

def cal_dev(real,pre):
    return 2*(pre-real)/(pre+real+0.000001)

def plain_filt(data,thre=0.2):#'data' is a dict{attributes:(real,pre)},'thre' is the threshold to filter
    inverse=defaultdict(list)
    for attr,d in data.items():
        real,pre=d[0],d[1]
        dev=cal_dev(real,pre)
        if abs(dev)>thre:
            inverse[dev].append(attr)
    return inverse

def knee_filt(data):
    newdata=[np.log(np.abs(v-f)+1) for v,f in data.values()]
    hists,bins=np.histogram(newdata,80)
    cdf=np.cumsum(hists)
    x=bins[1:]
    kneedle=KneeLocator(x,cdf,S=1.0,curve='concave',direction='increasing',online=True)
    kneedle.plot_knee()
    knee=kneedle.knee
    inverse = defaultdict(list)
    for attr, d in data.items():
        if np.log(np.abs(d[0]-d[1])+1) >=knee:
            dev = cal_dev(d[0], d[1])
            inverse[dev].append(attr)
    return inverse

def filter(data,thre=0.2,mode='auto'):
    if mode=='auto':
        return knee_filt(data)
    if mode == 'naive':
        return plain_filt(data,thre)
    warnings.warn("{} is a wrong filter mode,which can only be 'auto' or 'naive'".format(mode))
'''if __name__ == '__main__':
    data={(1,2,3):(2,3),(1,2,4):(2,5)}
    inverse=filter(data,0.1)'''