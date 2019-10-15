import Labyrinthe
import graph


def draw_rectangle(x1, x2, y1, y2, color="Black"):
    for x in range(x1, x2):
        for y in range(y1, y2):
            graph.plot(y, x, color)


def count_lines(mtx):
    return len(mtx)


def count_columns(mtx):
    return len(mtx[0])


def get_image_size(mtx, size):
    return count_columns(mtx) * size, count_lines(mtx) * size


def get_color(raw):
    colors = ["Black", "White", "Blue", "Red", "Orange"]
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


def explore_route(laby):
    # Start and end coordinates of the labyrinth.
    start = find_start(laby)
    end = find_end(laby)
    # If there is no start or end then do not resolve the labyrinth.
    if not start or not end:
        return []
    # Explored path represents the list of coordinates which are already explored and could lead to unsolvable paths.
    explored_path = [start]
    # Current taken path.
    path = [start]
    # The last point in the path.
    last_point = start
    # While we don't reach the end we search a path
    while last_point != end:
        # We search the neighbors cases on the current position.
        neighbors = find_acc_neighbors(laby, last_point)
        # The new point to go to.
        new_point = last_point
        # Search for a new point in the neighbor points.
        for n in neighbors:
            # If the point is already explored then search another.
            if not (n in explored_path) and (n != start):
                new_point = n
                break
        # If there is no new neighbors then we must go back.
        if new_point == last_point:
            # Old point is the last point with more than 2 directions available.
            old_point = last_point
            # We search in the current path the last point with at least 1 unexplored direction.
            for n in path:
                nn = find_acc_neighbors(laby, n)
                if len(nn) > 1 and not_contains(explored_path, nn):
                    old_point = n
                    neighbors = nn
            if old_point == last_point:
                # There is only one path, the labyrinth is impossible.
                return []
            for n in neighbors:
                print(n)
                if not (n in explored_path) and (n != start):
                    new_point = n
                    break
            z = index_of(path, old_point)
            # We go back in the path.
            path = path[0:z+1]
        # We change the last point to the new point and add it in the paths.
        last_point = new_point
        path += [last_point]
        explored_path += [last_point]
    return path


def draw_grid(mtx, size):
    """
    Draws the grid of the labyrinth.
    :param mtx: The grid.
    :param size: The size of each grid content.
    """
    image_size = get_image_size(mtx, size)
    graph.ouvre_fenetre(image_size[1], image_size[0])
    for i in range(count_lines(mtx)):
        for j in range(len(mtx[i])):
            if mtx[i][j] != 1:
                draw_rectangle(j * size, j * size + size, i * size, i * size + size, get_color(mtx[i][j]))
    graph.attend_fenetre()


#labyrinth = [[0, 0, 0, 0, 0, 0, 0],
#             [0, 2, 1, 1, 0, 1, 0],
#             [0, 1, 0, 0, 0, 1, 0],
#             [0, 1, 1, 1, 1, 3, 0],
#             [0, 0, 0, 0, 0, 0, 0]]
labyrinth = Labyrinthe.creer(50, 50, 10)
draw_grid(labyrinth, 10)
route = explore_route(labyrinth)
if route:
    for n in route:
        if labyrinth[n[1]][n[0]] == 1:
            labyrinth[n[1]][n[0]] = 4
draw_grid(labyrinth, 10)
