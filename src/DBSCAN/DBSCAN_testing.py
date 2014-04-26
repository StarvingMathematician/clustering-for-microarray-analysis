'''
Created on Apr 25, 2014

Testing DBSCAN

@author: Jonathan Simon
'''

import numpy as np
from sklearn.datasets import make_blobs
from DBSCAN import DBSCAN
import matplotlib.pyplot as plt

if __name__ == '__main__':
    #X = make_blobs(300, 2, 3) #3 2D blobs, each with 100 points
    data = make_blobs(n_samples=100, n_features=2, centers=np.array([[.2,.3],[.7,.6]]), cluster_std=.1) #testing plotting mechanics
    X = data[0]; actual_labels=data[1]
    My_DBSCAN = DBSCAN(X, minPts=5, eps=.1) 
    My_DBSCAN.cluster()
    #print My_DBSCAN.cluster_assignment
    my_colors = []
    for label in My_DBSCAN.cluster_assignment:
        if label==0:
            my_colors.append('yellow')
        elif label==1:
            my_colors.append('blue')
        elif label==2:
            my_colors.append('red')
    plt.scatter(X[:,0],X[:,1],c=my_colors,s=100,alpha=.7)
    plt.show()
    