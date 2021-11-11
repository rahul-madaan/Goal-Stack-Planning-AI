import copy
inits = [["A", "B"], ["C", "D"]]
'''
         [A]   [C]
    _____[B]___[D]______
'''
goals = [["A", "B", "D"]]

'''
         [A]   
         [B]
      ___[D]_____
'''


current_state = copy.deepcopy(inits)
arm_content = " "

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
    print("__________________________________\n")

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
    global current_state
    global arm_content
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

# Database:-
on_table_elements = set()
middle_elements = set()
clear_elements = set()

# ---------------------------------------------------------------------------

for i in inits:
    clear_elements.add(i[0])  # first in list is clear
    on_table_elements.add(i[-1])  # last in list is on table
    for j in range(len(i) - 1):
        middle_elements.add(i[j] + "*" + i[j + 1])  # 2 * 3 , 3 * 4   ---> 2 on 3 || 3 on 4


def solve(predicate):
    # predicate[0] -->  ON
    # predicate[1] -->   1
    # predicate[2] -->   2
    global clear_elements, middle_elements, on_table_elements, arm

    if predicate[0] == "ON":  # ON 1 2
        if predicate[1] + "*" + predicate[2] in middle_elements:
            return
        else:  # We need to perform stack action, before that call its predicates
            solve(["CL", predicate[2]])  # CLEAR 2
            solve(["HL", predicate[1]])  # HOLDING 1
            print("Stack", predicate[1], predicate[2])  # ''' Stack Action'''
            stack_boxes(predicate[2])
            print("UPDATED STATE:")
            print_current_state()

            clear_elements.remove(predicate[2])  # Modify database once performed action
            clear_elements.add(predicate[1])
            middle_elements.add(predicate[1] + "*" + predicate[2])
            arm = None

    elif predicate[0] == "CL":  # CLEAR 1
        if predicate[1] in clear_elements:  # To check if 1 is clear we need to traverse dbClear
            return
        else:  # If not clear ; To access block that is on (1 or a) i.e b
            a = predicate[1]
            b = None
            for i in middle_elements:  # Here we are traversing
                if a == i[2]:
                    b = i[0]
                    break
            if b == None: return  # If no such block found that means it is clear
            # Else we need to perform unstack operation , and before that statisy predicates
            solve(["CL", b])
            solve(["ON", b, a])
            solve(["AE"])
            arm = b
            clear_elements.add(a)
            clear_elements.add(b)
            on_table_elements.add(a)
            middle_elements.remove(b + "*" + a)
            print("UnStack", b, a)  # ''' UnStack Action '''
            unstack_boxes(b)
            print("UPDATED STATE:")
            print_current_state()

    elif predicate[0] == "AE":  # ARM EMPTY
        if arm == None:
            return
        else:  # If not arm empty perform putdown action
            print("PutDown", arm)  # ''' PUT DOWN ACTION '''
            putdown()
            print("UPDATED STATE:")
            print_current_state()
            on_table_elements.add(arm)
            arm = None

    elif predicate[0] == "ONT":  # ON TABLE 1
        if predicate[1] in on_table_elements:
            return  # check database
        else:
            b = None
            a = predicate[1]
            for i in middle_elements:  # If not ONTABLE check what is on it first
                if a == i[2]:
                    b = i[0]
                    break
            if b == None: return
            solve(["CL", b])
            solve(["ON", b, a])
            solve(["AE"])
            arm = b
            clear_elements.add(a)
            clear_elements.add(b)
            on_table_elements.add(a)
            middle_elements.remove(b + "*" + a)
            print("UnStack", b, a)  # '''  UNSTACK action '''
            unstack_boxes(b)
            print("UPDATED STATE:")
            print_current_state()

    elif predicate[0] == "HL":  # Holding
        if arm == predicate[1]:  # if holding somthing return else perform Pick UP action
            return
        else:
            solve(["CL", predicate[1]])
            solve(["ONT", predicate[0]])
            solve(["AE"])

            arm = predicate[1]
            print("PickUp", arm)  # '''  PICK UP action '''
            pickup(predicate[1])
            print("UPDATED STATE:")
            print_current_state()


# Start with satisfying goal state
for i in goals:
    solve(["CL", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve(["AE"])

for i in goals:
    solve(["CL", i[0]])
    for j in range(len(i) - 2, -1, -1):
        solve(["ON", i[j], i[j + 1]])
    solve(["ONT", i[-1]])
    solve("AE")
