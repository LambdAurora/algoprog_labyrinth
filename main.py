import Labyrinthe
import graph
import time

grid_element_size = 4


current_time_millis = lambda: int(round(time.time() * 1000))


def draw_rectangle(x1, y1, size, color="black"):
    return graph.fengra.create_rectangle(y1, x1, y1 + size, x1 + size, fill=color, width=0)


def count_lines(mtx):
    return len(mtx)


def count_columns(mtx):
    return len(mtx[0])


def get_image_size(mtx, size):
    return count_columns(mtx) * size, count_lines(mtx) * size


def get_color(raw):
    colors = ["black", "white", "blue", "red", "orange"]
    return colors[raw]


def index_of(lst, n):
    for i in range(len(lst)):
        if lst[i] == n:
            return i
    return None


def coord_of(laby, n):
    for y in range(len(laby)):
        i = index_of(laby[y], n)
        if i:
            return i, y
    return None


def labyrinth_size(laby):
    return len(laby[0]), len(laby)


def find_start(laby):
    """
    Finds the start of the labyrinth.
    :param laby: The labyrinth.
    :return: The coordinates of the start of the labyrinth.
    """
    start = coord_of(laby, 2)
    if start:
        return start
    print("Error: cannot find the start of the labyrinth.")


def find_end(laby):
    """
    Finds the end of the labyrinth.
    :param laby: The labyrinth.
    :return: The coordinates of the end of the labyrinth.
    """
    end = coord_of(laby, 3)
    if end:
        return end
    print("Error: cannot find the end of the labyrinth.")


def find_neighbors(width, height, x, y):
    """
    Finds all of the neighbors around a point at the specified x and y coordinates.
    :param width: The width of the space.
    :param height: The height of the space.
    :param x: The x coordinate to search around.
    :param y: The y coordinate to search around.
    :return: A list of the neighbors around the point.
    """
    result = []
    for j in range(y - 1, y + 2):
        for i in range(x - 1, x + 2):
            if (0 <= j < height) and (0 <= i < width) and (x != i or j != y):
                result += [(i, j)]
    return result


def find_acc_neighbors(laby, coord):
    """
    Finds accessible neighbors in the labyrinth at the specified coordinates.
    :param laby: The labyrinth.
    :param coord: The coordinates where to search the neighbors.
    :return: A list of coordinates of the accessible neighbors.
    """
    size = labyrinth_size(laby)
    neighbors = find_neighbors(size[0], size[1], coord[0], coord[1])
    result = []
    for n in neighbors:
        if not ((coord[0] != n[0] and coord[1] != n[1]) and (laby[n[1]][coord[0]] == 0 or laby[coord[1]][n[0]] == 0)):
            if laby[n[1]][n[0]] != 0:
                result += [n]
    return result


def not_contains(l1, l2):
    """
    Checks if the first list does not contain the second list.
    :param l1: The first list.
    :param l2: The second list.
    :return: True if the first list does not contain the second list, else false.
    """
    n = 0
    for j in l2:
        for i in l1:
            if j == i:
                n += 1
    return n != len(l2)


def try_route(laby, start, end, ignore_points):
    # Current taken path
    path = [start]
    graph_path = []
    # The last point in the path.
    last_point = start
    while last_point != end:
        neighbors = find_acc_neighbors(laby, last_point)
        available_neighbors = []
        for n in neighbors:
            if not (n in ignore_points or n in path) and (n != start):
                available_neighbors += [n]
        if len(available_neighbors) == 0:
            for i in range(len(graph_path)):
                graph.fengra.supprime(graph_path[len(graph_path) - 1 - i])
            return []
        elif len(available_neighbors) > 1:
            for i in range(len(available_neighbors)):
                neighbor_route = try_route(laby, last_point, end, ignore_points + path + [available_neighbors[i]])
                if neighbor_route:
                    path += neighbor_route
                    return path
            for i in range(len(graph_path)):
                graph.fengra.supprime(graph_path[len(graph_path) - 1 - i])
            return []
        else:
            path += [last_point]
            graph_path += [draw_rectangle(last_point[0] * grid_element_size, last_point[1] * grid_element_size, grid_element_size, "orange")]
            graph.fengra.update()
            last_point = available_neighbors[0]
    return path


def explore_route(laby):
    # Start and end coordinates of the labyrinth.
    start = find_start(laby)
    end = find_end(laby)
    # If there is no start or end then do not resolve the labyrinth.
    if not start or not end:
        return []

    # We try every paths.
    for n in find_acc_neighbors(laby, start):
        path = try_route(laby, n, end, [start])
        if path:
            return path

    return []


def draw_grid(mtx, size):
    """
    Draws the grid of the labyrinth.
    :param mtx: The grid.
    :param size: The size of each grid content.
    """
    image_size = get_image_size(mtx, size)
    if graph.fengra is None:
        graph.ouvre_fenetre(image_size[0], image_size[1])
    for i in range(count_lines(mtx)):
        for j in range(len(mtx[i])):
            if mtx[i][j] != 1:
                draw_rectangle(j * size, i * size, size, get_color(mtx[i][j]))


# labyrinth = [[0, 0, 0, 0, 0, 0, 0],
#             [0, 2, 1, 1, 0, 1, 0],
#             [0, 1, 0, 0, 0, 1, 0],
#             [0, 1, 1, 1, 1, 3, 0],
#             [0, 0, 0, 0, 0, 0, 0]]
labyrinth = Labyrinthe.creer(175, 175, 3)
draw_grid(labyrinth, grid_element_size)
graph.fengra.attend_clic()
start_time = current_time_millis()
route = explore_route(labyrinth)
print("Time: " + str(current_time_millis() - start_time) + "ms")
if route:
    for n in route:
        if labyrinth[n[1]][n[0]] == 1:
            labyrinth[n[1]][n[0]] = 4
draw_grid(labyrinth, grid_element_size)
graph.attend_fenetre()
