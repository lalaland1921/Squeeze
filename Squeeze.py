# -*- ecoding: utf-8 -*-
# @ModuleName: main
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/3/8 18:39



import numpy as np

from filter_normal.filter import filter
from clustering.density_cluster import den_cluster
from top_down_location.top_down import top_down
import warnings




class Squeeze(object):
    def __init__(self,data:dict,thre:float=0.2,theta:float=0.9,mode:str='auto',attrs="abcdef"):
        if data==None:
            warnings.warn("the data is empty!")
        self.attrnum=len(list(data.keys())[0])
        attr_value = [set() for _ in range(self.attrnum)]
        for attr,d in data.items():
            for i in range(self.attrnum):
                attr_value[i].add(attr[i])
        self.attr_vnum = sum(map(len, attr_value))
        self.data=data
        self.thre=thre
        self.theta=theta
        self.mode=mode
        self.attrs=attrs

        self.idata = filter(self.data, self.thre, self.mode)
        self.clusters = den_cluster(self.idata)
        self.C = -np.log(len(self.clusters) * len(self.idata) / len(self.data)) / np.log(self.attr_vnum) * self.attr_vnum
        self.root_causes = []
        self.rtpre = []
        rtpre1=[]
        for cluster in self.clusters:
            rt_cause = top_down(cluster, self.data, self.attrnum, self.theta, self.C)
            if not rt_cause:continue
            rtpre1.append(rt_cause)
        rtpre1=sorted(rtpre1,key=lambda x:sum(np.array(x)!=-1))
        for i in range(len(rtpre1)):
            rt_cause=rtpre1[i]
            flag=False
            for tmp in self.rtpre:
                if all(np.array(rt_cause)[np.array(tmp)!=-1]==np.array(tmp)[np.array(tmp)!=-1]):
                    flag=True
                    break
            if flag==False:
                self.rtpre.append(rt_cause)
                rt = []
                for i in range(self.attrnum):
                    if rt_cause[i] != -1:
                        rt.append(self.attrs[i] + '=' + self.attrs[i] + str(rt_cause[i]))
                rt_cause = '&'.join(rt)
                self.root_causes.append(rt_cause)








