'''
Created on Apr 26, 2014

Basic OPTICS algorithm

Current 'region_query' method is incredibly slow/redundant;
try to combine it with 'get_core_distance' (use a k-d tree) 

@author: Jonathan Simon
'''

import numpy as np
from sklearn.metrics.pairwise import pairwise_distances #output is easier to work with than 'pdist'
#from blist import blist #it works fine, ignore the error 
from blist import sortedlist #consider simply using a heap from the 'heapq' module

class OPTICS:
    '''
    classdocs
    '''

    def __init__(self, data, minPts=20, eps=None):
        '''
        Constructor
        '''
        
        self.minPts = minPts
        # Set default value of 'eps' to be large enough to engulf all points;
        # this method assumes the Euclidean metric:
        if not isinstance(eps, int):
            dim_ranges = np.amax(data,0) - np.amin(data,0)
            self.eps = sum(dim_ranges**2)
        else:
            self.eps = eps
        
        self.num_points = data.shape[0]
        self.num_features = data.shape[1]
        self.dist_mat = pairwise_distances(data)
        self.visited = np.zeros(self.num_points)
        self.noise = np.zeros(self.num_points) #what's the point of this?
        self.cluster_assignment = np.zeros(self.num_points) #cluster==0 --> cluster unassigned
        self.current_cluster = 1
        
        self.reachability_dist = -np.ones(self.num_points)
        self.ordered_points = [] #ordered by visitation order
        #self.seeds = blist([]) #ordered by reachability distance (i.e value)
        self.seeds = sortedlist([], key=lambda x: x[1]) #ordered by reachability distance (i.e value)
        self.core_dist = map(self._get_core_distance,range(self.num_points)) #compute core_dist ahead of time for simplicity
    
    def _region_query(self, this_point): #MAKE THIS SUCK LESS
        return np.where(self.dist_mat[this_point,:] < self.eps)[0] #don't need to convert to list
    
    def _get_core_distance(self, this_point): #incredibly inefficient
        neighbors = np.where(self.dist_mat[this_point,:] < self.eps)[0]
        if len(neighbors) < self.minPts:
            return -1
        else: #check this bit
            neighbor_dists = sorted(self.dist_mat[this_point,neighbors])
            return neighbor_dists[self.minPts-1]
            #ordered_neighbors = neighbors[neighbor_dists.argsort()]
            #return ordered_neighbors[:self.minPts].tolist()
    
    #def _update(self, this_point, neighbors, seeds):
    def _update(self, this_point, neighbors):
        for neighbor in neighbors:
            if not self.visited[neighbor]:
                new_reachability_dist = max(self.core_dist[this_point],self.dist_mat[this_point,neighbor])
                if self.reachability_dist[neighbor] == -1: #'neighbor' not yet in 'seeds'
                    self.seeds.add((neighbor,new_reachability_dist))
                    self.reachability_dist[neighbor] = new_reachability_dist
                else: #'neighbor' is in 'seeds'; check for improved position
                    if new_reachability_dist < self.reachability_dist[neighbor]:
                        self.seeds.remove((neighbor,self.reachability_dist[neighbor])) #remove old val; finding floats might be tricky
                        self.seeds.add((neighbor,new_reachability_dist)) #add new val
                        self.reachability_dist[neighbor] = new_reachability_dist
                    
    def cluster(self):
        for this_point in range(self.num_points):
            if not self.visited[this_point]:
                self.visited[this_point] = 1
                neighbors = self._region_query(this_point) #######
                self.ordered_points.append(this_point)
                #seeds = blist([])
                #seeds = sortedlist([], key=lambda x: x[1])
                if self.core_dist[this_point] != -1: #if it as a defined core dist
                    #self._update(this_point, neighbors, seeds)
                    self._update(this_point, neighbors)
                    while self.seeds:
                        new_point,new_dist = self.seeds.pop(0)
                        self.visited[new_point] = 1
                        new_neighbors =  self._region_query(new_point) #######
                        self.ordered_points.append(new_point)
                        if self.core_dist[new_point] != -1:
                            self._update(new_point, new_neighbors)
                        
                        
    