class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class ClaimQueue:
    """FIFO Queue for pending claims waiting for approval."""
    def __init__(self):
        self.__items = []

    def enqueue(self, claim):
        self.__items.append(claim)

    def dequeue(self):
        if self.is_empty():
            return None
        return self.__items.pop(0)

    def is_empty(self):
        return len(self.__items) == 0

    def get_all(self):
        return list(self.__items)


class AppealStack:
    """LIFO Stack for reviewing the most recent denied claim appeals."""
    def __init__(self):
        self.__items = []

    def push(self, claim):
        self.__items.append(claim)

    def pop(self):
        if self.is_empty():
            return None
        return self.__items.pop()

    def is_empty(self):
        return len(self.__items) == 0

    def get_all(self):
        return list(reversed(self.__items))


class ClaimHistoryList:
    """Singly Linked List for append-only lifetime claim history."""
    def __init__(self):
        self.__head = None

    def append(self, claim):
        new_node = Node(claim)
        if self.__head is None:
            self.__head = new_node
            return
        current = self.__head
        while current.next is not None:
            current = current.next
        current.next = new_node

    def get_all(self):
        results = []
        current = self.__head
        while current is not None:
            results.append(current.data)
            current = current.next
        return results
    