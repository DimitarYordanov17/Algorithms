# PCA (Principal Component Analysis) Python implementation. @DimitarYordanov17

# Short explanation:
# The main goal of the PCA algorithm is to represent an n-dimensional dataset into x-dimensional dataset, where x is smaller than n.
# In this program, I am representing a 2-dimensional dataset into an 1 dimensional axis (PC1).
# 1st dataset: 10 random points, characterised with x and y coordinates; 2nd dataset: 10 points from the 1st dataset, characterised just with distance from the center of the PC1 axis.
# (Sometimes the axis appears to be perpendicular to the direction (correlation) of the dataset, that is on micro-calculations)

import random
import numpy as np
import matplotlib.pyplot as plt
import sympy
import math

def generate_dataset():
    """
    Generate a 10-points dataset with positive/negative or approximately none correlation
    """
    points = []
    
    total_points = 10

    correlation_type = "positive" if random.randint(0, 1) else "negative"

    if correlation_type == "positive":
        starting_point = [random.randint(0, 2), random.randint(0, 2)]

        points.append(starting_point)

        last_point = starting_point

        for _ in range(total_points - 1):
            new_point = [last_point[0] + random.randint(0, 1), last_point[1] + random.randint(0, 1)]

            while new_point in points:
                new_point = [last_point[0] + random.randint(0, 1), last_point[1] + random.randint(0, 1)]

            points.append(new_point)

            last_point = new_point

    else: 
        starting_point = [random.randint(0, 2), random.randint(8, 10)]

        points.append(starting_point)

        last_point = starting_point

        for _ in range(total_points - 1):
            new_point = [last_point[0] + random.randint(0, 1), last_point[1] - random.randint(0, 1)]

            while new_point in points:
                new_point = [last_point[0] + random.randint(0, 1), last_point[1] - random.randint(0, 1)]

            points.append(new_point)

            last_point = new_point

    return points

def get_variance(dataset: list, axis: str):
    """
    Get variance of a specific axis (The axis parameter generalises the function instead of pre-extracting the specific axis coordinates)
    """
    index = 0 if axis == "x" else 1
    
    values = [i[index] for i in dataset]
    mean = sum(values) / len(values)
        
    distances = [(i - mean) ** 2 for i in values]
    variance = sum(distances) / len(distances)

    return round(variance)

def get_covariance(dataset: list):
    """
    Get covariance of a 2D dataset (Coordinates are mapped, so the dataset can be centered)
    """
    x_values = [i[0] for i in dataset]
    y_values = [i[1] for i in dataset]
    
    main_point = [sum(x_values) / len(x_values), sum(y_values) / len(y_values)]
    
    new_points_products = [(point[0] - main_point[0]) * (point[1] - main_point[1]) for point in dataset]
    
    covariance = sum(new_points_products) / len(new_points_products)
    
    return round(covariance)

def get_sigma_matrix(dataset: list):
    """
    Construct the sigma/covariance matrix using the predefined covariance/variance functions
    """
    sigma_matrix = [[0, 0], [0, 0]]
    
    covariance = get_covariance(dataset)
    
    sigma_matrix[0][0] = get_variance(dataset, "x")
    sigma_matrix[0][1] = covariance
    sigma_matrix[1][0] = covariance
    sigma_matrix[1][1] = get_variance(dataset, "y")
    
    return sigma_matrix
    
def get_longest_eigen_vector(sigma_matrix: list):
    """
    Get the eigen vectors of a transformation matrix (sympy did the work, but much indexing came as a consequence)
    """
    sympy_form_eigen_vectors = sympy.Matrix(sigma_matrix).eigenvects()
    eigen_vectors = [sympy_form_eigen_vectors[0][2][0].tolist(), sympy_form_eigen_vectors[1][2][0].tolist()]
        
    eigen_vector1 = [eigen_vectors[0][0][0], eigen_vectors[0][1][0]]
    eigen_vector2 = [eigen_vectors[1][0][0], eigen_vectors[1][1][0]]
        
    biggest_eigen_vector = eigen_vector1 if math.sqrt(abs(eigen_vector1[0]) ** 2 + abs(eigen_vector1[1]) ** 2) > math.sqrt(abs(eigen_vector2[0]) ** 2 + abs(eigen_vector2[1]) ** 2) else eigen_vector2
        
    return [int(round(i)) * 100 for i in biggest_eigen_vector]

def get_vector_projection(vector1, vector2):
    """
    Get vector1's projection onto vector2
    """    
    dot_product = vector1[0] * vector2[0] + vector1[1] * vector2[1]
    divisor = vector2[0] ** 2 + vector2[1] ** 2
    scalar = dot_product / divisor
    
    new_vector = [vector2[0] * scalar, vector2[1] * scalar]
    
    return new_vector

def get_corresponding_points_values(dataset: list, eigen_vector: list):
    """
    Get the new dataset, with points mapped to the main axis (vector)
    """
    points_values = []

    for point in dataset:
        new_coordinates = get_vector_projection(point, eigen_vector)
        points_values.append(new_coordinates)
        
    return points_values

def visualise_data(points: list, title, vector=[0, 0]):
    """
    Visualise everything using matplotlib.pyplot
    """
    if vector[0] or vector[1]:
        plt.quiver(0, 0, vector[0], vector[1], color="lightblue", angles="xy", scale_units="xy", scale=1, label="PC1 axis")
        plt.quiver(0, 0, -vector[0], -vector[1], color="lightblue", angles="xy", scale_units="xy", scale=1)
    
    for point in (points[:-1]):
        plt.scatter(point[0], point[1], color="darkcyan")
        
    plt.scatter(points[-1][0], points[-1][1], color="darkcyan", label="dataset point")
    plt.scatter(0, 0, color="aquamarine", label="center point")
    
    plt.legend(loc=1)
    plt.xlim(-15, 15)
    plt.ylim(-15, 15)
    plt.title(title)
    
    plt.show()   

def graph():
    """
    Demonstrate the whole transformation of datasets
    """
    starting_dataset = generate_dataset()
    sigma_matrix = get_sigma_matrix(starting_dataset)
    eigen_vector = get_longest_eigen_vector(sigma_matrix)
    one_d_dataset = get_corresponding_points_values(starting_dataset, eigen_vector)
    
    visualise_data(starting_dataset, "Starting dataset")
    visualise_data(starting_dataset, "Principal Component axis", eigen_vector)
    visualise_data(one_d_dataset, "Dataset represented on the PC1 axis", eigen_vector)
    
# Driver code:
graph()
