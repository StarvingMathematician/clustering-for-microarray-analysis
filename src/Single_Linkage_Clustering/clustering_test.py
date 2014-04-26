'''
Created on Oct 2, 2013

@author: Jonathan A Simon
'''

if __name__ == '__main__':
    from single_linkage_clustering import *
    data_arr = get_data_arr()
    dist_list = get_dist_list(data_arr)
    clusters_list, level_list = get_clusters_list(data_arr.shape[0],dist_list)
    
    for clusters in clusters_list:
        print clusters