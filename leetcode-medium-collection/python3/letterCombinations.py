from typing import List
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        dictMap = {
            '2': ['a', 'b', 'c'],
            '3': ['d', 'e', 'f'],
            '4': ['g', 'h', 'i'],
            '5': ['j', 'k', 'l'],
            '6': ['m', 'n', 'o'],
            '7': ['p', 'q', 'r', 's'],
            '8': ['t', 'u', 'v'],
            '9': ['w', 'x', 'y', 'z']
        }
        comb = []
        for i in digits:
            if not comb:
                comb = dictMap[i].copy()
            else:
                newComb = []
                for j in range(len(comb)):
                    for k in range(len(dictMap[i])):
                        newComb.append(comb[j]+dictMap[i][k])
                comb = newComb
        return comb

s = Solution()
print(s.letterCombinations('23'))