from typing import List
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        if not n:
            return ['']

        # initialize the first string, which collapse all
        res = ['(' * n + ')' * n]
        i = 0
        while i != len(res):
            # find all canonical ()s' indices
            indices = [j for j in range(len(res[i])) if res[i].startswith('()', j)]
            for ind in indices:
                if ind and ind != len(res[i])-2:
                    newLeft = res[i]
                    newLeft = newLeft[:ind-1] + '()' + newLeft[ind-1] + newLeft[ind+2:]
                    if newLeft not in res:
                        res.append(newLeft)
                    newRight = res[i]
                    newRight = newRight[:ind] + newRight[ind+2] + '()' + newRight[ind+3:]
                    if newRight not in res:
                        res.append(newRight)
            i += 1
        return res

    """
    Using recursive method, and no dupilication exists.
    """
    def generateParenthesis2(self, n):
        def generate(p, left, right, parens=[]):
            if left:         generate(p + '(', left-1, right)
            if right > left: generate(p + ')', left, right-1)
            if not right:    parens += p,
            return parens
        return generate('', n, n)

s = Solution()
print(s.generateParenthesis(4))