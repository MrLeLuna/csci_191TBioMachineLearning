import numpy as np
import matplotlib.pyplot as plt
# set the maximum depth of the cellular automata
MAX_SIZE = 120
# the initial state be double the max depth + 1 and have just one active cell in the center
initial_state = '0' * MAX_SIZE + '1' + '0' * MAX_SIZE
# this is the array that will be used to output teh CA
output = np.array([int(i) for i in initial_state])

# storing the rules in a dict for easy lookup
RULES = {30: {"111": '0', "110": '0', "101": '0', "000": '0',
              "100": '1', "011": '1', "010": '1', "001": '1'},

         90: {"111": "0", "110": "1", "101": "0", "100": "1",
              "011": "1", "010": "0", "001": "1", "000": "0"},

         110: {"111": '0', "110": '1', "101": '1', "100": '0',
               "011": '1', "010": '1', "001": '1', "000": '0'},

         184: {"111": "1", "110": "0", "101": "1", "100": "1",
               "011": "1", "010": "0", "001": "0", "000": "0"}
         }


# this functions gives a windows of three character which is useful when
# looking up that 3 char code in the dict for a specific rule
def window(iterable, stride=3):
    for index in range(len(iterable) - stride + 1):
        yield iterable[index:index + stride]


# actually generated the pattern that is then out put using matplot lib
def generate_pattern(state, rule):
    global output
    # out maximum time step is the same as out maximum depth
    for time in range(MAX_SIZE):
        # get all the three char pattern from the previous time step
        patterns = window(state)
        # for each of the 3 char patterns in the previous time step
        # we look it up in our dict for the given rule  and the join it
        # with the other patterns to form out new state
        state = ''.join(rule[pat] for pat in patterns)
        # format the new state so that it looks correct
        state = '0{}0'.format(state)
        # cast from string char to int so that it can be output using mat plot lib
        arr = [int(i) for i in state]
        # turn that array into a np array so that we can append the results of the pater
        npar = np.array(arr)
        output = np.append(output.reshape(-1, (MAX_SIZE*2+1)), npar.reshape(1, MAX_SIZE*2+1), axis=0)
        

def main():
    global output
    global initial_state
    # this is where you define what rule you want to generate
    rule = RULES[110]
    print("Using rule", 30)
    
    generate_pattern(initial_state, rule)
    # output to screen using matplot lib
    plt.figure(figsize=(10, 6))
    plt.imshow(output.tolist(), cmap='hot')
    plt.show()


if __name__ == "__main__":
    main()
