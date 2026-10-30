---
title: "74. 搜索二维矩阵"
aliases: ["yiduobo的每日leetcode 74.搜索二维矩阵"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/two-pointers", "leetcode/binary-search", "题单/二分算法", "题单/LeetCode-热题-100", "题单/面试经典-150-题", "题单/二分算法/一-二分查找", "题单/LeetCode-热题-100/二分查找", "题单/面试经典-150-题/二分查找"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/133327228"
zhihu_id: "133327228"
zhihu_title: "yiduobo的每日leetcode 74.搜索二维矩阵"
question_id: "74"
question: "搜索二维矩阵"
problem_url: "https://leetcode.cn/problems/search-a-2d-matrix/"
difficulty: "Medium"
created: "2020-04-18T23:21:52+08:00"
updated: "2020-04-18T23:21:52+08:00"
upvotes: 0
comments: 0
---

# 74. 搜索二维矩阵

> **[yiduobo的每日leetcode 74.搜索二维矩阵](https://zhuanlan.zhihu.com/p/133327228) · 知乎 · 2020-04-18 · 赞同 0**
> 力扣：[74. 搜索二维矩阵](https://leetcode.cn/problems/search-a-2d-matrix/) · Medium · 灵茶山艾府：[把二维矩阵拉成一维数组，二分查找（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

74.搜索二维矩阵<https://leetcode-cn.com/problems/search-a-2d-matrix/>

二分查找的题目。题目保证了所有的行和列都是单调递增的，那么可以先对第一列进行二分，确定target位于哪一行，然后再到对应的行中在进行二分即可。

需要注意边界条件的判断，例如target小于matrix[0][0]，或者target大于matrix[m - 1][0]。另外在二分时需要找的是k，使其满足matrix[k][0] \<\= target且matrix[k + 1][0] > target，因此二分的时候需要保留住左边界，即left \= mid而不是left \= mid - 1。

两次二分，最终的时间复杂度为O(logm + logn)。

最后附上python代码：

```python
class Solution(object):
    def searchMatrix(self, matrix, target):
        """
        :type matrix: List[List[int]]
        :type target: int
        :rtype: bool
        """

        m = len(matrix)
        if m == 0:
            return False
        n = len(matrix[0])
        if n == 0:
            return False

        line = None
        if target < matrix[0][0]:
            return False
        elif target > matrix[m - 1][0]:
            line = m - 1
        else:          
            left = 0
            right = m - 1
            while left <= right:
                if left >= right - 1:
                    if matrix[right][0] == target:
                        return True
                    elif matrix[right][0] < target:
                        line = right
                    else:
                        line = left
                    break
                mid = (left + right) / 2
                if matrix[mid][0] == target:
                    return True
                elif matrix[mid][0] > target:
                    right = mid - 1
                else:
                    left = mid

        left = 0
        right = n - 1
        while left <= right:
            mid = (left + right) / 2
            if matrix[line][mid] == target:
                return True
            elif matrix[line][mid] > target:
                right = mid - 1
            else:
                left = mid + 1
        
        return False
```
