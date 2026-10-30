---
title: "1105. 填充书架"
aliases: ["yiduobo的每日leetcode 1105.填充书架"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/recursion", "leetcode/memoization", "leetcode/dynamic-programming", "题单/动态规划", "题单/动态规划/五-划分型-DP"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/374477276"
zhihu_id: "374477276"
zhihu_title: "yiduobo的每日leetcode 1105.填充书架"
question_id: "1105"
question: "填充书架"
problem_url: "https://leetcode.cn/problems/filling-bookcase-shelves/"
difficulty: "Medium"
rating: 2014
created: "2021-05-22T23:17:24+08:00"
updated: "2021-05-22T23:17:24+08:00"
upvotes: 1
comments: 0
---

# 1105. 填充书架

> **[yiduobo的每日leetcode 1105.填充书架](https://zhuanlan.zhihu.com/p/374477276) · 知乎 · 2021-05-22 · 赞同 1**
> 力扣：[1105. 填充书架](https://leetcode.cn/problems/filling-bookcase-shelves/) · Medium · 灵茶山艾府：[教你一步步思考动态规划！（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1105.填充书架

[力扣](https://leetcode-cn.com/problems/filling-bookcase-shelves/)

动态规划的题目，令f[i]表示填充前i本书需要的最小高度，那么我们可以枚举j，将第j本书到第i本书都放在一层，那么就有f[i] \= min(f[i], f[j - 1] + max(height[j : i + 1])。当然，这里的j必须要满足sum(width[j : i +1]) \< shelf_width，即第j本书到第i本书的宽度之和不能超过书架的宽度。这里是一个经典的滑动窗口问题，那么可以在动态规划的过程中使用滑动窗口维护j的左边界。

另外，在j到i这个区间中，也存在某种单调性。简单来说就是最后枚举j的过程中，若存在某个k，其对应的高度height[k]特别高，设存在某个k'满足height[k'] > height[k]，且j \<\= k' \< k，那么对于k'到k之间的这些书就没有枚举的必要了。观察状态转移方程：

f[i] \= min(f[i], f[j - 1] + max(height[j : i + 1])

当选择将第k本书放到最后一层时，k'到k之间的书放到最后一层也不会影响最后一层的高度，即括号中的项必然是height[k]，但是这里的f是单调递增的，因此j越靠前越好，因此这里就有

f[i] \= min(f[i], f[k'] + height[k])

由于这里的k和k'满足单调递减的关系，因此可以在动态规划的过程中使用单调栈来进行维护。不过这里的优化对最终的时间复杂度无法产生决定性的影响，在极限情况下没有任何优化的空间。

最后附上python代码：

```python
class Solution(object):
    def minHeightShelves(self, books, shelf_width):
        """
        :type books: List[List[int]]
        :type shelf_width: int
        :rtype: int
        """

        n = len(books)
        bound = 0
        now = 0
        f = [0]
        q = []
        l = 0
        r = 0
        for index in range(n):
            now += books[index][0]
            while now > shelf_width:
                now -= books[bound][0]
                if l < r and q[l] == bound:
                    l += 1
                bound += 1
            
            while r > l and books[q[-1]][1] < books[index][1]:
                q.pop()
                r -= 1
            q.append(index)
            r += 1

            f.append(f[bound] + books[q[l]][1])
            for index in range(l, r - 1):
                f[-1] = min(f[-1], f[q[index] + 1] + books[q[index + 1]][1])

        return f[-1]
```
