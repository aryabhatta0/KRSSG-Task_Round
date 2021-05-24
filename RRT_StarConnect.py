#parameters
max_iteration = 5000
Step = 10
search_radius = 20
dist_away = 10       #how much pixel to be away from obstacle
port = 5555

import cv2 
import math
import random
import socket

img = cv2.imread("image1.png",1)
img = cv2.resize(img, (300,300))
l,m,_ = img.shape
print(l,m)

white = [255,255,255]
red = [0,0,255]
green = [0,255,0]

#finding start and end
switch1 = True
switch2 = True
for i in range(l):
    for j in range(m):
        if img[i][j][0] > 150 and img[i][j][1] > 150 and img[i][j][2] > 150:  #white
            img[i][j][0] = 255         
            img[i][j][1] = 255
            img[i][j][2] = 255
        elif img[i][j][0] < 50 and img[i][j][1] > 150 and img[i][j][2] < 50:  #green
            img[i][j][0] = 0
            img[i][j][1] = 255
            img[i][j][2] = 0
            if switch1:
                start = (i,j)     #start
                switch1 = False
        elif img[i][j][0] < 50 and img[i][j][1] < 50 and img[i][j][2] > 150:    #red
            img[i][j][0] = 0
            img[i][j][1] = 0
            img[i][j][2] = 255
            if switch2:
                end = (i,j)
                switch2 = False
        else:                                                                  #black
            img[i][j][0] = 0
            img[i][j][1] = 0
            img[i][j][2] = 0

print(start,end)

######################################################################################

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

#checks if point is out of bounds for image
def is_valid(point):
    if (point[0]>=0 and point[0]<l) and (point[1]>=0 and point[1]<m):
        return True
    return False

#func to find if image is far from obstacles or not in obstacle
def obstacle_free(x):
    for i in range(-dist_away,dist_away + 1):
        for j in range(-dist_away,dist_away + 1):
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

#func to find new vertex at step dist from x_nearest in the dirn of x_rand
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

#func to swap two things of same kind
def swap(a,b):
    temp = a
    a = b
    b = temp
    return a,b

#func to determine if the path to new vertex is obstacle free
def obst_free_path(x_nearest, x_new):
    if obstacle_free(x_nearest) and obstacle_free(x_new):
        return True
    return False

'''
#for large steps   :   Precaution
def obst_free_path(x_nearest, x_new):
    x_n, y_n = x_nearest
    x, y = x_new

    if x_n != x:
        slope = (y_n-y) / (x_n-x)  #for the eqn of line

        if x_n > x:
            x_n, x = swap(x_n,x)   #swap(p1,p2)
            y_n, y = swap(y_n,y)
        for u in range(x_n, x+1):                                  #x_n < x
            x_curr = u
            y_curr = int( slope * (u - x_n) + y_n)
            
            if not obstacle_free((x_curr, y_curr)):
                return False
    else:
        if y_n > y:
            y_n, y = swap(y_n,y)
            x_n, x = swap(x_n,x)
        for v in range(y_n, y+1):                                  #y_n < y
            if not obstacle_free((x,v)):
                return False
    return True
'''

#func to return the neighbour nodes of x_new
def near(vertex, x_new):
    x,y = x_new
    x_near = []
    for vert in vertex:
        if dist(vert,x_new) <=  search_radius:
            if obst_free_path(vert,x_new):                          #
                x_near.append(vert)
    return x_near

#func to choose parent resulting into lowesr cost
def choose_parent(tree,vertex, x_near, x_nearest, x_new):
    min_cost = tree[vertex.index(x_new)].cost
    x_parent = x_nearest

    for neighbour in x_near:
        c = tree[vertex.index(neighbour)].cost + dist(neighbour, x_new)
        if c < min_cost:
            min_cost = c
            x_parent = neighbour
    return x_parent


#func to rewire the tree.. lowering the costs of nodes
def rewire(tree,vertex, x_near, x_parent, x_new):
    for node in x_near:
        c1 = tree[vertex.index(node)].cost      #direct cost
        c2 = tree[vertex.index(x_new)].cost + dist(x_new,node)    #cost via x_new
        if c1 > c2:    #needs some update
            tree[vertex.index(node)].cost = c2
            tree[vertex.index(node)].parent = tree[vertex.index(x_new)]

#func to extend the tree
def extend(tree,vertex, x_rand):
    x,y = x_rand

    x_nearest = nearest(vertex, x_rand)
    x_new = steer(x_nearest, x_rand)   #good is to ensure x_new is valid & path obstacle free

    if obst_free_path(x_nearest, x_new):
        new_node = Node(x_new, cost= (tree[vertex.index(x_nearest)].cost + dist(x_nearest,x_new)), parent= tree[vertex.index(x_nearest)])   #x_nearest is not node but vertex
        tree.append(new_node)
        vertex.append(x_new)

        #searching for better parent
        x_near = near(vertex, x_new)   #returns a list containing neighbours of x_new

        x_parent = choose_parent(tree,vertex, x_near, x_nearest, x_new)       #node having least cost to go through to x_new
        new_node.parent = tree[vertex.index(x_parent)] 

        #rewiring the tree
        rewire(tree,vertex, x_near, x_parent, x_new)

        ################################################################ 
        if x_new == x_rand: 
            return x_new, "REACHED"
        else:
            return x_new, "ADVANCED"        #Advanced means can go more closer to x_new

    return x_new, "TRAPPED"        #Trapped means obstacle in the way

path = []
def show_path(tree,vertex,current_node,final_node, img, flag= 0):
    t = 0
    while current_node != final_node:
        t += 1
        #print(t)
        
        try:
            x1,y1 = current_node.index
            if t%5 ==0:                        #not selecting all index
                path.append((x1,y1))
        except:
            return img, path
        
        try:
            if flag == 0:
                img[x1][y1][0] = 0
                img[x1][y1][1] = 0
                img[x1][y1][2] = 255
            else:
                img[x1][y1][0] = 0
                img[x1][y1][1] = 255
                img[x1][y1][2] = 0
        except:
            pass
        
        current_node = current_node.parent

    return img

def connect(tree,vertex,x_new):
    _, msg = extend(tree,vertex,x_new)
    
    #while msg != "ADVANCED":
    #    _, msg = extend(tree,vertex,x_new)

    return msg

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

        if msg != "TRAPPED":
            if connect(tree2,vertex2,x_new) == "REACHED":
                print("Goal found... Total iteration:",n)
                img = show_path(tree1,vertex1, tree1[vertex1.index(x_new)],start_node, img,0)
                img = show_path(tree2,vertex2, tree2[vertex2.index(x_new)],end_node, img,1)
                return img

        #tree1, tree2 = swap(tree1,tree2)
        #vertex1, vertex2 = swap(vertex1,vertex2)
        
    print("Max iteration reached...")
    #returning till whatever tree1 has grown.
    img = show_path(tree1, vertex1, tree1[vertex1.index(nearest(vertex1,end))],start_node, img)
    return img     

img = RRTStar_Connect(start, end,img)

cv2.namedWindow("My Win", cv2.WINDOW_NORMAL)
cv2.imshow("My Win", img)
cv2.waitKey(0)

##################################################___turle
rrt = socket.socket()
rrt.bind(('localhost',port))

rrt.listen(1)
print('Waiting for turtle!')

turtle, addr = rrt.accept()
print('Connected with turtle' + addr[0] + "  " + str(addr[1]))


print("Path:",path)
turtle.send(str(path).encode())

cv2.destroyAllWindows()
