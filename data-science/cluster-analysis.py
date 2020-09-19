# K-means and Hierarchial clustering Python implementation. @DimitarYordanov17

import numpy as np
import matplotlib.pyplot as plt

def get_random_dataset():
    """
    Generate random 20 points arranged into 2 to 4 cluster-like groups
    """
    points = []
    total_clusters = np.random.randint(2, 5)
    clusters_main_points = [(np.random.randint(0, 21), np.random.randint(0, 21)) for _ in range(total_clusters)]
    
    for i in range(20):
        current_cluster = np.random.randint(0, total_clusters)
        new_point = (clusters_main_points[current_cluster][0] + np.random.choice([-1, 1]), clusters_main_points[current_cluster][1] + np.random.choice([-1, 1])) 
        while new_point in points:
            new_point = (clusters_main_points[current_cluster][0] + np.random.choice([-1, 1]), clusters_main_points[current_cluster][1] + np.random.choice([-1, 1])) 
        points.append(new_point)
        clusters_main_points[current_cluster] = new_point
            
    return points, total_clusters


def get_structured_dataset():
    """
    Generate points arranged into 2 to 4 well structured and distanced clusters
    """
    points = []
    total_clusters = np.random.randint(2, 5)
    clusters_main_points = []
    
    if total_clusters == 2:
        if np.random.randint(0, 2):
            clusters_main_points = [(np.random.randint(-5, 6), np.random.randint(-5, 6)), (np.random.randint(15, 26), np.random.randint(15, 26))]
        else:
            clusters_main_points = [(np.random.randint(-5, 6), np.random.randint(15, 26)), (np.random.randint(15, 26), np.random.randint(-5, 6))]
            
        last_point = clusters_main_points[0]
        
        for _ in range(6):
            new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
            while new_point in points:
                new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
            points.append(new_point)
            last_point = new_point
            
        last_point = clusters_main_points[1]
        
        for _ in range(6):
            new_point = last_point[0] + np.random.choice([-1, 1]), last_point[1] + np.random.choice([-1, 1])
            while new_point in points:
                new_point = last_point[0] + np.random.choice([-1, 1]), last_point[1] + np.random.choice([-1, 1])
            points.append(new_point)
            last_point = new_point
            
            
    elif total_clusters == 3:
        clusters_main_points = [(np.random.randint(-5, 6), np.random.randint(-5, 6)), (np.random.randint(10, 21), np.random.randint(15, 26)), (np.random.randint(20, 31), np.random.randint(-5, 6))]
        
        for i in range(2):
            last_point = clusters_main_points[i]
            for j in range(6):
                new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
                while new_point in points:
                    new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
                points.append(new_point)
                last_point = new_point
            
        last_point = clusters_main_points[2]
        
        for _ in range(6):
            new_point = last_point[0] + np.random.choice([-1, 1]), last_point[1] + np.random.choice([-1, 1])
            while new_point in points:
                new_point = last_point[0] + np.random.choice([-1, 1]), last_point[1] + np.random.choice([-1, 1])
            points.append(new_point)
            last_point = new_point
        
    elif total_clusters == 4:
        clusters_main_points = [(np.random.randint(-5, 6), np.random.randint(-5, 6)), (np.random.randint(15, 31), np.random.randint(15, 31)), (np.random.randint(-5, 6), np.random.randint(15, 31)), (np.random.randint(15, 31), np.random.randint(-5, 6))]
        
        for i in range(4):
            last_point = clusters_main_points[i]
            for j in range(6):
                new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
                while new_point in points:
                    new_point = last_point[0] + np.random.choice([0, 1]), last_point[1] + np.random.choice([0, 1])
                points.append(new_point)
                last_point = new_point

    return points, total_clusters

def get_distance(point1: tuple, point2: tuple):
    """
    Get the euclidean distance between 2 points
    """
    
    return np.sqrt(((point2[0] - point1[0]) ** 2) + ((point2[1] - point1[1]) ** 2))

def k_means(dataset: list, k: int, iterations: int):
    """
    Perform k-means clustering on the input dataset and return a point-cluster dictionary
    """
    cluster_main_points_list = []
    points_and_clusters_list = []
    
    cluster_main_points = k_means_init_points(dataset, k)
    cluster_main_points_list.append(cluster_main_points)
    
    
    for i in range(iterations):
        points_and_clusters = k_means_find_belongings(cluster_main_points, dataset)
        points_and_clusters_list.append(points_and_clusters)
        cluster_main_points = k_means_reorder(cluster_main_points, points_and_clusters)
        cluster_main_points_list.append(cluster_main_points)
        
    return points_and_clusters, cluster_main_points_list, points_and_clusters_list

def k_means_init_points(dataset: list, k: int):
    cluster_points = []

    for _ in range(k):
        new_point = (np.random.randint(0, 21), np.random.randint(0, 21))
        while new_point in dataset or new_point in cluster_points:
            new_point = (np.random.randint(0, 21), np.random.randint(0, 21))
        cluster_points.append(new_point)
        
    return cluster_points

def k_means_find_belongings(cluster_main_points: list, dataset: list):
    points_and_clusters  = dict()
    
    for point in dataset:
        smallest_distance = 1000
        cluster = 0
        
        for i in range(len(cluster_main_points)):
            current_cluster_point = cluster_main_points[i]
            distance = get_distance(point, current_cluster_point)
            
            if distance < smallest_distance:
                smallest_distance = distance
                cluster = i
                
        points_and_clusters[point] = cluster
    
    return points_and_clusters

def k_means_reorder(cluster_main_points, points_and_clusters):
    new_cluster_points = []
    
    for index, cluster_point in enumerate(cluster_main_points):
        cluster_belongings = dict(filter(lambda x: x[1] == index, points_and_clusters.items()))
        if cluster_belongings:
            avg_x_sum, avg_y_sum = sum([i[0] for i in cluster_belongings.keys()]), sum([i[1] for i in cluster_belongings.keys()])
            avg_x, avg_y = avg_x_sum / len(cluster_belongings), avg_y_sum / len(cluster_belongings)
            new_cluster_points.append((avg_x, avg_y))
        else:
            new_cluster_points.append(cluster_point)
        
    return new_cluster_points

def hierarchial_clustering(dataset: list, k: int):
    """
    Perform hierarchial clustering on the input dataset and return a point-cluster dictionary
    """
    points_and_clusters = {point: cluster + 1 for cluster, point in enumerate(dataset)}
    iteration_counter = 0
    
    for i in range(len(points_and_clusters), k, -1):
        closest_points = [((0, 0), 0), ((0, 0), 0)]
        smallest_distance = 99999
        
        for first_point, first_cluster in points_and_clusters.items():           
            current_closest_points = [(first_point, first_cluster), ((0, 0), 0)]
            current_smallest_distance = 99999
            
            for second_point, second_cluster in points_and_clusters.items():          
                if first_cluster != second_cluster:
                    current_distance = get_distance(first_point, second_point)
                    
                    if current_distance < current_smallest_distance:
                        current_smallest_distance = current_distance
                        current_closest_points[1] = second_point, second_cluster
                
            if current_smallest_distance < smallest_distance:
                smallest_distance = current_smallest_distance
                closest_points = current_closest_points
        
        smaller_cluster = min(closest_points[0][1], closest_points[1][1])
        bigger_cluster = max(closest_points[0][1], closest_points[1][1])
        
        points_and_clusters[closest_points[0][0]] = smaller_cluster
        points_and_clusters[closest_points[1][0]] = smaller_cluster
        
        for point, cluster in points_and_clusters.items():
            if cluster >= bigger_cluster:
                points_and_clusters[point] -= 1
        
        iteration_counter += 1
        
        # Remove the code below (without the return part)if you want just the algorithm, without the visualisation
        if iteration_counter < 4:
            visualise(points_and_clusters, f"Iteration №{iteration_counter}", [])
            
         
    return points_and_clusters

def hierarchial_clustering_visualise():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Hierarchial clustering ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    dataset, k = get_structured_dataset()
    
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ First three iterations ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("Our goal is to combine every cluster (point) with its closest.")
    
    final_points_and_clusters = hierarchial_clustering(dataset, k)
    
    print("Repeat these iterations until you reduce the clusters to k-number")
    
    visualise(final_points_and_clusters, "Resulting clusters", [])
    
    
def k_means_visualise():
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ K-means ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    dataset, k = get_structured_dataset()
    dataset_for_visualisation = {i: "initial" for i in dataset}
    points_and_clusters, cluster_main_points_list, points_and_clusters_list = k_means(dataset, k, 3)
    visualise(dataset_for_visualisation, "Starting dataset", [])
    visualise(dataset_for_visualisation, "Random k-points", cluster_main_points_list[0])
    
    visualise(points_and_clusters_list[0], "1. Assign points to their closest cluster point", cluster_main_points_list[0])
    visualise(points_and_clusters_list[0], "2. Move cluster point to the mean one ", cluster_main_points_list[1])
    
    print("Repeat steps 1 and 2 several times (In this current case - 3)")
    
    visualise(points_and_clusters, "Resulting clusters", [])   
    
def visualise(dataset: dict, title: str, others: list):
    clusters = {cluster for cluster in dataset.values()}
    color_map = {0: 'rosybrown',  1: 'goldenrod', 2: 'mediumturquoise', 3: 'mediumpurple',
                4: 'lightcoral', 5: 'cornsilk', 6: 'azure', 7: 'rebeccapurple',
                8: 'indianred', 9: 'gold', 10: 'lightcyan', 11: 'blueviolet',
                12: 'brown', 13: 'lemonchiffon', 14:'paleturquoise', 15:'indigo',
                16: 'mistyrose', 17: 'beige', 18: 'aqua', 19: 'black',
                20: 'chocolate', 21: 'chartreuse', 22: 'steelblue', 23: 'hotpink',
                24: 'blue', "initial": "yellowgreen"}
    
    for cluster in clusters:
        plt.scatter(-21, -21, color = color_map[cluster], label=f"Cluster {cluster}")
    
    for point, cluster in dataset.items():
        plt.scatter(point[0], point[1], color=color_map[cluster])
    
    for index, point in enumerate(others):
        plt.scatter(point[0], point[1], color=color_map[index])
        plt.scatter(point[0] - 0.5, point[1] - 0.5, color="black")
    
    plt.title(title)
    
    if len(clusters) < 8:
        plt.legend()
        
    plt.xlim(-10, 35)
    plt.ylim(-10, 35)
    
    plt.show() 
    
# Driver code:

k_means_visualise()
hierarchial_clustering_visualise()
