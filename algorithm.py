# searchMethod is the search method specified by --method flag (bfs,dfs,greedy,astar)

import queue
from copy import deepcopy


def algori(maze, searchMethod):
    return {
        "dfs": dfs,
        "bfs": bfs,
        "greedy": greedy,
        "astar": astar,
    }.get(searchMethod)(maze)
# This is bfs search solution
def bfs(maze):
    # return path, num_states_explored
    bfs_stack = []
    gone = set()
    bfs_stack.append([maze.getFirst()])
    while bfs_stack:
        currentPath = bfs_stack.pop(0)
        currentRow, currentCol = currentPath[-1]
        if (currentRow, currentCol) in gone:
            continue
        gone.add((currentRow, currentCol))
        if maze.checkObj(currentRow, currentCol):
            return currentPath[:len(currentPath)-1], len(gone)
        for item in maze.getnear(currentRow, currentCol):
            if item not in gone:
                bfs_stack.append(currentPath + [item])
    return [], 0

# This is dfs search solution
def dfs(maze):
    # return path, num_states_explored

    dfs_stack = []
    dfs_queue = []
    gone = set()
    dfs_stack.append([maze.getFirst()])
    while dfs_stack:
        currentPath = dfs_stack.pop(-1)
        currentRow, currentCol = currentPath[-1]
        if (currentRow, currentCol) in gone:
            continue
        gone.add((currentRow, currentCol))
        if maze.checkObj(currentRow, currentCol):
            return currentPath[:len(currentPath)-1], len(gone)
        for item in maze.dfs_getnear(currentRow, currentCol):
            if item not in gone:
                dfs_stack.append(currentPath + [item])
                # print([item])
    return [], 0

# This is greedy search solution
def greedy(maze):
    # return path, num_states_explored
    pq = queue.PriorityQueue()
    gone = set()
    result_row, result_col = maze.getObj()[0]
    start_row, start_col = maze.getFirst()
    # pq item - tuple: (distance, path list)
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [maze.getFirst()]))
    while not pq.empty():
        currentPath = pq.get()[1]
        currentRow, currentCol = currentPath[-1]

        for item in maze.getnear(currentRow, currentCol):
            item_row, item_col = item[0], item[1]
            if maze.checkObj(item_row, item_col):
                gone.add(item)
                currentPath += [item]
                return currentPath[:len(currentPath)-1], len(gone)

            if item not in gone:
                gone.add(item)
                cost = abs(item[0] - result_row) + abs(item[1] - result_col)
                pq.put((cost, currentPath + [item]))
    return [], 0

# ====================================== PART 2 ===============================================
# astar for part 1&2
# self-built data structure

class ctor:
    def __init__(self, row, col, cost, tcost):        
        self.not_gone = []
        self.row = row
        self.col = col
        self.position = (row, col)
        self.sofarcost = 0
        self.cost = cost  # heuristic
        self.tcost = tcost  # f = g + h（total）
        self.prev = None

    def __lt__(self, other):
        return self.tcost < other.tcost

# This is atar search solution
def astar(maze):
    # return path, num_states_explored
    num_of_state = 0
    if len(maze.getObj()) == 1:
        start_1 = maze.getFirst()
        end_1 = maze.getObj()[0]
        return cost_sofar(maze, start_1, end_1)

    start = maze.getFirst()
    points_left = maze.getObj()
    points_left.insert(0, start)
    edge_list = {}
    heuristicArray = {}
    # building graph for mst
    for i in points_left:
        for j in points_left:
            if i != j:
                edge_list[(i, j)] = cost_sofar(maze, i, j)[0]
                heuristicArray[(i, j)] = len(cost_sofar(maze, i, j)[0])
                num_of_state += 10
    not_gone_list = {}
    gone = {}
    currentPath = queue.PriorityQueue()
    mstWeight = getMst(maze, points_left, heuristicArray)
    start_r, start_c = maze.getFirst()
    start_state = ctor(start_r, start_c, 0, mstWeight)
    start_state.not_gone = maze.getObj()

    currentPath.put(start_state)
    not_gone_list[(start_r, start_c)] = len(start_state.not_gone)

    while len(points_left):
        cur_state = currentPath.get()
        if not cur_state.not_gone:
            break
        for n in cur_state.not_gone:
            n_row, n_col = n
            n_cost = cur_state.cost + \
                heuristicArray[(cur_state.position, n)] - 1
            next_state = ctor(n_row, n_col, n_cost, 0)
            next_state.prev = cur_state
            next_state.not_gone = deepcopy(cur_state.not_gone)
            if n in next_state.not_gone:
                next_state.not_gone.remove(n)
            gone[(n_row, n_col)] = 0
            not_gone_list[n] = len(next_state.not_gone)
            mstWeight = getMst(maze, cur_state.not_gone, heuristicArray)
            next_state.tcost = n_cost + mstWeight
            a = len(points_left) - 1
            if a:
                next_state.tcost += len(next_state.not_gone)
            currentPath.put(next_state)
    ret_path1 = print_path(maze, edge_list, cur_state)
    return ret_path1, num_of_state


def print_path(maze, path, state):
    ret_path = []
    points_list = []
    while state:
        points_list.append(state.position)
        state = state.prev
    total_dot = len(points_list)-1
    for i in range(total_dot):
        ret_path += path[(points_list[i], points_list[i+1])][:-1]
    start = maze.getFirst()
    ret_path.append(start)
    ret_path[::-1]
    return ret_path


def getMst(maze, points, heuristicArray):
    # Prim
    if not len(points):
        return 0
    start = points[0]
    gone = {}
    gone[start] = True
    MST_edges = []
    mstWeight = 0
    while len(gone) < len(points):
        qe = queue.PriorityQueue()
        for v in gone:
            for n in points:
                if gone.get(n) == True:
                    continue
                new_edge = (v, n)
                new_cost = heuristicArray[new_edge]-2
                qe.put((new_cost, new_edge))
        add_edge = qe.get()
        MST_edges.append(add_edge[1])
        mstWeight += add_edge[0]
        gone[add_edge[1][1]] = True
    return mstWeight


def cost_sofar(maze, start, end):
    pq = queue.PriorityQueue()
    gone = {}
    result_row, result_col = end
    start_row, start_col = start
    cost = abs(start_row-result_row) + abs(start_col - result_col)
    pq.put((cost, [(start_row, start_col)]))
    while not pq.empty():
        currentPath = pq.get()[1]
        currentRow, currentCol = currentPath[-1]
        if (currentRow, currentCol) in gone:
            continue
        cur_cost = abs(currentRow - result_row) + \
            abs(currentCol - result_col) + len(currentPath) - 1
        gone[(currentRow, currentCol)] = cur_cost
        if (currentRow, currentCol) == (result_row, result_col):
            return currentPath[:len(currentPath)-1], len(gone)
        for item in maze.getnear(currentRow, currentCol):
            new_cost = abs(item[0] - result_row) + \
                abs(item[1] - result_col) + len(currentPath) - 1
            if item not in gone:
                pq.put((new_cost, currentPath + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if gone[item] > new_cost:
                    gone[item] = new_cost
                    pq.put((new_cost, currentPath + [item]))
    return [], 0


# ====================================== extra credit ===============================================
# astar for extra_credit

def shortest(maze, start, end):
    queue = []
    gone = set()
    queue.append([start])
    while queue:
        currentPath = queue.pop(0)
        currentRow, currentCol = currentPath[-1]
        if (currentRow, currentCol) in gone:
            continue
        gone.add((currentRow, currentCol))
        if (currentRow, currentCol) == end:
            return len(currentPath)
        for item in maze.getnear(currentRow, currentCol):
            if item not in gone:
                queue.append(currentPath + [item])
    return 0


def update_pq(maze, objectives, start):
    ret = queue.PriorityQueue()
    for item in objectives:
        cost = shortest(maze, (start[0], start[1]), (item[0], item[1]))
        ret.put((cost, item))
    return ret


def astar_ec(maze):
    # return path, num_states_explored
    cur_pq = queue.PriorityQueue()
    gone = {}
    num_states_gone = set()
    objectives = maze.getObj()
    objectives_pq = update_pq(maze, objectives, maze.getFirst())
    cur_cost, cur_goal = objectives_pq.get()
    cur_pq.put((cur_cost, [maze.getFirst()]))

    while not cur_pq.empty():
        currentPath = cur_pq.get()[1]
        currentRow, currentCol = currentPath[-1]
        if (currentRow, currentCol) in gone:
            continue
        shortest_path = shortest(
            maze, (currentRow, currentCol), (cur_goal[0], cur_goal[1]))
        cur_cost = shortest_path + len(currentPath) - 1
        gone[(currentRow, currentCol)] = cur_cost
        num_states_gone.add((currentRow, currentCol))
        if (currentRow, currentCol) in objectives:
            objectives.remove((currentRow, currentCol))
            if len(objectives) == 0:
                return currentPath, len(num_states_gone)
            else:
                objectives_pq = update_pq(maze, objectives, (currentRow, currentCol))
                cur_cost, cur_goal = objectives_pq.get()
                cur_pq = queue.PriorityQueue()
                cur_pq.put((cur_cost, currentPath))
                gone.clear()
                continue
        for item in maze.getnear(currentRow, currentCol):
            shortest_path = shortest(
                maze, (item[0], item[1]), (cur_goal[0], cur_goal[1]))
            new_cost = shortest_path + len(currentPath) - 1
            if item not in gone:
                cur_pq.put((new_cost, currentPath + [item]))
            else:
                # if a node that’s already in the explored set found, test to see if the new h(n)+g(n) is smaller than the old one.
                if gone[item] > new_cost:
                    gone[item] = new_cost
                    cur_pq.put((new_cost, currentPath + [item]))
    return [], 0
