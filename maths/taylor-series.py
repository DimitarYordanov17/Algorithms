# Taylor Series algorithm Python implementation. @DimitarYordanov17

import sympy
import math

def get_derivative(function, n):
    """
    Returns the n-th derivative of the input function.
    """
    sympy_derivative = function
    
    for _ in range(n):
        sympy_derivative = sympy.Derivative(sympy_derivative).doit()
    
    derivative = sympy_derivative.doit()
    
    return derivative

def get_derivative_value(function, x_value, n):
    """
    Returns the n-th derivative of the input function value at x_value x coordinate
    """
    if n == 0: # 0-th derivative is the function itself
        return function.subs({x: x_value})
    
    derivative = get_derivative(function, n)
    
    return derivative.subs({x: x_value})

def get_taylor_series(function, x, polynomial_depth=50, center=0):
    """
    Returns the Taylor Series polynomial approximation of the input function by the formula at x
    and prints the terms in decimal value
    (a=center, x=x, n=polynomial_depth)
                    f`(a)              f``(a)             f```(a)
    f(x) = f(a) + -------- (x - a) + --------(x - a)^2 + ---------(x - a)^3 ...
                     1!                 2!                 3!
    """
    total_sum = 0
    
    for n in range(polynomial_depth):
        numerator = get_derivative_value(function, center, n)
        denominator = math.factorial(n)
        multiplier = (x - center) ** n
        current_term = (numerator / denominator) * multiplier
        
        print(f"1st term: ({numerator} / {denominator}) * {multiplier}")

        total_sum += current_term
    
    print()
    print(f"The polynomial approximation of {function} at x: {x} = {total_sum}")
    
    return total_sum

# Driver code:

x = sympy.Symbol('x')
result = get_taylor_series(sympy.sin(x), math.pi/2)






