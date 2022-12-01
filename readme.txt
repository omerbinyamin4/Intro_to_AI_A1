requirements: python 3.9
instructions:

----- Run command: -----

python3 startup.py -i <input_file_name>
*input need to be located in input_graphs directory and stand with the graph structure and guideline as given in the assignment.

flag -d can be added for additional prints (for debugging purposes):
python3 startup.py -i <input_file_name> -d

example:
python3 startup.py -i simple_env.txt -d

----- prompt: -----

after running command, two options are offered: one for the first task of the assignment and one for the second one (search agents).
after choosing the desired option, simply follow the prompt in order to config number of agents, their type, start locations
and different params for performance measurements and user optional limitations on agents search actions.

during agents runtime, prompts to describe their state, job and progress is printed to screen.

once agents finish their job, if solution was found, it is printed as prompt with agent name, solution path and other measurments
as the assignment required.
if no solution was found, a proper prompt is printed as well.