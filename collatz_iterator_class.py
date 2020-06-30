# import pdb
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

class Collatz:
    def __init__(self):
        """
        Defining Class for the Collatz object, describing Known State
        number itself, equivalence sets, up to an iterate, n
        """
        self.n = 0
        self.known_set = [[(1, 0)]]
        # self.linking_node_list = [1]
        # Not auto-initialised, only after being called
        self.graph = None

    """
    Generating function for the collatz numbers
    VERSION 1: finds next iterator based on the next smallest odd not in kS
    VERSION 2 (current): Use P_r
    Updates collatz upon yield
    """
    def __next__(self):
        self.n += 1
        # flatten known set for search function
        flat_list = [item[0] for sublist in self.known_set for item in sublist]

        # initialise a list for current equivalence set
        eq = []

        # pdb.set_trace()
        """
        Version 0: Without idea of equivalence sets
        # Terminates iff Collatz Conjecture is true!
        while c != 1:
            # e for number of multiples of 2 that c contains
            e = 0
            # checks if upon dividing by 2,
            while int(((c/2)*10)%10) == 0:
                c = c/2
                e += 1
            # now we have the smallest integer version of c
            eq.append((c,e))
            # re-initialise
            c = 3*c + 1
            e = 0
        """
        # Version 2: Using P_r
        # Should be sufficient; if it fails; our proposition must have been wrong
        # c for current number
        if self.n == 1:
            c = 3
        else:
            c = self.known_set[self.n-1][0][0] + 6

        # Earlier: we did an O(n) check
        """
        if c not in flat_list:
            break
        """

        """
        Version 1: Finds next iterator based on next smallest odd not in KS
        while True:
            c = c + 2
            if c not in flat_list:
                break
        """

        # e for number of multiples of 2 that c contains
        e = 0

        while c not in flat_list:
            # checks if upon dividing by 2,
            c2 = c/2
            # if c2 divisible by 2 and c2 is not already in flat_list
            while True:
                if c2 in flat_list:
                    break
                elif int((c2*10) % 10) != 0:
                    c = int(c2*2)
                    break
                # c2 not inflat_list, and we still can divide by 2
                c2 = c2/2
                e += 1

            # now we have the smallest odd integer version of c
            if c2 in flat_list:
                c2 = int(c2)
                e += 1
                eq.append((c2,e))
                self.known_set.append(eq)
                break
            else:
                eq.append((c, e))
                # re-initialise
                c = 3*(2*c2) + 1
                e = 0

    def graph_init(self):
        """
        Updates networkX graph object up to Collatz Set
        """
        pass
        self.graph = nx.DiGraph()

        # for each equiv set in known set
        for i in range(self.n+1):
            # Initialise P_r itself
            curr_val = self.known_set[i][0][0]
            self.graph.add_node(curr_val)
            curr_len = len(self.known_set[i])

            # for each next odd jth node the known_set[i]
            for j in range(curr_len-1):
                fcurr = 3*curr_val + 1
                self.graph.add_edge(curr_val,fcurr)

                # for each even number
                for k in range(self.known_set[i][j+1][1]):
                    curr_val = fcurr
                    fcurr = fcurr//2
                    self.graph.add_edge(curr_val,fcurr)
                curr_val = self.known_set[i][j+1][0]
                if fcurr != curr_val:
                    self.graph.add_edge(fcurr, curr_val)

                """
                fcurr = 3*curr_val+1
                self.graph.add_edge(curr_val, fcurr)

                # for each even number
                for k in range(self.known_set[i][j][1]):
                    curr_val = fcurr
                    fcurr = fcurr/2
                    self.graph.add_edge(curr_val,fcurr)
                curr_val = fcurr/2
                """
    def graph_find_Pr_lengths(self):
        source = []

        for i in self.known_set:
            j = i[0][0]
            source.append(j)

        for i in range(len(source)):
            l = nx.shortest_path_length(c1.graph,source=source[i], target=1)
            print("The shortest path to 1 for " + str(source[i])+ ", the " + str(i+1) + "th P_r"  + " is " +  str(l))

    def graph_plot_Pr_lengths(self):
        source = []
        out = []

        for i in self.known_set:
            j = i[0][0]
            source.append(j)

        for i in range(len(source)):
            l = nx.shortest_path_length(c1.graph,source=source[i], target=1)
            out.append(l)

        # Generate the 2 axis for plots

        fig, ax = plt.subplots()
        # ax.set_xlim([2,max_to_iter])

        # Always draw y=x
        ax.scatter(source, out, s=25, cmap=plt.cm.coolwarm, zorder=10, marker='o')
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]
        # ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0,)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.savefig('graph_plot_Pr' + str(self.n) + ' .png',dpi=300)


    def graph_plot_dyadic_Pr(self):
        source = []
        out = []
        test = nx.dfs_successors(self.graph)
        odd_nodes = {key:val for key, val in test.items() if key%2 ==1}

        # Generate the 2 axis for plots
        source = [i / (2**(np.floor(np.log2(i))+1)) for i in odd_nodes.keys()]
        out = [i / (2**(np.floor(np.log2(i))+1)) for i in odd_nodes.values()]

        fig, ax = plt.subplots()
        # ax.set_xlim([2,max_to_iter])

        # Always draw y=x
        ax.scatter(source, out, s=25, cmap=plt.cm.coolwarm, zorder=10, marker='o')
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]
        # ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0,)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.savefig('graph_plot_Pr_dyadic' + str(self.n) + ' .png',dpi=300)

    def graph_tree_write(self):
        self.graph_init()
        A = nx.nx_agraph.to_agraph(self.graph)

        # Change attribute
        A.node_attr['style'] = 'filled'
        # default color
        A.node_attr['fillcolor'] = '#FFFFFF'

        # Add colours to P_r
        for i in self.known_set:
            j = i[0][0]
            n = A.get_node(j)
            n.attr['fillcolor']="#ADFF2F"
        A.layout(prog='dot')
        A.draw("collatztestPr" + str(self.n) + ".png")
        return

    def graph_tree_binwrite(self):
        self.graph_init()
        c1.graph = nx.relabel_nodes(c1.graph, lambda n: str(bin(int(n)).replace("0b", "")) + ", " + str(n))
        A = nx.nx_agraph.to_agraph(self.graph)

        # Change attribute
        A.node_attr['style'] = 'filled'
        # default color
        A.node_attr['fillcolor'] = '#FFFFFF'

        # Add colours to P_r
        for i in self.known_set:
            j = i[0][0]
            j = str(bin(int(j)).replace("0b", "")) + ", " + str(j)
            n = A.get_node(j)
            n.attr['fillcolor']="#ADFF2F"
        A.layout(prog='dot')
        A.draw("bin_collatztestPr" + str(self.n) + ".png")
        return

    def graph_plot_write(self,k):
        """
        Input the number for f^k(x)
        Returns up to the self.n for all P_r calculated so far
        """
        output_fx = []
        # Define a dictionary in order to use looping property; since graph
        # object was actually a tree
        known_loop = {1:4, 2:2, 0:1}
        max_to_iter = self.known_set[-1][0][0]

        curr = max_to_iter
        state = 1
        break_time = 0
        # Go through all the numbers
        while state != max_to_iter:
            # pdb.set_trace()
            # Set curr based on new max_to_iter
            curr = state
            # We went to decrement f^k to f^1
            k_test = k
            # While we are not at f^1
            while k_test != 0:
                # Special case if curr is 1; no successor
                if curr == 1:
                    k_test = k_test % 3
                    curr = known_loop[k_test]
                    break
                # Else get successor; application of f once
                try:
                    curr = list(self.graph[curr])[0]
                except KeyError:
                    max_to_iter = curr-1
                    state = max_to_iter
                    k_test =1
                    break_time = 1
                k_test -= 1
            if break_time == 1:
                break
            output_fx.insert(0,curr)
            state += 2

        # pdb.set_trace()
        x = [i for i in range(1,max_to_iter+1,2)]
        output_fx.reverse()
        print(x,output_fx)

        # Matplotlib settings
        # axes = plt.gca()
        fig, ax = plt.subplots()
        ax.set_xlim([2,max_to_iter])

        # Draw additional lines for each f^{k} case

        # Always draw y=x
        ax.scatter(x, output_fx, s=25, cmap=plt.cm.coolwarm, zorder=10, marker='o')
        lims = [
            np.min([ax.get_xlim(), ax.get_ylim()]),  # min of both axes
            np.max([ax.get_xlim(), ax.get_ylim()]),  # max of both axes
        ]
        ax.plot(lims, lims, 'k--', alpha=0.75, zorder=0,)
        ax.set_aspect('equal')
        ax.set_xlim(lims)
        ax.set_ylim(lims)
        ax.xaxis.set_major_locator(MaxNLocator(integer=True))
        fig.savefig('graph_plot' + str(self.n) + ' .png',dpi=300)

    """
    Methods with collatz extension in front are for investigation of properties
    """
    def collatz_longest(self):
        """
        Returns longest equivalent set in the known set
        as (initial_seed, corresponding index in P_r, max_len)
        """
        # tuple remembering max_len and corresponding index
        max_len = (0,0)
        for i in range(self.n+1):
            curr_len = len(self.known_set[i])
            if curr_len > max_len[0]:
                max_len = (curr_len, i)
        return (self.known_set[max_len[1]][0][0], max_len[1], max_len[0])


    def collatz_number(self):
        return self.n
    def collatz_known_conventional(self):
        """
        Returns Collatz List in conventional, sorted form
        """
        # flatten known set for search function
        flat_list = [item[0] for sublist in self.known_set for item in sublist]
        return sorted(flat_list)
    def collatz_known_conventional_nr(self):
        """
        Returns Collatz List in conventional, sorted form, no repeats
        """
        # flatten known set for search function
        flat_list = [item[0] for sublist in self.known_set for item in sublist]
        final_list = []
        for num in flat_list:
            if num not in final_list:
                final_list.append(num)
        return sorted(final_list)
    def collatz_max_equiv():
        pass


c1 = Collatz()

for i in range(5):
    c1.__next__()

c1.graph_init()

# c1.__next__()

print("The list of odd collatz numbers, in the usual minmax ordering of the integers is :",  c1.collatz_known_conventional())
print("This was computed using ", c1.n, "number of 'equivalent sets'")
print("In order of computing the equivalent sets, this is the known set.")
print(c1.known_set)
print("The longest collatz sequence here is ",c1.collatz_longest())

# Task; after coming up with both Version 1 and 2 for the generator; store data
# of performance
"""
Queries distances of numbers based on object
"""

# optional for now
"""
Function that calls upon matplotlib
Plots traditional, known
"""

"""
REFERENCES:
https://www.geeksforgeeks.org/python-remove-duplicates-list/
"""

# odds = [node for node in list(c1.graph.nodes) if node % 2 == 1]
# c1.graph_tree_binwrite()
# c1.graph_tree_write()


