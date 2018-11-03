Joshua Clouse & Zack Lawrence

For our code we did a standard A* approach for the search. We looked at each of the adjacent actions using the graph function
and then compared the costs for each, taking into account our heuristic. We then put that onto a heapq which would automatically
sort the heap in order of lowest cost and then keep popping off the queue until we found the goal. The heurtistic was pretty
brute force. We basically just looked at how much of each item would ever be necessary to craft another item. For instance, you will
only ever need a maximum of 8 cobble because the highest amount of cobble needed for one recipe is 8. You will only ever need a maximum
of 1 wood block at a time because the highest cost of a wood block is to make planks which only require 1 wood block. If we ever had
more than the maximum amount of an item, we would make that item then have a cost of 50000 so that it would be very unlikely to be
considered again in the A* algorithm. If you used an item to craft another item, then the item count would go down below the max, making
the heuristic drop down to a normal level again.