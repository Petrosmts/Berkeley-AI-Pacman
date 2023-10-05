class Stack:
    def __init__(self):
        self.dlist = []
        
    def empty(self):  #checks if the list who implements the stack is empty
        if len(self.dlist) == 0:
            return True
        else:
            return False
        
    def top(self): #the top element of the stack is the last inserted in the list
        return self.dlist[len(self.dlist) - 1]
    
    def push(self, a):  #pushes the element a in the stack 
        self.dlist.append(a)
    
    def pop(self):  #removes the top element
        self.dlist.pop(len(self.dlist) - 1)
    
def main():
    stack1 = Stack()  #we create a stack named stack1
    a = input('Give a string:')
    if a[0] == ')' or a[0] == ']' or a[0] == '}': #if the first element is a closing one, there is no reason to search for something.
        print("Characters are not well balanced")
        return None
    for i in range(len(a)):  #access to all elements of the string one by one
        if a[i] == '(' or a[i] == '[' or a[i] == '{':  #if element is '(', '[' or '{' then we push it in the stack
            stack1.push(a[i])
        elif (stack1.top() == '(' and a[i] == ')') or (stack1.top() == '[' and a[i] == ']') or ( stack1.top() == '{' and a[i] == '}'):
            #if we find the type that matches the type of the top stack1 element, then pop the top element out of stack1
            stack1.pop()
    #if stack1 is empty then all characters found their matching type character with the right order, so they are well balanced
    if stack1.empty():
        print("Characters are well balanced")
    else:
        print("Characters are not well balanced")

if __name__ == '__main__':
    main()