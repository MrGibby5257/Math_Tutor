import random

operations = {
    '+': lambda a, b: a + b,
    '-': lambda a, b: a - b,
    '*': lambda a, b: a * b,
    '/': lambda a, b: a // b
}

number_range = 12
initial_weight = 15


# Create num weights list and op weights dictionary
num_weights = [initial_weight for i in range(number_range)]
op_weights = {op[0]: initial_weight for op in operations}

# Generate a random number in range of the length of num_weights with the associated weights
def generate_num():
    return random.choices(range(len(num_weights)), weights=num_weights)[0]

# Generate a random operation using the associated weights
def generate_op():
    op = random.choices(list(op_weights.keys()), weights=list(op_weights.values()))[0]
    return op, operations[op]

#Calculate the reward earned from each question based on result
def calculate_reward(result):
    r = 0
    if result == False: #if the user gets the wrong answer
        r = 0.5
    elif result == True: #if the user gets it correct
        r = 1
    else:
        print("WRONG INPUT FOR CALCULATE_REWARD")
    return r
    
# Update the weights of given numbers depending on correct state
def update_num_weights(correct, nums):
    unique_nums = list(set(nums))
    for num in unique_nums:
        if(num_weights[num] > 1):
            if (correct is False):
                num_weights[num] += 1
            else:
                num_weights[num] -= 1

# Update the weight of given operation depending on correct state
def update_op_weights(correct, ops):
    unique_ops = list(set(ops))
    for op in unique_ops:
        if(op_weights[op] > 1):
            if(correct is False):
                op_weights[op] += 1
            else:
                op_weights[op] -= 1

# Recursively generates a problem with c numbers
def gen_prob(c, RHS=None, num_list=None, op_list=None):
    # Initial call, create number and operator lists
    if num_list is None:
        num_list = []
    if op_list is None:
        op_list = []

    # Base case: return generated string and lists
    if (c == 0):
        return RHS, num_list, op_list
    
    # Generate a non-zero integer, append to number list and create a string with it
    num = 0
    while(num == 0):
        num = generate_num()
    num_list.append(num)
    str = f'{num}'

    # Runs on all calls except initial and base case
    if RHS is not None:
        # Generate the operation to occur between the generated number and existing string
        op, func = generate_op()
        
        # Get already generated numbers and operators (needed for division)
        RHS_list = RHS.split(' ')

        # If current operation and next operation are both division, regenerate current operation
        # Avoids having multiple divions in a row, which would result in very large numbers being divided
        if(len(RHS_list) > 1):
            prev_op = RHS_list[1]
            while(prev_op == '/' and op == '/'):
                op, func = generate_op()

        # If the current operation is division, make the numerator the denominator * the generated number
        # This assures that the quotient is an integer, more specifically it's the generated number
        if(op == "/"):
            nn = int(RHS_list[0])
            num *= nn
        # Update problem string, append new operation to operation list
        str = f'{num} {op} {RHS}'
        op_list.append(op)
    
    # Call function again with counter decremented
    return gen_prob(c - 1, str, num_list, op_list)


high_scores = [0,0,0] #keeps track of the high scores (rewards) of each level

#Generates problems for the intial quiz each user takes before entering MATHstermind
def gen_probs(expr_num):
    reward = 0 #sum the rewards receieved in each level
    num_of_qs_per_level = 10 #number of questions per level
    max_reward = num_of_qs_per_level #max reward should be equivalent to the number of ?'s per level (looking to maximize reward)
    count = 1 #count number of questions (STARTING AT QUESTION 1)
    while (True):
        # generate a problem
        problem, nums, ops = gen_prob(expr_num)

        # Verify problem exists and has integer solution
        if problem is not None and eval(problem) == int(eval(problem)):
            # Get answer
            answer = int(eval(problem))

            # Print problem and get user input
            print(f'\nQuestion {count}:')
            user_input = input(f'{problem} = ')

            tag = None #used to catch if we need to break from the while loop
            try:
                if count == num_of_qs_per_level: #if they got 10 { == num of ?'s per level} correct answers in each level
                    if reward == (max_reward-1):#user completed level with 100% correct
                        high_scores[expr_num-2] = reward #reset the high score
                        print("Level",expr_num-1, "complete! You have mastered this level!")
                    else:
                        if high_scores[expr_num-2] >= reward: #if the user did not do better or tied their high score
                            print("Level Complete! You scored:", reward, ". Try again for a better score. Previous high score: ", high_scores[expr_num-2])
                        else: #the user got a higher score but it was the not the maximum reward 
                            print("Level Complete! You scored:", reward, ". You got a new high score!! Previous high score: ", high_scores[expr_num-2])
                            high_scores[expr_num-2] = reward
                    
                    #displays the high score chart for the user to keep track of progress (list is based by level)
                    print("")
                    print("High Scores:")
                    for x in range(len(high_scores)):
                        print("Level",x+1,":",high_scores[x])
                    print("")
                    count = 0
                    tag = 'br' #make sure we break when we return
                    startMenu()
                else:
                    user_input = int(user_input)
            except:
                # treat invalid input as wrong answer
                if user_input == 'q' or user_input == "Q":
                    print("")
                    print("")
                    tag = 'br' #make sure we break when we return
                    startMenu()
                else:
                    user_input = None
            if tag == "br":
                break

            correct = (user_input == answer)
            print("Correct!" if correct else f'Incorrect! The correct answer is {answer}')
            print("")

            # Increase weight of a number if problem is incorrect, decrease otherwise
            update_num_weights(correct, nums)
            update_op_weights(correct, ops)
            reward += calculate_reward(correct)
            count+=1


# CHANGE: Any integer number can be entered to produce a problem with n+1 numbers
init_count = [1]
def gen_probs_init(expr_num):
    # generate random operation and numbers
    problem, nums, ops = gen_prob(expr_num)

    # Verify problem exists and has integer solution
    if problem is not None and eval(problem) == int(eval(problem)):
        # Get answer
        answer = int(eval(problem))

        # Print problem and get user input
        print(f'\nQuestion {init_count[0]}:')
        user_input = input(f'{problem} = ')
        tag = None #used to catch if we need to break from the while loop
        try:
            user_input = int(user_input)
        except:
            user_input = None

        correct = (user_input == answer)
        print("Correct!" if correct else f'Incorrect! The correct answer is {answer}')

        # Increase weight of a number if problem is incorrect, decrease otherwise
        update_num_weights(correct, nums)
        update_op_weights(correct, ops)
        init_count[0] +=1



#this is the starting menu for the math tutor application
finished_init = [False] #the boolean value determines if the user has completed the intial quiz
def startMenu():
    #create an intial quiz to train the system to understand better where to student struggles
    if(finished_init[0] == False):
        print("Welcome to Mathstermind! Our virtual assistant is here to help you improve your math skills!")
        print("We will start off with a initial quiz to understand where your strengths and weakness are")
        print("")
        q = 1
        quiz_limit = 15 #set quiz question limit to 15 to make it not too long but not short to train the model
        level = 1 #suggests what level we will be on
        while q <= quiz_limit:
            level = q%3 #by using modulous divison, we can generate a number between 0 and 2 to get a level for each iteration
            if(level == 0):
                level = 3
            gen_probs_init(level+1)
            q+=1
    finished_init[0] = True #tells the system that the intial quiz is complete
    print("")
    print("")
    #User-Interface (UI) for the user to select which level they want to go to or potentially leave.
    print("Welcome to Mathstermind! Our virtual assistant is here to help you improve your math skills!")
    print("There are three levels to choose from Beginner to Advance. Pick the level that suits you. Type 'q' to leave a level or the application")
    print("Level 1: Beginner (Two Numbers) -----> Type 1")
    print("Level 2: Moderate (Three Numbers) -----> Type 2")
    print("Level 3: Advanced (Four Numbers) -----> Type 3")
    #will keep asking for a valid input until given one
    while True:
        user_input = input("Please type in and enter your level: ")
        #makes sure the number input by the user is between 1 and 3 which are the current levels made
        if ((user_input == 'Q') or (user_input == 'q') or ((int(user_input) >= 1) and (int(user_input) <= 3))):
            print("")
            break
        else:
            print("Sorry! That is not a level. Try again!")
            print("")
    #check the makes sure the input is safe and generates problem based upon the level selected OR leaves the program
    if user_input.isnumeric():
        gen_probs(1 + int(user_input))
    elif user_input == 'q' or user_input == "Q":
        print("Thank you for using Mathstermind! I hope you learned a lot. Keep calculating and see you in the next equation.")
        return None
    else:
        print("ERROR!")
        return None
    

startMenu()
    

