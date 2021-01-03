from collections import deque

n = int(input())
queue = deque()
passed = []

while n > 0:
    n -= 1
    command = input().split(' ')
    if command[0] == "READY":
        name = command[1]
        queue.appendleft(name)
    elif command[0] == "PASSED":
        passed.append(queue.pop())
    elif command[0] == "EXTRA":
        queue.appendleft(queue.pop())

for name in passed:
    print(name)
