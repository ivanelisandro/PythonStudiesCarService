reversed_queue = deque()

while len(queue) > 0:
    reversed_queue.append(queue.pop())
