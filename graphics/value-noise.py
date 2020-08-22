# Value Noise algorithm Python implementation. @DimitarYordanov17
import random
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

# Matplotlib and numpy are used just for the rendering, if you just want to see the value matrix itself, do the following:
# 1.Remove the last line of the fancy_visualise function 2.Call fancy_visualise() 3.Call the normal visualisation function

class ValueNoise:
    """Main class to work with"""
    def __init__(self, grid_width, grid_length):
        self.grid_width = grid_width
        self.grid_length = grid_length
        
        self.grid = np.array([[0 for i in range(grid_length + 1)] for j in range(grid_width + 1)]) # Main grid, numpy array
        self.max_points = ((self.grid_length + 10) / 10) * ((self.grid_width + 10) / 10) # Calculating the smaller grid's corners
        
        for y in range(0, grid_width + 1, 10): # Fill the smaller grid's corner points, step is 10
            for x in range(0, grid_length + 1, 10):
                self.grid[y][x] = random.randint(0, 256)
               
    def generate_value(self, y, x):
        if y % 10 == 0 and x % 10 == 0: # Trying to get interpolation of main points
            print("Already ocupied")
            return
            
        if (y < 0 or y > self.grid_width) or (x < 0 or x > self.grid_length): # Out of boundaries
            print("Out of boundaries") 
            return
        
        
        if y % 10 == 0 and y != 0: # Corner elements
            y -= 1
        if x % 10 == 0 and x != 0:
            x -= 1
        
        
        # Some sick math below
        
        y_decimal = (y // 10) * 10
        x_decimal = (x // 10) * 10
        
        upper_left_coordinates, upper_right_coordinates = (y_decimal, x_decimal), (y_decimal, x_decimal + 10)
        lower_left_coordinates, lower_right_coordinates = (y_decimal + 10, x_decimal), (y_decimal + 10, x_decimal + 10)
        
        upper_left_value = self.grid[upper_left_coordinates[0]][upper_left_coordinates[1]]
        upper_right_value = self.grid[upper_right_coordinates[0]][upper_right_coordinates[1]]
        
        lower_left_value = self.grid[lower_left_coordinates[0]][lower_left_coordinates[1]]
        lower_right_value = self.grid[lower_right_coordinates[0]][lower_right_coordinates[1]]
        
        x1, x2 = upper_left_coordinates[1], upper_right_coordinates[1]
        y1, y2 = upper_left_coordinates[0], lower_right_coordinates[0]
        
        divisor = (x2 - x1) * (y2 - y1)
        
        part1 = (((x2 - x) * (y2 - y)) / divisor) * upper_left_value
        part2 = (((x - x1) * (y2 - y)) / divisor) * upper_right_value
        part3 = (((x2 - x) * (y - y1)) / divisor) * lower_left_value
        part4 = (((x - x1) * (y - y1)) / divisor) * lower_right_value
        
        result = part1 + part2 + part3 + part4
        
        return round(result)
        
    def visualise(self): # Visualise the grid normally
        for y in self.grid:
            for x in y:
                if x == 0:
                    print(" 0 ", end="")
                else:
                    print(x, end=" ")
            print()
            
    def fancy_visualise(self): # Fancy visualese, a.k.a render
        for y in range(0, self.grid_width + 1):
            for x in range(0, self.grid_length + 1):
                if y % 10 == 0 and x % 10 == 0:
                    continue
                self.grid[y][x] = self.generate_value(y, x)
        
        imgplot = plt.imshow(value_noise.grid)

# Driver code:

# Use only {0, 10, 20, 30... 1000} values for arguments (x % 10 == 0)
value_noise = ValueNoise(150, 150)

value_noise.fancy_visualise()