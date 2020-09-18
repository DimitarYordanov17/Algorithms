# Graphics algorithms

### A graphic algorithm is a very broad concept, but the main purpose is to generate some form of an image or just do some operations on it.

## 1. Value Noise

Value noise is an algorithm used in graphics and many other fields (which use randomness as a tool), similar to Perlin Noise.
The main concept of the algorithm is to generate a random number based on some factors. It is used because of its smoothness, mainly in two dimensions.

An image (gray scale) generated through the Value Noise algorithm, notice how everything looks so smooth:


![web-example](./resources/images/value-noise-web-example.png)

Minecraft uses a noise algorithm for the terrain generation:

![minecraft-example](./resources/images/minecraft-value-noise-example.png)

Steps:
1. The main grid (drawing plane, square, quadrant e.t.c) is divided into several smaller grids and at the corner of every small grid there is a "main" point.
2. Assign a random value to each main point (Pixel value).
3. Iterate through every grid point (except the main ones) and append the result from the bilinear interpolation (average value, dependent on the corner points).

~ If the algorithm is used in two dimensions, the function accepts 2 parameters -  x and y coordinates and returns a value (based on the corner (main) points) which can be used as many things (for example in graphics, it is used most commonly as pixel lightness value).
In this implementation, the generated array is rendered in RGB, using matplotlib and numpy. Also notice that the further away main points we use, the smoother image we get.

Input: No input (most of the time, we don't need input, but we might get a size for the image that is going to be generated)
Output: Image (n-dimensional list)

We do the steps above and we end up with a value array (matrix) that is ready to be visualised (in this case - using matplotlib.pyplot).

The result of the value-noise.py program - 10x10, 100x100 and 500x500 arrays (fancy visualised).

![my-example](./resources/images/value-noise.png)

