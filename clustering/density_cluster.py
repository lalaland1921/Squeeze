# -*- ecoding: utf-8 -*-
# @ModuleName: density_cluster
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/3/7 16:58

import numpy as np
from scipy.signal import argrelmax,argrelmin
from collections import defaultdict
from matplotlib import pyplot as plt

def den_cluster(data): #data={dev(int):attr([tuples])},return list of list of tuple
    data = sorted(data.items(), key=lambda x: x[0])
    devs = []
    for dev, attr in data:
        devs += [dev] * len(attr)
    hists, bins = np.histogram(a=devs, bins=40, range=(-2, 2))
    '''print("hist:", hists)
    plt.hist(devs, bins)
    plt.show()'''
    '''centers=argrelmax(hists,mode='wrap')[0]
    boundaries=set(list(argrelmin(hists,mode='wrap')[0])+[i for i in range(len(hists)) if hists[i]==0])
    centers=[(bins[center]+bins[center+1])/2 for center in centers]
    boundaries=[(bins[b]+bins[b+1])/2 for b in boundaries]
    
    edges=[]
    i=0
    for center in centers:
        while(i<len(boundaries) and boundaries[i]<center):
            i+=1
        i-=1
        if i<0:
            l=bins[0]
        else:
            l=boundaries[i]
        i+=1
        if i>=len(boundaries):
            r=bins[-1]
        else:
            r=boundaries[i]
        edges.append((l,r))'''
    edges=[]
    i=0
    while(i<len(hists)):
        while(i<len(hists) and hists[i]==0):
            i+=1
        if i <len(hists):l=bins[i]
        while i<len(hists) and hists[i]>0:i+=1
        r=bins[i]
        edges.append((l,r))
    clusters=defaultdict(list)

    i=0
    for dev,attr in data:
        while (dev >= edges[i][0] and dev >= edges[i][1]):
            i += 1
        if dev>=edges[i][0]:
            clusters[edges[i]]+=attr
    #for edge,attr in clusters.items():
        #print('edge:',edge,'number:',len(attr))
    print('the clusters:',clusters.keys())
    return clusters.values()

#def clustering(data,mode=):

'''修改一下聚类方法，可以直接把靠在一起的正的分在一类，或者将center改为局部最大，且大于0，允许局部相等的点'''

'''if __name__ == '__main__':
    data={0.2:[(1,2,3)],0.1:[(1,2,4)]}
    clusters=den_cluster(data)
    print(clusters)'''