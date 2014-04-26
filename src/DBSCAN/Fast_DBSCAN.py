'''
Created on Apr 25, 2014

Improves upon DBSCAN (both memory and runtime) by utilizing k-d trees

scipy's "KDTree" query requires a Minkowskian metric. That means I'll need to write my own, eventually.

scipy's "KDTree" function has parameters that I may want to tweak:
1) default "leafsize" of 10 after which brute force is used; seems too low for general purposes
2) utilizing the parameter for "approximate" nearest neighbor search could speed things up 

Note:
This algorithm offers only marginal runtime improvements when the dimension is very high (20 dims is
already pushing it). As discussed in the scipy manual, efficiently queries neighborhood in high dimensions is 
a largely unsolved problem, and even scipy's "cKDTree" heuristic offers only minimal improvements.
Similarly, the k-d trees wiki page mentions that a k-d tree will only provide a meaningful speedup if:
num_samples >> 2^(num_features) 

@author: Jonathan Simon
'''

import numpy as np
from scipy.spatial import KDTree

class Fast_DBSCAN:
    '''
    classdocs
    '''

    def __init__(self, data, minPts=5, eps=.1):
        '''
        Constructor
        '''
        self.minPts = minPts
        self.eps = eps
        
        self.data = data #necessary for KDTree queries
        self.num_points = data.shape[0]
        self.num_features = data.shape[1]
        #self.dist_mat = pairwise_distances(data)
        #self.kd_tree = KDTree(data) #consider changing the default "leafsize" parameter
        self.kd_tree = KDTree(data, self.num_points/8)#self.num_points**.5)
        self.visited = np.zeros(self.num_points)
        self.noise = np.zeros(self.num_points) #what's the point of this?
        self.cluster_assignment = np.zeros(self.num_points) #cluster==0 --> cluster unassigned
        self.current_cluster = 1
        
    def _region_query(self, this_point):
        # Needs to to be a list vs an array so that I can extend it while looping in "_expand_cluster"
        #return np.where(self.dist_mat[this_point,:] < self.eps)[0].tolist()
        return self.kd_tree.query_ball_point(self.data[this_point,:],self.eps)
    
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
                    