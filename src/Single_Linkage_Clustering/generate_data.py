'''
Created on Oct 2, 2013

@author: Jonathan A Simon
'''

#Generates a disk full of points all greater than min_dist apart.
#Runtime: ~1min with max_failures = 100, ~8min with max_failures = 1000
def make_sparse_disk(center,radius,min_dist,initial_side):
    import numpy as np
    from random import uniform
    cx = center[0]; cy = center[1] 
    if initial_side == "left":
        disk_points = np.array([[cx-radius,cy]])
    elif initial_side == "right":
        disk_points = np.array([[cx+radius,cy]])
    max_failures = 1000
    num_failures = 0
    #Keep generating points until we've unsuccessfully generated max_failures points in a row
    while num_failures < max_failures:
        #Generate a point lying within the square circumscribing our desired circle,
        #and eliminate it (i.e. "continue") if it does not lie within the circle itself.
        new_point = np.array([uniform(cx-radius,cx+radius),uniform(cy-radius,cy+radius)])
        if (new_point[0]-cx)**2 + (new_point[1]-cy)**2 > radius**2:
            continue
        #If the new_point is at least min_dist away from every other point, keep it
        #and reset the num_failures counter. Otherwise, add 1 to our num_failures counter.
        bad_point = False
        for old_point in disk_points:
            euc_dist = np.linalg.norm(new_point-old_point)
            if euc_dist <= min_dist:
                bad_point = True
                num_failures += 1
                break
        if not bad_point:
            disk_points = np.vstack((disk_points,new_point))
            num_failures = 0
                                    
    return disk_points

#Saves the points comprising each disk to a separate text file
def write_to_txt(disk_points1,disk_points2):
    from numpy import savetxt
    filename1 = "/Users/Macbook/Documents/Git_Repos/hierarchical-density-clustering/disk1.txt"
    filename2 = "/Users/Macbook/Documents/Git_Repos/hierarchical-density-clustering/disk2.txt"
    savetxt(filename1, disk_points1)
    savetxt(filename2, disk_points2)

#Saves the points comprising each disk to a separate text file
def plot_points(data_points):
    import matplotlib.pyplot as plt
    plt.plot(data_points[:,0],data_points[:,1],'o')
    plt.show()

#Both clusters have a density of 20pts/radius. And although they are only .5 apart,
#every pair of points in the second cluster is MORE than .5 apart. So using Ayasdi's
#single-linkage method, will either result in only discovering the left cluster, or
#incorrectly grouping both clusters together.
if __name__ == '__main__':
    from numpy import vstack
    disk_points1 = make_sparse_disk([0,0],1,.05,"right") 
    disk_points2 = make_sparse_disk([11.5,0],10,.5,"left")
    write_to_txt(disk_points1,disk_points2)
    plot_points(vstack((disk_points1,disk_points2)))
    
    
    
    