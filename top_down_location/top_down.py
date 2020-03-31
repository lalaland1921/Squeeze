# -*- ecoding: utf-8 -*-
# @ModuleName: calculation
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/3/8 10:20
from itertools import combinations
import numpy as np
from collections import defaultdict

'''def descent_ratio(attributes,n_ele,rtcause):
    for'''
def top_down(cluster,data,attrlen,theta,C):
    attrnum=np.arange(attrlen)
    #stop=0
    root_causes = defaultdict(dict)
    for layer in range(attrlen):
        #if stop==1:break
        cuboids=combinations(attrnum,layer+1)
        maxgps=0
        for cuboid in cuboids:
            #n_descents=leafs
            '''for i in cuboid:
                n_descents/=i'''
            split=defaultdict(list)
            for attr in cluster:
                rtcause=tuple([attr[i] if i in cuboid else -1 for i in range(len(attrnum))])
                split[rtcause].append(attr)
            n_descents={}
            for rtcause in split.keys():
                n_descents[rtcause]=0
            for attr in data.keys():
                rtcause = tuple([attr[i] if i in cuboid else -1 for i in range(len(attrnum))])
                if rtcause in n_descents:
                    n_descents[rtcause]+=1
            descent_ratio={}
            for rtcause in split.keys():
                descent_ratio[rtcause]=len(split[rtcause])/n_descents[rtcause]
            #if max(descent_ratio.values())<0.2:continue
            split=sorted(split.items(),key=lambda x:descent_ratio[x[0]],reverse=True)
            gpss=list()
            for item in split:
                rtcause,S1=item
                '''if descent_ratio[rtcause]<0.2:
                    break'''
                S2=[]
                for item in split:
                    if item[0]!=rtcause:
                        S2+=item[1]
                Vs1=np.array([data[attr][0] for attr in S1])
                Fs1=np.array([data[attr][1] for attr in S1])
                As1=np.sum(Vs1)/np.sum(Fs1)*Fs1
                Vs2 = np.array([data[attr][0] for attr in S2]) if S2 else 0
                Fs2 = np.array([data[attr][1] for attr in S2]) if S2 else 0
                gps=1-(np.average(np.abs(Vs1-As1))+np.average(np.abs(Vs2-Fs2)))/(np.average(np.abs(Vs1-Fs1))+np.average(np.abs(Vs2-Fs2)))

                gpss.append(gps)
            try:
                index = np.argmax(np.array(gpss))
                maxgps = max(gpss[index],maxgps)
                if gpss[index] > theta:

                    root_causes[split[index][0]] = {'score': gpss[index], 'n_ele': len(split[index][1]),
                                                'cuboid_layer': layer + 1}
            except:
                pass
        if maxgps<theta:
            break

    try:
        return sorted(root_causes.items(),key=lambda x:x[1]['score']*C+x[1]['n_ele']*x[1]['cuboid_layer'],reverse=True)[0][0]
    except:
        return None

