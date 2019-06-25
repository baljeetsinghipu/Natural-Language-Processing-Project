# -*- coding: utf-8 -*-
"""
Created on Wed Mar 20 15:30:13 2019

@author: Baljeet Singh
"""
from collections import Counter
def droppedRequests(requestTime):

    requestTime.sort()
    seta = set(requestTime)
    dict1 = {}
    count1 = total = step = 0
    initial_10 = requestTime[0]//10
    initial_60 = requestTime[0]//60
    dict1 = Counter(requestTime)
    flag=0
    # for val in seta:
    #     dict1[val] = requestTime.count(val)
    
    for key in sorted(dict1):
        value = dict1[key]
        if value > 3:
            count1 += (value - 3)
        
        

        if key//10 != initial_10:
            if step > 20:
                count1 += (step - 20)
            
            initial_10 = key // 10
            total += step
            step = 0
            flag=1
        
        if key//60 != initial_60:
            if total > 60:
                count1 += (total - 60)
            
            initial_60 = key // 60
            total = 0
#            flag=1
        
            
        if(flag==0):
            step += value
        
        flag=0
    
    if step > 20:
        count1 += step-20
        print("ssdd")
        print(step)
    if total > 60:
        count1 += total - 60
    return count1


    
        


#a=[1,1,1,1,2,2,2,3,3,3,4,4,4,11,11,11,6,6,6,5,5,5]
#a=[1,1,1,2,2,2,3,3,4,5,6,6,6,7,7,8,8,8,8]
#a= [1, 1, 1, 1, 2, 2, 2, 3, 3, 3, 3, 4, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 9, 10, 10, 11, 11, 11, 11, 11, 11, 12, 12, 12, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 14, 16, 16, 16, 16, 16, 16, 17, 17, 17, 18, 18, 18, 18, 18, 18, 18, 18, 19, 19, 19, 19, 19, 19, 19, 20, 20, 20, 20, 20]
a=[1,1,1,2,2,2,2,3,3,3,3,4,4,4,5,5,5,6,6,7,7,7,7,7,7,7]
print(len(a))
print(droppedRequests(a))
    