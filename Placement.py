from __future__ import print_function
import numpy as np
import math
import random
import copy
import turtle

# TEST CASE - 1
adjacency_list = np.array([[0, 1, 2, 3, 2],
                           [1, 0, 1, 4, 2],
                           [2, 1, 0, 3, 2],
                           [3, 4, 3, 0, 4],
                           [2, 2, 2, 4, 0]])

# TEST CASE - 2
#adjacency_list = np.array([[0,0,0,1,1,0,0,0],
#                            [0,0,0,0,1,1,0,0],
#                            [0,0,0,0,0,1,0,0],
#                            [1,0,0,0,0,0,1,0],
#                            [1,1,0,0,0,0,1,0],
#                            [0,1,1,0,0,0,0,1],
#                            [0,0,0,1,1,0,0,0],
#                            [0,0,0,0,0,1,0,0]])
#

# TEST CASE - 3
# adjacency_list = np.array([[0,1,0,0,0,0],
#                           [1,0,1,1,0,0],
#                           [0,1,0,0,0,0],
#                           [0,1,0,0,1,1],
#                           [0,0,0,1,0,1],
#                           [0,0,0,1,1,0]])


user_input = raw_input("Input from Input.txt file? Press no to run from inbuilt test case. (Yes/No) = ")
if user_input == 'yes' or user_input == 'Yes':
    input_file = open('Input.txt', mode='r')
    adjacency_list = []
    for line in input_file:
        line = line.replace('\n', '')
        line = line.split(' ')
        line_size = len(line)
        if line[line_size - 1] == '':
            del line[line_size - 1]
        line = list(map(int, line))
        adjacency_list.append(line)

rotate = int(raw_input("Is rotation allowed? (Ans '1' if allowed else '0') = "))


def cost(polish_exp, dim_list, rotate):
    class node:

        def __init__(self, data, dim):

            self.left = None
            self.right = None
            self.data = data
            self.dim = dim
            self.coordinates = 0

        def postorder(self):

            if self.left is not None:
                self.left.postorder()
            if self.right is not None:
                self.right.postorder()
            print(self.data, ':', self.dim, ':', self.coordinates, end='')

        def left_insert(self, data, dim):

            if self.left is None:
                if type(data) == str:
                    self.left = node(data, dim)
                else:
                    self.left = data

        def right_insert(self, data, dim):

            if self.right is None:
                if type(data) == str:
                    self.right = node(data, dim)
                else:
                    self.right = data

    def construct_slicing_tree(polish_exp, eval_list):
        nodes_list = []
        j = 0
        for i in polish_exp:
            if not i.isalpha():
                nodes_list.append(i)
            else:
                a = nodes_list.pop()
                b = nodes_list.pop()
                root = node(i, eval_list[j])
                if type(b) == str:
                    root.left_insert(b, eval_list[polish_exp.index(b)])
                else:
                    root.left_insert(b, 0)
                if type(a) == str:
                    root.right_insert(a, eval_list[polish_exp.index(a)])
                else:
                    root.right_insert(a, 0)
                nodes_list.append(root)
            j = j + 1
        root = nodes_list.pop()
        return root

    def minimum_area(polish_exp):
        nodes_list = []
        nodes_list_1 = []
        for i in polish_exp:
            if not i.isalpha():
                if rotate == 0:
                    nodes_list.append([dim_list[int(i) - 1]])
                    nodes_list_1.append([dim_list[int(i) - 1]])
                else:
                    p = []
                    q = dim_list[int(i) - 1]
                    r = copy.deepcopy(dim_list[int(i) - 1])
                    p.append(q)
                    r.reverse()
                    if r not in p:
                        p.append(r)
                    nodes_list.append(p)
                    nodes_list_1.append(p)

            else:
                a = nodes_list.pop()
                b = nodes_list.pop()
                a.sort(key=lambda x: x[0])
                b.sort(key=lambda x: x[0])
                a.reverse()
                b.reverse()
                j = 0
                k = 0
                evaluated_dim = []
                dimensions = []
                if i == 'H':
                    while j < len(a) and k < len(b):
                        if a[j][0] >= b[k][0]:
                            evaluated_dim.append([a[j][0], a[j][1] + b[k][1]])
                            j = j + 1
                        else:
                            evaluated_dim.append([b[k][0], a[j][1] + b[k][1]])
                            k = k + 1
                else:
                    while j < len(a) and k < len(b):
                        if a[j][1] >= b[k][1]:
                            evaluated_dim.append([a[j][0] + b[k][0], a[j][1]])
                            j = j + 1
                        else:
                            evaluated_dim.append([a[j][0] + b[k][0], b[k][1]])
                            k = k + 1
                nodes_list_1.append(evaluated_dim)
                nodes_list.append(evaluated_dim)
        nodes_list = nodes_list.pop()
        j = 0
        for i in nodes_list:
            area = i[0] * i[1]
            if nodes_list.index(i) == 0:
                min_area = area
                j = i
            elif area < min_area:
                min_area = area
                j = i
        return min_area, nodes_list_1, j

    def find_min_block_dim(root, min_dim, sizes):
        stack = []
        stack.append([root, min_dim])
        while len(stack) != 0:
            x = stack.pop()
            root = x[0]
            min_dim = x[1]
            root.dim = min_dim
            root.coordinates = [x / 2 for x in min_dim]
            flag = 0
            if root.data == 'H':
                a = root.left.dim
                b = root.right.dim
                for i in a:
                    for j in b:
                        dim = [max([i[0], j[0]]), i[1] + j[1]]
                        if min_dim == dim:
                            stack.append([root.left, i])
                            stack.append([root.right, j])
                            flag = 1
                            break
                    if flag == 1:
                        break
            elif root.data == 'V':
                a = root.left.dim
                b = root.right.dim
                for i in a:
                    for j in b:
                        dim = [i[0] + j[0], max([i[1], j[1]])]
                        if min_dim == dim:
                            stack.append([root.left, i])
                            stack.append([root.right, j])
                            flag = 1
                            break
                    if flag == 1:
                        break
            else:
                sizes[int(root.data) - 1] = min_dim
                root.dim = min_dim
                root.coordinates = [x / 2 for x in min_dim]

    def find_coordinates(root, coordinates):
        stack = []
        stack.append([root, [0, 0]])
        while len(stack) != 0:
            x = stack.pop()
            root = x[0]
            change_W = x[1][0]
            change_H = x[1][1]
            if root.data == 'H':
                a = root.left.dim
                b = root.right.coordinates
                c = root.left.coordinates
                root.right.coordinates = [b[0] + change_W, b[1] + a[1] + change_H]
                root.left.coordinates = [c[0] + change_W, c[1] + change_H]
                stack.append([root.left, [change_W, change_H]])
                change_H = change_H + a[1]
                stack.append([root.right, [change_W, change_H]])
            elif root.data == 'V':
                a = root.left.dim
                b = root.right.coordinates
                c = root.left.coordinates
                root.right.coordinates = [b[0] + a[0] + change_W, b[1] + change_H]
                root.left.coordinates = [c[0] + change_W, c[1] + change_H]
                stack.append([root.left, [change_W, change_H]])
                change_W = change_W + a[0]
                stack.append([root.right, [change_W, change_H]])
            else:
                coordinates[int(root.data) - 1] = root.coordinates

    [cost_area, nodes_list, min_dim] = minimum_area(polish_exp)
    root = construct_slicing_tree(polish_exp, nodes_list)
    root1 = root
    find_min_block_dim(root, min_dim, dim_list)
    dimensions = copy.deepcopy(dim_list)
    find_coordinates(root1, dim_list)

    HPWL = 0
    for i in range(1, len(adjacency_list) + 1):
        x = []
        y = []
        weight = 0
        x.append(dim_list[i - 1][0])
        y.append(dim_list[i - 1][1])
        for j in range(1, len(adjacency_list) + 1):
            if adjacency_list[i - 1][j - 1] != 0:
                weight = weight + adjacency_list[i - 1][j - 1]
                x.append(dim_list[j - 1][0])
                y.append(dim_list[j - 1][1])
        min_x = min(x)
        max_x = max(x)
        min_y = min(y)
        max_y = max(y)
        HPWL = HPWL + weight * (max_x + max_y - min_x - min_y)

    return HPWL, cost_area, dim_list, dimensions, min_dim


#polish_exp = "12H34H5H67HVH"
#dim_list = [[6, 4], [4, 4], [4, 3], [4, 4], [3, 4], [4, 4]]#, [8, 8], [6, 4], [3, 4], [6, 6], [5, 6], [6, 3], [3, 3],
#           [4, 4]]
output = open('Output.txt', 'w')
dim_list=[[8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [8, 5], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [3, 2], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [4, 3], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [5, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 4], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5], [6, 5]]

# Enable if random dimensions want to be assigned
# dim_list = []
# for i in range(0, len(adjacency_list)):
#     x = []
#     x.append(random.randint(1, 10))
#     x.append(random.randint(1, 10))
#     dim_list.append(x)
#
polish_exp = []
for j in range(1,20):
	for i in range(len(adjacency_list)*(j-1)/19+1 , int(len(adjacency_list)*j/19+1)):
    		polish_exp.append(str(i))
	for i in range(0, len(adjacency_list)/19 - 1):
    		if random.uniform(0, 1) < 0.5:
        		polish_exp.append("V")
    	else:
        	polish_exp.append("H")
print(polish_exp)



extra_width = []
for i in range(0, len(adjacency_list)):
    count = 0
    for j in range(0, len(adjacency_list)):
        if adjacency_list[i][j] > 0:
            count += 1
    dim_list[i][0] += int(len(adjacency_list)/4 * count)
    dim_list[i][1] += int(len(adjacency_list)/4 * count)
    extra_width.append(count)

print("LIST OF SIZES OF BLOCKS", file=output)
for i in range(0, len(dim_list)):
    print("BLOCK ", i + 1, ",", "SIZE =", dim_list[i], file=output)
if rotate == 1:
    print("ROTATION ENABLED", file=output)
else:
    print("ROTATION DISABLED", file=output)


# finding neighbourhood structure
def move_m1(polish_exp):
    indices = []
    indices2 = []
    length = len(polish_exp)
    for i in range(0, length):
        if (i != length - 1 and polish_exp[i].isdigit() and polish_exp[i + 1].isdigit()):
            indices.append(i)
            i += 1
        elif (i < length - 2 and polish_exp[i].isdigit() and polish_exp[i + 1].isalpha() and polish_exp[
            i + 2].isdigit()):
            indices2.append(i)
            i += 1
    indicesfinal = indices + indices2
    random_index = random.randint(0, len(indicesfinal) - 1)
    polish_exp = list(polish_exp)
    if indicesfinal[random_index] in indices:
        temp = polish_exp[indicesfinal[random_index]]
        polish_exp[indicesfinal[random_index]] = polish_exp[indicesfinal[random_index] + 1]
        polish_exp[indicesfinal[random_index] + 1] = temp
    else:
        temp = polish_exp[indicesfinal[random_index]]
        polish_exp[indicesfinal[random_index]] = polish_exp[indicesfinal[random_index] + 2]
        polish_exp[indicesfinal[random_index] + 2] = temp
    return polish_exp


def move_m2(polish_exp):
    indices = []
    i = 0
    length = len(polish_exp)
    while i != length - 1:
        if (polish_exp[i].isalpha() and polish_exp[i + 1].isalpha()):
            indices.append(i)
            while i != length - 1 and polish_exp[i].isdigit() != 1:
                i = i + 1
        else:
            i = i + 1
    if indices == []:
        return polish_exp

    else:
        random_index = random.randint(0, len(indices) - 1)
        polish_exp = list(polish_exp)
        j = indices[random_index]
        while j != length and polish_exp[j].isdigit() != 1:
            if polish_exp[j] == 'H':
                polish_exp[j] = 'V'
            else:
                polish_exp[j] = 'H'
            j = j + 1
        return polish_exp;


def move_m3(polish_exp):
    polish_old = polish_exp
    indices = []
    length = len(polish_exp)
    for i in range(0, length):
        if (i != length - 1 and (
                polish_exp[i].isalpha() and polish_exp[i + 1].isdigit() or polish_exp[i].isdigit() and polish_exp[
            i + 1].isalpha())):
            indices.append(i)
    random_index = random.randint(0, len(indices) - 1)
    polish_exp = list(polish_exp)
    temp = polish_exp[indices[random_index]]
    polish_exp[indices[random_index]] = polish_exp[indices[random_index] + 1]
    polish_exp[indices[random_index] + 1] = temp
    valid_var = valid_polish(polish_exp, indices[random_index])
    if valid_var != 1:
        polish_exp = move_m2(polish_old)

    return polish_exp


# this function checks if given polish expression is valid or not
def valid_polish(polish_exp, swap_pos):
    valid = 1
    count = 0
    for i in range(0, swap_pos + 1):
        if polish_exp[i].isalpha() == 1:
            count += 1

    for i in range(0, len(polish_exp)):
        if i != len(polish_exp) - 1 and polish_exp[i] == 'H' and polish_exp[i + 1] == 'H' or i != len(
                polish_exp) - 1 and polish_exp[i] == 'V' and polish_exp[i + 1] == 'V':
            valid = 0
            break
    if 2 * count < swap_pos + 1 and valid == 1:
        return 1
    else:
        return 0


# setting initial temperature
costarray = []
[HPWL, initial_cost, coordinates, dimensions, min_dim] = cost(polish_exp, copy.deepcopy(dim_list), rotate)
costarray.append(initial_cost)
for i in range(0, 3):
    random_num = random.uniform(0, 1)
    if random_num < 0.4:
        polish_expnew = move_m1(polish_exp)

    elif random_num < 0.8:
        polish_expnew = move_m2(polish_exp)

    else:
        polish_expnew = move_m3(polish_exp)

    polish_exp = polish_expnew
    [HPWL, new_cost, coordinates, dimensions, min_dim] = cost(polish_expnew, copy.deepcopy(dim_list), rotate)

    costarray.append(new_cost)
    sum = 0
for j in range(0, 3):
    sum += abs(costarray[j] - costarray[j + 1])
delta_ave = sum / 3
initial_temp = -delta_ave / math.log(0.9)
if initial_temp == 0:
    initial_temp = 100 * len(adjacency_list)

print("initial_temp=", initial_temp)


def SA(polish_exp, initial_temp):
    temp = initial_temp
    polish_expold = polish_exp
    total_attempts = 0

    # iterations
    while (1):
        uphill_moves = 0
        accepted_moves = 0
        max_iterations_per_temperature = 200
        for q in range(0, max_iterations_per_temperature):

            total_attempts += 1
            [HPWL, F_old, coordinates, dimensions, min_dim] = cost(polish_exp, copy.deepcopy(dim_list), rotate)

            random_num = random.uniform(0, 1)
            if random_num < 0.4:
                polish_expnew = move_m1(polish_exp)

            elif random_num < 0.8:
                polish_expnew = move_m2(polish_exp)

            else:
                polish_expnew = move_m3(polish_exp)

            [HPWL1, F_new, coordinates, dimensions, min_dim] = cost(polish_expnew, copy.deepcopy(dim_list), rotate)

            delta = F_new - F_old + 0.1 * (HPWL1 - HPWL)

            if ((delta <= 0) or ((delta > 0) and (np.random.uniform() < math.exp(-delta / temp)))):
                if delta > 0:
                    uphill_moves += 1
                polish_exp = polish_expnew
                accepted_moves += 1
            else:
                polish_exp = polish_expold

        temp = 0.95 * temp
        if (accepted_moves < 0.1 * max_iterations_per_temperature) or (temp < 0.01) or total_attempts >= 100000:
            break

    return polish_exp


final_expression = SA(polish_exp, initial_temp)
print("Final Polish Expression", final_expression)

[HPWL, cost_area, coordinates, dimensions, min_dim] = cost(final_expression, copy.deepcopy(dim_list), rotate)
for i in range(0, len(adjacency_list)):
    dimensions[i][0] -= int(len(adjacency_list)/4 * extra_width[i])
    dimensions[i][1] -= int(len(adjacency_list)/4 * extra_width[i])

print("HPWL=", HPWL)
print("Area=", cost_area)
print("Coordinates=", coordinates)
print("Dimensions=", dimensions)
print("Blocksize=", min_dim)

np.save("coordinates", np.array(coordinates))
np.save("dimensions", np.array(dimensions))
np.save("min_dim", np.array(min_dim))
np.save("adjacency_list", np.array(adjacency_list))

window_dim=np.max(coordinates,axis=0)
turtle.ht()
turtle.Screen().setup(width=1.0,height=1.0)
turtle.setworldcoordinates(1,-1,window_dim[0]+100,window_dim[1]+100)

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
ts = turtle.getscreen()
turtle.resizemode("auto")
ts.getcanvas().postscript(file="duck.eps")
turtle.done()
