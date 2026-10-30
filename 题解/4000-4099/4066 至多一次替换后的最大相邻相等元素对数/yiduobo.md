---
title: "4066. 至多一次替换后的最大相邻相等元素对数"
aliases: ["yiduobo的每日leetcode 4066.至多一次替换后的最大相邻相等元素对数"]
tags: ["leetcode", "yiduobo", "leetcode/medium", "leetcode/hash-table"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/2088748369921438246"
zhihu_id: "2088748369921438246"
zhihu_title: "yiduobo的每日leetcode 4066.至多一次替换后的最大相邻相等元素对数"
question_id: "4066"
question: "至多一次替换后的最大相邻相等元素对数"
problem_url: "https://leetcode.cn/problems/maximum-equal-adjacent-pairs-after-at-most-one-replacement/"
difficulty: "Medium"
created: "2026-09-30T22:29:48+08:00"
updated: "2026-09-30T22:29:48+08:00"
upvotes: 1
comments: 0
---

# 4066. 至多一次替换后的最大相邻相等元素对数

> **[yiduobo的每日leetcode 4066.至多一次替换后的最大相邻相等元素对数](https://zhuanlan.zhihu.com/p/2088748369921438246) · 知乎 · 2026-09-30 · 赞同 1**
> 力扣：[4066. 至多一次替换后的最大相邻相等元素对数](https://leetcode.cn/problems/maximum-equal-adjacent-pairs-after-at-most-one-replacement/) · Medium · 灵茶山艾府：[统计相邻不等的数对个数（Python/Java/C++/Go）](灵茶山艾府.md)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

4066.至多一次替换后的最大相邻相等元素对数

<https://leetcode.cn/problems/maximum-equal-adjacent-pairs-after-at-most-one-replacement/description/>

题目给出一个下标从1开始的整数数组nums。

现在可以选择两个不同的值x和y，并将nums中所有的x都替换为y。也可以选择不执行此操作。

问nums中相邻且相等的元素对最多可以到多少。

首先，对于一组本来就相等的相邻元素，那么无论怎样修改，这一组元素依然相等。理由也很简单：如果没有修改这个元素，那么自然还是相等的；如果修改的是这个元素，那么这一对元素都修改成了新的元素，依然相等。

基于这一点，在这里只需要关心本来不相等的元素对。为了使得答案最大，那么显然应该选择出现次数最多的不同元素对，将其中一个元素修改为另一个元素。同时，其他不相等的元素对在此次修改后依然维持不相等的状态。

因此可以使用一个哈希表pair记录不相等的相邻元素对数量，然后从下标1开始对nums进行一趟遍历。对于当前遍历到的index，若nums[index]与nums[index - 1]相同，那么将答案加上1，否则将nums[index - 1]与nums[index]按照升序做成key，然后将pair[key]加上1。遍历完成后，将pair中的最大值累加到答案中即可。

最后附上python代码：

```python
class Solution(object):
    def maxEqualAdjacentPairs(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        
        res = 0
        pair = {}
        for index in range(1, len(nums)):
            ma = max(nums[index], nums[index - 1])
            mi = min(nums[index], nums[index - 1])

            if ma == mi:
                res += 1
            else:
                key = (ma, mi)
                pair[key] = pair.get(key, 0) + 1
        
        if pair:
            res += max(pair.values())
        
        return res
```
