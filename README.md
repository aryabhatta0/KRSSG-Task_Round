## Task-Round-Submission

Following are the instructions to run the code:

# TASK - 1

1. Run `casino.py`.
2. Run `player.py` in 3 other terminals.

The game will start and will ask for a future game (Y/N) at the end.

**NOTE:** Try changing port number if failed to connect in socket programming tasks.

## Task1 - Bonus

1. Run `bonus_casino.py`.
2. Run `bonus_client.py`.

    Enter details of the game, such as the number of players and the number of rounds.

3. Run `bonus_player.py` in as many terminals as the number of players.

The game will start. Enjoy!

# TASK - 2

1. Run `FSM_traffic.py`.
2. Enter the number of time steps (`t`).
3. Enter the inputs, one by one. For example, if the inputs are `1 2 3 4`, you would enter `1`, then `2`, then `3`, and then `4`.

The traffic will be cleared in the lowest number of time steps possible, avoiding accumulation of cars on any side.

## Task2 - Bonus

1. Run `traffic_server.py`.
2. Enter the number of time steps (`t`).
3. Run `traffic_client.py` in 4 terminals.
4. Enter the inputs at each client in order. For example, if the inputs for side A are `1 2` and the inputs for side B are `3 4`, you would enter `1 2` in the first terminal and `3 4` in the second terminal.

The traffic will be cleared in the lowest number of time steps possible.

# TASK 3

## Part 1 (Path Planning)

1. Run `RRT_StarConnect.py` (with the first image)

    - The path will be generated. This generally takes 500-1000 iterations.
    - The number of iterations will be displayed on the output screen, so you can see that the algorithm is running.

2. Run `generalised_RRT.py` (with 2nd generalized image)

    - Enter start and end (int). This is based on the distance from the origin (0,0).
    - The path will take more time to generate, about 5000+ iterations.

## Part 2 (Turtlesim)

1. Copy the file `path_tracking (TASK-3).py` from GitHub to the `catkin_ws/src/turtlesim_cleaner/src` directory in the zip file.

Steps to move the turtle:

2. Run `RRT_StarConnect.py` as described above.
3. Run `roscore` in a terminal.
4. Run `rosrun turtlesim turtlesim_node` in another terminal.
5. cd to the `catkin_ws` directory and run `source devel/setup.bash`.
6. cd into `catkin_ws/src` directory and run `rosrun turtlesim_cleaner turtle_path_tracking-Task3`.

The `RRT_StarConnect.py` file should continue running while you follow these steps.

# TASK 5

This task is based on the [UTAustinVilla3D](https://github.com/LARG/utaustinvilla3d) codebase for the RoboCup Soccer Simulation 3D.

Run the `attacker` and `defender` files following the usual commands to run the robosoccer simulation:

1. Run `rcssserver3d`.
2. Run `./roboviz.sh` in the `roboviz` terminal.
3. Run `./start.sh` in both the `attacker` and `defender` terminals.