import copy
'''
Taking input of initial state
Input - 'ABCD EF'
can be visually represented as
[A]
[B]
[C] [E]
[D] [F]
--------
'''
lst = [item for item in input("ENTER THE INITIAL STATE").split()]

columns = []
initial = []
for i in lst:
    for letter in i:
        columns.append(letter)
    initial.append(columns)
    columns =[]

initial_state = initial
'''
Taking input of GOAL state
Input - 'ABCD EF G'
can be visually represented as
[A]
[B]
[C] [E]
[D] [F] [G]
--------
'''
lst2 = [item for item in input("ENTER THE GOAL STATE").split()]

columns = []
goal = []
for i in lst2:
    for letter in i:
        columns.append(letter)
    goal.append(columns)
    columns =[]

goal_state = goal
current_state = copy.deepcopy(initial_state)
arm_content = " "

'''
This function prints the state from parsing lists in the current state list
Arm content is read from global var arm_content
1st element in all lists are on top
last element in all lists are always on table
'''
def current_state_text():
    global current_state
    global arm_content
    output = []
    if arm_content != " ":
        output.append( "HOLD(" + arm_content + ")") # ARM
    for stack in current_state:
        output.append( "CL(" + stack[0] + ")")#first
        for i in range(len(stack)-1):
            output.append("ON(" + stack[i] +"," + stack[i+1] +")")
        output.append( "ONT(" + stack[-1] + ")" ) # last

    print(output)


'''
Current state is printed visually
along with a robot arm in beginning
uses global variable current_state
'''
def print_current_state():
    print_arm_content()
    global current_state
    current_state_copy = copy.deepcopy(current_state)
    max_length = 0
    for i in current_state_copy:
        length = len(i)
        if length > max_length:
            max_length = length
    iter = max_length
    for i in range(iter):
        for j in range(len(current_state_copy)):
            if len(current_state_copy[j]) == max_length:
                print("[", current_state_copy[j][0], "] ", sep="", end="")
                del current_state_copy[j][0]
            else:
                print("    ", sep="", end="")
        max_length -= 1
        print('')
    print("-------------------------------")
    print("CURRENT STATE TEXT:")
    current_state_text()
    print("-------------------------------\n")

'''
Visual print of the content in arm
uses global variable arm_content
'''
def print_arm_content():
    global arm_content
    print("                         |")
    print("                         |")
    print("                        / \\")
    print("                       /   \\")
    if arm_content == " ":
        print("                       \   /", sep="")
    else:
        print("                       \[", arm_content, "]/", sep="")

print("INITIAL STATE")
print_current_state()

'''
Places the box in arm on the box which is passed
it updates the global variable arm content to blank
it updates the global variable current_state to new state
'''
def stack_boxes(box):  # pass box jiske upar stack karna hai
    global current_state, arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    current_state[stack_of_box].insert(0, arm_content)
    arm_content = " "

'''
removes the box which is passed to the function
it holds the unstacked box in arm
it updates the global variable arm content to the box removed
it updates the global variable current_state to new state
'''
def unstack_boxes(box):  # pass box jisko utarna hai
    global arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    arm_content = current_state[stack_of_box][0]
    del current_state[stack_of_box][0]

'''
pick up the box which is passed to the function
picks up the box from table
it holds the picked up box in arm
it updates the global variable arm content to the box picked up
it updates the global variable current_state to new state
'''
def pickup(box):
    global arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    arm_content = current_state[stack_of_box][0]
    del current_state[stack_of_box]

'''
puts down the box which is passed to the function
puts down the box on table
it updates the global variable arm content to blank
it updates the global variable current_state to new state
'''
def putdown():
    global arm_content
    new_stack = []
    new_stack.append(arm_content)
    current_state.append(new_stack)
    arm_content = " "


arm = None

'''
list to keep track of
1. all elements touching table
2. all elements in the middle
3. all elements at top
'''
on_table_elements = []
middle_elements = []
clear_elements = []

'''
The following loop traverses the initial state list
registers the state of each box
populates the above 3 lists
$ is used as a delimiter
'''
for column in initial_state:
    clear_elements.append(column[0]) #First box will always b clear
    on_table_elements.append(column[-1])  # last box will always be on table
    for j in range(len(column) - 1):
        middle_elements.append(column[j] + "$" + column[j + 1])  # 2 $ 3 , 3 $ 4   ---> 2 on 3 || 3 on 4

'''
This is the main function
It is called recursively by itself
we are not maintaining any external stack
'''
def solve(action):
    global clear_elements, arm, middle_elements, on_table_elements

    '''
    ON means box1 is on top of box 2
    ONT means box1 is on table
    CL means box on does not have any box above it
    ARM_IS_HOLDING means arm is holding box1  
    '''
    if action[0] == "ON":
        if action[1] + "$" + action[2] in middle_elements:
            return
        else:  # We need to perform stack action, before that call its predicates
            solve(["CL", action[2]])  # means box 2 is clear
            solve(["ARM_IS_HOLDING", action[1]])  # arm holding box 1
            print("Stack", action[1], action[2])  # stacking
            stack_boxes(action[2]) #box 1 is put on top of box2
            print("UPDATED STATE:")
            print_current_state()
            # Updating all the list
            clear_elements.remove(action[2])
            clear_elements.append(action[1])
            middle_elements.append(action[1] + "$" + action[2]) # $ is used as delimiter
            arm = None
# Now checking if box 1 has box 2 on top of it
    elif action[0] == "CL":
        if action[1] in clear_elements:  #check in list of clears
            return
        else:
            box1 = action[1]
            box2 = None
            for i in middle_elements:
                if box1 == i[2]:
                    box2 = i[0]
                    break
            if box2 is None:
                return
            solve(["CL", box2])
            solve(["ON", box2, box1])
            solve(["AE"])
            arm = box2
            clear_elements.append(box1)
            clear_elements.append(box2)
            on_table_elements.append(box1)
            middle_elements.remove(box2 + "$" + box1)
            print("UnStack", box2, box1)  # picking up box1 from box2
            unstack_boxes(box2)
            print("UPDATED STATE:")
            print_current_state()

    elif action[0] == "AE":  # ARM EMPTY
        if arm == None:
            return
        else:  # If not arm empty perform putdown action
            print("PutDown", arm)  #puts the box in arm on table
            putdown()
            print("UPDATED STATE:")
            print_current_state()
            on_table_elements.append(arm)
            arm = None

    elif action[0] == "ONT":  # on table box 1
        if action[1] in on_table_elements:
            return  # check lists
        else:
            box2 = None
            box1 = action[1]
            for i in middle_elements:
                if box1 == i[2]:
                    box2 = i[0]
                    break
            if box2 is None: return
            solve(["CL", box2])
            solve(["ON", box2, box1])
            solve(["AE"])
            arm = box2
            clear_elements.append(box1)
            clear_elements.append(box2)
            on_table_elements.append(box1)
            middle_elements.remove(box2 + "$" + box1)
            print("UnStack", box2, box1)  # picks up the box1 from box 2
            unstack_boxes(box2)
            print("UPDATED STATE:")
            print_current_state()

    elif action[0] == "ARM_IS_HOLDING":  # Holding
        if arm == action[1]:
            return
        else:
            solve(["CL", action[1]])
            solve(["ONT", action[0]])
            solve(["AE"])

            arm = action[1]
            print("PickUp", arm)  # picks up the box1 from table
            pickup(action[1])
            print("UPDATED STATE:")
            print_current_state()


'''
The loop checks all the conditions in goal state and calls the solve function
Here the recursion of solve function starts
'''
for i in goal_state:
    solve(["CL", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve(["AE"])

for i in goal_state:
    solve(["CL", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve("AE")

