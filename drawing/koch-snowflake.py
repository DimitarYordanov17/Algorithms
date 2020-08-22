# Koch Snowflake Python Implementation. @DimitarYordanov17
import turtle

bob = turtle.Turtle()

bob.speed(100)


def koch(t, length):
    if length < 3:
        t.fd(length)
    else:
        m = length / 3
        koch(t, m)
        t.lt(60)
        koch(t, m)
        t.rt(120)
        koch(t, m)
        t.lt(60)
        koch(t, m)


def snowflake(t, length):
    koch(t, length)
    t.rt(120)
    koch(t, length)
    t.rt(120)
    koch(t, length)
    t.rt(120)

# Driver code:

snowflake(bob, 100)

turtle.mainloop()
