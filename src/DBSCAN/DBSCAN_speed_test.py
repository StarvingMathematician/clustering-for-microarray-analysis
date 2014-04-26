'''
Created on Apr 25, 2014

Comparing DBSCAN to Fast_DBSCAN

CONCLUSION: "Fast_DBSCAN" is 1-2 order of magnitude *SLOWER*???

Whatever, I'll stick with the old/simple/brute-force way of doing things for now.
Even if I do get the k-d trees working well, they won't help for the small-sample/large-dim
cases that I'll almost certainly be looking at.

(Might try rewriting the code later to utilize 'KDTree.query_pairs'. It will
certainly speed things up somewhat, although I'm not sure by how much.) 

@author: Jonathan Simon
'''

from sklearn.datasets import make_blobs
import matplotlib.pyplot as plt
from DBSCAN import DBSCAN
from Fast_DBSCAN import Fast_DBSCAN
from time import time

if __name__ == '__main__':
    data = make_blobs(n_samples=100, n_features=2, centers=[[.2,.3],[.7,.6]], cluster_std=.1) #testing plotting mechanics
    X = data[0]; labels=data[1]
    
    start1 = time()
    My_DBSCAN = DBSCAN(X, minPts=5, eps=.1) 
    My_DBSCAN.cluster()
    print "DBSCAN time:", time()-start1
    
    start2 = time()
    My_Fast_DBSCAN = Fast_DBSCAN(X, minPts=5, eps=.1) 
    My_Fast_DBSCAN.cluster()
    print "Fast_DBSCAN time:", time()-start2
    
    '''
    my_colors1 = []
    for pred1 in My_DBSCAN.cluster_assignment:
        if pred1==0:
            my_colors1.append('yellow')
        elif pred1==1:
            my_colors1.append('blue')
        elif pred1==2:
            my_colors1.append('red')
    
    my_colors2 = []
    for pred2 in My_Fast_DBSCAN.cluster_assignment:
        if pred2==0:
            my_colors2.append('yellow')
        elif pred2==1:
            my_colors2.append('blue')
        elif pred2==2:
            my_colors2.append('red')
            
    plt.subplot(121)
    plt.scatter(X[:,0],X[:,1],c=my_colors1,s=100,alpha=.5)
    plt.subplot(122)
    plt.scatter(X[:,0],X[:,1],c=my_colors2,s=100,alpha=.5)
    plt.show()
    '''