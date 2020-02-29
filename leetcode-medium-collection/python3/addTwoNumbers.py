# Definition for singly-linked list.
class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        # if not l1 or not l2:
        #     return l1 or l2
        # power1 = 0
        # num1 = [l1.val]
        # head1 = l1
        # while head1.next:
        #     power1 += 1
        #     head1 = head1.next
        #     if type(head1) is int:
        #         num1 += [head1]
        #     else:
        #         num1 += [head1.val]
        
        # power2 = 0
        # num2 = [l2.val]
        # head2 = l2
        # while head2.next:
        #     power2 += 1
        #     head2 = head2.next
        #     if type(head2) is int:
        #         num2 += [head2]
        #     else:
        #         num2 += [head2.val]
        
        # digit1 = [pow(10,k) for k in range(power1,-1,-1)]
        # integer1 = sum([a*b for a,b in zip(digit1, num1)])
        # digit2 = [pow(10,k) for k in range(power2,-1,-1)]
        # integer2 = sum([a*b for a,b in zip(digit2, num2)])

        """
        IMPORTANT: the next can't be an integer in the linked list.
        It could only be None or another ListNode.
        """
        carry = 0
        sumList = ListNode(0)
        sumListTail = sumList
        while l1 or l2 or carry:
            adder1 = (l1.val if l1 else 0)
            adder2 = (l2.val if l2 else 0)
            carry, res = divmod(adder1 + adder2 + carry, 10)

            sumListTail.next = ListNode(res)
            sumListTail = sumListTail.next

            l1 = (l1.next if l1 else None)
            l2 = (l2.next if l2 else None)

        return sumList.next

l1 = ListNode(1)
l2 = ListNode(2)
s = Solution()
print(s.addTwoNumbers(l1, l2))