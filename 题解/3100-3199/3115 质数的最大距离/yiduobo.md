---
title: "3115. 质数的最大距离"
aliases: ["yiduobo的每日leetcode 3115.质数的最大距离"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/bit-manipulation", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/701144772"
zhihu_id: "701144772"
zhihu_title: "yiduobo的每日leetcode 3115.质数的最大距离"
question_id: "3115"
question: "质数的最大距离"
problem_url: "https://leetcode.cn/problems/maximum-prime-difference/"
difficulty: "Medium"
rating: 1294
created: "2024-06-01T23:22:00+08:00"
updated: "2024-06-01T23:22:00+08:00"
upvotes: 0
comments: 0
---

# 3115. 质数的最大距离

> **[yiduobo的每日leetcode 3115.质数的最大距离](https://zhuanlan.zhihu.com/p/701144772) · 知乎 · 2024-06-01 · 赞同 0**
> 力扣：[3115. 质数的最大距离](https://leetcode.cn/problems/maximum-prime-difference/) · Medium · 灵茶山艾府：[三种方法：判断质数 / 预处理 / 位运算（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3115.质数的最大距离

[. - 力扣（LeetCode）](https://leetcode.cn/problems/maximum-prime-difference/description/)

题目给出一个整数数组nums，其中元素的大小在1到100之间，要求找出其中两个质数间距离的最大值。

由于nums中元素的范围很小，于是可以先找出1到100中的所有质数，接下来只需对nums进行一趟遍历，找出其中最靠前和最靠后的质数，然后计算二者下标之差即可。

最后附上python代码：

```python
class Solution(object):
    def maximumPrimeDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        prime = set()
        for v in range(2, 101):
            x = 2
            flag = True
            while x * x <= v:
                if v % x == 0:
                    flag = False
                    break
                x += 1
            
            if flag:
                prime.add(v)
        
        n = len(nums)
        for index in range(n):
            if nums[index] in prime:
                first = index
                break
        
        for index in range(n - 1, -1, -1):
            if nums[index] in prime:
                last = index
                break
        
        return last - first
```
