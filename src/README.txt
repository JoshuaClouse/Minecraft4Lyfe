Joshua Clouse & Zack Lawrence

For our code we did a standard A* approach for the search. We looked at each of the adjacent actions using the graph function
and then compared the costs for each, taking into account our heuristic. We then put that onto a heapq which would automatically
sort the heap in order of lowest cost and then keep popping off the queue until we found the goal. The heurtistic was pretty
brute force. We basically just looked at how much of each item would ever need to be needed or produced. That is to say, we take the
highest value seen of each item being used in crafting another item or made in crafting from other items. For instance, you will
only ever need a maximum of 8 cobble because the highest amount of cobble needed for one recipe is 8. You will only ever need a maximum
of 1 wood block at a time because the highest cost of a wood block is to make planks which only require 1 wood block. You will only need
to worry about continuing if you have 16 or less rails. 16 rails are produced by their recipe, and for our requirements we never need more
than 20 rails. The only deviation from this is sticks. For some reason, if rails need to be made, setting the limit of sticks at 8 rather than 4
makes the program run much faster. If we ever had more than the maximum amount of an item, we would make that item then have a cost of 50000000
so that it would be very unlikely to be considered again in the A* algorithm. If you used an item to craft another item, then the item count 
would go down below the max, making the heuristic drop down to a normal level again.