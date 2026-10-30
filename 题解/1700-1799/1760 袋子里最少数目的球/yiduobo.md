---
title: "1760. 袋子里最少数目的球"
aliases: ["yiduobo的每日leetcode 1760.袋子里最少数目的球"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/binary-search", "题单/二分算法", "题单/二分算法/二-二分答案"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/459628532"
zhihu_id: "459628532"
zhihu_title: "yiduobo的每日leetcode 1760.袋子里最少数目的球"
question_id: "1760"
question: "袋子里最少数目的球"
problem_url: "https://leetcode.cn/problems/minimum-limit-of-balls-in-a-bag/"
difficulty: "Medium"
rating: 1940
created: "2022-01-19T23:32:33+08:00"
updated: "2022-01-19T23:32:34+08:00"
upvotes: 0
comments: 0
---

# 1760. 袋子里最少数目的球

> **[yiduobo的每日leetcode 1760.袋子里最少数目的球](https://zhuanlan.zhihu.com/p/459628532) · 知乎 · 2022-01-19 · 赞同 0**
> 力扣：[1760. 袋子里最少数目的球](https://leetcode.cn/problems/minimum-limit-of-balls-in-a-bag/) · Medium · 灵茶山艾府：[二分答案（Python/Java/C++/C/Go/JS/Rust）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

1760.袋子里最少数目的球

[力扣](https://leetcode-cn.com/problems/minimum-limit-of-balls-in-a-bag/)

对于一个装有num个球的袋子而言，如果要求最终分出来的球的数目不超过k个，那么为了次数最少，肯定是顶着k个来分，于是一共需要执行num / k - 1次操作，将这些球分成num / k份。当然，如果这里num恰好就是k的倍数，这里分的次数就可以减去1。举个例子，将7个球分成每个袋子不超过2个，最终得到的是2、2、2、1，一共需要执行3次操作，而将8个球分成每个袋子不超过2个，最终得到的是2、2、2、2，同样是需要执行3次操作。

由于这里计算操作次数涉及到了整除，那么就不能将所有袋子的球放在一起来考虑。不过根据上面这个结论可以发现，随着答案的增大，需要分的次数必然是越来越小的，反过来也成立。为了使得分的次数小于等于maxOperations，又想要每个袋子里的球最大值最小，那么在这里二分答案是比较合适的做法。

二分的下限显然是1，而上限则是单个袋子中最大的球数。即max(nums)。对于当前二分到的k，对每个袋子计算需要操作的次数，并将这些次数累加起来，记为cnt。若最终cnt \<\= maxOperations，说明k是一个可行解，此时应该调整二分的上界，否则就需要调整二分的下界。

最后附上python代码：

```python
class Solution(object):
    def minimumSize(self, nums, maxOperations):
        """
        :type nums: List[int]
        :type maxOperations: int
        :rtype: int
        """

        l = 1
        r = max(nums)
        while l < r:
            mid = (l + r) >> 1
            cnt = 0
            for num in nums:
                cnt += num / mid
                if num % mid == 0:
                    cnt -= 1
            
            if cnt > maxOperations:
                l = mid + 1
            else:
                r = mid
        
        return l
```
