class Solution:
    def myAtoi(self, str: str) -> int:
        num = ' '
        for i in str:
            if i.isdigit() or i in ['+', '-', ' ']:
                last = num[-1].isdigit()
                if num[-1].isdigit() and not i.isdigit():
                    break
                num += i
            else:
                break
        try:
            if int(num) > 2147483647:
                return 2147483647
            elif int(num) < -2147483648:
                return -2147483648
            else:
                return int(num)
        except ValueError:
            return 0

s = Solution()
print(s.myAtoi(" -8   5655  U"))