from typing import List

class Solution:
    def generate(self, numRows: int) -> List[List[int]]:
        pyrimid = [[1], [1,1]]
        if numRows == 0:
            return []
        elif numRows == 1:
            return [[1]]
        elif numRows == 2:
            return pyrimid
        
        for j in range(3, numRows+1):
            last = pyrimid[-1]
            newBase = [1]
            for i in range(1, int((len(last)+1)/2) + 1):
                newBase += [last[i-1] + last[i]]

            if j%2 == 1:
                newBase += newBase[:-1][::-1]
            else:
                newBase += newBase[:-2][::-1]
            pyrimid += [newBase]
        return pyrimid

s = Solution()
print(s.generate(6))