class StateMachine:

    states = {(0,1),(0,2),(1,3),(1,4),(0,7),(2,3),(2,5),(3,6),(4,5),(4,6),(5,7),(6,7)}  #only one no (only one light glowing) will automatically be considered as a part of state.
    #start_state
    end_state = None   #when the queue will be all 0

    def run(self):
        while True:
            new_state = transitions(self.states)      #input queue for transition declared globally or will be read later.
            if new_state == self.end_state:
                print("Traffic cleared...")
                break
            update(new_state)    #function to let the corresponding cars go i.e, to update final queue


#functions to print output in proper way
def print_A(a,b):
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
def print_B(a,b):
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
def print_C(a,b):
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
def print_D(a,b):
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

def update(new_state):
    a = new_state[0]
    b = new_state[1]

    #updating final queue
    final_queue[a] -= 1
    if b != None:
        final_queue[b] -= 1

    #functions to print output in proper way
    print_A(a,b)
    print_B(a,b)
    print_C(a,b)
    print_D(a,b)

    print("Final queue - ",final_queue)  




final_queue = []
for _ in range(8):
    final_queue.append(0)
def take_input(n):
    input_queue = []
    print(f'Input line {n}:  ')
    for _ in range(8):
        input_queue.append(int(input()))   #have to enter one by one

    for i in range(8):
        final_queue[i] += input_queue[i]

    return final_queue     #previous transition's final queue will be initial of this

def find_newState(states,car_present,no_of_car_present):     
    #base condition for recursion
    if(len(car_present) == 1):
        a = car_present[0]
        return (a,None)        #2nd member of state considered as None

    #finding the index(position) having max no. of car
    max_car = max(no_of_car_present)
    max_car_index = no_of_car_present.index(max_car)
    a = car_present[max_car_index]

    #findind b: other member of new state
    flag = 0
    for item in states:
        if item[0] == a:
            b = item[1]
            if b in car_present:
                flag = 1
                break
        elif item[1] == a:
            if item[0] in states:
                a = item[0]
                b = item[1]      #so that a will always be less than b
                flag = 1
                break

    if flag == 1:    #flag = 1 means we have found b.
        return (a,b)

    else:        #means no state possible with a
        #so removing things corresponding to current max
        no_of_car_present.remove(max_car)
        car_present.remove(a)

        #calling again: RECURSION
        return find_newState(states,car_present,no_of_car_present)


def is_clear(final_queue):
    for item in final_queue:
        if item != 0:
            return False
    return True

n = 0
def transitions(states):
    global n
    n += 1
    if(n<=t):
        initial_queue = take_input(n)           #func to provide input to the FSM
    else:
        initial_queue = final_queue

    if is_clear(initial_queue): #func to check if end_state is reached
        return None

    #printing initial queue
    print(f'Time step {n}: ')
    print("Initial queue - ",initial_queue)

    #storing positions, where there is car present
    car_present = []    #indices where car is present
    no_of_car_present = []    #no. of car at each ind/pos

    for ind,cars in enumerate(initial_queue):
        if cars!=0:
            car_present.append(ind)
            no_of_car_present.append(cars)

    return find_newState(states,car_present,no_of_car_present)




    
fsm = StateMachine()

t = int(input("t = "))
fsm.run()
