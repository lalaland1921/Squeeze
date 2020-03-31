# -*- ecoding: utf-8 -*-
# @ModuleName: main
# @Function: 
# @Author: Yuxuan Xi
# @Time: 2020/3/20 20:48

from Squeeze import Squeeze
import pandas as pd
import re
import os

digit = re.compile(r'\d+')

def precessfile(file):
    df=pd.read_csv(file)
    attrnum=len(df.columns)-2
    data={}
    #leafnum=len(df.index)

    for row in df.values:
        attr=[int(row[i+2][1:]) for i in range(attrnum)]
        data[tuple(attr)]=tuple(row[:2])
        #attr_vnum=sum(map(len,attr_value))
    return data

def evaluation(subdir,thre,theta,mode='auto'):
    attrs='abcdefgh'
    files=os.listdir(subdir)
    #prediction=[]
    truth = pd.read_csv(os.path.join(subdir, 'injection_info.csv'))
    truth = truth[['set', 'timestamp']].set_index('timestamp').T.to_dict()
    correct = 0
    for file in files:
        print('reading the file ' + file)
        timestamp = re.match(digit, file)
        if timestamp == None: continue
        timestamp = int(timestamp.group())
        data= precessfile(os.path.join(subdir, file))
        sqz=Squeeze(data,thre,theta,mode, attrs)
        attrnum,rtpre, root_causes=sqz.attrnum,sqz.rtpre,sqz.root_causes
        rttrue = []
        set1 = truth[timestamp]['set']
        for string in set1.split(';'):
            rt = [-1 for _ in range(attrnum)]
            for s in string.split('&'):
                attr = ord(s[0]) - ord('a')
                value = int(re.search(digit, s).group(0))
                rt[attr] = value
            rttrue.append(tuple(rt))
        if set(rttrue) == set(rtpre):
            correct += 1
        root_causes = list(set(root_causes))
        root_causes_str = ';'.join(root_causes)
        print('pre:', root_causes_str, 'true:', set1)
        truth[timestamp]['prediction'] = root_causes_str

    print('in the directory:%s,the number of correct prediction is:%d,crrect ratio is:%f' % (
    subdir, correct, correct / len(truth)))

    truth_pre = pd.DataFrame(truth).T
    truth_pre.to_csv(os.path.join(subdir, 'truth_prediction.csv'))

    #return correct,len(truth)


if __name__ == '__main__':
    #for subdir in os.listdir('B0'):
        #correct, total = evaluation(os.path.join('B0',subdir), 0.1, 0.9,'naive')
    subdir='B0/B_cuboid_layer_2_n_ele_2'
    evaluation(subdir, 0.1, 0.9,'naive')