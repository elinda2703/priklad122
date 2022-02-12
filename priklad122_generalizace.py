try:
    import json
    import sys
    from math import sqrt
    import matplotlib.pyplot as plt
    
except ImportError:
    sys.exit("An error occured while importing a library. Check if the required libraries are installed correctly.")


def pythagoras(x1, y1, x2, y2):
    # Computes distance between two points using Pythagoras theorem.
    distance = sqrt((x1-x2)**2+(y1-y2)**2)
    return distance


def heron(a, b, c):
    # Computes area of a triangle defined by lengths of its sides using Herons' formula.
    s = (a+b+c)/2
    area = sqrt(s*(s-a)*(s-b)*(s-c))
    return area


def visvalingam_whyatt(vertices, epsilon):
    """
    Line simplification algorithm
    It takes the coordinates of points representing vertices of a line, eliminates redundant vertices while preserving the shape as much as possible.
    The epsilon parameter defines how many points will be discarded.

    Parameters:
        vertices (list): list of coordinates of the vertices of the line
        epsilon (float): smallest area of a triangle defined by three consecutive points on a line, determines the intensity of simplification

    Returns:
        simplified (iterator): iterator of tuples; iterates over x-coords and y-coords paralelly
            produces two tuples, one containing x-coords, second containing y-coords of the vertices of the simplified line
    """

    # list containing distances between two neighbouring vertices on a line
    lengths = []

    # list containing distances between two vertices on a line skipping one point
    third_sides = []

    # list containing areas of triangles defined by three consecutive points on a line
    areas = []

    for i in range(1, len(vertices)):
        # computes distance between every two consecutive points and adds them to a list
        v1 = vertices[i-1]
        v2 = vertices[i]
        d = pythagoras(*v1, *v2)
        lengths.append(d)
    for i in range(2, len(vertices)):
        # computes distance between every two vertices on a line skipping one point and adds them to a list
        w1 = vertices[i-2]
        w2 = vertices[i]
        c = pythagoras(*w1, *w2)
        third_sides.append(c)
    for i in range(1, len(lengths)):
        # computes areas of triangles defined by three consecutive points on a line and adds them to a list
        a = lengths[i-1]
        b = lengths[i]
        c = third_sides[i-1]
        area = heron(a, b, c)
        areas.append(area)

    while len(vertices) > 2 and min(areas) < epsilon:
        """
        While the line has more than 2 vertices and the smallest area of a triangle defined by three consecutive vertices on a line is smaller than epsilon:
            finds index of the smallest area of a triangle and eliminates its second point
            eliminates and recomputes areas and distances that have changed due to the removed vertex
        """
        rank = areas.index(min(areas))
        vertices.pop(rank+1)
        lengths[rank] = third_sides[rank]
        lengths.pop(rank+1)
        if rank != 0:
            # checks if the smallest area of a triangle isn't at the start of the line
            third_sides[rank - 1] = pythagoras(*vertices[rank-1], *vertices[rank+1])
            areas[rank-1] = heron(lengths[rank-1], lengths[rank], third_sides[rank-1])
        third_sides.pop(rank)
        areas.pop(rank)
        if rank != (len(areas)):
            # checks if the smallest area of a triangle isn't at the end of the line
            third_sides[rank] = pythagoras(*vertices[rank], *vertices[rank+2])
            areas[rank] = heron(lengths[rank+1], lengths[rank], third_sides[rank])
    simplified = zip(*vertices)
    return simplified


def visualize(raw_x, raw_y, simplified_x, simplified_y):
    # visualizes both the raw and simplified line knowing the coordinates of its vertices
    fig, (ax1, ax2) = plt.subplots(1, 2)
    fig.suptitle("Visvalingam-Whyatt line simplification")
    ax1.plot(raw_x, raw_y)
    ax2.plot(simplified_x, simplified_y)
    ax1.set_title("Raw line")
    ax2.set_title("Simplified line")
    ax1.get_xaxis().set_visible(False)
    ax1.get_yaxis().set_visible(False)
    ax2.get_xaxis().set_visible(False)
    ax2.get_yaxis().set_visible(False)
    plt.show()

# loads data from the input file
try:
    with open("input_d1.geojson", encoding="utf-8") as input:
        sample_line = json.load(input)
        vertices = sample_line['features'][0]['geometry']['coordinates']
except IOError:
    sys.exit("An error occured while opening the file with input data. Check if the file is in same directory as the script.")
except KeyError:
    sys.exit("An error ocuured while reading the input data. Check if the file contains the required attributes.")
except:
    sys.exit("Something went wrong.")

# minimum area treshold
epsilon = 0.001

# transposes coordinates of the vertices of the raw line
before = zip(*vertices)

after = visvalingam_whyatt(vertices,epsilon)
visualize(*before, *after)
