'''
Created on Oct 1, 2013

@author: Jonathan A Simon
'''

#Reads in a nondelimited text file whose rows are data points, and returns it as an array. Outputs an exception if it fails.
def get_data_arr():
    import numpy as np
    try:
        filename = raw_input("What is the name of the data file? ")
        data_arr = np.loadtxt(filename)
        return data_arr
    except:
        raise Exception("That is not a valid data file!")

#Takes an array of data points an input. Returns a sorted list of distances between them.  
def get_dist_list(data_arr):
    import numpy as np
    from operator import itemgetter
    num_points = data_arr.shape[0]
    dist_list = []
    for i in range(1,num_points):
        for j in range(i):
            euc_dist = np.linalg.norm(data_arr[i,:]-data_arr[j,:])
            dist_list.append(({i,j},euc_dist))
    
    dist_list = sorted(dist_list,key=itemgetter(1))
    print
    return dist_list

#Takes the number of data points and the list of distances between them as input.
#Returns a list of successively coarser clusterings, and the list of distances ("levels") associated with those clusterings.
#(We're assuming that no two points are exactly the same distance apart.) 
def get_clusters_list(num_points,dist_list):
    #clusters_list is initialized as a list whose 1 element is a tuple of all singleton sets
    clusters_list = [[{n} for n in range(num_points)]]
    level_list = [0]
    for val in dist_list:
        point_pair = val[0]
        dist_between = val[1]
        important_clusters = []
        for idx,cluster in enumerate(clusters_list[-1]): #loop through all previous clusters (this can be made more efficient using breaks)
            if len(point_pair & cluster) > 0:
                important_clusters.append(idx)
        if len(important_clusters) == 2: #if two closest points belonged to two different clusters
            level_list.append(dist_between) #add the distance between them to the level_list
            #make the new clusters the same as before, only merge the two important_clusters
            new_clusters = list(clusters_list[-1]) #using list() ensures that we're actually making a copy, not just a new reference
            new_clusters[important_clusters[0]] = new_clusters[important_clusters[0]] | new_clusters[important_clusters[1]]
            del new_clusters[important_clusters[1]]
            clusters_list.append(new_clusters)
        if len(clusters_list[-1]) == 1: #if all points are now in a single cluster, we're done
            break
    
    return clusters_list, level_list
            

