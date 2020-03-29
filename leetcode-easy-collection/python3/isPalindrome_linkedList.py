# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def isPalindrome(self, head: ListNode) -> bool:
        newList = []
        if head:
            newList.append(head.val)
        else:
            return True
        while head.next:
            head = head.next
            newList.append(head.val)

        return newList == newList[::-1]


# https://leetcode.com/problems/palindrome-linked-list/discuss/64500/11-lines-12-with-restore-O(n)-time-O(1)-space