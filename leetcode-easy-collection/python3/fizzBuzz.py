class Solution:
    def fizzBuzz(self, n: int) -> List[str]:
        ls = []
        for i in range(1, n+1):
            if i%15 == 0:
                ls.append('FizzBuzz')
            elif i%5 == 0:
                ls.append('Buzz')
            elif i%3 == 0:
                ls.append('Fizz')
            else:
                ls.append(str(i))
        return ls

        """
        Even though this new idea doesn't make it faster or save more memory,
        but the idea is great!
        Using multiplication of boolean.
        """
        return ['Fizz' * (not i % 3) + 'Buzz' * (not i % 5) or str(i) for i in range(1, n+1)]