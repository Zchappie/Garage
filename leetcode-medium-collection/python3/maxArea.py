from typing import List
class Solution:
    def maxArea(self, height: List[int]) -> int:
        up = len(height) - 1
        low = 0
        maxarea = 0
        for i in range(len(height)):
            if height[low] < height[up]:
                area = abs(up - low) * height[low]
                low += 1
            
            else:
                area = abs(up - low) * height[up]
                up -= 1
            
            if area > maxarea:
                maxarea = area
                
        return maxarea
                