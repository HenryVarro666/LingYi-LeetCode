---
title: "1250. 检查[好数组]"
aliases: ["yiduobo的每日leetcode 1250.检查[好数组]"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/385852452"
zhihu_id: "385852452"
zhihu_title: "yiduobo的每日leetcode 1250.检查[好数组]"
question_id: "1250"
question: "检查[好数组]"
problem_url: "https://leetcode.cn/problems/check-if-it-is-a-good-array/"
created: "2021-07-01T22:45:33+08:00"
updated: "2021-07-01T22:45:33+08:00"
upvotes: 0
comments: 0
---

# 1250. 检查[好数组]

> **[yiduobo的每日leetcode 1250.检查[好数组]](https://zhuanlan.zhihu.com/p/385852452) · 知乎 · 2021-07-01 · 赞同 0**
> 力扣：[1250. 检查[好数组]](https://leetcode.cn/problems/check-if-it-is-a-good-array/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1250.检查[好数组]

[力扣](https://leetcode-cn.com/problems/check-if-it-is-a-good-array/)

题目实际上是要求我们从数组中选出两个数x和y，二者满足

a \* x + b \* y \= 1

对于给定的x和y，可以使用扩展欧几里得算法来求解a和b，而有解的前提则是x和y互质，也就是x和y的最大公约数为1。

于是我们可以求出数组中所有数中的最大公约数，若为1，说明必然可以选出一组互质的x和y，否则说明无解。

最后附上python代码：

```python
class Solution(object):
    def isGoodArray(self, nums):
        """
        :type nums: List[int]
        :rtype: bool
        """

        now = nums[0]
        for num in nums[1:]:
            while num:
                now, num = num, now % num
            if now == 1:
                break
        
        return now == 1
```
