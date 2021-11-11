import copy

lst = [item for item in input("ENTER THE INITIAL STATE").split()]

columns = []
initial = []
for i in lst:
    for letter in i:
        columns.append(letter)
    initial.append(columns)
    columns =[]

initial_state = initial

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
    print("CURRENT STATE TEXT:")
    current_state_text()
    print("-------------------------------\n")

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

def stack_boxes(box):  # pass box jiske upar stack karna hai
    global current_state, arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    current_state[stack_of_box].insert(0, arm_content)
    arm_content = " "


def unstack_boxes(box):  # pass box jisko utarna hai
    global arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    arm_content = current_state[stack_of_box][0]
    del current_state[stack_of_box][0]


def pickup(box):
    global arm_content
    stack_of_box = -1
    for i in range(len(current_state)):
        if current_state[i][0] == box:
            stack_of_box = i
    arm_content = current_state[stack_of_box][0]
    del current_state[stack_of_box]


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

for column in initial_state:
    clear_elements.append(column[0]) #First box will always b clear
    on_table_elements.append(column[-1])  # last box will always be on table
    for j in range(len(column) - 1):
        middle_elements.append(column[j] + "$" + column[j + 1])  # 2 $ 3 , 3 $ 4   ---> 2 on 3 || 3 on 4


def solve(action):
    global clear_elements, arm, middle_elements, on_table_elements

    if action[0] == "ON":  #predicate 1 on 2
        if action[1] + "$" + action[2] in middle_elements:
            return
        else:  # We need to perform stack action, before that call its predicates
            solve(["IS_CLEAR", action[2]])  # CLEAR 2
            solve(["ARM_IS_HOLDING", action[1]])  # HOLDING 1
            print("Stack", action[1], action[2])  # ''' Stack Action'''
            stack_boxes(action[2])
            print("UPDATED STATE:")
            print_current_state()

            clear_elements.remove(action[2])  # Modify database once performed action
            clear_elements.append(action[1])
            middle_elements.append(action[1] + "$" + action[2])
            arm = None

    elif action[0] == "IS_CLEAR":  # IS_CLEAR 1
        if action[1] in clear_elements:  # To check if 1 is clear we need to traverse dbClear
            return
        else:  # If not clear ; To access block that is on (1 or a) i.e b
            a = action[1]
            b = None
            for i in middle_elements:  # Here we are traversing
                if a == i[2]:
                    b = i[0]
                    break
            if b is None: return  # If no such block found that means it is clear
            # Else we need to perform unstack operation , and before that statisy predicates
            solve(["IS_CLEAR", b])
            solve(["ON", b, a])
            solve(["AE"])
            arm = b
            clear_elements.append(a)
            clear_elements.append(b)
            on_table_elements.append(a)
            middle_elements.remove(b + "$" + a)
            print("UnStack", b, a)  # ''' UnStack Action '''
            unstack_boxes(b)
            print("UPDATED STATE:")
            print_current_state()

    elif action[0] == "AE":  # ARM EMPTY
        if arm == None:
            return
        else:  # If not arm empty perform putdown action
            print("PutDown", arm)  # ''' PUT DOWN ACTION '''
            putdown()
            print("UPDATED STATE:")
            print_current_state()
            on_table_elements.append(arm)
            arm = None

    elif action[0] == "ONT":  # ON TABLE 1
        if action[1] in on_table_elements:
            return  # check database
        else:
            b = None
            a = action[1]
            for i in middle_elements:  # If not ONTABLE check what is on it first
                if a == i[2]:
                    b = i[0]
                    break
            if b == None: return
            solve(["IS_CLEAR", b])
            solve(["ON", b, a])
            solve(["AE"])
            arm = b
            clear_elements.append(a)
            clear_elements.append(b)
            on_table_elements.append(a)
            middle_elements.remove(b + "$" + a)
            print("UnStack", b, a)  # '''  UNSTACK action '''
            unstack_boxes(b)
            print("UPDATED STATE:")
            print_current_state()

    elif action[0] == "ARM_IS_HOLDING":  # Holding
        if arm == action[1]:  # if holding somthing return else perform Pick UP action
            return
        else:
            solve(["IS_CLEAR", action[1]])
            solve(["ONT", action[0]])
            solve(["AE"])

            arm = action[1]
            print("PickUp", arm)  # '''  PICK UP action '''
            pickup(action[1])
            print("UPDATED STATE:")
            print_current_state()


# Start with satisfying goal state
for i in goal_state:
    solve(["IS_CLEAR", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve(["AE"])

for i in goal_state:
    solve(["IS_CLEAR", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve("AE")

