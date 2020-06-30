# import pdb
from sympy import symbols
from sympy.solvers import solve
from sympy.plotting import plot
from math import log10, floor
def round_sig(x, sig=3):
    return round(x, sig-int(floor(log10(abs(x))))-1)
from matplotlib import pyplot as plt

# x = symbols('x', integer=True, positive=True)
x = symbols('x', integer=True)
# x = symbols('x', positive=True)
# x = symbols('x')

# collatz odd
c_o = 3 * x + 1
c_e = x/2

class collatz_component_function:
    """
    Class as a holder of data for each component function
    """
    def __init__(self,ordering_tuple, expr):
        # default val 1
        self.k = len(ordering_tuple)
        self.expr = expr
        self.order = ordering_tuple


class Collatz_function:
    def __init__(self):
        self.k = 1
        self.comp = [ collatz_component_function( (1,), 3 * x + 1 ), collatz_component_function( (0,), x/2 )]

    def __next__(self):
        self.k += 1

        # init new list
        new_l = []
        # for each component function, let's update
        for i in self.comp:
            # branch into more functions
            if i.order[-1] == 0:

                # odd
                new_exp = c_o.subs(x, i.expr)
                new = collatz_component_function(tuple(list(i.order) + [1]), new_exp)
                new_l.append(new)

                # even
                new_exp = c_e.subs(x, i.expr)
                new = collatz_component_function(tuple(list(i.order) + [0]), new_exp)
                new_l.append(new)

            # Only even application
            else:
                # even
                new_exp = c_e.subs(x, i.expr)
                new = collatz_component_function(tuple(list(i.order) + [0]), new_exp)
                new_l.append(new)

        # write custom sorting function AFTER

        # update
        self.comp = new_l

    def plot(self):
        p = plot(x,show = False, line_color = 'red')
        for i in self.comp:
            p1 = plot(i.expr,show = False)
            p.append(p1[0])
        p.show()

    def print_exp(self):
        numbering = 1
        for i in self.comp:
            print(str(numbering)+ ". " + str(i.expr) + " with " + str(i.order))
            numbering += 1

    def print_exp_sol(self):
        numbering = 1
        for i in self.comp:
            print(str(numbering) + ". " + str(solve(i.expr - x,x)))
            numbering += 1

def paths_to_k(k):
    """
    input: number of 3*k iterates to check up to
    returns the position of the success nodes in the ordering.
    success nodes as {1,2,4}
    """
    if k <= 0:
        return
    c1 = Collatz_function()
    out = []
    for i in range(2):
        c1.__next__()
    num_expr = len(c1.comp)
    for m in range(num_expr):
        root = solve(c1.comp[m].expr - x,x)
        # Check if root is empty list
        if not root:
            pass
        elif root[0] in [1,2,4]:
            out.append([c1.k,m,num_expr,round_sig(m/num_expr), c1.comp[m].order ,c1.comp[m].expr])
    k = k - 1
    for j in range(k):
            for i in range(3):
               c1.__next__()
            num_expr = len(c1.comp)
            for m in range(num_expr):
                root = solve(c1.comp[m].expr - x,x)
                # Check if root is empty list
                if not root:
                    pass
                elif root[0] in [1,2,4]:
                    out.append([c1.k,m,num_expr, round_sig(m/num_expr), c1.comp[m].order,c1.comp[m].expr])
    return out


c1 = Collatz_function()

"""
for i in range(3):
    c1.__next__()
"""

plt.xlim(0,5)
plt.ylim(0,30)

# c1.plot()
print("We are currently looking at f^{" + str(c1.k) + "}")
c1.print_exp()
print()
print("Solutions")
c1.print_exp_sol()

out = paths_to_k(5)


# Run these 6 lines in iPYthon for every iteration to get a clear view.
c1.__next__()
print("We are currently looking at f^{" + str(c1.k) + "}")
c1.print_exp()
print()
print("Solutions")
c1.print_exp_sol()
c1.plot()

print("Adjust solution type on first few lines of python file, whether already restricted to integers in sympy etc")
print("Copy paste and run on iPython for best experience")


