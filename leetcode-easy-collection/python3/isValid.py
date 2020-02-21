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

        """
        Using a stack can solve this problem easily.
        """
    	# def isValid(self, s):
        # d = {'(':')', '{':'}','[':']'}
        # stack = []
        # for i in s:
        #     if i in d:  # 1
        #         stack.append(i)
        #     elif len(stack) == 0 or d[stack.pop()] != i:  # 2
        #         return False
        # return len(stack) == 0 # 3
	
        # 1. if it's the left bracket then we append it to the stack
        # 2. else if it's the right bracket and the stack is empty(meaning no matching left bracket), or the left bracket doesn't match
        # 3. finally check if the stack still contains unmatched left bracket
                    
solu = Solution()
print(solu.isValid("((()))}"))