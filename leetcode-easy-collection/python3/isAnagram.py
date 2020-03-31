class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        sSet = set(s)
        tSet = set(t)
        for i in sSet:
            if s.count(i) != t.count(i):
                return False
        
        return len(s) == len(t)