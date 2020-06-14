import numpy as np
import turtle
import math
import random
import copy

coordinates = np.load("./coordinates.npy")
coordinates *= 2
coordinates.tolist()
dimensions = np.load("./dimensions.npy")
dimensions *= 2
dimensions.tolist()
min_dim = np.load("./min_dim.npy")
min_dim *= 2
min_dim.tolist()
adjacency = np.load("./adjacency_list.npy")
adjacency.tolist()

adjacency_list= [[0 for i in range(12)] for j in range(0,12)] 
print(adjacency_list)
for i in range(1,13):
	for j in range(116,126):
		adjacency_list[i-1][j-116]=adjacency[i][j]
print(adjacency_list)
pins = []
pins_actual = []

for i in range(0, len(adjacency_list)):
    pins.append([[coordinates[i][0] + dimensions[i][0] / 2 + 1 , coordinates[i][1]],
                 [coordinates[i][0] - dimensions[i][0] / 2 - 1, coordinates[i][1]],
                 [coordinates[i][0], coordinates[i][1] - dimensions[i][1] / 2 - 1],
                 [coordinates[i][0], coordinates[i][1] + dimensions[i][1] / 2 + 1],
                 [coordinates[i][0] + dimensions[i][0] / 2 + 1, coordinates[i][1] + dimensions[i][1] / 4],
                 [coordinates[i][0] - dimensions[i][0] / 2 - 1, coordinates[i][1] + dimensions[i][1] / 4],
                 [coordinates[i][0] + dimensions[i][0] / 2 + 1, coordinates[i][1] - dimensions[i][1] / 4],
                 [coordinates[i][0] - dimensions[i][0] / 2 - 1, coordinates[i][1] - dimensions[i][1] / 4],
                 [coordinates[i][0] + dimensions[i][0] / 4, coordinates[i][1] + dimensions[i][1] / 2 + 1],
                 [coordinates[i][0] - dimensions[i][0] / 4, coordinates[i][1] + dimensions[i][1] / 2 + 1],
                 [coordinates[i][0] + dimensions[i][0] / 4, coordinates[i][1] - dimensions[i][1] / 2 - 1],
                 [coordinates[i][0] - dimensions[i][0] / 4, coordinates[i][1] - dimensions[i][1] / 2 - 1]])

for i in range(0, len(adjacency_list)):
    pins_actual.append([[coordinates[i][0] + dimensions[i][0] / 2 , coordinates[i][1]],
                 [coordinates[i][0] - dimensions[i][0] / 2, coordinates[i][1]],
                 [coordinates[i][0], coordinates[i][1] - dimensions[i][1] / 2],
                 [coordinates[i][0], coordinates[i][1] + dimensions[i][1] / 2],
                 [coordinates[i][0] + dimensions[i][0] / 2, coordinates[i][1] + dimensions[i][1] / 4],
                 [coordinates[i][0] - dimensions[i][0] / 2, coordinates[i][1] + dimensions[i][1] / 4],
                 [coordinates[i][0] + dimensions[i][0] / 2, coordinates[i][1] - dimensions[i][1] / 4],
                 [coordinates[i][0] - dimensions[i][0] / 2, coordinates[i][1] - dimensions[i][1] / 4],
                 [coordinates[i][0] + dimensions[i][0] / 4, coordinates[i][1] + dimensions[i][1] / 2],
                 [coordinates[i][0] - dimensions[i][0] / 4, coordinates[i][1] + dimensions[i][1] / 2],
                 [coordinates[i][0] + dimensions[i][0] / 4, coordinates[i][1] - dimensions[i][1] / 2],
                 [coordinates[i][0] - dimensions[i][0] / 4, coordinates[i][1] - dimensions[i][1] / 2]])

connections = []
connections_actual = []

for i in range(0, len(adjacency_list)):
    for j in range(0, len(adjacency_list)):
        if (adjacency_list[i][j] > 0) and (pins[i]!=[]) and (pins[j]!=[]):
            min_1 = pins[i][0]
            min_2 = pins[j][0]
            min_distance = math.sqrt((pins[i][0][0] - pins[j][0][0]) ** 2 + (pins[i][0][1] - pins[j][0][1]) ** 2)
            for k in pins[i]:
                for l in pins[j]:
                    distance = math.sqrt((k[0] - l[0]) ** 2 + (k[1] - l[1]) ** 2)
                    if distance <= min_distance:
                        min_1 = k
                        min_2 = l
                        min_distance = distance
            index_1 = pins[i].index(min_1)
            index_2 = pins[j].index(min_2)
            pins[i].remove(min_1)
            pins[j].remove(min_2)
            connections.append([min_1, min_2])
            min_1 = pins_actual[i][index_1]
            min_2 = pins_actual[j][index_2]
            connections_actual.append([min_1,min_2])
            pins_actual[i].remove(min_1)
            pins_actual[j].remove(min_2)
            adjacency_list[i][j] = 0
            adjacency_list[j][i] = 0
print("pins_done")
connections_actual.reverse()
class cell:
    def __init__(self, value=0, block=0, direction=None, routed = 0):
        self.value = value
        self.block = block
        self.direction = direction
        self.routed = routed

cols = max(min_dim)

rows = max(min_dim)
print(cols,rows, len(coordinates))
my_object_1 = [[cell(0, 0, None) for j in range(cols)] for i in range(rows)]

my_object_2 = [[cell(0, 0, None) for j in range(cols)] for i in range(rows)]

for i in range(0, len(coordinates)):
    for j in range(int(coordinates[i][0] - dimensions[i][0] / 2 - 1),
                   int(coordinates[i][0] + dimensions[i][0] / 2 + 1)):
        for k in range(int(coordinates[i][1] - dimensions[i][1] / 2 - 1),
                       int(coordinates[i][1] + dimensions[i][1] / 2 + 1)):
            my_object_1[j][k].block = 1

turtle.hideturtle()

coordinates = np.array(coordinates)
coordinates = np.multiply(coordinates, 5)
coordinates.tolist()

dimensions = np.array(dimensions)
dimensions = np.multiply(dimensions, 5)
dimensions.tolist()

for i in range(0, len(adjacency_list)):
    centre_x = coordinates[i][0]
    centre_y = coordinates[i][1]
    width = dimensions[i][0]
    height = dimensions[i][1]
    turtle.penup()
    turtle.goto(centre_x + width / 2, centre_y + height / 2)
    turtle.pendown()
    turtle.goto(centre_x - width / 2, centre_y + height / 2)
    turtle.goto(centre_x - width / 2, centre_y - height / 2)
    turtle.goto(centre_x + width / 2, centre_y - height / 2)
    turtle.goto(centre_x + width / 2, centre_y + height / 2)
turtle.penup()

for a in connections:
    b = connections_actual.pop()
    print(a)
    actual_start_x = int(b[0][0])
    actual_start_y = int(b[0][1])
    actual_end_x = int(b[1][0])
    actual_end_y = int(b[1][1])

    start_x = int(a[0][0])
    start_y = int(a[0][1])
    end_x = int(a[1][0])
    end_y = int(a[1][1])

    my_object_1[int(start_x)][int(start_y)].value = 1
    list_oldx = []
    list_x = []
    list_y = []
    list_oldy = []
    list_oldx.append(int(start_x))
    list_oldy.append(int(start_y))
    temp = 0
    bend_cost = 3
    iteration = 1
    layer = 0
    my_object_1[int(start_x)][int(start_y)].block = 0
    my_object_1[int(end_x)][int(end_y)].block = 0
    
    while my_object_1[int(end_x)][int(end_y)].value == 0:
        if len(list_oldx) == 0 and len(list_oldy) == 0:
            print("NO PATH FOUND IN LAYER 1 TRYING AGAIN")
            layer = 1
            break
	
        for index_x in list_oldx:
            list_oldy.reverse()
            index_y = list_oldy.pop()
            list_oldy.reverse()
	
            if index_x + 1 <= rows - 1 and my_object_1[index_x][index_y].direction != 'S' and my_object_1[index_x + 1][
                index_y].block != 1:
                # my_object_1[index_x + 1][index_y].direction = 'E'
                if iteration == 1:
                    my_object_1[index_x + 1][index_y].value = 2
                    my_object_1[index_x + 1][index_y].direction = 'N'
                    list_x.append(index_x + 1)
                    list_y.append(index_y)

                elif my_object_1[index_x][index_y].direction == 'N':
                    temp = my_object_1[index_x][index_y].value + 1

                else:
                    temp = my_object_1[index_x][index_y].value + bend_cost

                if iteration != 1:
                    if my_object_1[index_x + 1][index_y].value == 0 or temp <= my_object_1[index_x + 1][index_y].value:
                        my_object_1[index_x + 1][index_y].value = temp
                        my_object_1[index_x + 1][index_y].direction = 'N'
                        list_x.append(index_x + 1)
                        list_y.append(index_y)

            if index_x - 1 >= 0 and my_object_1[index_x][index_y].direction != 'N' and my_object_1[index_x - 1][
                index_y].block != 1:
                # my_object_1[index_x - 1][index_y].direction = 'W'
                if iteration == 1:
                    my_object_1[index_x - 1][index_y].value = 2
                    my_object_1[index_x - 1][index_y].direction = 'S'
                    list_x.append(index_x - 1)
                    list_y.append(index_y)

                elif my_object_1[index_x][index_y].direction == 'S':
                    temp = my_object_1[index_x][index_y].value + 1

                else:
                    temp = my_object_1[index_x][index_y].value + bend_cost

                if iteration != 1:
                    if my_object_1[index_x - 1][index_y].value == 0 or temp <= my_object_1[index_x - 1][index_y].value:
                        my_object_1[index_x - 1][index_y].value = temp
                        my_object_1[index_x - 1][index_y].direction = 'S'
                        list_x.append(index_x - 1)
                        list_y.append(index_y)

            if index_y + 1 <= cols - 1 and my_object_1[index_x][index_y].direction != 'E' and my_object_1[index_x][
                index_y + 1].block != 1:
                # my_object_1[index_x ][index_y+1].direction = 'N'
                if iteration == 1:
                    my_object_1[index_x][index_y + 1].value = 2
                    my_object_1[index_x][index_y + 1].direction = 'W'
                    list_x.append(index_x)
                    list_y.append(index_y + 1)

                elif my_object_1[index_x][index_y].direction == 'W':
                    temp = my_object_1[index_x][index_y].value + 1

                else:
                    temp = my_object_1[index_x][index_y].value + bend_cost

                if iteration != 1:
                    if my_object_1[index_x][index_y + 1].value == 0 or temp <= my_object_1[index_x][index_y + 1].value:
                        my_object_1[index_x][index_y + 1].value = temp
                        my_object_1[index_x][index_y + 1].direction = 'W'
                        list_x.append(index_x)
                        list_y.append(index_y + 1)

            if index_y - 1 >= 0 and my_object_1[index_x][index_y].direction != 'W' and my_object_1[index_x][
                index_y - 1].block != 1:

                if iteration == 1:
                    my_object_1[index_x][index_y - 1].value = 2
                    my_object_1[index_x][index_y - 1].direction = 'E'
                    list_x.append(index_x)
                    list_y.append(index_y - 1)

                elif my_object_1[index_x][index_y].direction == 'E':
                    temp = my_object_1[index_x][index_y].value + 1

                else:
                    temp = my_object_1[index_x][index_y].value + bend_cost

                if iteration != 1:
                    if my_object_1[index_x][index_y - 1].value == 0 or temp <= my_object_1[index_x][index_y - 1].value:
                        my_object_1[index_x][index_y - 1].value = temp
                        my_object_1[index_x][index_y - 1].direction = 'E'
                        list_x.append(index_x)
                        list_y.append(index_y - 1)
        list_oldx = list_x
        list_oldy = list_y
        list_x = []
        iteration += 1
        list_y = []
    
    # backtracking
    end_y = int(end_y)
    end_x = int(end_x)
    my_object_1[end_x][end_y].block = 1

    if layer == 0:
        turtle.goto(actual_end_x * 5, actual_end_y * 5)
        turtle.color('black')
        turtle.pendown()
        while True:
            turtle.goto(end_x * 5, end_y * 5)
            my_object_1[end_x][end_y].block = 1
            visited = 0
            if my_object_1[end_x][end_y].direction == 'N':
                end_x -= 1
                visited = 1
            elif my_object_1[end_x][end_y].direction == 'S':
                end_x += 1
                visited = 1
            elif my_object_1[end_x][end_y].direction == 'E':
                end_y += 1
                visited = 1
            elif my_object_1[end_x][end_y].direction == 'W':
                end_y -= 1
                visited = 1
            my_object_1[end_x][end_y].block = 1

            if end_x == int(start_x) and end_y == int(start_y):
                turtle.goto(end_x * 5, end_y * 5)
                turtle.goto(actual_start_x * 5, actual_start_y * 5)
                turtle.penup()
                layer = 0
                break

    for i in range(0, cols):
        for j in range(0, rows):
            my_object_1[i][j].value = 0
            my_object_1[i][j].direction = None

    if layer == 1:
        start_x = int(a[1][0])
        start_y = int(a[1][1])

        end_x = int(a[0][0])
        end_y = int(a[0][1])
        actual_start_x = int(b[1][0])
        actual_start_y = int(b[1][1])
        actual_end_x = int(b[0][0])
        actual_end_y = int(b[0][1])

        my_object_1[int(start_x)][int(start_y)].value = 1
        list_oldx = []
        list_x = []
        list_y = []
        list_oldy = []
        list_oldx.append(int(start_x))
        list_oldy.append(int(start_y))
        temp = 0
        bend_cost = 3
        iteration = 1
        my_object_1[start_x][start_y].block = 0
        my_object_1[int(end_x)][int(end_y)].block = 0

        while my_object_1[int(end_x)][int(end_y)].value == 0:
            if len(list_oldx) == 0 and len(list_oldy) == 0:
                print("NO PATH FOUND IN LAYER 1 MOVING TO LAYER 2")
                layer = 2
                break

            for index_x in list_oldx:
                list_oldy.reverse()
                index_y = list_oldy.pop()
                list_oldy.reverse()
                print(index_x)
                if index_x + 1 <= rows - 1 and my_object_1[index_x][index_y].direction != 'S' and \
                        my_object_1[index_x + 1][
                            index_y].block != 1:
                    if iteration == 1:
                        my_object_1[index_x + 1][index_y].value = 2
                        my_object_1[index_x + 1][index_y].direction = 'N'
                        list_x.append(index_x + 1)
                        list_y.append(index_y)

                    elif my_object_1[index_x][index_y].direction == 'N':
                        temp = my_object_1[index_x][index_y].value + 1

                    else:
                        temp = my_object_1[index_x][index_y].value + bend_cost

                    if iteration != 1:
                        if my_object_1[index_x + 1][index_y].value == 0 or temp <= my_object_1[index_x + 1][
                            index_y].value:
                            my_object_1[index_x + 1][index_y].value = temp
                            my_object_1[index_x + 1][index_y].direction = 'N'
                            list_x.append(index_x + 1)
                            list_y.append(index_y)

                if index_x - 1 >= 0 and my_object_1[index_x][index_y].direction != 'N' and my_object_1[index_x - 1][
                    index_y].block != 1:
                    if iteration == 1:
                        my_object_1[index_x - 1][index_y].value = 2
                        my_object_1[index_x - 1][index_y].direction = 'S'
                        list_x.append(index_x - 1)
                        list_y.append(index_y)

                    elif my_object_1[index_x][index_y].direction == 'S':
                        temp = my_object_1[index_x][index_y].value + 1

                    else:
                        temp = my_object_1[index_x][index_y].value + bend_cost

                    if iteration != 1:
                        if my_object_1[index_x - 1][index_y].value == 0 or temp <= my_object_1[index_x - 1][
                            index_y].value:
                            my_object_1[index_x - 1][index_y].value = temp
                            my_object_1[index_x - 1][index_y].direction = 'S'
                            list_x.append(index_x - 1)
                            list_y.append(index_y)

                if index_y + 1 <= cols - 1 and my_object_1[index_x][index_y].direction != 'E' and my_object_1[index_x][
                    index_y + 1].block != 1:
                    if iteration == 1:
                        my_object_1[index_x][index_y + 1].value = 2
                        my_object_1[index_x][index_y + 1].direction = 'W'
                        list_x.append(index_x)
                        list_y.append(index_y + 1)

                    elif my_object_1[index_x][index_y].direction == 'W':
                        temp = my_object_1[index_x][index_y].value + 1

                    else:
                        temp = my_object_1[index_x][index_y].value + bend_cost

                    if iteration != 1:
                        if my_object_1[index_x][index_y + 1].value == 0 or temp <= my_object_1[index_x][
                            index_y + 1].value:
                            my_object_1[index_x][index_y + 1].value = temp
                            my_object_1[index_x][index_y + 1].direction = 'W'
                            list_x.append(index_x)
                            list_y.append(index_y + 1)

                if index_y - 1 >= 0 and my_object_1[index_x][index_y].direction != 'W' and my_object_1[index_x][
                    index_y - 1].block != 1:

                    if iteration == 1:
                        my_object_1[index_x][index_y - 1].value = 2
                        my_object_1[index_x][index_y - 1].direction = 'E'
                        list_x.append(index_x)
                        list_y.append(index_y - 1)

                    elif my_object_1[index_x][index_y].direction == 'E':
                        temp = my_object_1[index_x][index_y].value + 1

                    else:
                        temp = my_object_1[index_x][index_y].value + bend_cost

                    if iteration != 1:
                        if my_object_1[index_x][index_y - 1].value == 0 or temp <= my_object_1[index_x][
                            index_y - 1].value:
                            my_object_1[index_x][index_y - 1].value = temp
                            my_object_1[index_x][index_y - 1].direction = 'E'
                            list_x.append(index_x)
                            list_y.append(index_y - 1)
            list_oldx = list_x
            list_oldy = list_y
            list_x = []
            iteration += 1
            list_y = []

        # backtracking
        end_y = int(end_y)
        end_x = int(end_x)
        my_object_1[end_x][end_y].block = 1

        turtle.penup()
        if layer == 1:
            turtle.color('black')
            turtle.goto(actual_end_x * 5, actual_end_y * 5)
            turtle.pendown()
            while True:
                turtle.goto(end_x * 5, end_y * 5)
                my_object_1[end_x][end_y].block = 1
                visited = 0
                if my_object_1[end_x][end_y].direction == 'N':
                    end_x -= 1
                    visited = 1
                elif my_object_1[end_x][end_y].direction == 'S':
                    end_x += 1
                    visited = 1
                elif my_object_1[end_x][end_y].direction == 'E':
                    end_y += 1
                    visited = 1
                elif my_object_1[end_x][end_y].direction == 'W':
                    end_y -= 1
                    visited = 1
                my_object_1[end_x][end_y].block = 1

                if end_x == int(start_x) and end_y == int(start_y):
                    turtle.goto(end_x * 5, end_y * 5)
                    turtle.goto(actual_start_x * 5, actual_start_y * 5)
                    turtle.penup()
                    layer = 0
                    break

        for i in range(0, cols):
            for j in range(0, rows):
                my_object_1[i][j].value = 0
                my_object_1[i][j].direction = None

        if layer == 2:

            actual_start_x = int(b[0][0])
            actual_start_y = int(b[0][1])
            actual_end_x = int(b[1][0])
            actual_end_y = int(b[1][1])

            start_x = int(a[0][0])
            start_y = int(a[0][1])
            end_x = int(a[1][0])
            end_y = int(a[1][1])

            list_oldx = []
            list_x = []
            list_y = []
            list_oldy = []
            list_oldx.append(int(start_x))
            list_oldy.append(int(start_y))
            cost = 4
            found_via = 0
            while my_object_1[int(end_x)][int(end_y)].value == 0:
                if len(list_oldx) == 0 and len(list_oldy) == 0 or found_via == 1:
                    print("FINDING VIA SUCCESSFUL")
                    break

                for index_x in list_oldx:
                    list_oldy.reverse()
                    index_y = list_oldy.pop()
                    list_oldy.reverse()

                    if index_x + 1 <= rows - 1 and my_object_1[index_x][index_y].direction != 'S' and \
                            my_object_1[index_x + 1][
                                index_y].block != 1:
                        if iteration == 1:
                            my_object_1[index_x + 1][index_y].value = 2
                            my_object_1[index_x + 1][index_y].direction = 'N'
                            list_x.append(index_x + 1)
                            list_y.append(index_y)

                        elif my_object_1[index_x][index_y].direction == 'N':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x + 1][index_y].value == 0 or temp <= my_object_1[index_x + 1][
                                index_y].value:
                                my_object_1[index_x + 1][index_y].value = temp
                                my_object_1[index_x + 1][index_y].direction = 'N'
                                list_x.append(index_x + 1)
                                list_y.append(index_y)

                    if index_x - 1 >= 0 and my_object_1[index_x][index_y].direction != 'N' and \
                            my_object_1[index_x - 1][
                                index_y].block != 1:
                        if iteration == 1:
                            my_object_1[index_x - 1][index_y].value = 2
                            my_object_1[index_x - 1][index_y].direction = 'S'
                            list_x.append(index_x - 1)
                            list_y.append(index_y)

                        elif my_object_1[index_x][index_y].direction == 'S':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x - 1][index_y].value == 0 or temp <= my_object_1[index_x - 1][
                                index_y].value:
                                my_object_1[index_x - 1][index_y].value = temp
                                my_object_1[index_x - 1][index_y].direction = 'S'
                                list_x.append(index_x - 1)
                                list_y.append(index_y)

                    if index_y + 1 <= cols - 1 and my_object_1[index_x][index_y].direction != 'E' and \
                            my_object_1[index_x][
                                index_y + 1].block != 1:
                        if iteration == 1:
                            my_object_1[index_x][index_y + 1].value = 2
                            my_object_1[index_x][index_y + 1].direction = 'W'
                            list_x.append(index_x)
                            list_y.append(index_y + 1)

                        elif my_object_1[index_x][index_y].direction == 'W':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x][index_y + 1].value == 0 or temp <= my_object_1[index_x][
                                index_y + 1].value:
                                my_object_1[index_x][index_y + 1].value = temp
                                my_object_1[index_x][index_y + 1].direction = 'W'
                                list_x.append(index_x)
                                list_y.append(index_y + 1)

                    if index_y - 1 >= 0 and my_object_1[index_x][index_y].direction != 'W' and my_object_1[index_x][
                        index_y - 1].block != 1:

                        if iteration == 1:
                            my_object_1[index_x][index_y - 1].value = 2
                            my_object_1[index_x][index_y - 1].direction = 'E'
                            list_x.append(index_x)
                            list_y.append(index_y - 1)

                        elif my_object_1[index_x][index_y].direction == 'E':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x][index_y - 1].value == 0 or temp <= my_object_1[index_x][
                                index_y - 1].value:
                                my_object_1[index_x][index_y - 1].value = temp
                                my_object_1[index_x][index_y - 1].direction = 'E'
                                list_x.append(index_x)
                                list_y.append(index_y - 1)

                list_oldx = list_x
                list_oldy = list_y
                list_x = []
                list_y = []
                iteration += 1

                for p in list_oldx:
                    for q in list_oldy:
                        if my_object_1[p][q].value > cost:
                            via_start_x = p
                            via_start_y = q
                            found_via = 1
                            break
                    if found_via == 1:
                        break

            if found_via == 1:
                end_x = via_start_x
                end_y = via_start_y
                turtle.penup()
                turtle.color('black')
                while True:
                    turtle.goto(end_x * 5, end_y * 5)
                    turtle.pendown()
                    my_object_1[end_x][end_y].block = 1
                    if my_object_1[end_x][end_y].direction == 'N':
                        end_x -= 1
                    elif my_object_1[end_x][end_y].direction == 'S':
                        end_x += 1
                    elif my_object_1[end_x][end_y].direction == 'E':
                        end_y += 1
                    elif my_object_1[end_x][end_y].direction == 'W':
                        end_y -= 1

                    if end_x == int(start_x) and end_y == int(start_y):
                        turtle.goto(end_x * 5, end_y * 5)
                        my_object_1[end_x][end_y].block = 1
                        turtle.goto(actual_start_x * 5, actual_start_y * 5)
                        my_object_1[actual_start_x][actual_start_y].block = 1
                        turtle.penup()
                        layer = 2
                        break

            start_x = int(a[1][0])
            start_y = int(a[1][1])
            end_x = int(a[0][0])
            end_y = int(a[0][1])

            list_oldx = []
            list_x = []
            list_y = []
            list_oldy = []
            list_oldx.append(int(start_x))
            list_oldy.append(int(start_y))
            cost = 4
            found_via = 0

            while my_object_1[int(end_x)][int(end_y)].value == 0:
                if len(list_oldx) == 0 and len(list_oldy) == 0 or found_via == 1:
                    print("FINDING VIA SUCCESSFUL")
                    break

                for index_x in list_oldx:
                    list_oldy.reverse()
                    index_y = list_oldy.pop()
                    list_oldy.reverse()

                    if index_x + 1 <= rows - 1 and my_object_1[index_x][index_y].direction != 'S' and \
                            my_object_1[index_x + 1][
                                index_y].block != 1:
                        if iteration == 1:
                            my_object_1[index_x + 1][index_y].value = 2
                            my_object_1[index_x + 1][index_y].direction = 'N'
                            list_x.append(index_x + 1)
                            list_y.append(index_y)

                        elif my_object_1[index_x][index_y].direction == 'N':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x + 1][index_y].value == 0 or temp <= my_object_1[index_x + 1][
                                index_y].value:
                                my_object_1[index_x + 1][index_y].value = temp
                                my_object_1[index_x + 1][index_y].direction = 'N'
                                list_x.append(index_x + 1)
                                list_y.append(index_y)

                    if index_x - 1 >= 0 and my_object_1[index_x][index_y].direction != 'N' and \
                            my_object_1[index_x - 1][
                                index_y].block != 1:
                        if iteration == 1:
                            my_object_1[index_x - 1][index_y].value = 2
                            my_object_1[index_x - 1][index_y].direction = 'S'
                            list_x.append(index_x - 1)
                            list_y.append(index_y)

                        elif my_object_1[index_x][index_y].direction == 'S':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x - 1][index_y].value == 0 or temp <= my_object_1[index_x - 1][
                                index_y].value:
                                my_object_1[index_x - 1][index_y].value = temp
                                my_object_1[index_x - 1][index_y].direction = 'S'
                                list_x.append(index_x - 1)
                                list_y.append(index_y)

                    if index_y + 1 <= cols - 1 and my_object_1[index_x][index_y].direction != 'E' and \
                            my_object_1[index_x][
                                index_y + 1].block != 1:
                        if iteration == 1:
                            my_object_1[index_x][index_y + 1].value = 2
                            my_object_1[index_x][index_y + 1].direction = 'W'
                            list_x.append(index_x)
                            list_y.append(index_y + 1)

                        elif my_object_1[index_x][index_y].direction == 'W':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x][index_y + 1].value == 0 or temp <= my_object_1[index_x][
                                index_y + 1].value:
                                my_object_1[index_x][index_y + 1].value = temp
                                my_object_1[index_x][index_y + 1].direction = 'W'
                                list_x.append(index_x)
                                list_y.append(index_y + 1)

                    if index_y - 1 >= 0 and my_object_1[index_x][index_y].direction != 'W' and my_object_1[index_x][
                        index_y - 1].block != 1:

                        if iteration == 1:
                            my_object_1[index_x][index_y - 1].value = 2
                            my_object_1[index_x][index_y - 1].direction = 'E'
                            list_x.append(index_x)
                            list_y.append(index_y - 1)

                        elif my_object_1[index_x][index_y].direction == 'E':
                            temp = my_object_1[index_x][index_y].value + 1

                        else:
                            temp = my_object_1[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_1[index_x][index_y - 1].value == 0 or temp <= my_object_1[index_x][
                                index_y - 1].value:
                                my_object_1[index_x][index_y - 1].value = temp
                                my_object_1[index_x][index_y - 1].direction = 'E'
                                list_x.append(index_x)
                                list_y.append(index_y - 1)

                list_oldx = list_x
                list_oldy = list_y
                found_via = 0
                for p in list_x:
                    for q in list_y:
                        if my_object_1[p][q].value > cost:
                            via_end_x = p
                            via_end_y = q
                            found_via = 1
                            break
                    if found_via == 1:
                        break

                list_x = []
                iteration += 1
                list_y = []

            if found_via == 1:
                end_x = via_end_x
                end_y = via_end_y
                turtle.penup()
                turtle.color('black')
                while True:
                    turtle.goto(end_x * 5, end_y * 5)
                    turtle.pendown()
                    my_object_1[end_x][end_y].block = 1
                    if my_object_1[end_x][end_y].direction == 'N':
                        end_x -= 1
                    elif my_object_1[end_x][end_y].direction == 'S':
                        end_x += 1
                    elif my_object_1[end_x][end_y].direction == 'E':
                        end_y += 1
                    elif my_object_1[end_x][end_y].direction == 'W':
                        end_y -= 1

                    if end_x == int(start_x) and end_y == int(start_y):
                        turtle.goto(end_x * 5, end_y * 5)
                        my_object_1[end_x][end_y].block = 1
                        turtle.goto(actual_end_x * 5, actual_end_y * 5)
                        my_object_1[actual_end_x][actual_end_y].block = 1
                        turtle.penup()
                        layer = 2
                        break

            start_x = via_start_x
            start_y = via_start_y
            end_x = via_end_x
            end_y = via_end_y

            my_object_2[int(start_x)][int(start_y)].value = 1
            list_oldx = []
            list_x = []
            list_y = []
            list_oldy = []
            list_oldx.append(int(start_x))
            list_oldy.append(int(start_y))
            temp = 0
            bend_cost = 3
            iteration = 1

            while my_object_2[int(end_x)][int(end_y)].value == 0:
                if len(list_oldx) == 0 and len(list_oldy) == 0:
                    print("NO PATH FOUND IN LAYER 2")
                    layer = 0
                    break

                for index_x in list_oldx:
                    list_oldy.reverse()
                    index_y = list_oldy.pop()
                    list_oldy.reverse()

                    if index_x + 1 <= rows - 1 and my_object_2[index_x][index_y].direction != 'S' and \
                            my_object_2[index_x + 1][
                                index_y].block != 1:
                        if iteration == 1:
                            my_object_2[index_x + 1][index_y].value = 2
                            my_object_2[index_x + 1][index_y].direction = 'N'
                            list_x.append(index_x + 1)
                            list_y.append(index_y)

                        elif my_object_2[index_x][index_y].direction == 'N':
                            temp = my_object_2[index_x][index_y].value + 1

                        else:
                            temp = my_object_2[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_2[index_x + 1][index_y].value == 0 or temp <= my_object_2[index_x + 1][
                                index_y].value:
                                my_object_2[index_x + 1][index_y].value = temp
                                my_object_2[index_x + 1][index_y].direction = 'N'
                                list_x.append(index_x + 1)
                                list_y.append(index_y)

                    if index_x - 1 >= 0 and my_object_2[index_x][index_y].direction != 'N' and my_object_2[index_x - 1][
                        index_y].block != 1:
                        if iteration == 1:
                            my_object_2[index_x - 1][index_y].value = 2
                            my_object_2[index_x - 1][index_y].direction = 'S'
                            list_x.append(index_x - 1)
                            list_y.append(index_y)

                        elif my_object_2[index_x][index_y].direction == 'S':
                            temp = my_object_2[index_x][index_y].value + 1

                        else:
                            temp = my_object_2[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_2[index_x - 1][index_y].value == 0 or temp <= my_object_2[index_x - 1][
                                index_y].value:
                                my_object_2[index_x - 1][index_y].value = temp
                                my_object_2[index_x - 1][index_y].direction = 'S'
                                list_x.append(index_x - 1)
                                list_y.append(index_y)

                    if index_y + 1 <= cols - 1 and my_object_2[index_x][index_y].direction != 'E' and \
                            my_object_2[index_x][
                                index_y + 1].block != 1:
                        if iteration == 1:
                            my_object_2[index_x][index_y + 1].value = 2
                            my_object_2[index_x][index_y + 1].direction = 'W'
                            list_x.append(index_x)
                            list_y.append(index_y + 1)

                        elif my_object_2[index_x][index_y].direction == 'W':
                            temp = my_object_2[index_x][index_y].value + 1

                        else:
                            temp = my_object_2[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_2[index_x][index_y + 1].value == 0 or temp <= my_object_2[index_x][
                                index_y + 1].value:
                                my_object_2[index_x][index_y + 1].value = temp
                                my_object_2[index_x][index_y + 1].direction = 'W'
                                list_x.append(index_x)
                                list_y.append(index_y + 1)

                    if index_y - 1 >= 0 and my_object_2[index_x][index_y].direction != 'W' and my_object_2[index_x][
                        index_y - 1].block != 1:

                        if iteration == 1:
                            my_object_2[index_x][index_y - 1].value = 2
                            my_object_2[index_x][index_y - 1].direction = 'E'
                            list_x.append(index_x)
                            list_y.append(index_y - 1)

                        elif my_object_2[index_x][index_y].direction == 'E':
                            temp = my_object_2[index_x][index_y].value + 1

                        else:
                            temp = my_object_2[index_x][index_y].value + bend_cost

                        if iteration != 1:
                            if my_object_2[index_x][index_y - 1].value == 0 or temp <= my_object_2[index_x][
                                index_y - 1].value:
                                my_object_2[index_x][index_y - 1].value = temp
                                my_object_2[index_x][index_y - 1].direction = 'E'
                                list_x.append(index_x)
                                list_y.append(index_y - 1)
                list_oldx = list_x
                list_oldy = list_y
                list_x = []
                iteration += 1
                list_y = []
       	    print("backtracking1")
            # backtracking
            end_y = int(end_y)
            end_x = int(end_x)
            my_object_2[end_x][end_y].block = 1

            while True:
                turtle.goto(end_x*5, end_y*5)
                turtle.color('blue')
                turtle.pendown()
                my_object_2[end_x][end_y].block = 1
                if my_object_2[end_x][end_y].direction == 'N':
                    end_x -= 1
                elif my_object_2[end_x][end_y].direction == 'S':
                    end_x += 1
                elif my_object_2[end_x][end_y].direction == 'E':
                    end_y += 1
                elif my_object_2[end_x][end_y].direction == 'W':
                    end_y -= 1

                if end_x == int(start_x) and end_y == int(start_y):
                    turtle.goto(end_x * 5, end_y * 5)
                    turtle.penup()
                    my_object_2[end_x][end_y].block = 1
                    layer = 0
                    break

            for i in range(0, cols):
                for j in range(0, rows):
                    my_object_2[i][j].value = 0
                    my_object_2[i][j].direction = None

turtle.resizemode("auto")
ts = turtle.getscreen()

ts.getcanvas().postscript(file="duck.eps")
turtle.done()
