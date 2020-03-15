class Solution:
    def titleToNumber(self, s: str) -> int:
        if not s:
            return 0
        
        num = 0
        for i in range(len(s)):
            num += (ord(s[i]) - 64)*pow(26, len(s)-i-1)
        return num

"""
Don't need to remember the Unicode, simple way:
curr = ord(a)-ord('A')+1
"""

s = Solution()
print(s.titleToNumber('Z'))