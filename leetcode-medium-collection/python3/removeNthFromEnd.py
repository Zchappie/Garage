# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        fast, slow = 0, 0
        fastNode = head
        newList = head
        newNode = head
        while fastNode.next:
            fastNode = fastNode.next
            fast += 1
            if fast >= n + 1:
                slow += 1


        # while loop stops at slow reach the need-to-be-deleted node
        if 