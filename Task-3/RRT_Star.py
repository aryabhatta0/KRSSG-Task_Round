max_iteration = 10000     #shows path after max iteration
Step = 2
search_radius = 5
port = 5555

import cv2
import random
import math
import socket

#loading image
img = cv2.imread("images/image1.png", 1)
img = cv2.resize(img, (300,300))
l,m,_ = img.shape 

#defining colour
white = [255,255,255]
red = [0,0,255]
blue = [255,0,0]
black = [0,0,0]
green = [0,255,0]

#manipulating image
for i in range(l):
    for j in range(m):
        if img[i][j][0] > 150 and img[i][j][1] > 150 and img[i][j][2] > 150:  #w
            img[i][j][0] = 255         #for loop ?
            img[i][j][1] = 255
            img[i][j][2] = 255
        elif img[i][j][1] > 170 and img[i][j][0] < 50 and img[i][j][2] < 50:  #g
            img[i][j][1] = 255
            img[i][j][0] = 0
            img[i][j][2] = 0
            start = (i,j)
        elif img[i][j][2] > 170 and img[i][j][0] < 50 and img[i][j][1] < 50:    #r
            img[i][j][2] = 255
            img[i][j][0] = 0
            img[i][j][1] = 0
        #elif img[i][j][0] < 50 and img[i][j][1] < 50 and img[i][j][2] < 50: #black
        elif img[i][j][0] > 170 and img[i][j][1] < 50 and img[i][j][2] < 50:
            img[i][j][0] = 255
            img[i][j][1] = 0
            img[i][j][2] = 0
        else:   #black
            img[i][j][0] = 0
            img[i][j][1] = 0
            img[i][j][2] = 0

#finding start and end
switch1 = True
switch2 = True
for i in range(l):
    for j in range(m):
        if switch1:
            if (img[i][j] == green).all():
                start = (i,j)
                switch1 = False
        if switch2:
            if (img[i][j] == red).all():
                end = (i,j)
                switch2 = False
print(start, end)

#######################################################

class Node():
    def __init__(self, index, cost= math.inf, parent = None):
        self.index = index
        self.cost = cost
        self.parent = parent

#func to sample a random point
def random_point():
    x = int(random.random() * l)
    y = int(random.random() * m)

    return (x,y)     #tupple

#func to find distance b/w 2 index
def dist(p1,p2):
    x1,y1 = p1
    x2,y2 = p2

    return (math.sqrt((x2-x1)**2 + (y2-y1)**2))

def is_valid(point):
    if (point[0]>=0 and point[0]<l) and (point[1]>=0 and point[1]<m):
        return True
    return False

def obstacle_free(x):
    for i in range(-10,11):
        for j in range(-10,11):
            point = (x[0] + i, x[1] + j)
            if is_valid(point):     #point should be valid
                if (img[point][0] == white[0] and img[point][1] == white[1] and img[point][2] == white[2]):   #white ho toh? #black/red/green na ho toh?
                    return False
    return True

#func to find nearest vertex of tree from x_rand
def nearest(vertex, x_rand):
    min = math.inf
    x_nearest = (-1, -1)
    for ver in vertex:
        #print(ver,x_rand)
        s = dist(ver,x_rand)
        if s < min:
            min = s
            x_nearest = ver
    return x_nearest


def steer(x_nearest, x_rand):
    x_n, y_n = x_nearest
    x, y = x_rand
    global Step
    if dist(x_nearest,x_rand) < Step:
        return x_rand

    if x_n != x:
        theta = math.atan( (y_n-y) / (x_n-x) )
    else:
        theta = math.pi
    #print(theta)
    a = int(x_n + Step * math.cos(theta))
    b = int(y_n + Step * math.sin(theta))

    return (a,b)

def swap(a,b):
    temp = a
    a = b
    b = temp

    return a,b

def obst_free_path(x_nearest, x_new):
    if obstacle_free(x_nearest) and obstacle_free(x_new):
        return True
    return False

#func to return the neighbour nodes of x_new
def near(vertex, x_new):
    x,y = x_new
    x_near = []
    for vert in vertex:
        if dist(vert,x_new) <=  search_radius:
            if obst_free_path(vert,x_new):                          #
                x_near.append(vert)

    return x_near

#func to choose parent leading to lowest cost
def choose_parent(tree,vertex, x_near, x_nearest, x_new):
    min_cost = tree[vertex.index(x_new)].cost
    x_parent = x_nearest

    for neighbour in x_near:
        c = tree[vertex.index(neighbour)].cost + dist(neighbour, x_new)
        if c < min_cost:
            min_cost = c
            x_parent = neighbour

    return x_parent

def rewire(tree,vertex, x_near, x_parent, x_new):
    for node in x_near:
        c1 = tree[vertex.index(node)].cost      #direct cost
        c2 = tree[vertex.index(x_new)].cost + dist(x_new,node)    #cost via x_new
        if c1 > c2:    #needs some update
            tree[vertex.index(node)].cost = c2
            tree[vertex.index(node)].parent = tree[vertex.index(x_new)]


#func to extend the graph towards x_rand, if possible (returns a boolean too for the same)
c = 0
def extend(tree,vertex, x_rand):
    x,y = x_rand
    global c
    c += 1

    x_nearest = nearest(vertex, x_rand)
    x_new = steer(x_nearest, x_rand)   #good is to ensure x_new is valid & path obstacle free

    if obst_free_path(x_nearest, x_new):
        #print(c,":",x_nearest, x_new)
        #if c > 500:
        #    exit()
        new_node = Node(x_new, cost= (tree[vertex.index(x_nearest)].cost + dist(x_nearest,x_new)), parent= tree[vertex.index(x_nearest)])   #x_nearest is not node but vertex
        tree.append(new_node)
        vertex.append(x_new)

        #searching for better parent
        x_near = near(vertex, x_new)   #returns a list containing neighbours of x_new

        x_parent = choose_parent(tree,vertex, x_near, x_nearest, x_new)       #node having least cost to go through to x_new
        new_node.parent = tree[vertex.index(x_parent)] 

        #rewiring the tree
        rewire(tree,vertex, x_near, x_parent, x_new)

        return x_new, True 
    else:
        return x_new, False

def show_path(tree,vertex,current_node,final_node, img, flag= 0):
    #t=0  
    path = []
    while current_node != final_node:
        #t+=1
        #print("t=",t)
        x1,y1 = current_node.index
        path.append((x1,y1))
        #x2,y2 = current_node.parent.index       
        try:
            x2,y2 = current_node.parent.index        #as final can be sth othe than end_node?
        except:
            return img, path
        
        img[x1][y1][0] = 0
        img[x1][y1][1] = 0
        img[x1][y1][2] = 255
        
        current_node = current_node.parent

    return img, path

#checks if the two points are near
def is_near(p1,p2):
    if dist(p1,p2) <= search_radius:  #kaafi bada hai smooth path mein gadbad naa aa jaye
        if obst_free_path(p1, p2):
            return True
    return False

def nearest_common(vertex1,vertex2):
    min = math.inf
    for v1 in vertex1:
        for v2 in vertex2:
            if dist(v1,v2) < min:
                a = v1
                b = v2
    return a,b


def RRTStar_Connect(start, end, img):

    #from start
    tree1 = []
    vertex1 = []
    #from end
    tree2 = []
    vertex2 = []

    #initialize
    start_node = Node(start, 0)
    tree1.append(start_node)
    vertex1.append(start)

    end_node = Node(end, 0)
    tree2.append(end_node)
    vertex2.append(end)

    for n in range(max_iteration):
        print("n=",n)
        x_rand = random_point()

        #checks for validity of x_rand (wrt vertex1)
        while x_rand in vertex1 or not obstacle_free(x_rand):
            x_rand = random_point()
        
        x_new, msg = extend(tree1,vertex1, x_rand)
 
        if msg == True:
            x,y = x_new
            img[x][y][0] = 0
            img[x][y][1] = 255
            img[x][y][2] = 0
            #if is_near(x_new, end):
            if (img[x][y][0],img[x][y][1],img[x][y][2]) == (0,0,255):
                print("Goal found... Total iteration:",n)
                img,path = show_path(tree1,vertex1, tree1[vertex1.index(x_new)],start_node, img,0)
                return img, path
        
    print("After max iteration...")
    img, path = show_path(tree1, vertex1, tree1[vertex1.index(nearest(vertex1,end))],start_node, img)
    return img, path

img, path = RRTStar_Connect(start, end, img)

cv2.namedWindow("RRT_Star", cv2.WINDOW_NORMAL)
cv2.imshow("RRT_Star", img)
cv2.waitKey(0)


######################################___turle
rrt = socket.socket()
rrt.bind(('localhost',port))

rrt.listen(1)
print('Waiting for turtle!')

turtle, addr = rrt.accept()
print('Connected with turtle' + addr[0] + "  " + str(addr[1]))

turtle.send(str(path).encode())

cv2.destroyAllWindows()
