class Solution:
    def longestPalindrome(self, s: str) -> str:
        if s == '':
            return ''
        longest = s[0]
        for i in range(0, len(s)):
            head = i
            tail = i+1
            subs = s[i]
            while head != -1 and tail <= len(s)-1:
                if len(subs)>=1 and len(set(subs))==1:
                    while tail != len(s) and s[tail]==subs[0]:
                        subs += s[tail]
                        tail += 1
                if tail >= len(s):
                    break
                if head-1 >= 0 and s[head-1] == s[tail]:
                    subs = s[head-1: tail+1]
                    head -= 1
                    tail += 1
                else:
                    head = -1
                    if len(subs)>len(longest):
                        longest = subs
            if len(subs)>len(longest):
                longest = subs
        return longest


    """
    Difference: separate the 'aba' and 'aa' cases.
    """
    def longestPalindrome(self, s):
        """
        :type s: str
        :rtype: str
        """
        longest = s[0]
        for i in range(len(s)):
            # for odd and even cases
            longest = max(self.helper(s,i,i), self.helper(s,i,i+1), longest, key=len)

        return longest
           
    def helper(self,s,l,r):
        while 0<=l and r < len(s) and s[l]==s[r]:
            l-=1
            r+=1
        return s[l+1:r]

s = Solution()
print(s.longestPalindrome("aabbccddccbba"))