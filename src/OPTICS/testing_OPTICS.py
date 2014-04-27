'''
Created on Apr 26, 2014

Checking that OPTICS works

The 'cluster_std' parameter of sklearn's 'make_blobs' is broken; just run the function twice, separately

Hooray, everything work! (It's terribly slow, though.)

@author: Jonathan Simon
'''

import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from OPTICS import OPTICS
from random import shuffle

if __name__ == '__main__':
    #blob_means = [[0,0], [.7,.7], [1.3,.7], [.7,1.3], [1.3,1.3]]
    #blob_devs = np.array([.5, .1, .1, .1, .1])
    #data = make_blobs(n_samples=250, n_features=2, centers=blob_means, cluster_std=blob_devs) #testing plotting mechanics
    #X = data[0]; y=data[1]
    
    #X1, y1 = make_blobs(n_samples=50, n_features=2, centers=[[0,0]], cluster_std=.2)
    X1, y1 = make_blobs(n_samples=300, n_features=2, centers=[[-.5,0]], cluster_std=.4)
    #X2, y2 = make_blobs(n_samples=200, n_features=2, centers=[[.7,.7],[1.3,.7],[.7,1.3],[1.3,1.3]], cluster_std=.1)
    X2, y2 = make_blobs(n_samples=150, n_features=2, centers=[[.7,.7],[.4,1.3],[1,1.3]], cluster_std=.1)
    X = np.concatenate([X1,X2],0)
    y = np.concatenate([y1,y2])
    # Randomly permute the concatenated arrays, for good measure
    new_inds = range(len(y)) 
    shuffle(new_inds)
    X = X[new_inds,:]
    y = y[new_inds]
    
    My_OPTICS = OPTICS(X, minPts=20, eps=.5) 
    My_OPTICS.cluster()
    # Order distances by points
    ordered_dists = My_OPTICS.reachability_dist[My_OPTICS.ordered_points]
    
    plt.subplot(211)
    plt.scatter(X[:,0],X[:,1],s=50,alpha=.8)
    plt.subplot(212)
    plt.vlines(x=range(X.shape[0]),ymin=0,ymax=ordered_dists,lw=2)
    plt.ylim([0,max(ordered_dists)])
    plt.show()
    