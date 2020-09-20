# Data-Science algorithms

### Most of the data-science algorithms aim to do some operations on big/small datasets or gather information from them

## 1. Principal Component Analysis (PCA)

Principal component analysis (PCA) is a data-science algorithm used mainly to transform big-dimensional datasets into smaller ones.
This is done via some math concepts like vectors, matrices and transformation.

Steps:
(Example for 2D set to 1D set)
1. Calculate the axes variances (In 2D we have 2 axes, so we get 2 variances values)
2. Calculate the covariance (In 2D the covariance matrix, covariance is motly the correlation)
3. Construct the sigma matrix (often called covariance matrix but it is confusing with the covariance value)
4. Think of the sigma matrix as transformation matrix
5. Find the eigen vectors and eigen values of the sigma matrix
6. Get the biggest eigen vector (In 2D we get the biggest fromn the two)
7. Project every point from the 2D plot on the eigen vector
8. Now we got 1D dataset out of the 2D one, every point is characterised just by the distance from the center of the eigen-vector, rather than x and y coordinates

~ In the example below, PCA1 is the bigger eigen-vector (scaled and fliped so we can look at it as an axis)

~ In practice the algorithm might be used to transform hundreds of dimension into several (This is commonly used in face recognition!)

Input: 2D dataset

Output: 1D dataset

Example:

![pca](./resources/images/pca.png)
