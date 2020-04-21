# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def removeNthFromEnd(self, head: ListNode, n: int) -> ListNode:
        # consider the deleted node is at the beginning
        fast, slow = 0, 0
        fastNode = head
        newList = head
        curNode = newList.next
        while fastNode.next:
            fastNode = fastNode.next
            fast += 1
            if fast >= n + 1:
                slow += 1
                curNode = curNode.next

        # while loop stops at slow reach the need-to-be-deleted node
        try:
            curNode = curNode.next.next
        except:
            curNode.next = None
            return newList