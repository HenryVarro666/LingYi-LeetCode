---
title: "674. 最长连续递增序列"
aliases: ["yiduobo的每日leetcode 674.最长连续递增序列"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/296982305"
zhihu_id: "296982305"
zhihu_title: "yiduobo的每日leetcode 674.最长连续递增序列"
question_id: "674"
question: "最长连续递增序列"
problem_url: "https://leetcode.cn/problems/longest-continuous-increasing-subsequence/"
created: "2020-11-16T22:51:17+08:00"
updated: "2020-11-16T22:51:17+08:00"
upvotes: 1
comments: 0
---

# 674. 最长连续递增序列

> **[yiduobo的每日leetcode 674.最长连续递增序列](https://zhuanlan.zhihu.com/p/296982305) · 知乎 · 2020-11-16 · 赞同 1**
> 力扣：[674. 最长连续递增序列](https://leetcode.cn/problems/longest-continuous-increasing-subsequence/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧。

674.最长连续递增序列

[力扣](https://leetcode-cn.com/problems/longest-continuous-increasing-subsequence/)

依然是使用动态规划来做，f[i]表示以nums[i]结尾的连续递增序列的长度，那么就有：

1、若nums[i] > num[i - 1]，则f[i] \= f[i - 1] + 1

2、若nums[i] \<\= nums[i - 1]，则f[i] \= 1

注意到这里的状态转移只跟上一个数有关，因此可以省略掉f数组，直接用一个变量来表示以当前数为结尾的连续递增序列的长度。

最后附上python代码：

```python
class Solution(object):
    def findLengthOfLCIS(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        if not nums:
            return 0

        now = nums[0]
        cnt = res = 1
        
        for num in nums[1:]:
            if num > now:
                cnt += 1
                res = max(res, cnt)
            else:
                cnt = 1
            now = num

        return res
```
