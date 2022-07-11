import numpy as np

def cluster_points(v, E=0.1, N=3):
    res = []
    points_n = [0] * len(v)

    # iterate over each point
    for i in range(0, len(v)):
        n = 0

        # memoized check
        if points_n[i] >= N-1:
            res.append(v[i])
            continue

        # compare to other points
        for j in range(i, len(v)):
            if j == i:
                continue
            net_v = v[i] - v[j]
            #print(type(net_v))
            net_s = np.linalg.norm(net_v)
            # if the points are within threshold distance
            if net_s <= E:
                n += 1
                points_n[j] += 1
        
        # if this point meets neighbor threshold
        if n >= N-1:
            res.append(v[i])
        
    return res

if __name__ == '__main__':
    my_points = [np.array([0,0]), np.array([1.0,0]), np.array([0,0.1]), np.array([0.5,0]), np.array([0.5,0.05]), np.array([0.48,0])]
    my_result = cluster_points(my_points, E=0.1, N=3)
    print(my_result)