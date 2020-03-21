class Solution:
    def isHappy(self, n: int) -> bool:
        recur = []
        while n != 1 :
            n = sum([(int(i))**2 for i in list(str(n))])
            if n in recur:
                return False
            else:
                recur.append(n)
        return True

s = Solution()
print(s.isHappy(15))
