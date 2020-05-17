from typing import List
class Solution:
    def helper(self, row):
        dots = row.count('.')
        diffElements = len(set(row))
        if diffElements != 9 - dots + 1:
            return False
        else:
            return True
            
    def isValidSudoku(self, board: List[List[str]]) -> bool:
        # first check the rows
        for row in board:
            if not self.helper(row):
                return False
            
        # then check columns
        import numpy as np
        boardArr = np.array(board)
        for row in np.transpose(boardArr):
            if not self.helper(row.tolist()):
                return False
        
        # Finally the sub-boxes
        for i in [0, 3, 6]:
            for j in [0, 3, 6]:
                row = boardArr[i:i+3, j:j+3]
                row = row.ravel()
                if not self.helper(row.tolist()):
                    return False
        return True

a = [["5","3",".",".","7",".",".",".","."],["6",".",".","1","9","5",".",".","."],[".","9","8",".",".",".",".","6","."],["8",".",".",".","6",".",".",".","3"],["4",".",".","8",".","3",".",".","1"],["7",".",".",".","2",".",".",".","6"],[".","6",".",".",".",".","2","8","."],[".",".",".","4","1","9",".",".","5"],[".",".",".",".","8",".",".","7","9"]]
s = Solution()
print(s.isValidSudoku(a))