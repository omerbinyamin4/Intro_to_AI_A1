----- Run command: -----
python3 startup.py -i <input_file_name>

flag -d can be added for additional prints:
python3 startup.py -i <input_file_name> -d

example:
python3 startup.py -i simple_env.txt -d


----- prompt: -----
print by program: "Insert task number to run:"
user_options: 1 for task 1 or 2 for task 2

next prints by program are to decide which type of agent to run.
Our current program only support running one agent, so you should enter -1 for all agents,
except one agent for whom you should enter starting location in the graph
