---
title: "1283. 使结果不超过阈值的最小除数"
aliases: ["yiduobo的每日leetcode 1283.使结果不超过阈值的最小除数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/math", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/388725323"
zhihu_id: "388725323"
zhihu_title: "yiduobo的每日leetcode 1283.使结果不超过阈值的最小除数"
question_id: "1283"
question: "使结果不超过阈值的最小除数"
problem_url: "https://leetcode.cn/problems/find-the-smallest-divisor-given-a-threshold/"
difficulty: "Medium"
rating: 1542
created: "2021-07-11T22:18:15+08:00"
updated: "2021-07-11T22:18:15+08:00"
upvotes: 0
comments: 0
---

# 1283. 使结果不超过阈值的最小除数

> **[yiduobo的每日leetcode 1283.使结果不超过阈值的最小除数](https://zhuanlan.zhihu.com/p/388725323) · 知乎 · 2021-07-11 · 赞同 0**
> 力扣：[1283. 使结果不超过阈值的最小除数](https://leetcode.cn/problems/find-the-smallest-divisor-given-a-threshold/) · Medium · 灵茶山艾府：[【模板】二分答案求最小（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1283.使结果不超过阈值的最小除数

[力扣](https://leetcode-cn.com/problems/find-the-smallest-divisor-given-a-threshold/)

注意到题目这里的除法是向上取整的，因此使用数学方法是不太方便的。不过有一点可以明确的是，除数越大，最后得到的结果就越小，因此可以二分这个除数，然后根据除法的结果与阈值的大小关系来调整除数。

最后附上python代码：

```python
class Solution(object):
    def smallestDivisor(self, nums, threshold):
        """
        :type nums: List[int]
        :type threshold: int
        :rtype: int
        """

        l = 1
        r = max(nums)
        while l < r:
            mid = (l + r) >> 1
            tmp = 0
            for num in nums:
                tmp += num / mid
                if num % mid != 0:
                    tmp += 1

            if tmp > threshold:
                l = mid + 1
            else:
                r = mid
        

        return l
```
