# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        if not head:
            return None
        
        currNode = head
        prevNode = ListNode(None)
        while currNode:
            nextNode = currNode.next
            currNode.next = prevNode
            prevNode = currNode
            currNode = nextNode

        return prevNode