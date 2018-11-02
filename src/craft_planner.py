import json
from collections import namedtuple, defaultdict, OrderedDict
from timeit import default_timer as time

Recipe = namedtuple('Recipe', ['name', 'check', 'effect', 'cost'])


class State(OrderedDict):
    """ This class is a thin wrapper around an OrderedDict, which is simply a dictionary which keeps the order in
        which elements are added (for consistent key-value pair comparisons). Here, we have provided functionality
        for hashing, should you need to use a state as a key in another dictionary, e.g. distance[state] = 5. By
        default, dictionaries are not hashable. Additionally, when the state is converted to a string, it removes
        all items with quantity 0.

        Use of this state representation is optional, should you prefer another.
    """

    def __key(self):
        return tuple(self.items())

    def __hash__(self):
        return hash(self.__key())

    def __lt__(self, other):
        return self.__key() < other.__key()

    def copy(self):
        new_state = State()
        new_state.update(self)
        return new_state

    def __str__(self):
        return str(dict(item for item in self.items() if item[1] > 0))


def make_checker(rule):
    # Implement a function that returns a function to determine whether a state meets a
    # rule's requirements. This code runs once, when the rules are constructed before
    # the search is attempted.

    def check(state):
        # This code is called by graph(state) and runs millions of times.
        # Tip: Do something with rule['Consumes'] and rule['Requires'].
        if 'Requires' in rule:
            for requirement in rule['Requires']:
                if state[requirement] <= 0:
                    return False
        if 'Consumes' in rule:
            for item in rule['Consumes']:
                if state[item] < rule['Consumes'][item]:
                    return False
        return True

    return check


def make_effector(rule):
    # Implement a function that returns a function which transitions from state to
    # new_state given the rule. This code runs once, when the rules are constructed
    # before the search is attempted.

    def effect(state):
        # This code is called by graph(state) and runs millions of times
        # Tip: Do something with rule['Produces'] and rule['Consumes'].
        next_state = None
        next_state = state.copy()
        if 'Consumes' in rule:
            for item in rule['Consumes']:
                next_state[item] -= rule['Consumes'][item]
        if 'Produces' in rule:
            for item in rule['Produces']
            next_state[item] += rule['Produces'][item]
        return next_state

    return effect


def make_goal_checker(goal):
    # Implement a function that returns a function which checks if the state has
    # met the goal criteria. This code runs once, before the search is attempted.

    def is_goal(state):
        for item in goal:
            if goal[item] >= state[item]:
                return False
        return True

    return is_goal


def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_recipes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)


def heuristic(state):
    #I think the goal here is to find out what items it takes to get to the goal. This loop is making a list of all the items
    #needed to get to the goal. I want to move this to the get_shopping_list 
    '''
    shopping_list = {}
    for goalItem in state["Goal"]:
        for recipe in state["Recipes"]:
            #check each recipe for what it produces
            for item in recipe["Produces"]:
                if item == goalItem:
    '''


    return 0

#This function should ideally look at all the things needed to create the goal item/items by doing recursion since each goal item
#will have sub items which will also have their own sub items
#parameter is the items we need and a dictionary to put items into passed by reference
def get_shopping_list(goalItems, shopping_list):
    for goalItem in goals:
        for recipe in Crafting["Recipes"]:

def search(graph, state, is_goal, limit, heuristic):

    start_time = time()
    
    closed = []
    open = []
    heappush(open, (0, state))
    parents = {}
    parent[state] = None
    costs = {}
    costs[state] = 0
    actions = {}
    actions[state] = None
    path = []
    # Implement your search here! Use your heuristic here!
    # When you find a path to the goal return a list of tuples [(state, action)]
    # representing the path. Each element (tuple) of the list represents a state
    # in the path and the action that took you to this state
    while time() - start_time < limit:
        curr_cost, curr_state = heappop(open)
        if is_goal(curr_state):
            back_state = parents[curr_state]
            path = [(curr_state, actions[curr_state])]
            while parents[curr_state] != None:
                path.insert(0, (back_state, actions[back_state]))
                curr_state = back_state
                back_state = parents[back_state]
                print(time() - start_time, "seconds.")
                return path
        #make copy to pass to graph since it's passed by reference
        temp_state = curr_state.copy()
        for rule, new_state, time_cost in graph(temp_state)
            if new_state not in closed:
                #because it's a heapqueue it will automatically sort by lowest value
                heappush(open, (time_cost, new_state))
                #we only want to update the costs and parents dicts if the new_state isn't in there or if the new cost
                #is lower than the previous cost
                if new_state not in costs:
                    costs[new_state] = time_cost
                    parents[new_state] = state
                    actions[new_state] = rule
                elif time_cost < costs[new_state]
                    costs[new_state] = time_cost
                    parents[new_state] = state
                    actions[new_state] = rule
        closed[curr_state] = 1
                
    # Failed to find a path
    print(time() - start_time, 'seconds.')
    print("Failed to find a path from", state, 'within time limit.')
    return None

if __name__ == '__main__':
    with open('Crafting.json') as f:
        Crafting = json.load(f)

    # # List of items that can be in your inventory:
    # print('All items:', Crafting['Items'])
    #
    # # List of items in your initial inventory with amounts:
    # print('Initial inventory:', Crafting['Initial'])
    #
    # # List of items needed to be in your inventory at the end of the plan:
    # print('Goal:',Crafting['Goal'])
    #
    # # Dict of crafting recipes (each is a dict):
    # print('Example recipe:','craft stone_pickaxe at bench ->',Crafting['Recipes']['craft stone_pickaxe at bench'])

    # Build rules
    all_recipes = []
    for name, rule in Crafting['Recipes'].items():
        checker = make_checker(rule)
        effector = make_effector(rule)
        recipe = Recipe(name, checker, effector, rule['Time'])
        all_recipes.append(recipe)

    # Create a function which checks for the goal
    is_goal = make_goal_checker(Crafting['Goal'])

    # Initialize first state from initial inventory
    state = State({key: 0 for key in Crafting['Items']})
    state.update(Crafting['Initial'])

    # Search for a solution
    resulting_plan = search(graph, state, is_goal, 1000, heuristic)

    if resulting_plan:
        # Print resulting plan
        for state, action in resulting_plan:
            print('\t',state)
            print(action)
