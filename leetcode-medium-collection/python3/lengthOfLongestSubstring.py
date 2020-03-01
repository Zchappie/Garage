class Solution:
    # def lengthOfLongestSubstring(self, s: str) -> int:
    #     """
    #     Use stack property to pop the letter to find the longest substring.
    #     Once duplicated, delete all, and record the previous length.

    #     This is slow, probably because of converting to the list.
    #     """        
    #     longestLen = 0
    #     temp = []

    #     sList = list(s)
    #     while len(sList) != 0:
    #         letter = sList.pop(0)
    #         if letter in temp:
    #             temp = temp[temp.index(letter)+1:]
    #             temp.append(letter)

    #         else:
    #             temp.append(letter)
    #         longestLen = max(len(temp), longestLen)
    #     return longestLen

    def lengthOfLongestSubstring(self, s:str) -> int:
        """
        This is much faster than the previous one.
        Use the str property similar to stack but not explicitly converting to list.
        """
        longestLen = 0
        temp = ''
        for letter in s:
            if letter in temp:
                temp = temp[temp.index(letter)+1:]
                temp += letter
            else:
                temp += letter
            longestLen = max(len(temp), longestLen)
        return longestLen
        




s = Solution()
print(s.lengthOfLongestSubstring("aabaab!bb"))