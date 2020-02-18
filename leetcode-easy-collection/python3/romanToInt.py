import typing
class Solution:
    def romanToInt(self, s: str) -> int:
        dict_num = {
            'I' : 1,
            'V' : 5,
            'X' : 10,
            'L' : 50,
            'C' : 100,
            'D' : 500,
            'M' : 1000
        }
        dict_order = {
            'I' : 1,
            'V' : 2,
            'X' : 3,
            'L' : 4,
            'C' : 5,
            'D' : 6,
            'M' : 7
        }

        num = 0
        for i in range(len(s) - 1):
            if dict_order[s[i]] >= dict_order[s[i+1]]:
                num += dict_num[s[i]]
            else:
                num -= dict_num[s[i]]
            
        num += dict_num[s[-1]]
        return num

"""
In general, the dict_order is not needed, as dict_num contains this property.
Python variable initialization: a,b = 0,0 
"""
solu = Solution()
print(solu.romanToInt("I"))