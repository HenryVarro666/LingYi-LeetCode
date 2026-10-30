---
title: "3591. 检查元素频次是否为质数"
aliases: ["yiduobo的每日leetcode 3591.检查元素频次是否为质数"]
tags: ["leetcode", "yiduobo", "leetcode/easy", "leetcode/hash-table", "leetcode/math", "leetcode/number-theory", "题单/数学算法", "题单/数学算法/一-数论"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/1939818724677911776"
zhihu_id: "1939818724677911776"
zhihu_title: "yiduobo的每日leetcode 3591.检查元素频次是否为质数"
question_id: "3591"
question: "检查元素频次是否为质数"
problem_url: "https://leetcode.cn/problems/check-if-any-element-has-prime-frequency/"
difficulty: "Easy"
rating: 1235
created: "2025-08-16T00:12:28+08:00"
updated: "2025-08-16T00:12:28+08:00"
upvotes: 0
comments: 0
---

# 3591. 检查元素频次是否为质数

> **[yiduobo的每日leetcode 3591.检查元素频次是否为质数](https://zhuanlan.zhihu.com/p/1939818724677911776) · 知乎 · 2025-08-16 · 赞同 0**
> 力扣：[3591. 检查元素频次是否为质数](https://leetcode.cn/problems/check-if-any-element-has-prime-frequency/) · Easy · 灵茶山艾府：[预处理质数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

3591.检查元素频次是否为质数

[3591. 检查元素频次是否为质数 - 力扣（LeetCode）](https://leetcode.cn/problems/check-if-any-element-has-prime-frequency/description/)

题目给出一个整数数组nums，如果其中任一元素出现的频次为质数，那么就返回true，否则返回false。

一趟遍历，使用哈希表统计每种元素出现的次数，接下来遍历这个哈希表中元素出现的频次，检测其中是否有质数即可。

最后附上python代码：

```python
class Solution(object):
    def checkPrimeFrequency(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """
        
        freq = {}
        for v in nums:
            freq[v] = freq.get(v, 0) + 1
        
        for f in freq.values():
            if f == 1:
                continue
            
            p = 2
            prime = True
            while p * p <= f:
                if f % p == 0:
                    prime = False
                    break
                p += 1
            
            if prime:
                return True
        
        return False
```
