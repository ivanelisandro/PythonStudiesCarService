from collections import deque

n = int(input())
queue = deque()

while n > 0:
    n -= 1
    command = input().split(' ')
    if command[0] == "ENQUEUE":
        number = int(command[1])
        queue.appendleft(number)
    elif command[0] == "DEQUEUE":
        queue.pop()

while len(queue) > 0:
    print(queue.pop())
