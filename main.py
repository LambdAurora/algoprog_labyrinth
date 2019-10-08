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
    colors = ["Black", "White", "Blue", "Red"]
    return colors[raw]


def find_start(laby):
    """
    Finds the start of the labyrinth.
    :param laby: The labyrinth.
    :return: The coordinates of the start of the labyrinth.
    """
    for y in range(len(laby)):
        for x in range(len(laby[y])):
            if laby[y][x] == 2:
                return x, y
    print("Error: cannot find the start of the labyrinth.")


def find_end(laby):
    """
    Finds the end of the labyrinth.
    :param laby: The labyrinth.
    :return: The coordinates of the end of the labyrinth.
    """
    for y in range(len(laby)):
        for x in range(len(laby[y])):
            if laby[y][x] == 3:
                return x, y
    print("Error: cannot find the end of the labyrinth.")


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


labyrinth = Labyrinthe.creer(11, 15)
draw_grid(labyrinth, 20)
