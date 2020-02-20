import typing

class Solution:
    def __init__(self):
        self.dictionary = {
                '[' : ']',
                '{' : '}',
                '(' : ')'
                }

    def isValid(self, s: str) -> bool:
        if len(s) == 0:
            return True
        elif s[0] not in self.dictionary or len(s) % 2 == 1:
            return False
        else:
            i = 0
            while s[i+1] != self.dictionary[s[i]] and i < len(s)-1:
                i += 1
                if s[i] not in self.dictionary or i+1==len(s):
                    return False
            if i == len(s) - 1:
                return False
            else:
                s = s[:i] + s[i+2:]
                return self.isValid(s)

            
                    
solu = Solution()
print(solu.isValid("((()))}"))