# Initial implementation without FSM structure

t = int(input("t = "))

#indexes whose car can be allowed to go
valid_indexes = {(0,1),(0,2),(1,3),(1,4),(0,7),(2,3),(2,5),(3,6),(4,5),(4,6),(5,7),(6,7)}

n = 0 
cars = []  #no. of cars at each corresponding 8 side
for _ in range(8):
    cars.append(0)

#functions to print output in proper way
def road_A(a,b):
    if a==0 and b==1:
        print("A - go straight, go right")
        return
    elif a==0 or b==0:
        print("A - go straigt")        #means when any of them equal to 0, as both already considered
        return
    elif a==1 or b==1:
        print("A - go right")
        return
    print("A - off")
def road_B(a,b):
    if a==2 and b==3:
        print("B - go straight, go right")
        return
    elif a==2 or b==2:
        print("B - go straigt")
        return
    elif a==3 or b==3:
        print("B - go right")
        return
    print("B - off")
def road_C(a,b):
    if a==4 and b==5:
        print("C - go straight, go right")
        return
    elif a==4 or b==4:
        print("C - go straigt")
        return
    elif a==5 or b==5:
        print("C - go right")
        return
    print("C - off")
def road_D(a,b):
    '''
    if a!=6 and b!=7:
        print("D - off")
        return
    '''
    if a==6 and b==7:
        print("D - go straight, go right")
        return
    #elif a==6 and b!=7:
    elif a==6 or b==6:           #means any of them equal to 6, as both already considered
        print("D - go straigt")
        return
    elif a==7 or b==7:
        print("D - go right")
        return
    print("D - off")      #nothing, so neither 6 nor 7 means D - off.

#function to check if traffic is cleared
def is_emptry(cars):
    for car in cars:
        if car!=0:
            return False
    return True  

#func to let a,b pos car go
def allow(a,b=None):
    '''
    if b == None:        #generally a<b means a is even. But for only a, it can be odd. So, making a none & b odd (to let road func perform fine)
        if a%2 != 0:
            b=a
            a=None
    '''
    road_A(a,b)
    road_B(a,b)
    road_C(a,b)
    road_D(a,b)        #functions to print output in proper way

    #if a!= None:
    cars[a] -= 1
    if b != None:
        cars[b] -= 1

    print("Final queue -",cars)
    return cars 


def find_pos(car_present,no_of_car_present):

    #base condition for recursion
    if(len(car_present) == 1):
        a = car_present[0]
        cars = allow(a)
        return cars

    #finding the index(position) having max no. of car
    max_car = max(no_of_car_present)
    max_car_index = no_of_car_present.index(max_car)
    a = car_present[max_car_index]

    #findind b: other position whose car will be allowed to go
    flag = 0
    for item in valid_indexes:
        if item[0] == a:
            b = item[1]
            if b in car_present:
                flag = 1
                break
        elif item[1] == a:
            if item[0] in car_present:
                a = item[0]
                b = item[1]      #so that a will always be less than b
                flag = 1
                break

    if flag == 1:    #flag = 1 means we have found b.
        cars = allow(a,b)    #func to let a,b pos car go
        return cars

    else:        #means no valid config with max car position
        #so removing things corresponding to current max
        no_of_car_present.remove(max_car)
        car_present.remove(a)

        #calling again: RECURSION
        return find_pos(car_present,no_of_car_present)


while True:
    n+=1
    print(f'Time step {n}: ')

    #taking input queue; only for 1st t iterations(time-steps).
    if(n<=t):
        input_queue = []
        print(f'Input line {n}:  ')
        for _ in range(8):
            input_queue.append(int(input()))   #have to enter one by one

        for ind,item in enumerate(input_queue):
            cars[ind] += item

    #printing initial queue
    print("Initial queue - ",cars)

    #storing positions, where there is car present
    car_present = []    #indices where car is present
    no_of_car_present = []    #no. of car at each ind/pos

    for ind,item in enumerate(cars):
        if item!=0:
            car_present.append(ind)
            no_of_car_present.append(item)
    
    #adjusting the signals
    cars = find_pos(car_present,no_of_car_present)      #func to find the indices coresponding to position whose car will be allowed to go.

    #terminating the program after clearing trafic
    if(n>=t):
        if is_emptry(cars):
            print("Traffic cleared! Exiting...")
            break
