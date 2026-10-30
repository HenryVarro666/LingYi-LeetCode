---
title: "2393. 严格递增的子数组个数"
aliases: ["yiduobo的每日leetcode 2393.严格递增的子数组个数"]
tags: ["leetcode", "yiduobo"]
author: "yiduobo"
source: "知乎"
url: "https://zhuanlan.zhihu.com/p/630959869"
zhihu_id: "630959869"
zhihu_title: "yiduobo的每日leetcode 2393.严格递增的子数组个数"
question_id: "2393"
question: "严格递增的子数组个数"
problem_url: "https://leetcode.cn/problems/count-strictly-increasing-subarrays/"
created: "2023-05-21T01:03:32+08:00"
updated: "2023-05-21T01:03:32+08:00"
upvotes: 0
comments: 0
---

# 2393. 严格递增的子数组个数

> **[yiduobo的每日leetcode 2393.严格递增的子数组个数](https://zhuanlan.zhihu.com/p/630959869) · 知乎 · 2023-05-21 · 赞同 0**
> 力扣：[2393. 严格递增的子数组个数](https://leetcode.cn/problems/count-strictly-increasing-subarrays/)

祖传的手艺不想丢了，所以按顺序写一个leetcode的题解。计划每日两题，争取不卡题吧

常规题号的题目已经写到头了，开始从头补vip题的题

2393.严格递增的子数组个数

[力扣](https://leetcode.cn/problems/count-strictly-increasing-subarrays/)

对于一段长度为k的严格递增子数组，从里面可以拆分出k个长度为1的子数组，k - 1个长度为2的子数组，...，1个长度为k的子数组，也就是说一共可以提供(1 + k) \* k / 2个子数组。于是只需一趟遍历，找出数组中的尽量长的递增子数组，然后通过其长度计算其中包含的子数组数量，然后累加到答案中。

最后附上python代码：

```python
class Solution(object):
    def countSubarrays(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """

        last = 10 ** 6 + 1
        cnt = 0
        res = 0
        for num in nums:
            if last >= num:
                res += cnt * (cnt + 1) / 2
                cnt = 0
            
            last = num
            cnt += 1

        res += cnt * (cnt + 1) / 2
        return res
```
