# http://www.cplusplus.com/reference/cstring/strstr/
import typing

class Solution:
    def strStr(self, haystack: str, needle: str) -> int:
        if needle == '':
            return 0
        first_letter_ind = 0
        while first_letter_ind + len(needle) <= len(haystack) + 1:
            if needle[0] in haystack[first_letter_ind:]:
                potential_ind = haystack.index(needle[0], first_letter_ind)
                if haystack[potential_ind : potential_ind + len(needle)] == needle:
                    return potential_ind
                else:
                    first_letter_ind = potential_ind+1
            else:
                return -1
        return -1


"""
Nasty test case

>>> 'aaa', 'aaaa'
"""
solu = Solution()
print(solu.strStr(haystack = "abaa", needle = "aa"))