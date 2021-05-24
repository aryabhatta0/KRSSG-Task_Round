Task-Round-Submission

# Imp. points
* In Task-3 Keep the image file name in cv2.imread() accordingly
* Keep changing port no. if failed to connect in socket programming tasks.

# TASK - 1

Run "casino.py"

Run "player.py" in other 3 terminals.
//Game will start.. and will ask for future game (Y/N) at the end.

# Task1 - Bonus

Run "bonus_casino.py"

Then, Run "bonus_client.py"
//Enter details of game like no. of player & rounds for game.

Run "bonus_player.py" in as many asno. of player terminal.
//Game will start.. Enjoy :)


# TASK - 2

Run "FSM_traffic.py"

Enter t.
Enter respective inputs.
** Input queue should be enterred one by one, like:
'''
1  (Enter)

1
1
1
1
1
1
1
& not as: 1 1 1 1 1 1 1 1 
'''
//Traffic will be cleared in lowest time step possible avoiding accumulation of cars on any side.

# Task2 - Bonus

Run "traffic_server.py"

Enter t.

Then, Run "traffic_client.py" in 4 terminals.  
//one for each side (A,B,C,D). ** The first terminal opened will automatically considered as A & so on..

Enter inputs at each client.

** Here, Enter all the 2 input for a side at once like: 1 1


# TASK 3 

# Part - 1 (Path Planning)

## Please run the one on GitHub 
## or, change the parameter Step to 10 & search_radius to 20 in Zip File uploaded through form.
//as I manipulated this after uploading zip, otherwise it will take lot of time.

(i) 
Run "RRT_StarConnect.py (with 1st image in task doc)
//Path will be generated.. It generally takes 500-1000 iterations.

//On output screen, it shows no. of iterations so that we can see that our algo is running. :)

(ii)
Run "generalised_RRT.py" (with 2nd image in doc)
Enter start & end (int).    //it's on the basis of distance from origin (0,0)

//It will take more time to generate the path, i guess.. Takes approx 5000+ iterations
# Part - 2 (Turtlesim)

Copy the file "path_tracking (TASK-3).py" from GitHub to (TASK-3/catkin_ws/src/turtlesim_cleaner/src/path_tracking (TASK-3).py) in zip.
//as I have modified a small thing (x,y co-ordinates) after uploading zip otherwise, it will go out of bound for turtlesim window.

STEPS to MOVE the TURTLE:
> Run Part-1's "RRT_StarConnect.py" as said above 
> roscore
//run this command in terminal

> rosrun turtlesim turtlesim_node  
//in other terminal

> cd into "catkin_ws" dir (provided in zip) & run:
> source devel/setup.bash

> cd into "catkin_ws/src"
> rosrun turtlesim_cleaner path_tracking (TASK-3).py
** "RRT_StarConnect.py" should keep running while following above
// can rename this path_tracking file if faced any problem b/c of space in name.


# TASK 5

Run "attacker" & "defender" files following the usual commands to run the robosoccer simulation::

> rcssserver3d
> ./roboviz.sh  (in roboviz terminal)
> ./start.sh   (in both the attacker & defender terminal)
