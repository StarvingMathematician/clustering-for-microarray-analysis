'''
Created on Apr 24, 2014

Assume that the metric being used is euclidean. This can be changed later.
 
Assume that the data comes in via a mxn matrix, where each row is one n-dimensional point.

Since the point sets in question will likely be small and high-dimensional,
store the distance mat rather than recomputing via an indexing structure.
 
Not using a k-d tree (for now).

Currently has O(n^3) complexity, vs n*log(n) (although I can't image how one could do better than n^2 * log(n))

Not using the point class yet. That comes next.

Change numeric arrays to boolean

@author: Jonathan Simon
'''

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances #output is easier to work with than 'pdist' 

class DBSCAN:
    '''
    classdocs
    '''

    def __init__(self, data, minPts=5, eps=.1):
        '''
        Constructor
        '''
        self.minPts = minPts
        self.eps = eps
        #self.dist_fun = dist_fun
        #self.points = self._transform_data(data)
        
        self.num_points = data.shape[0]
        self.num_features = data.shape[1]
        self.dist_mat = pairwise_distances(data)
        self.visited = np.zeros(self.num_points)
        self.noise = np.zeros(self.num_points) #what's the point of this?
        self.cluster_assignment = np.zeros(self.num_points) #cluster==0 --> cluster unassigned
        self.current_cluster = 1
        
    #def _transform_data(self, data):
    #     return map(Point, data)
         
    def _region_query(self, this_point):
        # I need to to be a list vs an array so that I can extend it while looping in "_expand_cluster"
        return np.where(self.dist_mat[this_point,:] < self.eps)[0].tolist() 
    
    def _expand_cluster(self,base_point,neighbors):
        self.cluster_assignment[base_point] = self.current_cluster #needs it's own case since it was already visited
        for this_point in neighbors:
            if not self.visited[this_point]:
                self.visited[this_point] = 1
                new_neighbors = self._region_query(this_point)
                if len(new_neighbors) >= self.minPts:
                    neighbors += new_neighbors
            if self.cluster_assignment[this_point] == 0:
                self.cluster_assignment[this_point] = self.current_cluster
                
    def cluster(self):
        for this_point in range(self.num_points):
            if not self.visited[this_point]:
                self.visited[this_point] = 1
                neighbors = self._region_query(this_point)
                if len(neighbors) < self.minPts:
                    self.noise[this_point] = 1
                else:
                    self._expand_cluster(this_point,neighbors)
                    self.current_cluster += 1
    
    ## Too many restrictions when we also account for number of clusters; just do this separately
    #def plot_clusters(self):
    #    if np.all(self.visited) == 1:
    #        if self.num_features == 2:
    #            pt.scatter()
    #        else:
    #            #later change this to use t-SNE
    #            raise Exception("The data needs to be 2D for plotting to work")
    #        
    #    else:
    #        raise Exception("You need to first call 'DBSCAN.cluster()' to perform the clustering.")


        
#class Point:
#    
#    def __init__(self, datum):
#        '''
#        Constructor
#        '''
#        self.value = datum
#        self.visited = False
#        self.noise = None
    
        