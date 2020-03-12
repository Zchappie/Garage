# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def getIntersectionNode(self, headA: ListNode, headB: ListNode) -> ListNode:
        if headA == None and headB == None:
            return None

        a = headA
        b = headB

        while a != b:
            p_A = p_A.next if p_A != None else headB
            p_B = p_B.next if p_B != None else headA
        return a


"""
SO DAMN BRILLIANT!!!
Check explanation here
https://leetcode.com/problems/intersection-of-two-linked-lists/discuss/49785/Java-solution-without-knowing-the-difference-in-len!
"""