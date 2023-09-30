class Stack:
    def __init__(self):
        self.dlist = []
        
    def empty(self):
        if len(self.dlist) == 0:
            return True
        else:
            return False
    
    def push(self, a):
        self.dlist.append(a)
    
    def pop(self):
        self.dlist.pop(len(self.dlist) - 1)
    
    def length(self):
        return len(self.dlist)
    
    def top(self):
        return self.dlist[len(self.dlist) - 1]


stack1 = Stack()
a = input('Give a string:')
for i in range(len(a)):
    if a[i] == '(' or a[i] == '[' or a[i] == '{':
        stack1.push(a[i])
    elif (stack1.top() == '(' and a[i] == ')') or (stack1.top() == '[' and a[i] == ']') or ( stack1.top() == '{' and a[i] == '}'):
        stack1.pop()
if stack1.empty():
    print("Characters are well balanced")
else:
    print("Characters are not well balanced")

