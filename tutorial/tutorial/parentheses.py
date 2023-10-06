class Stack:
    def __init__(self):
        self.dlist = []
        
    def empty(self):  #checks if the list who implements the stack is empty
        if len(self.dlist) == 0:
            return True
        else:
            return False
    
    def push(self, a):  #pushes the element a in the stack 
        self.dlist.append(a)
    
    def pop(self):  #removes and returns the top element
        return self.dlist.pop(len(self.dlist) - 1)


def str_ok(sstr):  #just to check that all symbols of the string are (,[,{,},],)
    for i in sstr:
        if i != '{' and i != '[' and i != '(' and i != ')' and i != ']' and i != '}':
            return False
    return True
    
def main():
    stack1 = Stack()  #we create a stack named stack1
    a = input('Give a string:')
    if str_ok(a):
        if a[0] == ')' or a[0] == ']' or a[0] == '}': #if the first element is a closing one, there is no reason to search for something.
            print("Characters are not well balanced")
            return None
        for i in range(len(a)):  #access to all elements of the string one by one
            if a[i] == '(' or a[i] == '[' or a[i] == '{':  #if element is '(', '[' or '{' then we push it into the stack
                stack1.push(a[i])
            else: 
                popped = stack1.pop()
                #if the popped element has not the same type with the current string letter, then we push it again into the stack
                if (popped == '(' and a[i] != ')') or (popped == '[' and a[i] != ']') or (popped == '{' and a[i] != '}'):
                    stack1.push(popped)
        if stack1.empty():
            print("Characters are well balanced")
        else:
            print("Characters are not well balanced")
    else:
        print("Invalid string given")


if __name__ == '__main__':  #here we run the above function main
    main()