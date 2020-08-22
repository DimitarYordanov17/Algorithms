# Fractal tree using recursion, Python implementation. @DimitarYordanov17
from turtle import *

def draw_branch(branch_length, angle):
    if branch_length > 5:
        forward(branch_length)
        right(angle)
        draw_branch(branch_length - 15, angle)
        left(2 * angle)
        draw_branch(branch_length - 15, angle)
        right(angle)
        backward(branch_length)

def draw_tree(trunk_length, angle):
    speed(0)
    right(90)
    up()
    forward(trunk_length)
    left(180)
    down()
    draw_branch(trunk_length, angle)
    done()

# Driver code:

draw_tree(100, 20)