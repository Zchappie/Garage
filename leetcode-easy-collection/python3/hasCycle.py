# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        try:
            walker = head
            runner = head.next
            while walker is not runner:
                walker = walker.next
                runner = runner.next.next
            return True
        except:
            return False

class Solution:
    def hasCycle(self, head: ListNode) -> bool:
        visited = set()
        while head:
            if head in visited:
                return True
            else:
                visited.add(head)
            head = head.next
        return False


"""
Things learnt: chasing algo. The runner will catch the walker.
"""