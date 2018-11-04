# Data structures and algorithms course
# Program to add and remove customers from Queue
# Made by Aleksi Hytönen

from collections import deque

QUEUE_SIZE = 10

def menu():
    """Main menu"""

    print('Choice:')
    print('1. Add customer')
    print('2. Remove customer')
    print('3. Exit')

def main():    
    line = deque()
    choice = 0
    count = 0
    while choice != 3:
        menu()
        choice = int(input('> '))
        if choice == 1:
            # Add a customer if possible
            if adding(line, count):
                print("Error in adding customer! Queue already full.")
            else:
                print("Successfully added a customer to queue!")
                count += 1
        elif choice == 2:
            # Remove a customer from queue if possible
            # and print customer's number
            if removing(line):
                print("Error in removing a customer! Queue is empty.")

def adding(q, c):
    """This function adds customers and customer number to queue.
    arg1 = queue
    arg2 = customer number
    Returns True if queue is full, false if adding was successful"""

    if len(q) == QUEUE_SIZE:
        return True
    c += 1
    q.append(((input("Input customer name> ")), c))
    return False

def removing(q):
    """This function removes first customer from queue and prints the customer number.
    arg = queue
    returns False if removing was successful, true if queue is empty."""

    if len(q) == 0:
        return True
    rem = q.popleft()
    print("Customer number {} removed from queue!".format(rem[1]))
    return False

if __name__ == "__main__":
    main()