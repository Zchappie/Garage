from typing import List
class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        string = ''.join(str(e) for e in digits)
        string = str(int(string) + 1)
        listNew = [int(d) for d in string]
        return listNew

solu = Solution()
print(solu.plusOne([0]))