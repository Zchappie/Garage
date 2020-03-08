class Solution:
    def isPalindrome(self, s: str) -> bool:
        if not s:
            return True
        
        stack = []
        for i in s:
            if i.isalnum():
                stack.append(i.lower())
            else:
                pass
        # print(stack)
        return stack == stack[::-1]

    def isPalindrome2(self, s: str) -> bool:
        """
        Use two pointers.
        """
        if not s :
            return True
        
        head = 0
        end = len(s)-1
        while head < end:
            if s[head].isalnum():
                if s[end].isalnum():
                    if s[head].lower() == s[end].lower():
                        head += 1
                        end -=1
                    else:
                        return False
                else:
                    end -= 1
            else:
                head += 1
        return True
    
    def isPalindrome3(self, s):
        """
        Simple one. Same idea as my first one.
        """
        s = ''.join(e for e in s if e.isalnum()).lower()
        return s==s[::-1]

s = Solution()
# print(s.isPalindrome("0P"))
print(s.isPalindrome2("A man, a plan, a canal: Panama"))