---
title: "3618. 根据质数下标分割数组"
aliases: ["yiduobo的每日leetcode 3618.根据质数下标分割数组"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1944163499501650170"
zhihu_id: "1944163499501650170"
zhihu_title: "yiduobo的每日leetcode 3618.根据质数下标分割数组"
question_id: "3618"
question: "根据质数下标分割数组"
problem_url: "https://leetcode.cn/problems/split-array-by-prime-indices/"
difficulty: "Medium"
rating: 1227
created: "2025-08-27T22:28:38+08:00"
updated: "2025-08-27T22:28:38+08:00"
upvotes: 0
comments: 0
---

# 3618. 根据质数下标分割数组

> **[yiduobo的每日leetcode 3618.根据质数下标分割数组](https://zhuanlan.zhihu.com/p/1944163499501650170) · 知乎 · 2025-08-27 · 赞同 0**
> 力扣：[3618. 根据质数下标分割数组](https://leetcode.cn/problems/split-array-by-prime-indices/) · Medium · 灵茶山艾府：[预处理质数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3618.根据质数下标分割数组

<https://leetcode.cn/problems/split-array-by-prime-indices/description/>

题目给出一个整数数组nums，其长度不超过10^5。现在要求将nums中位于质数下标的元素加入到数组A中，然后将其他剩下的元素加入到数组B中，问A和B的数组和的差的绝对值是多少。

n的规模不算小，因此在这里需要先通过筛法，找出1到n中所有的质数。接下来只需一趟遍历，根据当前下标是否为质数计算A和B的数组和，然后返回这两者差的绝对值即可。

最后附上python代码：

```python
class Solution(object):
    def splitArray(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        n = len(nums)
        prime = [True] * n
        prime[0] = False
        if n > 1:
            prime[1] = False
        x = 2
        while x < n:
            if prime[x]:
                for y in range(x + x, n, x):
                    prime[y] = False
            x += 1
        
        res = 0
        for index in range(n):
            if prime[index]:
                res += nums[index]
            else:
                res -= nums[index]
        
        return abs(res)
```
