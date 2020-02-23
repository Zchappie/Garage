import typing 

class Solution:
    def helper(self, term: str) -> str:
        termList = list(term)
        readOut = ''
        counter = {}
        while len(termList) != 0:
            digit = termList.pop(0)
            if digit in counter:
                counter[digit] += 1
            elif len(counter) != 0:
                key, value = counter.popitem()
                readOut = readOut + str(value) + key
                counter[str(digit)] = 1
            else:
                counter[str(digit)] = 1
        key, value = counter.popitem()
        readOut = readOut + str(value) + key
        return readOut

    def countAndSay(self, n: int) -> str:
        firstFive = {
            '1' : '1',
            '2' : '11',
            '3' : '21',
            '4' : '1211',
            '5' : '111221'
            }
        if str(n) in firstFive:
            return firstFive[str(n)]
        increaser = 5
        term = firstFive['5']
        while increaser != n:
            term = self.helper(term)
            increaser += 1
        return term

    """
    itertools.groupby(): 
    Make an iterator that returns consecutive keys and groups from the iterable. 
    The key is a function computing a key value for each element.
    """
    def countAndSay(n):
        result = "1"
        for _ in range(n - 1):
            # original
            # s = ''.join(str(len(list(group))) + digit for digit, group in itertools.groupby(s))
            
            # decomposed
            v = '' # accumulator string
            # iterate the characters (digits) grouped by digit
            for digit, group in itertools.groupby(result):
                count = len(list(group)) # eg. the 2 in two 1s 
                v += "%i%s" % (count, digit) # create the 21 string and accumulate it
            result = v # save to result for the next for loop pass

        # return the accumulated string
        return result
        
solu = Solution()
print(solu.countAndSay(7))