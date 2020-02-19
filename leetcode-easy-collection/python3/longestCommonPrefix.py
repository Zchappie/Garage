from typing import List

class Solution:
    def helper(self, string1: str, string2: str) -> str:
        prefix = ""
        length = min(len(string1), len(string2))
        for i in range(length):
            if string1[i] == string2[i]:
                prefix += string1[i]
            else:
                break
        return prefix

    def longestCommonPrefix(self, strs: List[str]) -> str:
        # first remove the duplicated elements
        strsCopy = list(set(strs))

        # for speed
        if len(strsCopy) == 0:
            return ""
        elif len(strsCopy) == 1:
            return strsCopy[0]

        commonPrefix = ""
        length = min([len(x) for x in strsCopy])
        shortestStr = min(strsCopy, key=len)
        strsCopy.remove(shortestStr)
        secShortestStr = min(strsCopy, key=len)
        strsCopy.remove(secShortestStr)

        commonPrefix = self.helper(shortestStr, secShortestStr)
        if len(commonPrefix) == 0 or len(strsCopy) == 0:
            return commonPrefix
        prefix = ""
        for i in range(len(commonPrefix)):
            contin = False
            for j in range(len(strsCopy)):
                if commonPrefix[i] == strsCopy[j][i]:
                    contin = True
                else:
                    contin = False
                    break
            if contin:
                prefix += commonPrefix[i]
            else:
                return prefix
        return prefix

    """
    This is so damn brilliant!!!!

    b = 'abcde'
    list(*[b])
    >>> ['a', 'b', 'c', 'd', 'e']

    zip('ABCD', 'xy') 
    >>> Ax By

    strs = ["flower","flow","flight"]
    l = list(zip(*strs))
    >>> l = [('f', 'f', 'f'), ('l', 'l', 'l'), ('o', 'o', 'i'), ('w', 'w', 'g')]

    # if want to keep all the elements in every list
    list(itertools.zip_longest('ABCD', 'xy', fillvalue='-'))
    >>> [('A', 'x'), ('B', 'y'), ('C', '-'), ('D', '-')]
    """
    # def longestCommonPrefix(self, strs: List[str]) -> str:
    #     l = list(zip(*strs))
    #     prefix = ""
    #     for i in l:
    #         if len(set(i))==1: # then a set operation, remove the duplicants
    #             prefix += i[0]
    #         else:
    #             break
    #     return prefix
solu = Solution()
print(solu.longestCommonPrefix(["aac","bb","bc","b","caca"]))
    
